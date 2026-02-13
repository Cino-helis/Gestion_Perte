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

# CORRECTION #1 : suppression de l'import `User` depuis .models (qui était
# immédiatement écrasé par get_user_model() deux lignes plus bas).
# On importe uniquement les autres modèles nécessaires.
from .models import CategoriePiece, Declaration, Notification
from .serializers import (
    UserSerializer, UserProfileSerializer, CategoriePieceSerializer,
    DeclarationListSerializer, DeclarationDetailSerializer,
    DeclarationCreateSerializer, NotificationSerializer,
    StatistiquesSerializer, RechercheCorrespondanceSerializer
)
# CORRECTION #2 : import des permissions personnalisées basées sur `role`
# (IsAdminUser de DRF vérifie is_staff=True, pas notre champ role)
from .permissions import IsAdminOrPolice, IsAdminOnly, IsOwnerOrAdminOrPolice

# Récupération du modèle User actif (notre User personnalisé)
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
    ViewSet pour les catégories de pièces
    Liste et détails uniquement (lecture seule pour tous)
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
        """
        Filtre les déclarations selon le rôle de l'utilisateur.
        admin/police → toutes les déclarations
        citoyen       → uniquement les siennes
        """
        user = self.request.user

        # CORRECTION #2 appliquée ici aussi : on vérifie `user.role`
        if user.role in ['admin', 'police']:
            return Declaration.objects.select_related(
                'categorie', 'user', 'declaration_correspondante'
            ).all()
        else:
            return Declaration.objects.select_related(
                'categorie', 'user', 'declaration_correspondante'
            ).filter(user=user)

    
    @action(detail=True, methods=['get'])
    def telecharger_recepisse(self, request, pk=None):
        """"
        Génère et retourne le récépissé PDF d'une déclaration.
        GET /api/declarations/{id}/telecharger_recepisse/

        Le PDF est généré à la volée avec ReportLab (aucun stockage disque).
        Permissions :
        - Le propriétaire peut télécharger son propre récépissé
        - Admin et police peuvent tout télécharger
        """
        declaration = self.get_object()
        

        # Vérification de permission manuelle (propriétaire ou staff)
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

        nom_fichier = f"recepisse_{declaration.numero_recepisse}.pdf"

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=nom_fichier,
            content_type='application/pdf'
        )
    

    def get_serializer_class(self):
        """
        Utilise différents sérialiseurs selon l'action
        """
        if self.action == 'list':
            return DeclarationListSerializer
        elif self.action == 'create':
            return DeclarationCreateSerializer
        else:
            return DeclarationDetailSerializer

    def get_permissions(self):
        """
        Permissions granulaires par action :
        - create / list / retrieve / mes_declarations / pertes / trouvailles
          / rechercher : utilisateur authentifié
        - changer_statut : admin ou police uniquement
        - destroy : admin uniquement
        """
        if self.action == 'changer_statut':
            return [IsAdminOrPolice()]
        if self.action == 'destroy':
            return [IsAdminOnly()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Associe automatiquement l'utilisateur connecté"""
        serializer.save(user=self.request.user)

    # ------------------------------------------------------------------
    # Actions personnalisées
    # ------------------------------------------------------------------

    @action(detail=False, methods=['get'])
    def mes_declarations(self, request):
        """
        Déclarations de l'utilisateur connecté
        GET /api/declarations/mes_declarations/
        """
        declarations = Declaration.objects.filter(user=request.user)
        serializer = DeclarationListSerializer(declarations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pertes(self, request):
        """
        Uniquement les pertes (filtrées selon le rôle)
        GET /api/declarations/pertes/
        """
        pertes = self.get_queryset().filter(type_declaration='PERTE')
        serializer = DeclarationListSerializer(pertes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trouvailles(self, request):
        """
        Uniquement les trouvailles (filtrées selon le rôle)
        GET /api/declarations/trouvailles/
        """
        trouvailles = self.get_queryset().filter(type_declaration='TROUVAILLE')
        serializer = DeclarationListSerializer(trouvailles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def rechercher(self, request):
        """
        Recherche de correspondances entre pertes et trouvailles
        POST /api/declarations/rechercher/
        Body: {"numero_piece": "12345", "nom_sur_piece": "AKODJO"}
        """
        serializer = RechercheCorrespondanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        numero_piece = serializer.validated_data.get('numero_piece')
        nom_sur_piece = serializer.validated_data.get('nom_sur_piece', '')
        categorie_id = serializer.validated_data.get('categorie')

        query = Q(
            type_declaration='TROUVAILLE',
            statut='VALIDE',
            numero_piece__icontains=numero_piece
        )

        if nom_sur_piece:
            query &= Q(nom_sur_piece__icontains=nom_sur_piece)

        if categorie_id:
            query &= Q(categorie_id=categorie_id)

        correspondances = Declaration.objects.filter(query)
        result_serializer = DeclarationListSerializer(correspondances, many=True)

        return Response({
            'nombre_resultats': correspondances.count(),
            'correspondances': result_serializer.data
        })

    @action(detail=True, methods=['patch'])
    def changer_statut(self, request, pk=None):
        """
        Permet à un admin ou agent de police de changer le statut.
        CORRECTION #2 : la permission est maintenant gérée par IsAdminOrPolice
        dans get_permissions(), qui vérifie user.role au lieu de is_staff.

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

        # Notification pour le déclarant
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
    """
    ViewSet pour les notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Chaque utilisateur voit uniquement ses propres notifications"""
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        """
        Notifications non lues
        GET /api/notifications/non_lues/
        """
        notifications = self.get_queryset().filter(lue=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def marquer_lue(self, request, pk=None):
        """
        Marque une notification comme lue
        POST /api/notifications/{id}/marquer_lue/
        """
        notification = self.get_object()
        notification.lue = True
        notification.save()
        return Response({'status': 'Notification marquée comme lue'})

    @action(detail=False, methods=['post'])
    def tout_marquer_lues(self, request):
        """
        Marque toutes les notifications comme lues
        POST /api/notifications/tout_marquer_lues/
        """
        count = self.get_queryset().update(lue=True)
        return Response({'status': f'{count} notification(s) marquée(s) comme lue(s)'})


# =============================================================================
# STATISTIQUES (DASHBOARD ADMIN)
# =============================================================================

class StatistiquesView(APIView):
    """
    Statistiques pour le dashboard admin/police
    GET /api/statistiques/

    CORRECTION #2 : remplace permissions.IsAdminUser (vérifie is_staff)
    par IsAdminOrPolice (vérifie user.role).
    """
    # CORRECTION #2 appliquée ici
    permission_classes = [IsAdminOrPolice]

    def get(self, request):
        total_declarations = Declaration.objects.count()
        total_pertes = Declaration.objects.filter(type_declaration='PERTE').count()
        total_trouvailles = Declaration.objects.filter(type_declaration='TROUVAILLE').count()

        en_attente = Declaration.objects.filter(statut='EN_ATTENTE').count()
        validees = Declaration.objects.filter(statut='VALIDE').count()
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
            'total_declarations': total_declarations,
            'total_pertes': total_pertes,
            'total_trouvailles': total_trouvailles,
            'en_attente': en_attente,
            'validees': validees,
            'retrouvees': retrouvees,
            'restituees': restituees,
            'declarations_recentes': DeclarationListSerializer(
                declarations_recentes, many=True
            ).data,
            'categories_populaires': list(categories_populaires)
        }

        return Response(data)