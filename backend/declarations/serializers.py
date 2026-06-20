"""
Sérialiseurs pour l'API REST
VERSION AVEC WORKFLOW DE REMPLACEMENT
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, CategoriePiece, Declaration, Notification, DemandeRemplacement


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model  = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'telephone', 'role',
            'date_creation', 'is_active'
        ]
        read_only_fields = ['id', 'date_creation', 'role']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class CreateAgentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model  = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'telephone', 'role',
            'date_creation', 'is_active'
        ]
        read_only_fields = ['id', 'date_creation']

    def validate_role(self, value):
        if value not in ['police', 'admin']:
            raise serializers.ValidationError("Rôle invalide. Valeurs acceptées : 'police', 'admin'.")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        if not attrs.get('role'):
            raise serializers.ValidationError({"role": "Le rôle est obligatoire."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    nombre_declarations = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'telephone', 'role', 'date_creation', 'nombre_declarations', 'is_active'
        ]
        read_only_fields = ['id', 'username', 'role', 'date_creation']

    def get_nombre_declarations(self, obj):
        return obj.declarations.count()


class CategoriePieceSerializer(serializers.ModelSerializer):
    nombre_declarations = serializers.SerializerMethodField()

    class Meta:
        model  = CategoriePiece
        fields = ['id', 'libelle', 'description', 'icone', 'actif', 'date_creation', 'nombre_declarations']
        read_only_fields = ['id', 'date_creation']

    def get_nombre_declarations(self, obj):
        return obj.declarations.filter(statut='VALIDE').count()


class DeclarationListSerializer(serializers.ModelSerializer):
    categorie_nom  = serializers.CharField(source='categorie.libelle', read_only=True)
    declarant      = serializers.CharField(source='user.username', read_only=True)
    type_display   = serializers.CharField(source='get_type_declaration_display', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    # Indique si un dossier de remplacement existe
    a_dossier_remplacement = serializers.SerializerMethodField()
    numero_dossier_remplacement = serializers.SerializerMethodField()

    class Meta:
        model  = Declaration
        fields = [
            'id', 'numero_recepisse', 'type_declaration', 'type_display',
            'categorie', 'categorie_nom', 'numero_piece', 'nom_sur_piece',
            'nom_declarant', 'prenom_declarant',
            'date_naissance', 'lieu_naissance', 'profession',
            'statut', 'statut_display', 'declarant', 'date_declaration',
            'date_perte', 'lieu_perte',
            'a_dossier_remplacement', 'numero_dossier_remplacement',
        ]

    def get_a_dossier_remplacement(self, obj):
        return hasattr(obj, 'demande_remplacement')

    def get_numero_dossier_remplacement(self, obj):
        if hasattr(obj, 'demande_remplacement'):
            return obj.demande_remplacement.numero_dossier
        return None


class DeclarationDetailSerializer(serializers.ModelSerializer):
    categorie_detail      = CategoriePieceSerializer(source='categorie', read_only=True)
    declarant_detail      = UserProfileSerializer(source='user', read_only=True)
    type_display          = serializers.CharField(source='get_type_declaration_display', read_only=True)
    statut_display        = serializers.CharField(source='get_statut_display', read_only=True)
    correspondance_detail = DeclarationListSerializer(source='declaration_correspondante', read_only=True)
    a_dossier_remplacement       = serializers.SerializerMethodField()
    numero_dossier_remplacement  = serializers.SerializerMethodField()
    statut_dossier_remplacement  = serializers.SerializerMethodField()

    class Meta:
        model  = Declaration
        fields = '__all__'
        read_only_fields = [
            'id', 'numero_recepisse', 'user', 'date_declaration',
            'date_modification', 'declaration_correspondante',
        ]

    def get_a_dossier_remplacement(self, obj):
        return hasattr(obj, 'demande_remplacement')

    def get_numero_dossier_remplacement(self, obj):
        if hasattr(obj, 'demande_remplacement'):
            return obj.demande_remplacement.numero_dossier
        return None

    def get_statut_dossier_remplacement(self, obj):
        if hasattr(obj, 'demande_remplacement'):
            return obj.demande_remplacement.statut
        return None

    def validate_numero_piece(self, value):
        if not value:
            return value
        if len(value) < 3:
            raise serializers.ValidationError("Le numéro de pièce doit contenir au moins 3 caractères.")
        return value.upper()

    def validate_photo_piece(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("La taille de l'image ne doit pas dépasser 5 MB.")
            if value.content_type not in ['image/jpeg', 'image/jpg', 'image/png']:
                raise serializers.ValidationError("Format non autorisé. Utilisez JPG ou PNG.")
        return value


class DeclarationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Declaration
        fields = [
            'type_declaration', 'categorie',
            'numero_piece', 'nom_sur_piece',
            'nom_declarant', 'prenom_declarant',
            'date_naissance', 'lieu_naissance', 'profession',
            'description', 'lieu_perte', 'date_perte', 'photo_piece',
            'latitude', 'longitude',
        ]
        extra_kwargs = {
            'numero_piece':     {'required': False, 'allow_blank': True, 'allow_null': True},
            'nom_sur_piece':    {'required': False, 'allow_blank': True},
            'nom_declarant':    {'required': False, 'allow_blank': True, 'allow_null': True},
            'prenom_declarant': {'required': False, 'allow_blank': True, 'allow_null': True},
            'date_naissance':   {'required': False, 'allow_null': True},
            'lieu_naissance':   {'required': False, 'allow_blank': True, 'allow_null': True},
            'profession':       {'required': False, 'allow_blank': True, 'allow_null': True},
            'description':      {'required': False, 'allow_blank': True},
            'lieu_perte':       {'required': False, 'allow_blank': True},
            'date_perte':       {'required': False, 'allow_null': True},
            'photo_piece':      {'required': False},
            'latitude':         {'required': False, 'allow_null': True},
            'longitude':        {'required': False, 'allow_null': True},
        }

    def validate_numero_piece(self, value):
        if value:
            return value.strip().upper()
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        if not validated_data.get('nom_sur_piece'):
            nom    = (validated_data.get('nom_declarant')    or '').strip().upper()
            prenom = (validated_data.get('prenom_declarant') or '').strip()
            validated_data['nom_sur_piece'] = f"{nom} {prenom}".strip() or 'NC'
        if not validated_data.get('numero_piece'):
            validated_data['numero_piece'] = 'NC'
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    declaration_detail = DeclarationListSerializer(source='declaration', read_only=True)
    type_display       = serializers.CharField(source='get_type_notification_display', read_only=True)

    class Meta:
        model  = Notification
        fields = [
            'id', 'type_notification', 'type_display', 'titre', 'message',
            'lue', 'date_creation', 'declaration', 'declaration_detail'
        ]
        read_only_fields = ['id', 'user', 'date_creation']


class StatistiquesSerializer(serializers.Serializer):
    total_declarations    = serializers.IntegerField()
    total_pertes          = serializers.IntegerField()
    total_trouvailles     = serializers.IntegerField()
    en_attente            = serializers.IntegerField()
    validees              = serializers.IntegerField()
    retrouvees            = serializers.IntegerField()
    restituees            = serializers.IntegerField()
    en_remplacement       = serializers.IntegerField()
    declarations_recentes = DeclarationListSerializer(many=True)
    categories_populaires = serializers.ListField()


class RechercheCorrespondanceSerializer(serializers.Serializer):
    numero_piece     = serializers.CharField(required=False, allow_blank=True, default='')
    nom_sur_piece    = serializers.CharField(required=False, allow_blank=True, default='')
    nom_declarant    = serializers.CharField(required=False, allow_blank=True, default='')
    prenom_declarant = serializers.CharField(required=False, allow_blank=True, default='')
    categorie        = serializers.IntegerField(required=False)


# ── Sérialiseurs pour le workflow de remplacement ────────────────────────────

class DemandeRemplacementSerializer(serializers.ModelSerializer):
    """Sérialiseur léger pour les listes."""
    declaration_recepisse = serializers.CharField(source='declaration.numero_recepisse', read_only=True)
    declaration_nom       = serializers.CharField(source='declaration.nom_sur_piece', read_only=True)
    declaration_categorie = serializers.CharField(source='declaration.categorie.libelle', read_only=True)
    declaration_type      = serializers.CharField(source='declaration.type_declaration', read_only=True)
    declarant_username    = serializers.CharField(source='declaration.user.username', read_only=True)
    declarant_nom         = serializers.SerializerMethodField()
    declarant_telephone   = serializers.CharField(source='declaration.user.telephone', read_only=True)
    declarant_email       = serializers.CharField(source='declaration.user.email', read_only=True)
    traite_par_nom        = serializers.SerializerMethodField()
    statut_display        = serializers.CharField(source='get_statut_display', read_only=True)
    progression_pct       = serializers.IntegerField(read_only=True)
    autorisation_disponible = serializers.BooleanField(read_only=True)

    class Meta:
        model  = DemandeRemplacement
        fields = [
            'id', 'numero_dossier', 'statut', 'statut_display', 'progression_pct',
            'autorisation_disponible',
            'commissariat', 'adresse_commissariat', 'horaires_commissariat',
            'remarques',
            'declaration', 'declaration_recepisse', 'declaration_nom',
            'declaration_categorie', 'declaration_type',
            'declarant_username', 'declarant_nom', 'declarant_telephone', 'declarant_email',
            'traite_par', 'traite_par_nom',
            'date_creation', 'date_echeance_match',
            'date_emission_recepisse', 'date_depot_commissariat',
            'date_document_pret', 'date_retrait',
        ]
        read_only_fields = ['id', 'numero_dossier', 'date_creation', 'date_echeance_match']

    def get_declarant_nom(self, obj):
        u = obj.declaration.user
        return f"{u.first_name} {u.last_name}".strip() or u.username

    def get_traite_par_nom(self, obj):
        if obj.traite_par:
            return f"{obj.traite_par.first_name} {obj.traite_par.last_name}".strip() or obj.traite_par.username
        return None


class ChangerStatutRemplacementSerializer(serializers.Serializer):
    """Payload pour le changement de statut d'un dossier de remplacement."""
    statut               = serializers.ChoiceField(choices=DemandeRemplacement.STATUT_CHOICES)
    commissariat         = serializers.CharField(required=False, allow_blank=True)
    adresse_commissariat = serializers.CharField(required=False, allow_blank=True)
    horaires_commissariat= serializers.CharField(required=False, allow_blank=True)
    remarques            = serializers.CharField(required=False, allow_blank=True)
