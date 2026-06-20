"""
Modèles de données pour la plateforme de déclarations de pertes - Togo
VERSION AVEC WORKFLOW DE REMPLACEMENT
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import transaction


class User(AbstractUser):
    ROLE_CHOICES = [
        ('citoyen', 'Citoyen'),
        ('admin', 'Administrateur'),
        ('police', 'Agent de Police'),
    ]

    phone_regex = RegexValidator(
        regex=r'^(\+228)?[0-9]{8}$',
        message="Format: '+22890123456' ou '90123456'"
    )

    telephone = models.CharField(
        validators=[phone_regex], max_length=15,
        blank=True, null=True, verbose_name="Numéro de téléphone"
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='citoyen', verbose_name="Rôle"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")

    groups = models.ManyToManyField(
        'auth.Group', verbose_name='groups', blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set', related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', verbose_name='user permissions', blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set', related_query_name='custom_user',
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class CategoriePiece(models.Model):
    libelle = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    icone = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="Nom de l'icône (ex: 'id-card', 'car', 'graduation-cap')",
        verbose_name="Icône"
    )
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Catégorie de pièce"
        verbose_name_plural = "Catégories de pièces"
        ordering = ['libelle']

    def __str__(self):
        return self.libelle


class Declaration(models.Model):
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
        ('REMPLACEMENT', 'En cours de remplacement'),  # ← NOUVEAU : déclenché après 7j sans match
    ]

    type_declaration = models.CharField(max_length=15, choices=TYPE_CHOICES, verbose_name="Type de déclaration")
    categorie = models.ForeignKey(
        CategoriePiece, on_delete=models.PROTECT,
        related_name='declarations', verbose_name="Catégorie"
    )
    numero_piece = models.CharField(
        max_length=100, db_index=True, verbose_name="Numéro de la pièce",
        help_text="Ex: Numéro CNI, Passeport, Plaque d'immatriculation"
    )
    nom_sur_piece = models.CharField(max_length=200, verbose_name="Nom figurant sur la pièce")
    nom_declarant    = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom de famille (sur la pièce)")
    prenom_declarant = models.CharField(max_length=100, blank=True, null=True, verbose_name="Prénom(s) (sur la pièce)")
    date_naissance   = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    lieu_naissance   = models.CharField(max_length=200, blank=True, null=True, verbose_name="Lieu de naissance")
    profession       = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profession")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='declarations', verbose_name="Déclarant"
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES,
        default='EN_ATTENTE', verbose_name="Statut"
    )
    description  = models.TextField(blank=True, null=True, verbose_name="Description détaillée")
    lieu_perte   = models.CharField(max_length=300, blank=True, null=True, verbose_name="Lieu de la perte/trouvaille")
    date_perte   = models.DateField(blank=True, null=True, verbose_name="Date de la perte/trouvaille")
    photo_piece  = models.ImageField(upload_to='pieces/%Y/%m/', blank=True, null=True, verbose_name="Photo de la pièce")
    latitude     = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitude")
    longitude    = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitude")

    date_declaration  = models.DateTimeField(auto_now_add=True, verbose_name="Date de déclaration")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    numero_recepisse = models.CharField(
        max_length=50, unique=True, blank=True, null=True,
        verbose_name="Numéro de récépissé"
    )
    declaration_correspondante = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='correspondances', verbose_name="Déclaration correspondante"
    )
    remarques_admin = models.TextField(blank=True, null=True, verbose_name="Remarques de l'administrateur")

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
        if not self.numero_recepisse:
            prefixe = 'PERTE' if self.type_declaration == 'PERTE' else 'TROUV'
            annee = timezone.now().year
            with transaction.atomic():
                count = Declaration.objects.select_for_update().filter(
                    type_declaration=self.type_declaration,
                    date_declaration__year=annee
                ).count() + 1
                self.numero_recepisse = f"{prefixe}-{annee}-{count:05d}"
        super().save(*args, **kwargs)

    @property
    def est_en_cours(self):
        return self.statut in ['EN_ATTENTE', 'VALIDE']

    @property
    def peut_etre_matche(self):
        return self.statut == 'VALIDE' and not self.declaration_correspondante


class DemandeRemplacement(models.Model):
    """
    Dossier de remplacement d'une pièce perdue.

    Cycle de vie :
      EN_ATTENTE      → Créé automatiquement 7 jours après une PERTE sans match
      RECEPISSE_EMIS  → Agent a émis l'autorisation officielle + assigné un commissariat
      EN_TRAITEMENT   → Citoyen a déposé le dossier au commissariat
      DOCUMENT_PRET   → La nouvelle pièce est prête à être retirée
      RETIRE          → Citoyen a retiré son document
      ANNULE          → Annulé (ex : la pièce a finalement été retrouvée)
    """

    STATUT_CHOICES = [
        ('EN_ATTENTE',     "En attente de traitement par un agent"),
        ('RECEPISSE_EMIS', "Autorisation officielle émise — à déposer au commissariat"),
        ('EN_TRAITEMENT',  "Dossier en traitement au commissariat"),
        ('DOCUMENT_PRET',  "Nouvelle pièce prête à retirer"),
        ('RETIRE',         "Document retiré — dossier clôturé"),
        ('ANNULE',         "Annulé"),
    ]

    declaration = models.OneToOneField(
        Declaration,
        on_delete=models.CASCADE,
        related_name='demande_remplacement',
        verbose_name="Déclaration de perte"
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES,
        default='EN_ATTENTE', verbose_name="Statut du dossier"
    )
    numero_dossier = models.CharField(
        max_length=50, unique=True, blank=True, null=True,
        verbose_name="Numéro de dossier"
    )

    # ── Commissariat agréé ──────────────────────────────────────────
    commissariat          = models.CharField(max_length=300, blank=True, null=True, verbose_name="Commissariat agréé")
    adresse_commissariat  = models.TextField(blank=True, null=True, verbose_name="Adresse du commissariat")
    horaires_commissariat = models.CharField(max_length=200, blank=True, null=True, verbose_name="Horaires d'ouverture")

    # ── Traçabilité ─────────────────────────────────────────────────
    traite_par = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='remplacements_traites',
        verbose_name="Traité par"
    )
    remarques = models.TextField(blank=True, null=True, verbose_name="Remarques agent")

    # ── Dates clés ──────────────────────────────────────────────────
    date_creation           = models.DateTimeField(auto_now_add=True,  verbose_name="Date de création du dossier")
    date_echeance_match     = models.DateTimeField(verbose_name="Échéance du matching (J+7)")
    date_emission_recepisse = models.DateTimeField(blank=True, null=True, verbose_name="Date d'émission de l'autorisation")
    date_depot_commissariat = models.DateTimeField(blank=True, null=True, verbose_name="Date de dépôt au commissariat")
    date_document_pret      = models.DateTimeField(blank=True, null=True, verbose_name="Date de disponibilité du document")
    date_retrait            = models.DateTimeField(blank=True, null=True, verbose_name="Date de retrait")

    class Meta:
        verbose_name = "Demande de remplacement"
        verbose_name_plural = "Demandes de remplacement"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.numero_dossier} — {self.declaration.nom_sur_piece}"

    def save(self, *args, **kwargs):
        if not self.numero_dossier:
            annee = timezone.now().year
            with transaction.atomic():
                count = DemandeRemplacement.objects.select_for_update().filter(
                    date_creation__year=annee
                ).count() + 1
                self.numero_dossier = f"REMP-{annee}-{count:05d}"
        super().save(*args, **kwargs)

    @property
    def progression_pct(self):
        """Pourcentage d'avancement pour la barre de progression."""
        scores = {
            'EN_ATTENTE': 10,
            'RECEPISSE_EMIS': 30,
            'EN_TRAITEMENT': 55,
            'DOCUMENT_PRET': 80,
            'RETIRE': 100,
            'ANNULE': 0,
        }
        return scores.get(self.statut, 0)

    @property
    def autorisation_disponible(self):
        return self.statut in ['RECEPISSE_EMIS', 'EN_TRAITEMENT', 'DOCUMENT_PRET', 'RETIRE']


class Notification(models.Model):
    TYPE_CHOICES = [
        ('INFO',        'Information'),
        ('MATCH',       'Correspondance trouvée'),
        ('STATUT',      'Changement de statut'),
        ('ADMIN',       'Message administrateur'),
        ('REMPLACEMENT','Remplacement de pièce'),   # ← NOUVEAU
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='notifications', verbose_name="Destinataire"
    )
    declaration = models.ForeignKey(
        Declaration, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='notifications', verbose_name="Déclaration concernée"
    )
    type_notification = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    titre   = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    lue     = models.BooleanField(default=False, verbose_name="Lue")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.user.username}"
