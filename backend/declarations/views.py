"""
Vues de l'API REST
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from django.http import FileResponse
from .pdf_generator import generate_recepisse_pdf
import logging  # ← ajouté pour les logs d'email

from .models import CategoriePiece, Declaration, Notification
from .serializers import (
    UserSerializer, UserProfileSerializer,
    CreateAgentSerializer,
    CategoriePieceSerializer,
    DeclarationListSerializer, DeclarationDetailSerializer,
    DeclarationCreateSerializer, NotificationSerializer,
    StatistiquesSerializer, RechercheCorrespondanceSerializer
)
from .permissions import IsAdminOrPolice, IsAdminOnly, IsOwnerOrAdminOrPolice
from .email_service import envoyer_email_retrouve  # ← ajouté pour les notifications Gmail

User = get_user_model()
logger = logging.getLogger(__name__)


# =============================================================================
# AUTHENTIFICATION & PROFIL
# =============================================================================

class RegisterView(APIView):
    """Inscription publique — crée UNIQUEMENT des comptes citoyens."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Compte créé avec succès',
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Profil de l'utilisateur connecté. GET / PUT /api/profile/"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================================================================
# GESTION DES AGENTS — RÉSERVÉ AUX ADMINISTRATEURS
# =============================================================================

class AgentManagementView(APIView):
    """
    GET  /api/admin/agents/   → liste agents
    POST /api/admin/agents/   → créer un agent
    """
    permission_classes = [IsAdminOnly]

    def get(self, request):
        agents = User.objects.filter(role__in=['police', 'admin']).order_by('-date_creation')
        return Response(UserProfileSerializer(agents, many=True).data)

    def post(self, request):
        serializer = CreateAgentSerializer(data=request.data)
        if serializer.is_valid():
            agent = serializer.save()
            return Response({
                'message': f"Agent '{agent.username}' créé avec succès.",
                'agent': UserProfileSerializer(agent).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentDetailView(APIView):
    """
    PATCH  /api/admin/agents/<id>/  → modifier
    DELETE /api/admin/agents/<id>/  → désactiver (soft-delete)
    """
    permission_classes = [IsAdminOnly]

    def _get_agent(self, pk):
        try:
            return User.objects.get(pk=pk, role__in=['police', 'admin'])
        except User.DoesNotExist:
            return None

    def patch(self, request, pk):
        agent = self._get_agent(pk)
        if not agent:
            return Response({'error': 'Agent introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        if agent == request.user and request.data.get('role') == 'citoyen':
            return Response(
                {'error': 'Vous ne pouvez pas modifier votre propre rôle.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = UserProfileSerializer(agent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        agent = self._get_agent(pk)
        if not agent:
            return Response({'error': 'Agent introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        if agent == request.user:
            return Response(
                {'error': 'Vous ne pouvez pas désactiver votre propre compte.'},
                status=status.HTTP_403_FORBIDDEN
            )
        agent.is_active = False
        agent.save(update_fields=['is_active'])
        return Response({'message': f"Le compte de '{agent.username}' a été désactivé."})


# =============================================================================
# GESTION COMPLÈTE DES UTILISATEURS — ADMIN UNIQUEMENT
# =============================================================================

class UserManagementView(APIView):
    """
    Liste TOUS les utilisateurs (citoyens + agents + admins).
    GET /api/admin/users/?role=citoyen&search=jean
    """
    permission_classes = [IsAdminOnly]

    def get(self, request):
        qs = User.objects.all().order_by('-date_creation')

        role = request.query_params.get('role', '').strip()
        if role:
            qs = qs.filter(role=role)

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        return Response(UserProfileSerializer(qs, many=True).data)


class UserDetailAdminView(APIView):
    """
    Opérations sur un utilisateur quelconque (citoyen, agent, admin).

    GET    /api/admin/users/<id>/  → détail
    PATCH  /api/admin/users/<id>/  → modifier
    DELETE /api/admin/users/<id>/  → suppression DÉFINITIVE
    """
    permission_classes = [IsAdminOnly]

    def _get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserProfileSerializer(user).data)

    def patch(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        if user == request.user:
            return Response(
                {'error': 'Modifiez votre propre compte depuis /api/profile/.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        if user == request.user:
            return Response(
                {'error': 'Vous ne pouvez pas supprimer votre propre compte.'},
                status=status.HTTP_403_FORBIDDEN
            )
        username = user.username
        user.delete()   # suppression définitive en base (cascade sur déclarations/notifs)
        return Response(
            {'message': f"L'utilisateur « {username} » a été supprimé définitivement."},
            status=status.HTTP_200_OK
        )


# =============================================================================
# CATÉGORIES
# =============================================================================

class CategoriePieceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoriePiece.objects.filter(actif=True)
    serializer_class = CategoriePieceSerializer
    permission_classes = [permissions.AllowAny]


# =============================================================================
# DÉCLARATIONS
# =============================================================================

class DeclarationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'police']:
            return Declaration.objects.select_related(
                'categorie', 'user', 'declaration_correspondante'
            ).all()
        return Declaration.objects.select_related(
            'categorie', 'user', 'declaration_correspondante'
        ).filter(user=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return DeclarationListSerializer
        if self.action == 'create':
            return DeclarationCreateSerializer
        return DeclarationDetailSerializer

    def get_permissions(self):
        if self.action == 'changer_statut':
            return [IsAdminOrPolice()]
        if self.action == 'destroy':
            return [IsAdminOnly()]      # ← seul l'admin supprime
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Suppression DÉFINITIVE d'une déclaration — admin uniquement."""
        declaration = self.get_object()
        numero = declaration.numero_recepisse
        declaration.delete()
        return Response(
            {'message': f"La déclaration « {numero} » a été supprimée définitivement."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def telecharger_recepisse(self, request, pk=None):
        declaration = self.get_object()
        if request.user.role not in ['admin', 'police']:
            if declaration.user != request.user:
                return Response(
                    {'error': 'Vous ne pouvez télécharger que vos propres récépissés.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        try:
            pdf_buffer = generate_recepisse_pdf(declaration)
        except Exception as e:
            return Response(
                {'error': f'Erreur génération PDF : {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return FileResponse(
            pdf_buffer, as_attachment=True,
            filename=f"recepisse_{declaration.numero_recepisse}.pdf",
            content_type='application/pdf'
        )

    @action(detail=False, methods=['get'])
    def mes_declarations(self, request):
        qs = Declaration.objects.filter(user=request.user).select_related('categorie')
        return Response(DeclarationListSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'])
    def pertes(self, request):
        return Response(DeclarationListSerializer(
            self.get_queryset().filter(type_declaration='PERTE'), many=True
        ).data)

    @action(detail=False, methods=['get'])
    def trouvailles(self, request):
        return Response(DeclarationListSerializer(
            self.get_queryset().filter(type_declaration='TROUVAILLE'), many=True
        ).data)

    @action(detail=False, methods=['post'])
    def rechercher(self, request):
        serializer = RechercheCorrespondanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        numero_piece     = d.get('numero_piece', '').strip()
        nom_sur_piece    = d.get('nom_sur_piece', '').strip()
        nom_declarant    = d.get('nom_declarant', '').strip()
        prenom_declarant = d.get('prenom_declarant', '').strip()
        categorie_id     = d.get('categorie')

        if not any([numero_piece, nom_sur_piece, nom_declarant, prenom_declarant]):
            return Response(
                {'error': 'Fournissez au moins un critère de recherche.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        query = Q(type_declaration='TROUVAILLE', statut='VALIDE')
        if numero_piece:
            query &= Q(numero_piece__icontains=numero_piece)
        if nom_declarant:
            query &= (Q(nom_declarant__icontains=nom_declarant) | Q(nom_sur_piece__icontains=nom_declarant))
        if prenom_declarant:
            query &= (Q(prenom_declarant__icontains=prenom_declarant) | Q(nom_sur_piece__icontains=prenom_declarant))
        if nom_sur_piece and not nom_declarant and not prenom_declarant:
            query &= Q(nom_sur_piece__icontains=nom_sur_piece)
        if categorie_id:
            query &= Q(categorie_id=categorie_id)

        qs = Declaration.objects.filter(query).select_related('categorie', 'user')
        return Response({
            'nombre_resultats': qs.count(),
            'correspondances':  DeclarationListSerializer(qs, many=True).data,
        })

    @action(detail=True, methods=['patch'])
    def changer_statut(self, request, pk=None):
        declaration = self.get_object()
        nouveau_statut = request.data.get('statut')
        remarques = request.data.get('remarques', '')

        if nouveau_statut not in dict(Declaration.STATUT_CHOICES):
            return Response(
                {'error': f"Statut invalide. Valeurs : {list(dict(Declaration.STATUT_CHOICES).keys())}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ancien_statut = declaration.statut          # ← mémorisé avant modification
        ancien_label  = declaration.get_statut_display()

        declaration.statut = nouveau_statut
        if remarques:
            declaration.remarques_admin = remarques
        declaration.save()

        # ── Notification in-app (existante, inchangée) ────────────────────────
        Notification.objects.create(
            user=declaration.user, declaration=declaration,
            type_notification='STATUT',
            titre=f"Changement de statut : {declaration.numero_recepisse}",
            message=(
                f"Votre déclaration est passée de « {ancien_label} » "
                f"à « {declaration.get_statut_display()} ». {remarques}"
            )
        )

        # ── Emails Gmail si passage à RETROUVE ────────────────────────────────
        if nouveau_statut == 'RETROUVE' and ancien_statut != 'RETROUVE':
            self._envoyer_emails_retrouve(declaration, remarques)

        return Response(DeclarationDetailSerializer(declaration).data)

    # -------------------------------------------------------------------------
    # Méthode privée : envoi des emails lors d'un passage manuel à RETROUVE
    # -------------------------------------------------------------------------

    def _envoyer_emails_retrouve(self, declaration, remarques=''):
        """
        Envoie les emails Gmail aux déclarants concernés quand
        l'agent passe manuellement une déclaration au statut RETROUVE.

        Cas 1 — La déclaration a déjà une correspondance (match) :
            → Email au déclarant principal + email à la partie adverse.
        Cas 2 — Pas de correspondance (action manuelle sans match) :
            → Email au seul déclarant de la déclaration concernée.
        """
        match = declaration.declaration_correspondante  # peut être None

        # Email au déclarant de la déclaration modifiée par l'agent
        try:
            envoyer_email_retrouve(
                user=declaration.user,
                declaration=declaration,
                match=match,
                remarques=remarques,
            )
        except Exception as exc:
            logger.error(
                "Échec email RETROUVÉ (déclarant principal) %s : %s",
                declaration.numero_recepisse, exc
            )

        # Email au déclarant de la déclaration correspondante (si présent et distinct)
        if match and match.user != declaration.user:
            try:
                envoyer_email_retrouve(
                    user=match.user,
                    declaration=match,
                    match=declaration,
                    remarques=remarques,
                )
            except Exception as exc:
                logger.error(
                    "Échec email RETROUVÉ (déclarant correspondant) %s : %s",
                    match.numero_recepisse, exc
                )


# =============================================================================
# NOTIFICATIONS
# =============================================================================

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        return Response(self.get_serializer(
            self.get_queryset().filter(lue=False), many=True
        ).data)

    @action(detail=True, methods=['post'])
    def marquer_lue(self, request, pk=None):
        notif = self.get_object()
        notif.lue = True
        notif.save()
        return Response({'status': 'Notification marquée comme lue'})

    @action(detail=False, methods=['post'])
    def tout_marquer_lues(self, request):
        count = self.get_queryset().update(lue=True)
        return Response({'status': f'{count} notification(s) marquée(s) comme lue(s)'})


# =============================================================================
# STATISTIQUES
# =============================================================================

class StatistiquesView(APIView):
    permission_classes = [IsAdminOrPolice]

    def get(self, request):
        date_limite = timezone.now() - timedelta(days=7)
        data = {
            'total_declarations':    Declaration.objects.count(),
            'total_pertes':          Declaration.objects.filter(type_declaration='PERTE').count(),
            'total_trouvailles':     Declaration.objects.filter(type_declaration='TROUVAILLE').count(),
            'en_attente':            Declaration.objects.filter(statut='EN_ATTENTE').count(),
            'validees':              Declaration.objects.filter(statut='VALIDE').count(),
            'retrouvees':            Declaration.objects.filter(statut='RETROUVE').count(),
            'restituees':            Declaration.objects.filter(statut='RESTITUE').count(),
            'total_utilisateurs':    User.objects.count(),
            'total_citoyens':        User.objects.filter(role='citoyen').count(),
            'total_agents':          User.objects.filter(role__in=['police', 'admin']).count(),
            'declarations_recentes': DeclarationListSerializer(
                Declaration.objects.filter(date_declaration__gte=date_limite)
                           .order_by('-date_declaration')[:10],
                many=True
            ).data,
            'categories_populaires': list(
                CategoriePiece.objects.annotate(nombre=Count('declarations'))
                              .order_by('-nombre')[:5].values('libelle', 'nombre')
            ),
        }
        return Response(data)