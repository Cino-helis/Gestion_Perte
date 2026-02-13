"""
Permissions personnalisées pour l'API REST
Basées sur le champ `role` du modèle User personnalisé
(et non sur `is_staff` comme le fait IsAdminUser par défaut)
"""

from rest_framework import permissions


class IsAdminOrPolice(permissions.BasePermission):
    """
    Autorise uniquement les utilisateurs avec le rôle 'admin' ou 'police'.
    Utilisé pour : changer_statut, dashboard statistiques, etc.
    """
    message = "Accès réservé aux administrateurs et agents de police."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ['admin', 'police']
        )


class IsAdminOnly(permissions.BasePermission):
    """
    Autorise uniquement les utilisateurs avec le rôle 'admin'.
    Utilisé pour les actions sensibles (suppression, etc.)
    """
    message = "Accès réservé aux administrateurs."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsOwnerOrAdminOrPolice(permissions.BasePermission):
    """
    Autorise le propriétaire de l'objet, ou un admin/police.
    Utilisé pour : voir/modifier une déclaration spécifique.
    """
    message = "Vous n'avez pas la permission d'accéder à cette ressource."

    def has_object_permission(self, request, view, obj):
        # Les admins et policiers ont accès à tout
        if request.user.role in ['admin', 'police']:
            return True
        # Le propriétaire a accès à son propre objet
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Autorise la lecture à tous les authentifiés,
    mais la modification uniquement au propriétaire.
    """
    message = "Vous ne pouvez modifier que vos propres ressources."

    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous les authentifiés
        if request.method in permissions.SAFE_METHODS:
            return True
        # Écriture uniquement pour le propriétaire
        return obj.user == request.user