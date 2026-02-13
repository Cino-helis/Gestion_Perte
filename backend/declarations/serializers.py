"""
Sérialiseurs pour l'API REST
Transforment les modèles Django en JSON et vice-versa
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, CategoriePiece, Declaration, Notification


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle User
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'telephone', 'role',
            'date_creation', 'is_active'
        ]
        read_only_fields = ['id', 'date_creation', 'role']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le profil utilisateur (sans mot de passe)
    """
    nombre_declarations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'telephone', 'role', 'date_creation', 'nombre_declarations'
        ]
        read_only_fields = ['id', 'username', 'role', 'date_creation']

    def get_nombre_declarations(self, obj):
        return obj.declarations.count()


class CategoriePieceSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les catégories de pièces
    """
    nombre_declarations = serializers.SerializerMethodField()

    class Meta:
        model = CategoriePiece
        fields = [
            'id', 'libelle', 'description', 'icone',
            'actif', 'date_creation', 'nombre_declarations'
        ]
        read_only_fields = ['id', 'date_creation']

    def get_nombre_declarations(self, obj):
        return obj.declarations.filter(statut='VALIDE').count()


class DeclarationListSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la liste des déclarations (version simplifiée)
    """
    categorie_nom = serializers.CharField(source='categorie.libelle', read_only=True)
    declarant     = serializers.CharField(source='user.username', read_only=True)
    type_display  = serializers.CharField(source='get_type_declaration_display', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)

    class Meta:
        model = Declaration
        fields = [
            'id', 'numero_recepisse', 'type_declaration', 'type_display',
            'categorie', 'categorie_nom', 'numero_piece', 'nom_sur_piece',
            # ── Identité ───────────────────────────────────────────────────
            'nom_declarant', 'prenom_declarant',
            'date_naissance', 'lieu_naissance', 'profession',
            # ──────────────────────────────────────────────────────────────
            'statut', 'statut_display', 'declarant', 'date_declaration',
            'date_perte', 'lieu_perte',
        ]


class DeclarationDetailSerializer(serializers.ModelSerializer):
    """
    Sérialiseur détaillé pour une déclaration
    """
    categorie_detail     = CategoriePieceSerializer(source='categorie', read_only=True)
    declarant_detail     = UserProfileSerializer(source='user', read_only=True)
    type_display         = serializers.CharField(source='get_type_declaration_display', read_only=True)
    statut_display       = serializers.CharField(source='get_statut_display', read_only=True)
    correspondance_detail = DeclarationListSerializer(
        source='declaration_correspondante',
        read_only=True
    )

    class Meta:
        model = Declaration
        fields = '__all__'          # inclut automatiquement les 5 nouveaux champs
        read_only_fields = [
            'id', 'numero_recepisse', 'user', 'date_declaration',
            'date_modification', 'declaration_correspondante',
        ]

    def validate_numero_piece(self, value):
        """
        Numéro de pièce optionnel — validé seulement s'il est fourni.
        """
        if not value:
            return value        # vide autorisé
        if len(value) < 3:
            raise serializers.ValidationError(
                "Le numéro de pièce doit contenir au moins 3 caractères."
            )
        return value.upper()

    def validate_photo_piece(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    "La taille de l'image ne doit pas dépasser 5 MB."
                )
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Format non autorisé. Utilisez JPG ou PNG."
                )
        return value


class DeclarationCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création d'une déclaration.
    Accepte les champs identité séparément et construit nom_sur_piece
    automatiquement si non fourni.
    """
    class Meta:
        model = Declaration
        fields = [
            # ── Type / catégorie ──────────────────────────────────────────
            'type_declaration',
            'categorie',

            # ── Pièce ────────────────────────────────────────────────────
            'numero_piece',     # optionnel côté Vue
            'nom_sur_piece',    # auto-construit dans create() si vide

            # ── Identité du titulaire (stockés séparément) ───────────────
            'nom_declarant',
            'prenom_declarant',
            'date_naissance',
            'lieu_naissance',
            'profession',

            # ── Circonstances ────────────────────────────────────────────
            'description',
            'lieu_perte',
            'date_perte',
            'photo_piece',

            # ── Géolocalisation (optionnel) ───────────────────────────────
            'latitude',
            'longitude',
        ]
        extra_kwargs = {
            # Numéro de pièce : optionnel (l'utilisateur peut ne pas le connaître)
            'numero_piece': {'required': False, 'allow_blank': True, 'allow_null': True},
            # nom_sur_piece : facultatif en entrée, auto-construit si vide
            'nom_sur_piece': {'required': False, 'allow_blank': True},
            # Champs identité : obligatoires métier mais pas au niveau sérialiseur
            # (la validation est faite côté Vue + erreurs lisibles en retour)
            'nom_declarant':    {'required': False, 'allow_blank': True, 'allow_null': True},
            'prenom_declarant': {'required': False, 'allow_blank': True, 'allow_null': True},
            'date_naissance':   {'required': False, 'allow_null': True},
            'lieu_naissance':   {'required': False, 'allow_blank': True, 'allow_null': True},
            'profession':       {'required': False, 'allow_blank': True, 'allow_null': True},
            # Circonstances : optionnels
            'description': {'required': False, 'allow_blank': True},
            'lieu_perte':  {'required': False, 'allow_blank': True},
            'date_perte':  {'required': False, 'allow_null': True},
            'photo_piece': {'required': False},
            'latitude':    {'required': False, 'allow_null': True},
            'longitude':   {'required': False, 'allow_null': True},
        }

    def validate_numero_piece(self, value):
        """Optionnel — converti en majuscules s'il est fourni."""
        if value:
            return value.strip().upper()
        return value

    def create(self, validated_data):
        """
        - Associe l'utilisateur connecté.
        - Construit nom_sur_piece depuis nom_declarant + prenom_declarant
          si le champ n'est pas fourni explicitement.
        """
        validated_data['user'] = self.context['request'].user

        # Auto-construction de nom_sur_piece
        if not validated_data.get('nom_sur_piece'):
            nom    = (validated_data.get('nom_declarant')    or '').strip().upper()
            prenom = (validated_data.get('prenom_declarant') or '').strip()
            validated_data['nom_sur_piece'] = f"{nom} {prenom}".strip() or 'NC'

        # Numéro de pièce : fallback 'NC' si vide (champ requis en BDD)
        if not validated_data.get('numero_piece'):
            validated_data['numero_piece'] = 'NC'

        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les notifications
    """
    declaration_detail = DeclarationListSerializer(source='declaration', read_only=True)
    type_display = serializers.CharField(source='get_type_notification_display', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'type_notification', 'type_display', 'titre', 'message',
            'lue', 'date_creation', 'declaration', 'declaration_detail'
        ]
        read_only_fields = ['id', 'user', 'date_creation']


class StatistiquesSerializer(serializers.Serializer):
    """
    Sérialiseur pour les statistiques du dashboard
    """
    total_declarations  = serializers.IntegerField()
    total_pertes        = serializers.IntegerField()
    total_trouvailles   = serializers.IntegerField()
    en_attente          = serializers.IntegerField()
    validees            = serializers.IntegerField()
    retrouvees          = serializers.IntegerField()
    restituees          = serializers.IntegerField()
    declarations_recentes   = DeclarationListSerializer(many=True)
    categories_populaires   = serializers.ListField()


class RechercheCorrespondanceSerializer(serializers.Serializer):
    """
    Sérialiseur pour la recherche de correspondances.
    Accepte désormais nom + prénom séparément EN PLUS de nom_sur_piece.
    """
    numero_piece  = serializers.CharField(required=False, allow_blank=True, default='')
    nom_sur_piece = serializers.CharField(required=False, allow_blank=True, default='')
    # Nouveaux champs identité pour affiner la recherche
    nom_declarant    = serializers.CharField(required=False, allow_blank=True, default='')
    prenom_declarant = serializers.CharField(required=False, allow_blank=True, default='')
    categorie        = serializers.IntegerField(required=False)