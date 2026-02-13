"""
Modèles de données pour la plateforme de déclarations de pertes - Togo
VERSION CORRIGÉE
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé
    Hérite de AbstractUser pour ajouter des champs spécifiques au Togo
    """
    
    ROLE_CHOICES = [
        ('citoyen', 'Citoyen'),
        ('admin', 'Administrateur'),
        ('police', 'Agent de Police'),
    ]
    
    # Validateur pour numéro de téléphone togolais
    phone_regex = RegexValidator(
        regex=r'^(\+228)?[0-9]{8}$',
        message="Format: '+22890123456' ou '90123456'"
    )
    
    telephone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Numéro de téléphone"
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='citoyen',
        verbose_name="Rôle"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )
    
    # CORRECTION: Ajout de related_name pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # ← AJOUTÉ
        related_query_name='custom_user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # ← AJOUTÉ
        related_query_name='custom_user',
    )
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class CategoriePiece(models.Model):
    """
    Catégories de pièces administratives
    Ex: Identité, Véhicule, Scolaire, etc.
    """
    
    libelle = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la catégorie"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    
    icone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Nom de l'icône (ex: 'id-card', 'car', 'graduation-cap')",
        verbose_name="Icône"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    class Meta:
        verbose_name = "Catégorie de pièce"
        verbose_name_plural = "Catégories de pièces"
        ordering = ['libelle']
    
    def __str__(self):
        return self.libelle


class Declaration(models.Model):
    """
    Déclaration de perte ou de trouvaille
    """
    
    TYPE_CHOICES = [
        ('PERTE', 'Perte'),
        ('TROUVAILLE', 'Trouvaille'),
    ]
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente de validation'),
        ('VALIDE', 'Validé'),
        ('RETROUVE', 'Retrouvé/Correspondance trouvée'),
        ('RESTITUE', 'Restitué au propriétaire'),
        ('REJETE', 'Rejeté'),
        ('CLOTURE', 'Clôturé'),
    ]
    
    # Champs obligatoires
    type_declaration = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        verbose_name="Type de déclaration"
    )
    
    categorie = models.ForeignKey(
        CategoriePiece,
        on_delete=models.PROTECT,
        related_name='declarations',
        verbose_name="Catégorie"
    )
    
    numero_piece = models.CharField(
        max_length=100,
        db_index=True,  # Index pour recherche rapide
        verbose_name="Numéro de la pièce",
        help_text="Ex: Numéro CNI, Passeport, Plaque d'immatriculation"
    )
    
    nom_sur_piece = models.CharField(
        max_length=200,
        verbose_name="Nom figurant sur la pièce"
    )
    nom_declarant    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom de famille (sur la pièce)")
    prenom_declarant = models.CharField(max_length=100, blank=True, null=True, verbose_name="Prénom(s) (sur la pièce)")
    date_naissance   = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    lieu_naissance   = models.CharField(max_length=200, blank=True, null=True, verbose_name="Lieu de naissance")
    profession       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profession")
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='declarations',
        verbose_name="Déclarant"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        verbose_name="Statut"
    )
    
    # Informations complémentaires
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description détaillée"
    )
    
    lieu_perte = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Lieu de la perte/trouvaille"
    )
    
    date_perte = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date de la perte/trouvaille"
    )
    
    # Photo de la pièce (optionnel)
    photo_piece = models.ImageField(
        upload_to='pieces/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Photo de la pièce"
    )
    
    # Coordonnées GPS (optionnel - pour future carte)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Latitude"
    )
    
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Longitude"
    )
    
    # Métadonnées
    date_declaration = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de déclaration"
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    # Numéro de récépissé (généré automatiquement)
    numero_recepisse = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Numéro de récépissé"
    )
    
    # Matching (si une correspondance est trouvée)
    declaration_correspondante = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='correspondances',
        verbose_name="Déclaration correspondante"
    )
    
    # Remarques de l'administrateur
    remarques_admin = models.TextField(
        blank=True,
        null=True,
        verbose_name="Remarques de l'administrateur"
    )
    
    class Meta:
        verbose_name = "Déclaration"
        verbose_name_plural = "Déclarations"
        ordering = ['-date_declaration']
        indexes = [
            models.Index(fields=['numero_piece', 'type_declaration']),
            models.Index(fields=['statut', 'date_declaration']),
        ]
    
    def __str__(self):
        return f"{self.get_type_declaration_display()} - {self.numero_piece} ({self.nom_sur_piece})"
    
    def save(self, *args, **kwargs):
        """
        Génère automatiquement un numéro de récépissé si non existant
        Format: PERTE-2024-00001 ou TROUV-2024-00001
        """
        if not self.numero_recepisse:
            prefixe = 'PERTE' if self.type_declaration == 'PERTE' else 'TROUV'
            annee = timezone.now().year
            
            # Compter les déclarations du même type cette année
            count = Declaration.objects.filter(
                type_declaration=self.type_declaration,
                date_declaration__year=annee
            ).count() + 1
            
            self.numero_recepisse = f"{prefixe}-{annee}-{count:05d}"
        
        super().save(*args, **kwargs)
    
    @property
    def est_en_cours(self):
        """Vérifie si la déclaration est encore en cours"""
        return self.statut in ['EN_ATTENTE', 'VALIDE']
    
    @property
    def peut_etre_matche(self):
        """Vérifie si la déclaration peut être matchée"""
        return self.statut == 'VALIDE' and not self.declaration_correspondante


class Notification(models.Model):
    """
    Notifications pour les utilisateurs
    Ex: Votre pièce a peut-être été retrouvée
    """
    
    TYPE_CHOICES = [
        ('INFO', 'Information'),
        ('MATCH', 'Correspondance trouvée'),
        ('STATUT', 'Changement de statut'),
        ('ADMIN', 'Message administrateur'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Destinataire"
    )
    
    declaration = models.ForeignKey(
        Declaration,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='notifications',
        verbose_name="Déclaration concernée"
    )
    
    type_notification = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type"
    )
    
    titre = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )
    
    message = models.TextField(
        verbose_name="Message"
    )
    
    lue = models.BooleanField(
        default=False,
        verbose_name="Lue"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.titre} - {self.user.username}"