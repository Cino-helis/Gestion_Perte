"""
URLs de l'application declarations
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserProfileView,
    AgentManagementView, AgentDetailView,
    UserManagementView, UserDetailAdminView,   # ← NOUVEAU
    CategoriePieceViewSet, DeclarationViewSet,
    NotificationViewSet, StatistiquesView
)

router = DefaultRouter()
router.register(r'categories',    CategoriePieceViewSet, basename='categorie')
router.register(r'declarations',  DeclarationViewSet,    basename='declaration')
router.register(r'notifications', NotificationViewSet,   basename='notification')

urlpatterns = [
    # Auth & profil
    path('register/', RegisterView.as_view(),    name='register'),
    path('profile/',  UserProfileView.as_view(), name='profile'),

    # Statistiques
    path('statistiques/', StatistiquesView.as_view(), name='statistiques'),

    # ── Gestion agents (admin) ───────────────────────────────────────
    path('admin/agents/',          AgentManagementView.as_view(), name='agent-list'),
    path('admin/agents/<int:pk>/', AgentDetailView.as_view(),     name='agent-detail'),

    # ── Gestion utilisateurs (admin) — NOUVEAU ───────────────────────
    path('admin/users/',           UserManagementView.as_view(),  name='user-list'),
    path('admin/users/<int:pk>/',  UserDetailAdminView.as_view(), name='user-detail'),

    # Routes auto (router)
    path('', include(router.urls)),
]