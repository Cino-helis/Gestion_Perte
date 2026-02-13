"""
Vues de l'API REST
Gèrent les requêtes HTTP et la logique métier
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

from .models import CategoriePiece, Declaration, Notification
from .serializers import (
    UserSerializer, UserProfileSerializer, CategoriePieceSerializer,
    DeclarationListSerializer, DeclarationDetailSerializer,
    DeclarationCreateSerializer, NotificationSerializer,
    StatistiquesSerializer, RechercheCorrespondanceSerializer
)
from .permissions import IsAdminOrPolice, IsAdminOnly, IsOwnerOrAdminOrPolice

User = get_user_model()


# =============================================================================
# AUTHENTIFICATION & PROFIL
# =============================================================================

class RegisterView(APIView):
    """
    Vue pour l'inscription d'un nouvel utilisateur
    POST /api/register/
    """
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
    """
    Vue pour voir et modifier le profil de l'utilisateur connecté
    GET/PUT /api/profile/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================================================================
# CATÉGORIES
# =============================================================================

class CategoriePieceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les catégories de pièces (lecture seule pour tous)
    """
    queryset = CategoriePiece.objects.filter(actif=True)
    serializer_class = CategoriePieceSerializer
    permission_classes = [permissions.AllowAny]


# =============================================================================
# DÉCLARATIONS
# =============================================================================

class DeclarationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les déclarations (CRUD complet)
    """
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
        elif self.action == 'create':
            return DeclarationCreateSerializer
        return DeclarationDetailSerializer

    def get_permissions(self):
        if self.action == 'changer_statut':
            return [IsAdminOrPolice()]
        if self.action == 'destroy':
            return [IsAdminOnly()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """L'utilisateur est injecté dans DeclarationCreateSerializer.create()"""
        serializer.save()

    # ------------------------------------------------------------------
    # PDF
    # ------------------------------------------------------------------

    @action(detail=True, methods=['get'])
    def telecharger_recepisse(self, request, pk=None):
        """
        Génère et retourne le récépissé PDF.
        GET /api/declarations/{id}/telecharger_recepisse/
        """
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
                {'error': f'Erreur lors de la génération du PDF : {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=f"recepisse_{declaration.numero_recepisse}.pdf",
            content_type='application/pdf'
        )

    # ------------------------------------------------------------------
    # Actions personnalisées
    # ------------------------------------------------------------------

    @action(detail=False, methods=['get'])
    def mes_declarations(self, request):
        """
        Déclarations de l'utilisateur connecté
        GET /api/declarations/mes_declarations/
        """
        declarations = Declaration.objects.filter(user=request.user).select_related('categorie')
        serializer = DeclarationListSerializer(declarations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pertes(self, request):
        """GET /api/declarations/pertes/"""
        pertes = self.get_queryset().filter(type_declaration='PERTE')
        serializer = DeclarationListSerializer(pertes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trouvailles(self, request):
        """GET /api/declarations/trouvailles/"""
        trouvailles = self.get_queryset().filter(type_declaration='TROUVAILLE')
        serializer = DeclarationListSerializer(trouvailles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def rechercher(self, request):
        """
        Recherche de correspondances entre pertes et trouvailles.
        Cherche dans numero_piece, nom_sur_piece, nom_declarant et prenom_declarant.

        POST /api/declarations/rechercher/
        Body: {
          "numero_piece":   "TG20240001",   ← optionnel
          "nom_declarant":  "AKODJO",       ← optionnel
          "prenom_declarant": "Jean",       ← optionnel
          "nom_sur_piece":  "AKODJO Jean",  ← optionnel (rétrocompat)
          "categorie":      1               ← optionnel
        }
        """
        serializer = RechercheCorrespondanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        numero_piece     = serializer.validated_data.get('numero_piece', '').strip()
        nom_sur_piece    = serializer.validated_data.get('nom_sur_piece', '').strip()
        nom_declarant    = serializer.validated_data.get('nom_declarant', '').strip()
        prenom_declarant = serializer.validated_data.get('prenom_declarant', '').strip()
        categorie_id     = serializer.validated_data.get('categorie')

        # Base : trouvailles validées uniquement
        query = Q(type_declaration='TROUVAILLE', statut='VALIDE')

        # Au moins un critère doit être fourni
        has_criteria = any([numero_piece, nom_sur_piece, nom_declarant, prenom_declarant])
        if not has_criteria:
            return Response(
                {'error': 'Fournissez au moins un critère de recherche.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Numéro de pièce
        if numero_piece:
            query &= Q(numero_piece__icontains=numero_piece)

        # Nom — cherche dans nom_declarant ET nom_sur_piece (rétrocompat)
        if nom_declarant:
            query &= (
                Q(nom_declarant__icontains=nom_declarant) |
                Q(nom_sur_piece__icontains=nom_declarant)
            )

        # Prénom — cherche dans prenom_declarant ET nom_sur_piece (rétrocompat)
        if prenom_declarant:
            query &= (
                Q(prenom_declarant__icontains=prenom_declarant) |
                Q(nom_sur_piece__icontains=prenom_declarant)
            )

        # nom_sur_piece complet (ancien champ — rétrocompatibilité)
        if nom_sur_piece and not nom_declarant and not prenom_declarant:
            query &= Q(nom_sur_piece__icontains=nom_sur_piece)

        # Catégorie
        if categorie_id:
            query &= Q(categorie_id=categorie_id)

        correspondances = Declaration.objects.filter(query).select_related('categorie', 'user')
        result_serializer = DeclarationListSerializer(correspondances, many=True)

        return Response({
            'nombre_resultats': correspondances.count(),
            'correspondances':  result_serializer.data,
        })

    @action(detail=True, methods=['patch'])
    def changer_statut(self, request, pk=None):
        """
        Permet à un admin ou agent de police de changer le statut.
        PATCH /api/declarations/{id}/changer_statut/
        Body: {"statut": "VALIDE", "remarques": "..."}
        """
        declaration = self.get_object()
        nouveau_statut = request.data.get('statut')
        remarques = request.data.get('remarques', '')

        if nouveau_statut not in dict(Declaration.STATUT_CHOICES):
            return Response(
                {'error': f"Statut invalide. Valeurs acceptées : {list(dict(Declaration.STATUT_CHOICES).keys())}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ancien_statut = declaration.get_statut_display()
        declaration.statut = nouveau_statut
        if remarques:
            declaration.remarques_admin = remarques
        declaration.save()

        Notification.objects.create(
            user=declaration.user,
            declaration=declaration,
            type_notification='STATUT',
            titre=f"Changement de statut : {declaration.numero_recepisse}",
            message=(
                f"Votre déclaration est passée de '{ancien_statut}' "
                f"à '{declaration.get_statut_display()}'. {remarques}"
            )
        )

        serializer = DeclarationDetailSerializer(declaration)
        return Response(serializer.data)


# =============================================================================
# NOTIFICATIONS
# =============================================================================

class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet pour les notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        """GET /api/notifications/non_lues/"""
        notifications = self.get_queryset().filter(lue=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def marquer_lue(self, request, pk=None):
        """POST /api/notifications/{id}/marquer_lue/"""
        notification = self.get_object()
        notification.lue = True
        notification.save()
        return Response({'status': 'Notification marquée comme lue'})

    @action(detail=False, methods=['post'])
    def tout_marquer_lues(self, request):
        """POST /api/notifications/tout_marquer_lues/"""
        count = self.get_queryset().update(lue=True)
        return Response({'status': f'{count} notification(s) marquée(s) comme lue(s)'})


# =============================================================================
# STATISTIQUES (DASHBOARD ADMIN)
# =============================================================================

class StatistiquesView(APIView):
    """
    Statistiques pour le dashboard admin/police
    GET /api/statistiques/
    """
    permission_classes = [IsAdminOrPolice]

    def get(self, request):
        total_declarations = Declaration.objects.count()
        total_pertes       = Declaration.objects.filter(type_declaration='PERTE').count()
        total_trouvailles  = Declaration.objects.filter(type_declaration='TROUVAILLE').count()

        en_attente = Declaration.objects.filter(statut='EN_ATTENTE').count()
        validees   = Declaration.objects.filter(statut='VALIDE').count()
        retrouvees = Declaration.objects.filter(statut='RETROUVE').count()
        restituees = Declaration.objects.filter(statut='RESTITUE').count()

        date_limite = timezone.now() - timedelta(days=7)
        declarations_recentes = Declaration.objects.filter(
            date_declaration__gte=date_limite
        ).order_by('-date_declaration')[:10]

        categories_populaires = CategoriePiece.objects.annotate(
            nombre=Count('declarations')
        ).order_by('-nombre')[:5].values('libelle', 'nombre')

        data = {
            'total_declarations':   total_declarations,
            'total_pertes':         total_pertes,
            'total_trouvailles':    total_trouvailles,
            'en_attente':           en_attente,
            'validees':             validees,
            'retrouvees':           retrouvees,
            'restituees':           restituees,
            'declarations_recentes': DeclarationListSerializer(
                declarations_recentes, many=True
            ).data,
            'categories_populaires': list(categories_populaires),
        }

        return Response(data)