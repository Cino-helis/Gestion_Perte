"""
URLs de l'application declarations
Définit les routes de l'API
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserProfileView,
    CategoriePieceViewSet, DeclarationViewSet,
    NotificationViewSet, StatistiquesView
)

# Router pour les ViewSets
router = DefaultRouter()
router.register(r'categories', CategoriePieceViewSet, basename='categorie')
router.register(r'declarations', DeclarationViewSet, basename='declaration')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Authentification et profil
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Statistiques
    path('statistiques/', StatistiquesView.as_view(), name='statistiques'),
    
    # Inclure les routes du router
    path('', include(router.urls)),
]