"""
Vues de l'API REST — VERSION AVEC WORKFLOW DE REMPLACEMENT
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
from django.contrib.auth import authenticate

from .models import CategoriePiece, Declaration, Notification, DemandeRemplacement
from .serializers import (
    UserSerializer, UserProfileSerializer, CreateAgentSerializer,
    CategoriePieceSerializer,
    DeclarationListSerializer, DeclarationDetailSerializer, DeclarationCreateSerializer,
    NotificationSerializer, StatistiquesSerializer, RechercheCorrespondanceSerializer,
    DemandeRemplacementSerializer, ChangerStatutRemplacementSerializer,
)
from .permissions import IsAdminOrPolice, IsAdminOnly, IsOwnerOrAdminOrPolice
from .pdf_generator import generate_recepisse_pdf
from .pdf_remplacement import generate_autorisation_pdf
from .email_service import envoyer_email_retrouve
from .email_remplacement import envoyer_email_remplacement

import logging
User = get_user_model()
logger = logging.getLogger(__name__)


# =============================================================================
# AUTHENTIFICATION & PROFIL
# =============================================================================

class RegisterView(APIView):
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
# GESTION DES AGENTS
# =============================================================================

class AgentManagementView(APIView):
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
            return Response({'error': 'Vous ne pouvez pas modifier votre propre rôle.'}, status=status.HTTP_403_FORBIDDEN)
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
            return Response({'error': 'Vous ne pouvez pas désactiver votre propre compte.'}, status=status.HTTP_403_FORBIDDEN)
        agent.is_active = False
        agent.save(update_fields=['is_active'])
        return Response({'message': f"Le compte de '{agent.username}' a été désactivé."})


# =============================================================================
# GESTION DES UTILISATEURS
# =============================================================================

class UserManagementView(APIView):
    permission_classes = [IsAdminOnly]

    def get(self, request):
        qs = User.objects.all().order_by('-date_creation')
        role = request.query_params.get('role', '').strip()
        if role:
            qs = qs.filter(role=role)
        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(username__icontains=search) | Q(first_name__icontains=search) |
                Q(last_name__icontains=search) | Q(email__icontains=search)
            )
        return Response(UserProfileSerializer(qs, many=True).data)


class UserDetailAdminView(APIView):
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
            return Response({'error': 'Modifiez votre propre compte depuis /api/profile/.'}, status=status.HTTP_403_FORBIDDEN)
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
            return Response({'error': 'Vous ne pouvez pas supprimer votre propre compte.'}, status=status.HTTP_403_FORBIDDEN)
        username = user.username
        user.delete()
        return Response({'message': f"L'utilisateur « {username} » a été supprimé définitivement."})


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
        qs   = Declaration.objects.select_related('categorie', 'user', 'declaration_correspondante')
        if user.role in ['admin', 'police']:
            return qs.all()
        return qs.filter(user=user)

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
            return [IsAdminOnly()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        declaration = self.get_object()
        numero = declaration.numero_recepisse
        declaration.delete()
        return Response({'message': f"La déclaration « {numero} » a été supprimée définitivement."})

    @action(detail=True, methods=['get'])
    def telecharger_recepisse(self, request, pk=None):
        declaration = self.get_object()
        if request.user.role not in ['admin', 'police'] and declaration.user != request.user:
            return Response({'error': 'Vous ne pouvez télécharger que vos propres récépissés.'}, status=403)
        try:
            pdf_buffer = generate_recepisse_pdf(declaration)
        except Exception as e:
            return Response({'error': f'Erreur génération PDF : {str(e)}'}, status=500)
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
            return Response({'error': 'Fournissez au moins un critère de recherche.'}, status=400)

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
        return Response({'nombre_resultats': qs.count(), 'correspondances': DeclarationListSerializer(qs, many=True).data})

    @action(detail=True, methods=['patch'])
    def changer_statut(self, request, pk=None):
        declaration = self.get_object()
        nouveau_statut = request.data.get('statut')
        remarques = request.data.get('remarques', '')

        if nouveau_statut not in dict(Declaration.STATUT_CHOICES):
            return Response({'error': f"Statut invalide. Valeurs : {list(dict(Declaration.STATUT_CHOICES).keys())}"}, status=400)

        ancien_statut = declaration.statut
        ancien_label  = declaration.get_statut_display()

        declaration.statut = nouveau_statut
        if remarques:
            declaration.remarques_admin = remarques
        declaration.save(update_fields=['statut', 'remarques_admin', 'date_modification'])

        Notification.objects.create(
            user=declaration.user, declaration=declaration,
            type_notification='STATUT',
            titre=f"Changement de statut : {declaration.numero_recepisse}",
            message=(
                f"Votre déclaration est passée de « {ancien_label} » "
                f"à « {declaration.get_statut_display()} ». {remarques}"
            )
        )

        if nouveau_statut == 'RETROUVE' and ancien_statut != 'RETROUVE':
            self._envoyer_emails_retrouve(declaration, remarques)

        return Response(DeclarationDetailSerializer(declaration).data)

    def _envoyer_emails_retrouve(self, declaration, remarques=''):
        match = declaration.declaration_correspondante
        try:
            envoyer_email_retrouve(user=declaration.user, declaration=declaration, match=match, remarques=remarques)
        except Exception as exc:
            logger.error("Échec email RETROUVÉ (principal) %s : %s", declaration.numero_recepisse, exc)
        if match and match.user != declaration.user:
            try:
                envoyer_email_retrouve(user=match.user, declaration=match, match=declaration, remarques=remarques)
            except Exception as exc:
                logger.error("Échec email RETROUVÉ (correspondant) %s : %s", match.numero_recepisse, exc)


# =============================================================================
# WORKFLOW DE REMPLACEMENT — CITOYEN
# =============================================================================

class DemandeRemplacementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Citoyen : consulter ses propres dossiers de remplacement.
    Agent/Admin : via AdminDemandeRemplacementView.
    """
    serializer_class   = DemandeRemplacementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'police']:
            # L'admin/police peut voir tous les dossiers via ce endpoint aussi
            return DemandeRemplacement.objects.select_related(
                'declaration__user', 'declaration__categorie', 'traite_par'
            ).all()
        return DemandeRemplacement.objects.filter(
            declaration__user=user
        ).select_related('declaration__categorie', 'traite_par')

    @action(detail=True, methods=['get'])
    def telecharger_autorisation(self, request, pk=None):
        """Télécharge le PDF d'autorisation de remplacement."""
        demande = self.get_object()

        # Vérification des droits
        if request.user.role not in ['admin', 'police']:
            if demande.declaration.user != request.user:
                return Response({'error': 'Accès refusé.'}, status=status.HTTP_403_FORBIDDEN)

        if not demande.autorisation_disponible:
            return Response(
                {'error': "L'autorisation n'est pas encore disponible. En attente de traitement par un agent."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pdf_buffer = generate_autorisation_pdf(demande)
        except Exception as e:
            logger.error("Erreur génération PDF autorisation %s : %s", demande.numero_dossier, e)
            return Response({'error': f'Erreur génération PDF : {str(e)}'}, status=500)

        return FileResponse(
            pdf_buffer, as_attachment=True,
            filename=f"autorisation_{demande.numero_dossier}.pdf",
            content_type='application/pdf'
        )


# =============================================================================
# WORKFLOW DE REMPLACEMENT — AGENT / ADMIN
# =============================================================================

class AdminDemandeRemplacementListView(APIView):
    """
    GET  /api/admin/remplacements/         → liste tous les dossiers
    Filtres query params : statut, search
    """
    permission_classes = [IsAdminOrPolice]

    def get(self, request):
        qs = DemandeRemplacement.objects.select_related(
            'declaration__user', 'declaration__categorie', 'traite_par'
        ).all()

        statut = request.query_params.get('statut', '').strip()
        if statut:
            qs = qs.filter(statut=statut)

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(numero_dossier__icontains=search) |
                Q(declaration__numero_recepisse__icontains=search) |
                Q(declaration__nom_sur_piece__icontains=search) |
                Q(declaration__numero_piece__icontains=search) |
                Q(declaration__user__username__icontains=search) |
                Q(declaration__user__first_name__icontains=search) |
                Q(declaration__user__last_name__icontains=search)
            )

        return Response(DemandeRemplacementSerializer(qs, many=True).data)


class AdminDemandeRemplacementDetailView(APIView):
    """
    GET    /api/admin/remplacements/<pk>/  → détail d'un dossier
    PATCH  /api/admin/remplacements/<pk>/  → changer le statut + infos commissariat
    """
    permission_classes = [IsAdminOrPolice]

    def _get_demande(self, pk):
        try:
            return DemandeRemplacement.objects.select_related(
                'declaration__user', 'declaration__categorie', 'traite_par'
            ).get(pk=pk)
        except DemandeRemplacement.DoesNotExist:
            return None

    def get(self, request, pk):
        demande = self._get_demande(pk)
        if not demande:
            return Response({'error': 'Dossier introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(DemandeRemplacementSerializer(demande).data)

    def patch(self, request, pk):
        demande = self._get_demande(pk)
        if not demande:
            return Response({'error': 'Dossier introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChangerStatutRemplacementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        nouveau_statut = data.get('statut')
        ancien_statut  = demande.statut
        now = timezone.now()

        # Mise à jour des champs de commissariat (toujours)
        if data.get('commissariat'):
            demande.commissariat = data['commissariat']
        if data.get('adresse_commissariat'):
            demande.adresse_commissariat = data['adresse_commissariat']
        if data.get('horaires_commissariat'):
            demande.horaires_commissariat = data['horaires_commissariat']
        if data.get('remarques'):
            demande.remarques = data['remarques']

        # Transition de statut
        if nouveau_statut and nouveau_statut != ancien_statut:
            demande.statut     = nouveau_statut
            demande.traite_par = request.user

            # Dates automatiques selon la transition
            if nouveau_statut == 'RECEPISSE_EMIS':
                demande.date_emission_recepisse = now
                # Passer la déclaration en REMPLACEMENT si pas déjà fait
                Declaration.objects.filter(pk=demande.declaration.pk).update(statut='REMPLACEMENT')

            elif nouveau_statut == 'EN_TRAITEMENT':
                demande.date_depot_commissariat = now

            elif nouveau_statut == 'DOCUMENT_PRET':
                demande.date_document_pret = now

            elif nouveau_statut == 'RETIRE':
                demande.date_retrait = now
                # Clôturer la déclaration
                Declaration.objects.filter(pk=demande.declaration.pk).update(statut='CLOTURE')

            elif nouveau_statut == 'ANNULE':
                # Remettre la déclaration en VALIDE si on annule le remplacement
                Declaration.objects.filter(pk=demande.declaration.pk).update(statut='VALIDE')

        demande.save()

        # Recharger les relations pour la sérialisation
        demande.refresh_from_db()

        # Notification in-app
        _notifier_citoyen_remplacement(demande, ancien_statut)

        # Email
        _mapping_email = {
            'RECEPISSE_EMIS': 'recepisse_emis',
            'EN_TRAITEMENT':  'en_traitement',
            'DOCUMENT_PRET':  'document_pret',
            'RETIRE':         'retire',
        }
        if nouveau_statut in _mapping_email:
            try:
                envoyer_email_remplacement(
                    _mapping_email[nouveau_statut],
                    demande.declaration.user,
                    demande
                )
            except Exception as exc:
                logger.error("Email remplacement '%s' échoué pour %s : %s",
                             nouveau_statut, demande.numero_dossier, exc)

        return Response(DemandeRemplacementSerializer(demande).data)


def _notifier_citoyen_remplacement(demande, ancien_statut=None):
    """Crée une notification in-app lors d'un changement de statut du dossier."""
    titres = {
        'RECEPISSE_EMIS': '📄 Votre autorisation de remplacement est prête',
        'EN_TRAITEMENT':  '⚙️ Votre dossier est en cours de traitement au commissariat',
        'DOCUMENT_PRET':  '🎉 Votre nouvelle pièce est prête à être retirée !',
        'RETIRE':         '✅ Procédure de remplacement terminée',
        'ANNULE':         '❌ Votre dossier de remplacement a été annulé',
    }
    messages = {
        'RECEPISSE_EMIS': (
            f"Votre autorisation pour le dossier {demande.numero_dossier} est disponible. "
            f"Connectez-vous à DéclaTogo pour la télécharger et déposez-la au commissariat "
            f"{demande.commissariat or 'désigné'}."
        ),
        'EN_TRAITEMENT': (
            f"Le commissariat a bien reçu votre dossier {demande.numero_dossier}. "
            "Votre nouvelle pièce est en cours de fabrication."
        ),
        'DOCUMENT_PRET': (
            f"Votre nouvelle pièce (dossier {demande.numero_dossier}) est prête ! "
            f"Rendez-vous au commissariat {demande.commissariat or ''} pour la retirer."
        ),
        'RETIRE': (
            f"Votre dossier de remplacement {demande.numero_dossier} est clôturé. "
            "Bonne continuation !"
        ),
        'ANNULE': (
            f"Le dossier de remplacement {demande.numero_dossier} a été annulé. "
            "Contactez le service pour plus d'informations."
        ),
    }

    statut = demande.statut
    if statut not in titres:
        return

    Notification.objects.create(
        user=demande.declaration.user,
        declaration=demande.declaration,
        type_notification='REMPLACEMENT',
        titre=titres[statut],
        message=messages[statut],
    )


# =============================================================================
# NOTIFICATIONS
# =============================================================================

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class   = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        return Response(self.get_serializer(self.get_queryset().filter(lue=False), many=True).data)

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
            'en_remplacement':       Declaration.objects.filter(statut='REMPLACEMENT').count(),
            'total_utilisateurs':    User.objects.count(),
            'total_citoyens':        User.objects.filter(role='citoyen').count(),
            'total_agents':          User.objects.filter(role__in=['police', 'admin']).count(),
            'remplacements_en_attente': DemandeRemplacement.objects.filter(statut='EN_ATTENTE').count(),
            'remplacements_recents': DemandeRemplacementSerializer(
                DemandeRemplacement.objects.order_by('-date_creation')[:5], many=True
            ).data,
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


# =============================================================================
# CHANGEMENT DE MOT DE PASSE
# =============================================================================

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user    = request.user
        old_pwd = request.data.get('current_password', '')
        new_pwd = request.data.get('new_password', '')
        if not authenticate(username=user.username, password=old_pwd):
            return Response({'current_password': 'Mot de passe actuel incorrect.'}, status=400)
        if len(new_pwd) < 8:
            return Response({'new_password': 'Minimum 8 caractères.'}, status=400)
        user.set_password(new_pwd)
        user.save()
        return Response({'message': 'Mot de passe modifié avec succès.'})
