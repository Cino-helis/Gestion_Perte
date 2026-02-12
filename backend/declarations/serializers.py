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
        read_only_fields = ['id', 'date_creation', 'role']  # Le rôle est géré par l'admin
    
    def validate(self, attrs):
        """
        Validation personnalisée
        """
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        return attrs
    
    def create(self, validated_data):
        """
        Création d'un nouvel utilisateur
        """
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
        """Compte le nombre de déclarations de l'utilisateur"""
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
        """Compte le nombre de déclarations dans cette catégorie"""
        return obj.declarations.filter(statut='VALIDE').count()


class DeclarationListSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la liste des déclarations (version simplifiée)
    """
    categorie_nom = serializers.CharField(source='categorie.libelle', read_only=True)
    declarant = serializers.CharField(source='user.username', read_only=True)
    type_display = serializers.CharField(source='get_type_declaration_display', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = Declaration
        fields = [
            'id', 'numero_recepisse', 'type_declaration', 'type_display',
            'categorie', 'categorie_nom', 'numero_piece', 'nom_sur_piece',
            'statut', 'statut_display', 'declarant', 'date_declaration',
            'date_perte', 'lieu_perte'
        ]


class DeclarationDetailSerializer(serializers.ModelSerializer):
    """
    Sérialiseur détaillé pour une déclaration
    """
    categorie_detail = CategoriePieceSerializer(source='categorie', read_only=True)
    declarant_detail = UserProfileSerializer(source='user', read_only=True)
    type_display = serializers.CharField(source='get_type_declaration_display', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    correspondance_detail = DeclarationListSerializer(
        source='declaration_correspondante',
        read_only=True
    )
    
    class Meta:
        model = Declaration
        fields = '__all__'
        read_only_fields = [
            'id', 'numero_recepisse', 'user', 'date_declaration',
            'date_modification', 'declaration_correspondante'
        ]
    
    def validate_numero_piece(self, value):
        """
        Validation du numéro de pièce
        """
        if len(value) < 3:
            raise serializers.ValidationError(
                "Le numéro de pièce doit contenir au moins 3 caractères."
            )
        return value.upper()  # Convertir en majuscules pour uniformiser
    
    def validate_photo_piece(self, value):
        """
        Validation de la photo uploadée
        """
        if value:
            # Limite de 5 MB
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    "La taille de l'image ne doit pas dépasser 5 MB."
                )
            
            # Types autorisés
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Format non autorisé. Utilisez JPG ou PNG."
                )
        
        return value


class DeclarationCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création de déclaration
    """
    class Meta:
        model = Declaration
        fields = [
            'type_declaration', 'categorie', 'numero_piece', 'nom_sur_piece',
            'description', 'lieu_perte', 'date_perte', 'photo_piece',
            'latitude', 'longitude'
        ]
    
    def create(self, validated_data):
        """
        Création de la déclaration avec l'utilisateur connecté
        """
        validated_data['user'] = self.context['request'].user
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
    total_declarations = serializers.IntegerField()
    total_pertes = serializers.IntegerField()
    total_trouvailles = serializers.IntegerField()
    en_attente = serializers.IntegerField()
    validees = serializers.IntegerField()
    retrouvees = serializers.IntegerField()
    restituees = serializers.IntegerField()
    declarations_recentes = DeclarationListSerializer(many=True)
    categories_populaires = serializers.ListField()


class RechercheCorrespondanceSerializer(serializers.Serializer):
    """
    Sérialiseur pour la recherche de correspondances
    """
    numero_piece = serializers.CharField(required=True, min_length=3)
    nom_sur_piece = serializers.CharField(required=False, allow_blank=True)
    categorie = serializers.IntegerField(required=False)