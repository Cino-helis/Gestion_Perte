"""
Vues de l'API REST
Gèrent les requêtes HTTP et la logique métier
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from .models import User, CategoriePiece, Declaration, Notification
from .serializers import (
    UserSerializer, UserProfileSerializer, CategoriePieceSerializer,
    DeclarationListSerializer, DeclarationDetailSerializer,
    DeclarationCreateSerializer, NotificationSerializer,
    StatistiquesSerializer, RechercheCorrespondanceSerializer
)

User = get_user_model()


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


class CategoriePieceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les catégories de pièces
    Liste et détails uniquement (lecture seule pour les utilisateurs)
    """
    queryset = CategoriePiece.objects.filter(actif=True)
    serializer_class = CategoriePieceSerializer
    permission_classes = [permissions.AllowAny]  # Accessible sans authentification


class DeclarationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les déclarations (CRUD complet)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtre les déclarations selon le rôle de l'utilisateur
        """
        user = self.request.user
        
        if user.role in ['admin', 'police']:
            # Les admins voient toutes les déclarations
            return Declaration.objects.all()
        else:
            # Les citoyens voient uniquement leurs propres déclarations
            return Declaration.objects.filter(user=user)
    
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
    
    def perform_create(self, serializer):
        """
        Associe automatiquement l'utilisateur connecté
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def mes_declarations(self, request):
        """
        Endpoint personnalisé pour voir ses propres déclarations
        GET /api/declarations/mes_declarations/
        """
        declarations = self.get_queryset().filter(user=request.user)
        serializer = DeclarationListSerializer(declarations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pertes(self, request):
        """
        Filtre uniquement les pertes
        GET /api/declarations/pertes/
        """
        pertes = self.get_queryset().filter(type_declaration='PERTE')
        serializer = DeclarationListSerializer(pertes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trouvailles(self, request):
        """
        Filtre uniquement les trouvailles
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
        
        # Recherche dans les trouvailles
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
        serializer = DeclarationListSerializer(correspondances, many=True)
        
        return Response({
            'nombre_resultats': correspondances.count(),
            'correspondances': serializer.data
        })
    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def changer_statut(self, request, pk=None):
        """
        Permet à un admin de changer le statut d'une déclaration
        PATCH /api/declarations/{id}/changer_statut/
        Body: {"statut": "VALIDE", "remarques": "..."}
        """
        declaration = self.get_object()
        nouveau_statut = request.data.get('statut')
        remarques = request.data.get('remarques', '')
        
        if nouveau_statut not in dict(Declaration.STATUT_CHOICES):
            return Response(
                {'error': 'Statut invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ancien_statut = declaration.statut
        declaration.statut = nouveau_statut
        if remarques:
            declaration.remarques_admin = remarques
        declaration.save()
        
        # Créer une notification pour l'utilisateur
        Notification.objects.create(
            user=declaration.user,
            declaration=declaration,
            type_notification='STATUT',
            titre=f"Changement de statut : {declaration.numero_recepisse}",
            message=f"Votre déclaration est passée de '{ancien_statut}' à '{nouveau_statut}'. {remarques}"
        )
        
        serializer = DeclarationDetailSerializer(declaration)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Chaque utilisateur voit uniquement ses propres notifications
        """
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        """
        Récupère uniquement les notifications non lues
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
        self.get_queryset().update(lue=True)
        return Response({'status': 'Toutes les notifications ont été marquées comme lues'})


class StatistiquesView(APIView):
    """
    Vue pour les statistiques du dashboard admin
    GET /api/statistiques/
    """
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Statistiques générales
        total_declarations = Declaration.objects.count()
        total_pertes = Declaration.objects.filter(type_declaration='PERTE').count()
        total_trouvailles = Declaration.objects.filter(type_declaration='TROUVAILLE').count()
        
        # Par statut
        en_attente = Declaration.objects.filter(statut='EN_ATTENTE').count()
        validees = Declaration.objects.filter(statut='VALIDE').count()
        retrouvees = Declaration.objects.filter(statut='RETROUVE').count()
        restituees = Declaration.objects.filter(statut='RESTITUE').count()
        
        # Déclarations récentes (7 derniers jours)
        date_limite = timezone.now() - timedelta(days=7)
        declarations_recentes = Declaration.objects.filter(
            date_declaration__gte=date_limite
        ).order_by('-date_declaration')[:10]
        
        # Catégories les plus populaires
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
            'declarations_recentes': DeclarationListSerializer(declarations_recentes, many=True).data,
            'categories_populaires': list(categories_populaires)
        }
        
        return Response(data)