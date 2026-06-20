"""
URLs de l'application declarations — VERSION AVEC WORKFLOW DE REMPLACEMENT
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserProfileView,
    AgentManagementView, AgentDetailView,
    UserManagementView, UserDetailAdminView,
    CategoriePieceViewSet, DeclarationViewSet,
    NotificationViewSet, StatistiquesView,
    DemandeRemplacementViewSet,
    AdminDemandeRemplacementListView, AdminDemandeRemplacementDetailView,
    ChangePasswordView,
)

router = DefaultRouter()
router.register(r'categories',       CategoriePieceViewSet,        basename='categorie')
router.register(r'declarations',     DeclarationViewSet,           basename='declaration')
router.register(r'notifications',    NotificationViewSet,          basename='notification')
router.register(r'remplacements',    DemandeRemplacementViewSet,   basename='remplacement')

urlpatterns = [
    # Auth & profil
    path('register/', RegisterView.as_view(),    name='register'),
    path('profile/',  UserProfileView.as_view(), name='profile'),

    # Statistiques
    path('statistiques/', StatistiquesView.as_view(), name='statistiques'),

    # ── Gestion agents (admin) ───────────────────────────────────────────────
    path('admin/agents/',          AgentManagementView.as_view(), name='agent-list'),
    path('admin/agents/<int:pk>/', AgentDetailView.as_view(),     name='agent-detail'),

    # ── Gestion utilisateurs (admin) ─────────────────────────────────────────
    path('admin/users/',           UserManagementView.as_view(),  name='user-list'),
    path('admin/users/<int:pk>/',  UserDetailAdminView.as_view(), name='user-detail'),

    # ── Dossiers de remplacement (agent/admin) ───────────────────────────────
    path('admin/remplacements/',
         AdminDemandeRemplacementListView.as_view(),   name='admin-remplacement-list'),
    path('admin/remplacements/<int:pk>/',
         AdminDemandeRemplacementDetailView.as_view(), name='admin-remplacement-detail'),

    # Routes auto (router)
    path('', include(router.urls)),

    # Changement de mot de passe
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
