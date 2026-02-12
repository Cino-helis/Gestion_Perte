"""
Configuration de l'interface d'administration Django
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, CategoriePiece, Declaration, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administration personnalisée pour le modèle User
    """
    list_display = ['username', 'email', 'telephone', 'role', 'is_active', 'date_creation']
    list_filter = ['role', 'is_active', 'date_creation']
    search_fields = ['username', 'email', 'telephone', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('telephone', 'role')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('telephone', 'role')
        }),
    )


@admin.register(CategoriePiece)
class CategoriePieceAdmin(admin.ModelAdmin):
    """
    Administration pour les catégories de pièces
    """
    list_display = ['libelle', 'icone', 'actif', 'nombre_declarations', 'date_creation']
    list_filter = ['actif', 'date_creation']
    search_fields = ['libelle', 'description']
    list_editable = ['actif']
    
    def nombre_declarations(self, obj):
        """Affiche le nombre de déclarations dans cette catégorie"""
        count = obj.declarations.count()
        return format_html('<strong>{}</strong>', count)
    nombre_declarations.short_description = 'Nombre de déclarations'


@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):
    """
    Administration pour les déclarations
    """
    list_display = [
        'numero_recepisse', 'type_declaration', 'categorie', 'numero_piece',
        'nom_sur_piece', 'statut_badge', 'user', 'date_declaration'
    ]
    list_filter = [
        'type_declaration', 'statut', 'categorie',
        'date_declaration', 'date_perte'
    ]
    search_fields = [
        'numero_recepisse', 'numero_piece', 'nom_sur_piece',
        'user__username', 'user__email', 'lieu_perte'
    ]
    readonly_fields = [
        'numero_recepisse', 'date_declaration', 'date_modification',
        'user', 'type_declaration'
    ]
    list_editable = []
    date_hierarchy = 'date_declaration'
    
    fieldsets = (
        ('Informations de base', {
            'fields': (
                'numero_recepisse', 'type_declaration', 'categorie',
                'numero_piece', 'nom_sur_piece', 'user'
            )
        }),
        ('Détails de la déclaration', {
            'fields': (
                'description', 'lieu_perte', 'date_perte',
                'photo_piece', 'latitude', 'longitude'
            )
        }),
        ('Gestion administrative', {
            'fields': (
                'statut', 'remarques_admin', 'declaration_correspondante'
            )
        }),
        ('Métadonnées', {
            'fields': ('date_declaration', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def statut_badge(self, obj):
        """Affiche le statut avec une couleur"""
        colors = {
            'EN_ATTENTE': '#f39c12',  # Orange
            'VALIDE': '#3498db',      # Bleu
            'RETROUVE': '#2ecc71',    # Vert
            'RESTITUE': '#27ae60',    # Vert foncé
            'REJETE': '#e74c3c',      # Rouge
            'CLOTURE': '#95a5a6',     # Gris
        }
        color = colors.get(obj.statut, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
    
    actions = ['valider_declarations', 'marquer_retrouvees']
    
    def valider_declarations(self, request, queryset):
        """Action pour valider plusieurs déclarations en masse"""
        count = queryset.filter(statut='EN_ATTENTE').update(statut='VALIDE')
        self.message_user(request, f'{count} déclaration(s) validée(s).')
    valider_declarations.short_description = "Valider les déclarations sélectionnées"
    
    def marquer_retrouvees(self, request, queryset):
        """Action pour marquer comme retrouvées"""
        count = queryset.update(statut='RETROUVE')
        self.message_user(request, f'{count} déclaration(s) marquée(s) comme retrouvée(s).')
    marquer_retrouvees.short_description = "Marquer comme retrouvées"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Administration pour les notifications
    """
    list_display = ['titre', 'user', 'type_notification', 'lue_badge', 'date_creation']
    list_filter = ['type_notification', 'lue', 'date_creation']
    search_fields = ['titre', 'message', 'user__username']
    readonly_fields = ['date_creation']
    date_hierarchy = 'date_creation'
    
    def lue_badge(self, obj):
        """Affiche si la notification est lue"""
        if obj.lue:
            return format_html(
                '<span style="color: green;">✓ Lue</span>'
            )
        return format_html(
            '<span style="color: orange;">✗ Non lue</span>'
        )
    lue_badge.short_description = 'État'
    
    actions = ['marquer_lues']
    
    def marquer_lues(self, request, queryset):
        """Action pour marquer comme lues"""
        count = queryset.update(lue=True)
        self.message_user(request, f'{count} notification(s) marquée(s) comme lue(s).')
    marquer_lues.short_description = "Marquer comme lues"