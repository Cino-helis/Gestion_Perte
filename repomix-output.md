This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: **/node_modules/**, **/dist/**, **/.nuxt/**, **/.vuepress/.temp/**, **/venv/**, **/.venv/**, **/env/**, **/*.pyc, **/__pycache__/**, **/db.sqlite3, **/.git/**, **/package-lock.json, **/yarn.lock
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.gitignore
backend/backend/__init__.py
backend/backend/asgi.py
backend/backend/settings.py
backend/backend/urls.py
backend/backend/wsgi.py
backend/create_test_data_windows.py
backend/declarations/__init__.py
backend/declarations/admin.py
backend/declarations/apps.py
backend/declarations/email_service.py
backend/declarations/migrations/__init__.py
backend/declarations/migrations/0001_initial.py
backend/declarations/migrations/0002_declaration_date_naissance_and_more.py
backend/declarations/models.py
backend/declarations/pdf_generator.py
backend/declarations/permissions.py
backend/declarations/serializers.py
backend/declarations/signals.py
backend/declarations/tests.py
backend/declarations/urls.py
backend/declarations/views.py
backend/init_categories_windows.py
backend/manage.py
frontend/.gitignore
frontend/.vscode/extensions.json
frontend/index.html
frontend/package.json
frontend/postcss.config.js
frontend/public/vite.svg
frontend/README.md
frontend/src/App.vue
frontend/src/assets/vue.svg
frontend/src/components/HelloWorld.vue
frontend/src/i18n/index.js
frontend/src/main.js
frontend/src/router/index.js
frontend/src/services/api.js
frontend/src/stores/auth.js
frontend/src/style.css
frontend/src/views/admin/AdminDeclarationsView.vue
frontend/src/views/admin/DashboardView.vue
frontend/src/views/admin/ManageAgentsView.vue
frontend/src/views/admin/ManageUsersView.vue
frontend/src/views/auth/LoginView.vue
frontend/src/views/auth/RegisterView.vue
frontend/src/views/citizen/DeclarationDetailView.vue
frontend/src/views/citizen/DeclareView.vue
frontend/src/views/citizen/MyDeclarationsView.vue
frontend/src/views/citizen/NotificationsView.vue
frontend/src/views/citizen/ProfileView.vue
frontend/src/views/HomeView.vue
frontend/src/views/NotFoundView.vue
frontend/src/views/SearchView.vue
frontend/tailwind.config.js
frontend/vite.config.js
package.json
README.md
repomix.config.json
requirements.txt
```

# Files

## File: .gitignore
```
node_modules

venv/
__pycache__/
*.pyc
```

## File: backend/backend/__init__.py
```python

```

## File: backend/backend/asgi.py
```python
"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()
```

## File: backend/backend/settings.py
```python
"""
Django settings for backend project.
Configuration pour la plateforme de déclarations - Togo
VERSION CORRIGÉE
"""

from pathlib import Path
from datetime import timedelta
import os  # ← ajouté pour les variables d'environnement (configuration email)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-votre-cle-secrete-a-changer-en-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applications tierces
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Notre application
    'declarations',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS doit être avant CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database - MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'declarations_togo',
        'USER': 'declarations_user',
        'PASSWORD': 'MotDePasse123!',  # À changer
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# CORRECTION: Modèle User personnalisé
AUTH_USER_MODEL = 'declarations.User'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'fr-fr'  # Français pour le Togo
TIME_ZONE = 'Africa/Lome'  # Fuseau horaire du Togo
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Uploads utilisateurs - photos de pièces)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ======================
# DJANGO REST FRAMEWORK
# ======================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DATETIME_FORMAT': '%d/%m/%Y %H:%M',
}


# ======================
# JWT CONFIGURATION
# ======================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}


# ======================
# CORS CONFIGURATION
# ======================
# Permet au frontend Vue.js de communiquer avec Django
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite (Vue.js)
    "http://localhost:8080",  # Vue CLI
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

CORS_ALLOW_CREDENTIALS = True

# En développement seulement (À RETIRER EN PRODUCTION)
CORS_ALLOW_ALL_ORIGINS = True


# ======================
# CONFIGURATION SÉCURITÉ
# ======================
# À activer en production
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True


# ======================
# UPLOAD FILES
# ======================
# Limite de taille pour les uploads (10 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

# Types de fichiers autorisés pour les photos de pièces
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']


# ======================
# EMAIL — GMAIL SMTP
# ======================
# Prérequis Gmail :
#   1. Activez la vérification en 2 étapes sur le compte Gmail.
#   2. Créez un "Mot de passe d'application" dans :
#      Compte Google → Sécurité → Mots de passe des applis
#   3. Renseignez les 3 variables d'environnement ci-dessous
#      dans votre fichier .env ou dans le système.
#
# Variables à définir :
#   DECLATOGO_EMAIL_HOST_USER     = votre.adresse@gmail.com
#   DECLATOGO_EMAIL_HOST_PASSWORD = xxxx xxxx xxxx xxxx  (App Password 16 car.)
#   DECLATOGO_DEFAULT_FROM_EMAIL  = DéclaTogo <votre.adresse@gmail.com>

EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_USE_SSL       = False  # TLS et SSL s'excluent mutuellement
EMAIL_TIMEOUT       = 10     # secondes avant abandon de connexion

EMAIL_HOST_USER     = os.environ.get('DECLATOGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DECLATOGO_EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL  = os.environ.get(
    'DECLATOGO_DEFAULT_FROM_EMAIL',
    f'DéclaTogo <{EMAIL_HOST_USER}>'
)

# ---------------------------------------------------------------------
# DÉVELOPPEMENT : remplacez EMAIL_BACKEND ci-dessus par la ligne
# suivante pour afficher les emails dans la console sans les envoyer :
#
#   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# ---------------------------------------------------------------------
```

## File: backend/backend/urls.py
```python
"""
URLs principales du projet backend
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    
    # Authentification JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API de l'application
    path('api/', include('declarations.urls')),
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personnalisation de l'admin
admin.site.site_header = "Administration - Plateforme Déclarations Togo"
admin.site.site_title = "Admin Déclarations"
admin.site.index_title = "Gestion de la plateforme"
```

## File: backend/backend/wsgi.py
```python
"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
```

## File: backend/create_test_data_windows.py
```python
"""
Script pour créer des données de test
Exécutez avec : python create_test_data_windows.py
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from declarations.models import CategoriePiece, Declaration
from datetime import datetime, timedelta

User = get_user_model()

print("=" * 60)
print("Création des données de test")
print("=" * 60)
print()

# 1. Créer des utilisateurs de test
print("1. Création des utilisateurs...")

# Admin
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@declarations.tg',
        'first_name': 'Administrateur',
        'last_name': 'Système',
        'role': 'admin',
        'telephone': '+22890000001',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"✓ Admin créé : {admin.username}")
else:
    print(f"- Admin existe : {admin.username}")

# Agent de police
police, created = User.objects.get_or_create(
    username='police',
    defaults={
        'email': 'police@declarations.tg',
        'first_name': 'Agent',
        'last_name': 'KOFFI',
        'role': 'police',
        'telephone': '+22890000002',
        'is_staff': True
    }
)
if created:
    police.set_password('police123')
    police.save()
    print(f"✓ Agent police créé : {police.username}")

# Citoyens
citoyens_data = [
    {
        'username': 'jean_akodjo',
        'email': 'jean@example.tg',
        'first_name': 'Jean',
        'last_name': 'AKODJO',
        'telephone': '+22890123456'
    },
    {
        'username': 'marie_eklou',
        'email': 'marie@example.tg',
        'first_name': 'Marie',
        'last_name': 'EKLOU',
        'telephone': '+22890123457'
    },
    {
        'username': 'kofi_mensah',
        'email': 'kofi@example.tg',
        'first_name': 'Kofi',
        'last_name': 'MENSAH',
        'telephone': '+22890123458'
    }
]

citoyens = []
for data in citoyens_data:
    citoyen, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'telephone': data['telephone'],
            'role': 'citoyen'
        }
    )
    if created:
        citoyen.set_password('citoyen123')
        citoyen.save()
        print(f"✓ Citoyen créé : {citoyen.username}")
    citoyens.append(citoyen)

# 2. Récupérer les catégories
print("\n2. Récupération des catégories...")
categories = list(CategoriePiece.objects.all())
if not categories:
    print("⚠️ Aucune catégorie trouvée. Exécutez d'abord init_categories_windows.py")
    sys.exit(1)
print(f"✓ {len(categories)} catégories disponibles")

# 3. Créer des déclarations de PERTE
print("\n3. Création de déclarations de PERTE...")

pertes_data = [
    {
        'user': citoyens[0],
        'categorie': categories[0],  # Pièce d'identité
        'numero_piece': 'TG20240001',
        'nom_sur_piece': 'AKODJO Jean',
        'description': 'CNI perdue lors d\'un déplacement à Lomé',
        'lieu_perte': 'Marché de Lomé',
        'date_perte': datetime.now() - timedelta(days=3),
        'statut': 'VALIDE'
    },
    {
        'user': citoyens[1],
        'categorie': categories[1],  # Véhicule
        'numero_piece': 'AB-1234-CD',
        'nom_sur_piece': 'EKLOU Marie',
        'description': 'Carte grise perdue',
        'lieu_perte': 'Boulevard du 13 Janvier',
        'date_perte': datetime.now() - timedelta(days=5),
        'statut': 'VALIDE'
    },
    {
        'user': citoyens[2],
        'categorie': categories[0],  # Pièce d'identité
        'numero_piece': 'TG20240002',
        'nom_sur_piece': 'MENSAH Kofi',
        'description': 'Passeport perdu à l\'aéroport',
        'lieu_perte': 'Aéroport de Lomé',
        'date_perte': datetime.now() - timedelta(days=1),
        'statut': 'EN_ATTENTE'
    },
    {
        'user': citoyens[0],
        'categorie': categories[2],  # Documents scolaires
        'numero_piece': 'DIPLOME-2023-001',
        'nom_sur_piece': 'AKODJO Jean',
        'description': 'Diplôme de licence perdu',
        'lieu_perte': 'Université de Lomé',
        'date_perte': datetime.now() - timedelta(days=10),
        'statut': 'VALIDE'
    }
]

for perte in pertes_data:
    declaration, created = Declaration.objects.get_or_create(
        type_declaration='PERTE',
        numero_piece=perte['numero_piece'],
        defaults=perte
    )
    if created:
        print(f"✓ Perte créée : {declaration.numero_recepisse}")

# 4. Créer des déclarations de TROUVAILLE
print("\n4. Création de déclarations de TROUVAILLE...")

trouvailles_data = [
    {
        'user': citoyens[1],
        'categorie': categories[0],  # Pièce d'identité
        'numero_piece': 'TG20240001',  # Correspond à la perte de Jean
        'nom_sur_piece': 'AKODJO Jean',
        'description': 'CNI trouvée près du marché',
        'lieu_perte': 'Avenue de la Paix, Lomé',
        'date_perte': datetime.now() - timedelta(days=2),
        'statut': 'VALIDE'
    },
    {
        'user': citoyens[2],
        'categorie': categories[3],  # Documents bancaires
        'numero_piece': '1234-5678-9012-3456',
        'nom_sur_piece': 'DUPONT Pierre',
        'description': 'Carte bancaire trouvée',
        'lieu_perte': 'Supermarché Casino',
        'date_perte': datetime.now() - timedelta(days=1),
        'statut': 'VALIDE'
    }
]

for trouvaille in trouvailles_data:
    declaration, created = Declaration.objects.get_or_create(
        type_declaration='TROUVAILLE',
        numero_piece=trouvaille['numero_piece'],
        nom_sur_piece=trouvaille['nom_sur_piece'],
        defaults=trouvaille
    )
    if created:
        print(f"✓ Trouvaille créée : {declaration.numero_recepisse}")

# 5. Créer une correspondance
print("\n5. Création d'une correspondance...")
try:
    perte_jean = Declaration.objects.get(
        type_declaration='PERTE',
        numero_piece='TG20240001'
    )
    trouvaille_jean = Declaration.objects.get(
        type_declaration='TROUVAILLE',
        numero_piece='TG20240001'
    )
    
    perte_jean.declaration_correspondante = trouvaille_jean
    perte_jean.statut = 'RETROUVE'
    perte_jean.save()
    
    trouvaille_jean.declaration_correspondante = perte_jean
    trouvaille_jean.statut = 'RETROUVE'
    trouvaille_jean.save()
    
    print(f"✓ Correspondance créée entre {perte_jean.numero_recepisse} et {trouvaille_jean.numero_recepisse}")
except:
    print("⚠️ Impossible de créer la correspondance")

# Résumé
print("\n" + "=" * 60)
print("RÉSUMÉ")
print("=" * 60)
print(f"Utilisateurs : {User.objects.count()}")
print(f"Catégories : {CategoriePiece.objects.count()}")
print(f"Déclarations : {Declaration.objects.count()}")
print(f"  - Pertes : {Declaration.objects.filter(type_declaration='PERTE').count()}")
print(f"  - Trouvailles : {Declaration.objects.filter(type_declaration='TROUVAILLE').count()}")
print(f"  - Retrouvées : {Declaration.objects.filter(statut='RETROUVE').count()}")

print("\n" + "=" * 60)
print("IDENTIFIANTS DE CONNEXION")
print("=" * 60)
print("Admin :")
print("  Username: admin")
print("  Password: admin123")
print("\nAgent de police :")
print("  Username: police")
print("  Password: police123")
print("\nCitoyens :")
print("  Username: jean_akodjo, marie_eklou, kofi_mensah")
print("  Password: citoyen123")

print("\n✅ Données de test créées avec succès !")
```

## File: backend/declarations/__init__.py
```python

```

## File: backend/declarations/admin.py
```python
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
```

## File: backend/declarations/apps.py
```python
"""
Configuration de l'application 'declarations'
La méthode ready() charge les signaux au démarrage de Django.
Sans cette étape, les signaux définis dans signals.py ne seraient jamais connectés.
"""

from django.apps import AppConfig


class DeclarationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'declarations'
    verbose_name = 'Gestion des Déclarations'

    def ready(self):
        """
        Appelé une seule fois au démarrage de Django.
        L'import de signals.py enregistre les @receiver auprès du dispatcher.
        """
        import declarations.signals  # noqa: F401
```

## File: backend/declarations/email_service.py
```python
"""
Service d'envoi d'emails pour DéclaTogo
Déclenché quand un statut passe à RETROUVE.

Deux scénarios :
  1. Avec correspondance (match) → email aux DEUX déclarants
  2. Sans correspondance (admin manuel) → email au seul déclarant

Usage :
    from declarations.email_service import envoyer_email_retrouve
    envoyer_email_retrouve(user, declaration, match=None, remarques='')
"""

import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


# =============================================================================
# GÉNÉRATION HTML
# =============================================================================

def _build_html(titre, couleur, nom, type_decl, num_recepisse, num_piece,
                nom_piece, num_match=None, type_match=None,
                instructions=None, remarques=None):
    """Corps HTML de l'email, responsive, couleurs drapeau togolais."""

    date_envoi = timezone.localtime(timezone.now()).strftime('%d/%m/%Y à %H:%M')

    # Badge type principal
    badge_bg  = '#FEE2E2' if type_decl == 'PERTE' else '#E8F4F0'
    badge_txt = '#C41230' if type_decl == 'PERTE' else '#005A3C'
    label     = 'PERTE'   if type_decl == 'PERTE' else 'TROUVAILLE'
    emoji     = '😟'      if type_decl == 'PERTE' else '🤲'

    # Bloc correspondance (optionnel)
    bloc_match = ''
    if num_match:
        e2 = '😟' if type_match == 'PERTE' else '🤲'
        l2 = 'PERTE' if type_match == 'PERTE' else 'TROUVAILLE'
        bloc_match = f"""
        <tr><td style="padding:0 32px 24px;">
          <table width="100%" cellpadding="0" cellspacing="0"
                 style="background:#f0fdf4;border:2px solid #86efac;border-radius:10px;">
            <tr><td style="padding:16px 20px;">
              <p style="margin:0 0 6px;font-size:11px;font-weight:700;color:#166534;
                         text-transform:uppercase;letter-spacing:.07em;">Déclaration correspondante</p>
              <p style="margin:0 0 4px;font-size:14px;color:#1A2E22;">
                {e2} <strong>{l2}</strong></p>
              <p style="margin:0;font-family:monospace;font-size:16px;font-weight:700;
                         color:#005A3C;letter-spacing:.1em;">{num_match}</p>
            </td></tr>
          </table>
          <p style="margin:10px 0 0;font-size:13px;color:#374151;text-align:center;">
            Présentez <strong>les deux récépissés</strong> au commissariat.
          </p>
        </td></tr>"""

    # Instructions numérotées
    lignes_instr = ''
    for i, instr in enumerate(instructions or [], 1):
        lignes_instr += f"""
        <tr><td style="padding:5px 0;">
          <table cellpadding="0" cellspacing="0"><tr>
            <td style="width:26px;height:26px;background:#005A3C;border-radius:50%;
                        color:white;font-weight:700;font-size:12px;text-align:center;
                        vertical-align:middle;">{i}</td>
            <td style="padding-left:10px;font-size:13px;color:#374151;">{instr}</td>
          </tr></table>
        </td></tr>"""

    # Remarques admin
    bloc_rem = ''
    if remarques:
        bloc_rem = f"""
        <tr><td style="padding:0 32px 20px;">
          <table width="100%" cellpadding="0" cellspacing="0"
                 style="background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;">
            <tr><td style="padding:12px 16px;font-size:13px;color:#92400e;">
              <strong>Message du service :</strong> {remarques}
            </td></tr>
          </table>
        </td></tr>"""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>DéclaTogo — {titre}</title></head>
<body style="margin:0;padding:0;background:#FAF7F2;
             font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#FAF7F2">
<tr><td align="center" style="padding:32px 16px;">
<table width="600" cellpadding="0" cellspacing="0"
       style="max-width:600px;background:#fff;border-radius:16px;overflow:hidden;
              box-shadow:0 4px 24px rgba(0,90,60,.12);">

  <!-- Bande drapeau haut -->
  <tr><td style="height:6px;padding:0;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td style="background:#005A3C;width:40%;height:6px;"></td>
      <td style="background:#D4A017;width:20%;height:6px;"></td>
      <td style="background:#C41230;width:40%;height:6px;"></td>
    </tr></table>
  </td></tr>

  <!-- Logo -->
  <tr><td style="background:#005A3C;padding:24px 32px;text-align:center;">
    <table cellpadding="0" cellspacing="0" align="center"><tr>
      <td style="background:#D4A017;width:42px;height:42px;border-radius:9px;
                  text-align:center;vertical-align:middle;font-weight:700;
                  font-size:15px;color:#005A3C;">DT</td>
      <td style="padding-left:10px;font-size:22px;font-weight:700;color:#fff;
                  vertical-align:middle;">
        Décla<span style="color:#D4A017;">Togo</span></td>
    </tr></table>
    <p style="margin:10px 0 0;font-size:11px;color:rgba(255,255,255,.6);
               text-transform:uppercase;letter-spacing:.1em;">
      Plateforme officielle — République Togolaise</p>
  </td></tr>

  <!-- Bandeau statut -->
  <tr><td style="background:{couleur};padding:18px 32px;text-align:center;">
    <p style="margin:0;font-size:20px;font-weight:700;color:#fff;">🎉 {titre}</p>
  </td></tr>

  <!-- Salutation -->
  <tr><td style="padding:24px 32px 8px;">
    <p style="margin:0;font-size:15px;color:#374151;line-height:1.6;">
      Bonjour <strong>{nom}</strong>,</p>
  </td></tr>

  <!-- Récépissé principal -->
  <tr><td style="padding:14px 32px 22px;">
    <table width="100%" cellpadding="0" cellspacing="0"
           style="background:#f8fafc;border:2px solid {couleur};border-radius:12px;">
      <tr><td style="padding:18px 22px;">
        <p style="margin:0 0 6px;font-size:11px;font-weight:700;color:#6b7280;
                   text-transform:uppercase;letter-spacing:.07em;">Votre déclaration</p>
        <span style="display:inline-block;background:{badge_bg};color:{badge_txt};
                     font-size:11px;font-weight:700;padding:3px 10px;
                     border-radius:20px;margin-bottom:8px;">
          {emoji} {label}</span>
        <p style="margin:0;font-family:monospace;font-size:19px;font-weight:700;
                   color:{couleur};letter-spacing:.1em;">{num_recepisse}</p>
        <p style="margin:6px 0 0;font-size:13px;color:#374151;">
          Pièce : <strong>{num_piece}</strong> — {nom_piece}</p>
      </td></tr>
    </table>
  </td></tr>

  {bloc_match}
  {bloc_rem}

  <!-- Instructions -->
  <tr><td style="padding:0 32px 26px;">
    <p style="margin:0 0 12px;font-size:14px;font-weight:700;color:#1A2E22;">
      📋 Que faire maintenant ?</p>
    <table width="100%" cellpadding="0" cellspacing="0">
      {lignes_instr}
    </table>
  </td></tr>

  <!-- Avertissement récépissé -->
  <tr><td style="padding:0 32px 26px;">
    <table width="100%" cellpadding="0" cellspacing="0"
           style="background:#fffbeb;border-left:4px solid #D4A017;border-radius:0 8px 8px 0;">
      <tr><td style="padding:13px 16px;font-size:13px;color:#92400e;line-height:1.6;">
        ⚠️ <strong>Important :</strong> Le récépissé est <strong>obligatoire</strong>
        pour toute restitution. Sans ce document, le commissariat ne pourra pas traiter
        votre dossier.
      </td></tr>
    </table>
  </td></tr>

  <!-- Pied de page -->
  <tr><td style="background:#f8fafc;padding:18px 32px;border-top:1px solid #e5e7eb;
                  text-align:center;">
    <p style="margin:0;font-size:11px;color:#9ca3af;line-height:1.6;">
      Email envoyé le {date_envoi}<br/>
      DéclaTogo — Plateforme officielle, République Togolaise<br/>
      <em>Cet email est automatique, ne pas répondre.</em></p>
  </td></tr>

  <!-- Bande drapeau bas -->
  <tr><td style="height:5px;padding:0;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td style="background:#C41230;width:40%;height:5px;"></td>
      <td style="background:#D4A017;width:20%;height:5px;"></td>
      <td style="background:#005A3C;width:40%;height:5px;"></td>
    </tr></table>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


# =============================================================================
# FONCTION PUBLIQUE
# =============================================================================

def envoyer_email_retrouve(user, declaration, match=None, remarques=''):
    """
    Envoie l'email de notification RETROUVÉ à un utilisateur.

    Args:
        user        : instance User destinataire
        declaration : instance Declaration qui concerne cet utilisateur
        match       : instance Declaration correspondante (optionnel)
        remarques   : commentaire de l'agent (optionnel)

    Returns:
        True si envoi réussi, False sinon.
    """
    if not user.email:
        logger.info(
            "Email non envoyé à %s : aucune adresse email.", user.username
        )
        return False

    est_perte   = declaration.type_declaration == 'PERTE'
    nom_affiche = f"{user.first_name} {user.last_name}".strip() or user.username

    # ── Personnalisation selon type de déclaration ───────────────────────────
    if est_perte:
        titre    = "Votre pièce a été retrouvée !"
        couleur  = '#005A3C'
        sujet    = f"[DéclaTogo] Bonne nouvelle ! Votre pièce a été retrouvée — N° {declaration.numero_recepisse}"
        instrs   = [
            "Rendez-vous au commissariat le plus proche.",
            f"Apportez votre <strong>récépissé de perte N° {declaration.numero_recepisse}</strong>.",
            "Présentez une pièce d'identité en cours de validité.",
            "Un agent procédera à la vérification et à la restitution.",
        ]
        if match:
            instrs.insert(1,
                f"Apportez aussi le récépissé de trouvaille "
                f"<strong>N° {match.numero_recepisse}</strong> si vous le recevez."
            )
        texte_brut = (
            f"Bonjour {nom_affiche},\n\n"
            f"Bonne nouvelle ! Votre déclaration de perte "
            f"N° {declaration.numero_recepisse} a une correspondance.\n\n"
            f"Pièce : {declaration.numero_piece} — {declaration.nom_sur_piece}\n\n"
            "Que faire ?\n"
            f"  1. Rendez-vous au commissariat.\n"
            f"  2. Apportez votre récépissé N° {declaration.numero_recepisse}.\n"
            f"  3. Présentez une pièce d'identité valide.\n"
        )
        if match:
            texte_brut += f"\nRécépissé de trouvaille : {match.numero_recepisse}\n"
    else:
        titre    = "La pièce que vous avez trouvée a un propriétaire"
        couleur  = '#C41230'
        sujet    = f"[DéclaTogo] Correspondance trouvée pour votre déclaration — N° {declaration.numero_recepisse}"
        instrs   = [
            "Rendez-vous au commissariat le plus proche.",
            f"Apportez votre <strong>récépissé de trouvaille N° {declaration.numero_recepisse}</strong>.",
            "Apportez la <strong>pièce originale</strong> que vous avez trouvée.",
            "Un agent vérifiera et procédera à la restitution au propriétaire.",
        ]
        texte_brut = (
            f"Bonjour {nom_affiche},\n\n"
            f"La pièce que vous avez déclarée (N° {declaration.numero_recepisse}) "
            f"correspond à une déclaration de perte.\n\n"
            f"Pièce : {declaration.numero_piece} — {declaration.nom_sur_piece}\n\n"
            "Que faire ?\n"
            f"  1. Rendez-vous au commissariat.\n"
            f"  2. Apportez votre récépissé N° {declaration.numero_recepisse}.\n"
            f"  3. Apportez la pièce originale trouvée.\n"
        )
        if match:
            texte_brut += f"\nRécépissé de perte associé : {match.numero_recepisse}\n"

    texte_brut += (
        "\n⚠️ Le récépissé est OBLIGATOIRE pour toute restitution.\n\n"
        "— L'équipe DéclaTogo\n"
        "Plateforme officielle — République Togolaise"
    )

    # ── Génération HTML ──────────────────────────────────────────────────────
    html = _build_html(
        titre         = titre,
        couleur       = couleur,
        nom           = nom_affiche,
        type_decl     = declaration.type_declaration,
        num_recepisse = declaration.numero_recepisse,
        num_piece     = declaration.numero_piece or 'NC',
        nom_piece     = declaration.nom_sur_piece,
        num_match     = match.numero_recepisse   if match else None,
        type_match    = match.type_declaration   if match else None,
        instructions  = instrs,
        remarques     = remarques or declaration.remarques_admin,
    )

    # ── Envoi ────────────────────────────────────────────────────────────────
    try:
        expediteur = (
            getattr(settings, 'DEFAULT_FROM_EMAIL', None)
            or getattr(settings, 'EMAIL_HOST_USER', 'noreply@declatogo.tg')
        )
        msg = EmailMultiAlternatives(
            subject    = sujet,
            body       = texte_brut,
            from_email = f"DéclaTogo <{expediteur}>",
            to         = [user.email],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send(fail_silently=False)

        logger.info(
            "Email RETROUVÉ envoyé à %s <%s> — déclaration %s",
            user.username, user.email, declaration.numero_recepisse
        )
        return True

    except Exception as exc:
        logger.error(
            "Échec email à %s <%s> — déclaration %s : %s",
            user.username, user.email, declaration.numero_recepisse, exc
        )
        return False
```

## File: backend/declarations/migrations/__init__.py
```python

```

## File: backend/declarations/migrations/0001_initial.py
```python
# Generated by Django 5.2.11 on 2026-02-09 07:08

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriePiece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100, unique=True, verbose_name='Nom de la catégorie')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('icone', models.CharField(blank=True, help_text="Nom de l'icône (ex: 'id-card', 'car', 'graduation-cap')", max_length=50, null=True, verbose_name='Icône')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
            ],
            options={
                'verbose_name': 'Catégorie de pièce',
                'verbose_name_plural': 'Catégories de pièces',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telephone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Format: '+22890123456' ou '90123456'", regex='^(\\+228)?[0-9]{8}$')], verbose_name='Numéro de téléphone')),
                ('role', models.CharField(choices=[('citoyen', 'Citoyen'), ('admin', 'Administrateur'), ('police', 'Agent de Police')], default='citoyen', max_length=20, verbose_name='Rôle')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_user_set', related_query_name='custom_user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_set', related_query_name='custom_user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
                'ordering': ['-date_creation'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_declaration', models.CharField(choices=[('PERTE', 'Perte'), ('TROUVAILLE', 'Trouvaille')], max_length=15, verbose_name='Type de déclaration')),
                ('numero_piece', models.CharField(db_index=True, help_text="Ex: Numéro CNI, Passeport, Plaque d'immatriculation", max_length=100, verbose_name='Numéro de la pièce')),
                ('nom_sur_piece', models.CharField(max_length=200, verbose_name='Nom figurant sur la pièce')),
                ('statut', models.CharField(choices=[('EN_ATTENTE', 'En attente de validation'), ('VALIDE', 'Validé'), ('RETROUVE', 'Retrouvé/Correspondance trouvée'), ('RESTITUE', 'Restitué au propriétaire'), ('REJETE', 'Rejeté'), ('CLOTURE', 'Clôturé')], default='EN_ATTENTE', max_length=20, verbose_name='Statut')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description détaillée')),
                ('lieu_perte', models.CharField(blank=True, max_length=300, null=True, verbose_name='Lieu de la perte/trouvaille')),
                ('date_perte', models.DateField(blank=True, null=True, verbose_name='Date de la perte/trouvaille')),
                ('photo_piece', models.ImageField(blank=True, null=True, upload_to='pieces/%Y/%m/', verbose_name='Photo de la pièce')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude')),
                ('date_declaration', models.DateTimeField(auto_now_add=True, verbose_name='Date de déclaration')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('numero_recepisse', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Numéro de récépissé')),
                ('remarques_admin', models.TextField(blank=True, null=True, verbose_name="Remarques de l'administrateur")),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='declarations', to='declarations.categoriepiece', verbose_name='Catégorie')),
                ('declaration_correspondante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='correspondances', to='declarations.declaration', verbose_name='Déclaration correspondante')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='declarations', to=settings.AUTH_USER_MODEL, verbose_name='Déclarant')),
            ],
            options={
                'verbose_name': 'Déclaration',
                'verbose_name_plural': 'Déclarations',
                'ordering': ['-date_declaration'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_notification', models.CharField(choices=[('INFO', 'Information'), ('MATCH', 'Correspondance trouvée'), ('STATUT', 'Changement de statut'), ('ADMIN', 'Message administrateur')], max_length=20, verbose_name='Type')),
                ('titre', models.CharField(max_length=200, verbose_name='Titre')),
                ('message', models.TextField(verbose_name='Message')),
                ('lue', models.BooleanField(default=False, verbose_name='Lue')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('declaration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='declarations.declaration', verbose_name='Déclaration concernée')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Destinataire')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-date_creation'],
            },
        ),
        migrations.AddIndex(
            model_name='declaration',
            index=models.Index(fields=['numero_piece', 'type_declaration'], name='declaration_numero__59da5d_idx'),
        ),
        migrations.AddIndex(
            model_name='declaration',
            index=models.Index(fields=['statut', 'date_declaration'], name='declaration_statut_f65813_idx'),
        ),
    ]
```

## File: backend/declarations/migrations/0002_declaration_date_naissance_and_more.py
```python
# Generated by Django 5.2.11 on 2026-02-13 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declarations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaration',
            name='date_naissance',
            field=models.DateField(blank=True, null=True, verbose_name='Date de naissance'),
        ),
        migrations.AddField(
            model_name='declaration',
            name='lieu_naissance',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Lieu de naissance'),
        ),
        migrations.AddField(
            model_name='declaration',
            name='nom_declarant',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nom de famille (sur la pièce)'),
        ),
        migrations.AddField(
            model_name='declaration',
            name='prenom_declarant',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Prénom(s) (sur la pièce)'),
        ),
        migrations.AddField(
            model_name='declaration',
            name='profession',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Profession'),
        ),
    ]
```

## File: backend/declarations/models.py
```python
"""
Modèles de données pour la plateforme de déclarations de pertes - Togo
VERSION CORRIGÉE
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import transaction


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
        if not self.numero_recepisse:
            prefixe = 'PERTE' if self.type_declaration == 'PERTE' else 'TROUV'
            annee = timezone.now().year
            with transaction.atomic():
                # select_for_update bloque les lectures concurrentes
                count = Declaration.objects.select_for_update().filter(
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
```

## File: backend/declarations/pdf_generator.py
```python
"""
Générateur de récépissés PDF avec ReportLab
Produit un document officiel de style administratif togolais.

Installation requise :
    pip install reportlab pillow

Usage :
    from declarations.pdf_generator import generer_recepisse_pdf
    buffer = generer_recepisse_pdf(declaration)
    # buffer est un BytesIO prêt à être envoyé en réponse HTTP
"""

import io
from datetime import datetime

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)


# =============================================================================
# COULEURS DU DRAPEAU TOGOLAIS (rouge, vert, blanc)
# =============================================================================
VERT_TOGO    = colors.HexColor('#006A4E')
ROUGE_TOGO   = colors.HexColor('#D21034')
JAUNE_TOGO   = colors.HexColor('#FFCE00')
GRIS_CLAIR   = colors.HexColor('#F5F5F5')
GRIS_BORDURE = colors.HexColor('#CCCCCC')
NOIR         = colors.black
BLANC        = colors.white


# =============================================================================
# STYLES TYPOGRAPHIQUES
# =============================================================================

def _get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='Entete',
        fontSize=9,
        textColor=GRIS_CLAIR,
        alignment=TA_CENTER,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='TitreRepublique',
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=BLANC,
        alignment=TA_CENTER,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='TitreDocument',
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=VERT_TOGO,
        alignment=TA_CENTER,
        spaceBefore=12,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name='SousTitre',
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=ROUGE_TOGO,
        alignment=TA_CENTER,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='SectionTitre',
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=BLANC,
        alignment=TA_LEFT,
        leftIndent=6,
        spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name='Corps',
        fontSize=9,
        textColor=NOIR,
        alignment=TA_LEFT,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name='CorpsCentre',
        fontSize=9,
        textColor=NOIR,
        alignment=TA_CENTER,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name='Note',
        fontSize=8,
        textColor=colors.HexColor('#555555'),
        alignment=TA_LEFT,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name='NumeroBold',
        fontSize=13,
        fontName='Helvetica-Bold',
        textColor=VERT_TOGO,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=6,
    ))

    return styles


# =============================================================================
# FONCTIONS HELPERS
# =============================================================================

def _ligne_section(titre, styles):
    """Retourne un tableau d'une ligne faisant office de titre de section."""
    cell = Paragraph(f"  {titre.upper()}", styles['SectionTitre'])
    table = Table([[cell]], colWidths=[17 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), VERT_TOGO),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
    ]))
    return table


def _tableau_infos(donnees, styles):
    """
    Crée un tableau à deux colonnes (label | valeur) avec style alternance.
    donnees : liste de (str label, str valeur)
    """
    rows = []
    for label, valeur in donnees:
        rows.append([
            Paragraph(f"<b>{label}</b>", styles['Corps']),
            Paragraph(str(valeur) if valeur else '—', styles['Corps'])
        ])

    table = Table(rows, colWidths=[6 * cm, 11 * cm])
    style = TableStyle([
        ('GRID',          (0, 0), (-1, -1), 0.5, GRIS_BORDURE),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ])

    # Alternance de couleurs sur les lignes
    for i in range(len(rows)):
        bg = GRIS_CLAIR if i % 2 == 0 else BLANC
        style.add('BACKGROUND', (0, i), (-1, i), bg)

    table.setStyle(style)
    return table


# =============================================================================
# GENERATEUR PRINCIPAL
# =============================================================================

def generate_recepisse_pdf(declaration) -> io.BytesIO:
    """
    Génère le PDF de récépissé pour une déclaration.

    Args:
        declaration : instance du modèle Declaration

    Returns:
        io.BytesIO : buffer contenant le PDF prêt à l'envoi
    """
    buffer = io.BytesIO()
    styles = _get_styles()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.5 * cm,
        bottomMargin=2 * cm,
        title=f"Récépissé {declaration.numero_recepisse}",
        author="Plateforme Déclarations Togo",
    )

    elements = []

    # ------------------------------------------------------------------
    # 1. EN-TÊTE OFFICIEL
    # ------------------------------------------------------------------
    entete_data = [[
        Paragraph("REPUBLIQUE TOGOLAISE<br/>Travail – Liberté – Patrie", styles['TitreRepublique']),
        Paragraph(
            "MINISTÈRE DE LA SÉCURITÉ ET DE LA PROTECTION CIVILE<br/>"
            "Direction Générale de la Police Nationale",
            styles['Entete']
        ),
    ]]
    entete_table = Table(entete_data, colWidths=[8.5 * cm, 8.5 * cm])
    entete_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), VERT_TOGO),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEAFTER',     (0, 0), (0, 0), 1, JAUNE_TOGO),
    ]))
    elements.append(entete_table)
    elements.append(Spacer(1, 0.4 * cm))

    # Bande rouge décorative
    elements.append(HRFlowable(width="100%", thickness=4, color=ROUGE_TOGO, spaceAfter=6))

    # ------------------------------------------------------------------
    # 2. TITRE PRINCIPAL
    # ------------------------------------------------------------------
    type_display = declaration.get_type_declaration_display().upper()
    elements.append(Paragraph(
        f"RÉCÉPISSÉ DE DÉCLARATION DE {type_display}",
        styles['TitreDocument']
    ))
    elements.append(Paragraph(
        f"Pièces et Documents Administratifs",
        styles['SousTitre']
    ))

    # Numéro de récépissé encadré
    num_data = [[Paragraph(
        f"N° {declaration.numero_recepisse}",
        styles['NumeroBold']
    )]]
    num_table = Table(num_data, colWidths=[17 * cm])
    num_table.setStyle(TableStyle([
        ('BOX',           (0, 0), (-1, -1), 2, VERT_TOGO),
        ('BACKGROUND',    (0, 0), (-1, -1), GRIS_CLAIR),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(num_table)
    elements.append(Spacer(1, 0.4 * cm))

    # ------------------------------------------------------------------
    # 3. INFORMATIONS DU DÉCLARANT
    # ------------------------------------------------------------------
    elements.append(_ligne_section("Informations du déclarant", styles))
    elements.append(Spacer(1, 0.15 * cm))

    user = declaration.user
    infos_declarant = [
        ("Nom complet",    f"{user.last_name} {user.first_name}".strip() or user.username),
        ("Nom d'utilisateur", user.username),
        ("Téléphone",      user.telephone or "Non renseigné"),
        ("Email",          user.email or "Non renseigné"),
    ]
    elements.append(_tableau_infos(infos_declarant, styles))
    elements.append(Spacer(1, 0.4 * cm))

    # ------------------------------------------------------------------
    # 4. INFORMATIONS SUR LA PIÈCE
    # ------------------------------------------------------------------
    elements.append(_ligne_section("Informations sur la pièce", styles))
    elements.append(Spacer(1, 0.15 * cm))

    date_perte_str = (
        declaration.date_perte.strftime('%d/%m/%Y')
        if declaration.date_perte else "Non renseignée"
    )

    infos_piece = [
        ("Catégorie",          declaration.categorie.libelle),
        ("Numéro de la pièce", declaration.numero_piece),
        ("Nom sur la pièce",   declaration.nom_sur_piece),
        ("Date de la perte",   date_perte_str),
        ("Lieu",               declaration.lieu_perte or "Non renseigné"),
        ("Description",        declaration.description or "Aucune description"),
    ]
    elements.append(_tableau_infos(infos_piece, styles))
    elements.append(Spacer(1, 0.4 * cm))

    # ------------------------------------------------------------------
    # 5. INFORMATIONS ADMINISTRATIVES
    # ------------------------------------------------------------------
    elements.append(_ligne_section("Informations administratives", styles))
    elements.append(Spacer(1, 0.15 * cm))

    date_declaration_str = timezone.localtime(declaration.date_declaration).strftime(
        '%d/%m/%Y à %H:%M'
    )
    statut_display = declaration.get_statut_display()

    infos_admin = [
        ("Numéro de récépissé", declaration.numero_recepisse),
        ("Type de déclaration", declaration.get_type_declaration_display()),
        ("Statut actuel",       statut_display),
        ("Date de déclaration", date_declaration_str),
    ]

    if declaration.remarques_admin:
        infos_admin.append(("Remarques", declaration.remarques_admin))

    if declaration.declaration_correspondante:
        infos_admin.append((
            "Correspondance",
            f"Déclaration {declaration.declaration_correspondante.numero_recepisse}"
        ))

    elements.append(_tableau_infos(infos_admin, styles))
    elements.append(Spacer(1, 0.5 * cm))

    # ------------------------------------------------------------------
    # 6. ZONE DE SIGNATURE
    # ------------------------------------------------------------------
    date_impression = datetime.now().strftime('%d/%m/%Y à %H:%M')

    signature_data = [[
        Paragraph(
            f"Fait à Lomé, le {date_impression}<br/><br/><br/>"
            "<b>Le Déclarant</b><br/>(Signature)",
            styles['CorpsCentre']
        ),
        Paragraph(
            "<br/><br/><br/>"
            "<b>Le Responsable du Service</b><br/>(Cachet et Signature)",
            styles['CorpsCentre']
        ),
    ]]
    sig_table = Table(signature_data, colWidths=[8.5 * cm, 8.5 * cm])
    sig_table.setStyle(TableStyle([
        ('BOX',        (0, 0), (-1, -1), 0.5, GRIS_BORDURE),
        ('LINEAFTER',  (0, 0), (0, -1), 0.5, GRIS_BORDURE),
        ('TOPPADDING',    (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLAIR),
    ]))
    elements.append(sig_table)
    elements.append(Spacer(1, 0.3 * cm))

    # ------------------------------------------------------------------
    # 7. PIED DE PAGE
    # ------------------------------------------------------------------
    elements.append(HRFlowable(width="100%", thickness=1, color=VERT_TOGO, spaceAfter=6))
    elements.append(Paragraph(
        "⚠️  <b>Ce document est un récépissé de déclaration et ne constitue pas une pièce d'identité.</b><br/>"
        "Plateforme officielle de déclaration de pertes de pièces administratives — République Togolaise<br/>"
        f"Document généré le {date_impression} — Réf : {declaration.numero_recepisse}",
        styles['Note']
    ))

    # ------------------------------------------------------------------
    # CONSTRUCTION DU PDF
    # ------------------------------------------------------------------
    doc.build(elements)
    buffer.seek(0)
    return buffer
```

## File: backend/declarations/permissions.py
```python
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
```

## File: backend/declarations/serializers.py
```python
"""
Sérialiseurs pour l'API REST
Transforment les modèles Django en JSON et vice-versa
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, CategoriePiece, Declaration, Notification


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'inscription publique (citoyens uniquement).
    Le rôle est en lecture seule → toujours 'citoyen'.
    """
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
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'telephone', 'role',
            'date_creation', 'is_active'
        ]
        # role en lecture seule : l'inscription publique crée toujours des citoyens
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


# ─────────────────────────────────────────────────────────────────────
# NOUVEAU — Réservé aux administrateurs
# ─────────────────────────────────────────────────────────────────────

class CreateAgentSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création d'un agent (police ou admin).
    Utilisé UNIQUEMENT par les administrateurs.
    - Le rôle est OBLIGATOIRE et limité à 'police' ou 'admin'.
    - Génère un mot de passe initial que l'admin communique à l'agent.
    """
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
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'telephone', 'role',
            'date_creation', 'is_active'
        ]
        read_only_fields = ['id', 'date_creation']

    def validate_role(self, value):
        """Seuls les rôles 'police' et 'admin' sont autorisés ici."""
        if value not in ['police', 'admin']:
            raise serializers.ValidationError(
                "Rôle invalide. Valeurs acceptées : 'police', 'admin'."
            )
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        if not attrs.get('role'):
            raise serializers.ValidationError({
                "role": "Le rôle est obligatoire."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


# ─────────────────────────────────────────────────────────────────────
# Sérialiseurs existants (inchangés)
# ─────────────────────────────────────────────────────────────────────

class UserProfileSerializer(serializers.ModelSerializer):
    nombre_declarations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'telephone', 'role', 'date_creation', 'nombre_declarations',
            'is_active'
        ]
        read_only_fields = ['id', 'username', 'role', 'date_creation']

    def get_nombre_declarations(self, obj):
        return obj.declarations.count()


class CategoriePieceSerializer(serializers.ModelSerializer):
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
    categorie_nom  = serializers.CharField(source='categorie.libelle', read_only=True)
    declarant      = serializers.CharField(source='user.username', read_only=True)
    type_display   = serializers.CharField(source='get_type_declaration_display', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)

    class Meta:
        model = Declaration
        fields = [
            'id', 'numero_recepisse', 'type_declaration', 'type_display',
            'categorie', 'categorie_nom', 'numero_piece', 'nom_sur_piece',
            'nom_declarant', 'prenom_declarant',
            'date_naissance', 'lieu_naissance', 'profession',
            'statut', 'statut_display', 'declarant', 'date_declaration',
            'date_perte', 'lieu_perte',
        ]


class DeclarationDetailSerializer(serializers.ModelSerializer):
    categorie_detail      = CategoriePieceSerializer(source='categorie', read_only=True)
    declarant_detail      = UserProfileSerializer(source='user', read_only=True)
    type_display          = serializers.CharField(source='get_type_declaration_display', read_only=True)
    statut_display        = serializers.CharField(source='get_statut_display', read_only=True)
    correspondance_detail = DeclarationListSerializer(
        source='declaration_correspondante', read_only=True
    )

    class Meta:
        model = Declaration
        fields = '__all__'
        read_only_fields = [
            'id', 'numero_recepisse', 'user', 'date_declaration',
            'date_modification', 'declaration_correspondante',
        ]

    def validate_numero_piece(self, value):
        if not value:
            return value
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
    class Meta:
        model = Declaration
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
        model = Notification
        fields = [
            'id', 'type_notification', 'type_display', 'titre', 'message',
            'lue', 'date_creation', 'declaration', 'declaration_detail'
        ]
        read_only_fields = ['id', 'user', 'date_creation']


class StatistiquesSerializer(serializers.Serializer):
    total_declarations      = serializers.IntegerField()
    total_pertes            = serializers.IntegerField()
    total_trouvailles       = serializers.IntegerField()
    en_attente              = serializers.IntegerField()
    validees                = serializers.IntegerField()
    retrouvees              = serializers.IntegerField()
    restituees              = serializers.IntegerField()
    declarations_recentes   = DeclarationListSerializer(many=True)
    categories_populaires   = serializers.ListField()


class RechercheCorrespondanceSerializer(serializers.Serializer):
    numero_piece     = serializers.CharField(required=False, allow_blank=True, default='')
    nom_sur_piece    = serializers.CharField(required=False, allow_blank=True, default='')
    nom_declarant    = serializers.CharField(required=False, allow_blank=True, default='')
    prenom_declarant = serializers.CharField(required=False, allow_blank=True, default='')
    categorie        = serializers.IntegerField(required=False)
```

## File: backend/declarations/signals.py
```python
"""
Signaux Django pour le matching automatique
Déclenché après chaque sauvegarde d'une Declaration.

Logique métier :
  - Une PERTE est sauvegardée → on cherche une TROUVAILLE avec le même numéro de pièce
  - Une TROUVAILLE est sauvegardée → on cherche une PERTE avec le même numéro de pièce
  - Si correspondance trouvée (statut VALIDE, pas déjà matchée) :
      → Les deux déclarations passent au statut RETROUVE
      → Les deux sont liées (declaration_correspondante)
      → Chaque déclarant reçoit une Notification de type MATCH
      → Chaque déclarant reçoit un email Gmail avec les instructions
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

logger = logging.getLogger(__name__)


@receiver(post_save, sender='declarations.Declaration')
def chercher_correspondance(sender, instance, created, **kwargs):
    """
    Signal déclenché après chaque sauvegarde d'une déclaration.
    On ne cherche que si :
      - la déclaration vient d'être créée OU vient de passer à VALIDE
      - elle n'a pas encore de correspondance
    """
    # Import local pour éviter les imports circulaires
    from .models import Declaration, Notification

    # Conditions de déclenchement du matching
    if instance.statut != 'VALIDE':
        return
    if instance.declaration_correspondante is not None:
        return
    if not created:
        update_fields = kwargs.get('update_fields')
        # Si le save ne concerne pas le statut, on ignore
        if update_fields and 'statut' not in update_fields:
            return

    # Déterminer le type opposé à chercher
    type_oppose = 'TROUVAILLE' if instance.type_declaration == 'PERTE' else 'PERTE'

    # Chercher une déclaration opposée correspondante :
    # même numéro de pièce (insensible à la casse), validée, pas encore matchée
    correspondances = Declaration.objects.filter(
        type_declaration=type_oppose,
        statut='VALIDE',
        numero_piece__iexact=instance.numero_piece,
        declaration_correspondante__isnull=True
    ).exclude(pk=instance.pk)

    if not correspondances.exists():
        return  # Pas de correspondance trouvée

    # On prend la correspondance la plus récente
    match = correspondances.order_by('-date_declaration').first()

    # Utiliser une transaction pour garantir l'atomicité
    with transaction.atomic():
        Declaration.objects.filter(pk=instance.pk).update(
            declaration_correspondante=match,
            statut='RETROUVE'
        )
        Declaration.objects.filter(pk=match.pk).update(
            declaration_correspondante=instance,
            statut='RETROUVE'
        )
        # Recharger pour avoir des objets à jour
        instance_fresh = Declaration.objects.get(pk=instance.pk)
        match_fresh    = Declaration.objects.get(pk=match.pk)

        _creer_notification_match(
            user=instance.user,
            declaration_propre=instance_fresh,
            declaration_match=match_fresh
        )
        _creer_notification_match(
            user=match.user,
            declaration_propre=match_fresh,
            declaration_match=instance_fresh
        )


def _creer_notification_match(user, declaration_propre, declaration_match):
    """
    Crée une notification in-app de type MATCH ET envoie l'email Gmail
    pour un utilisateur lors d'un matching automatique.
    """
    from .models import Notification
    from .email_service import envoyer_email_retrouve  # import local → évite les imports circulaires

    # ── Notification in-app ───────────────────────────────────────────────────
    if declaration_propre.type_declaration == 'PERTE':
        titre = "🎉 Bonne nouvelle ! Votre pièce a peut-être été retrouvée"
        message = (
            f"Votre déclaration de perte '{declaration_propre.numero_recepisse}' "
            f"({declaration_propre.numero_piece} - {declaration_propre.nom_sur_piece}) "
            f"correspond à une trouvaille enregistrée sous le numéro "
            f"'{declaration_match.numero_recepisse}'. "
            f"Veuillez contacter le commissariat pour la restitution."
        )
    else:
        titre = "📋 Une pièce que vous avez trouvée a un propriétaire"
        message = (
            f"La trouvaille que vous avez déclarée sous '{declaration_propre.numero_recepisse}' "
            f"({declaration_propre.numero_piece} - {declaration_propre.nom_sur_piece}) "
            f"correspond à une déclaration de perte '{declaration_match.numero_recepisse}'. "
            f"Merci de vous rapprocher du commissariat pour la restitution."
        )

    Notification.objects.create(
        user=user,
        declaration=declaration_propre,
        type_notification='MATCH',
        titre=titre,
        message=message
    )

    # ── Email Gmail ───────────────────────────────────────────────────────────
    try:
        envoyer_email_retrouve(
            user=user,
            declaration=declaration_propre,
            match=declaration_match,
        )
    except Exception as exc:
        logger.error(
            "Échec email MATCH pour %s <%s> — déclaration %s : %s",
            user.username,
            getattr(user, 'email', '?'),
            declaration_propre.numero_recepisse,
            exc
        )
```

## File: backend/declarations/tests.py
```python
from django.test import TestCase

# Create your tests here.
```

## File: backend/declarations/urls.py
```python
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
from .views import ChangePasswordView

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

    # Changement de mot de passe
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
```

## File: backend/declarations/views.py
```python
"""
Vues de l'API REST
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from django.http import FileResponse
from .pdf_generator import generate_recepisse_pdf
import logging  # ← ajouté pour les logs d'email
from django.contrib.auth import authenticate

from .models import CategoriePiece, Declaration, Notification
from .serializers import (
    UserSerializer, UserProfileSerializer,
    CreateAgentSerializer,
    CategoriePieceSerializer,
    DeclarationListSerializer, DeclarationDetailSerializer,
    DeclarationCreateSerializer, NotificationSerializer,
    StatistiquesSerializer, RechercheCorrespondanceSerializer
)
from .permissions import IsAdminOrPolice, IsAdminOnly, IsOwnerOrAdminOrPolice
from .email_service import envoyer_email_retrouve  # ← ajouté pour les notifications Gmail

User = get_user_model()
logger = logging.getLogger(__name__)


# =============================================================================
# AUTHENTIFICATION & PROFIL
# =============================================================================

class RegisterView(APIView):
    """Inscription publique — crée UNIQUEMENT des comptes citoyens."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Compte créé avec succès',
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Profil de l'utilisateur connecté. GET / PUT /api/profile/"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================================================================
# GESTION DES AGENTS — RÉSERVÉ AUX ADMINISTRATEURS
# =============================================================================

class AgentManagementView(APIView):
    """
    GET  /api/admin/agents/   → liste agents
    POST /api/admin/agents/   → créer un agent
    """
    permission_classes = [IsAdminOnly]

    def get(self, request):
        agents = User.objects.filter(role__in=['police', 'admin']).order_by('-date_creation')
        return Response(UserProfileSerializer(agents, many=True).data)

    def post(self, request):
        serializer = CreateAgentSerializer(data=request.data)
        if serializer.is_valid():
            agent = serializer.save()
            return Response({
                'message': f"Agent '{agent.username}' créé avec succès.",
                'agent': UserProfileSerializer(agent).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentDetailView(APIView):
    """
    PATCH  /api/admin/agents/<id>/  → modifier
    DELETE /api/admin/agents/<id>/  → désactiver (soft-delete)
    """
    permission_classes = [IsAdminOnly]

    def _get_agent(self, pk):
        try:
            return User.objects.get(pk=pk, role__in=['police', 'admin'])
        except User.DoesNotExist:
            return None

    def patch(self, request, pk):
        agent = self._get_agent(pk)
        if not agent:
            return Response({'error': 'Agent introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        if agent == request.user and request.data.get('role') == 'citoyen':
            return Response(
                {'error': 'Vous ne pouvez pas modifier votre propre rôle.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = UserProfileSerializer(agent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        agent = self._get_agent(pk)
        if not agent:
            return Response({'error': 'Agent introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        if agent == request.user:
            return Response(
                {'error': 'Vous ne pouvez pas désactiver votre propre compte.'},
                status=status.HTTP_403_FORBIDDEN
            )
        agent.is_active = False
        agent.save(update_fields=['is_active'])
        return Response({'message': f"Le compte de '{agent.username}' a été désactivé."})


# =============================================================================
# GESTION COMPLÈTE DES UTILISATEURS — ADMIN UNIQUEMENT
# =============================================================================

class UserManagementView(APIView):
    """
    Liste TOUS les utilisateurs (citoyens + agents + admins).
    GET /api/admin/users/?role=citoyen&search=jean
    """
    permission_classes = [IsAdminOnly]

    def get(self, request):
        qs = User.objects.all().order_by('-date_creation')

        role = request.query_params.get('role', '').strip()
        if role:
            qs = qs.filter(role=role)

        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        return Response(UserProfileSerializer(qs, many=True).data)


class UserDetailAdminView(APIView):
    """
    Opérations sur un utilisateur quelconque (citoyen, agent, admin).

    GET    /api/admin/users/<id>/  → détail
    PATCH  /api/admin/users/<id>/  → modifier
    DELETE /api/admin/users/<id>/  → suppression DÉFINITIVE
    """
    permission_classes = [IsAdminOnly]

    def _get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserProfileSerializer(user).data)

    def patch(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        if user == request.user:
            return Response(
                {'error': 'Modifiez votre propre compte depuis /api/profile/.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self._get_user(pk)
        if not user:
            return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        if user == request.user:
            return Response(
                {'error': 'Vous ne pouvez pas supprimer votre propre compte.'},
                status=status.HTTP_403_FORBIDDEN
            )
        username = user.username
        user.delete()   # suppression définitive en base (cascade sur déclarations/notifs)
        return Response(
            {'message': f"L'utilisateur « {username} » a été supprimé définitivement."},
            status=status.HTTP_200_OK
        )


# =============================================================================
# CATÉGORIES
# =============================================================================

class CategoriePieceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoriePiece.objects.filter(actif=True)
    serializer_class = CategoriePieceSerializer
    permission_classes = [permissions.AllowAny]


# =============================================================================
# DÉCLARATIONS
# =============================================================================

class DeclarationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'police']:
            return Declaration.objects.select_related(
                'categorie', 'user', 'declaration_correspondante'
            ).all()
        return Declaration.objects.select_related(
            'categorie', 'user', 'declaration_correspondante'
        ).filter(user=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return DeclarationListSerializer
        if self.action == 'create':
            return DeclarationCreateSerializer
        return DeclarationDetailSerializer

    def get_permissions(self):
        if self.action == 'changer_statut':
            return [IsAdminOrPolice()]
        if self.action == 'destroy':
            return [IsAdminOnly()]      # ← seul l'admin supprime
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Suppression DÉFINITIVE d'une déclaration — admin uniquement."""
        declaration = self.get_object()
        numero = declaration.numero_recepisse
        declaration.delete()
        return Response(
            {'message': f"La déclaration « {numero} » a été supprimée définitivement."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def telecharger_recepisse(self, request, pk=None):
        declaration = self.get_object()
        if request.user.role not in ['admin', 'police']:
            if declaration.user != request.user:
                return Response(
                    {'error': 'Vous ne pouvez télécharger que vos propres récépissés.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        try:
            pdf_buffer = generate_recepisse_pdf(declaration)
        except Exception as e:
            return Response(
                {'error': f'Erreur génération PDF : {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return FileResponse(
            pdf_buffer, as_attachment=True,
            filename=f"recepisse_{declaration.numero_recepisse}.pdf",
            content_type='application/pdf'
        )

    @action(detail=False, methods=['get'])
    def mes_declarations(self, request):
        qs = Declaration.objects.filter(user=request.user).select_related('categorie')
        return Response(DeclarationListSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'])
    def pertes(self, request):
        return Response(DeclarationListSerializer(
            self.get_queryset().filter(type_declaration='PERTE'), many=True
        ).data)

    @action(detail=False, methods=['get'])
    def trouvailles(self, request):
        return Response(DeclarationListSerializer(
            self.get_queryset().filter(type_declaration='TROUVAILLE'), many=True
        ).data)

    @action(detail=False, methods=['post'])
    def rechercher(self, request):
        serializer = RechercheCorrespondanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        d = serializer.validated_data
        numero_piece     = d.get('numero_piece', '').strip()
        nom_sur_piece    = d.get('nom_sur_piece', '').strip()
        nom_declarant    = d.get('nom_declarant', '').strip()
        prenom_declarant = d.get('prenom_declarant', '').strip()
        categorie_id     = d.get('categorie')

        if not any([numero_piece, nom_sur_piece, nom_declarant, prenom_declarant]):
            return Response(
                {'error': 'Fournissez au moins un critère de recherche.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        query = Q(type_declaration='TROUVAILLE', statut='VALIDE')
        if numero_piece:
            query &= Q(numero_piece__icontains=numero_piece)
        if nom_declarant:
            query &= (Q(nom_declarant__icontains=nom_declarant) | Q(nom_sur_piece__icontains=nom_declarant))
        if prenom_declarant:
            query &= (Q(prenom_declarant__icontains=prenom_declarant) | Q(nom_sur_piece__icontains=prenom_declarant))
        if nom_sur_piece and not nom_declarant and not prenom_declarant:
            query &= Q(nom_sur_piece__icontains=nom_sur_piece)
        if categorie_id:
            query &= Q(categorie_id=categorie_id)

        qs = Declaration.objects.filter(query).select_related('categorie', 'user')
        return Response({
            'nombre_resultats': qs.count(),
            'correspondances':  DeclarationListSerializer(qs, many=True).data,
        })

    @action(detail=True, methods=['patch'])
    def changer_statut(self, request, pk=None):
        declaration = self.get_object()
        nouveau_statut = request.data.get('statut')
        remarques = request.data.get('remarques', '')

        if nouveau_statut not in dict(Declaration.STATUT_CHOICES):
            return Response(
                {'error': f"Statut invalide. Valeurs : {list(dict(Declaration.STATUT_CHOICES).keys())}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ancien_statut = declaration.statut          # ← mémorisé avant modification
        ancien_label  = declaration.get_statut_display()

        declaration.statut = nouveau_statut
        if remarques:
            declaration.remarques_admin = remarques
        declaration.save(update_fields=['statut', 'remarques_admin', 'date_modification'])

        # ── Notification in-app (existante, inchangée) ────────────────────────
        Notification.objects.create(
            user=declaration.user, declaration=declaration,
            type_notification='STATUT',
            titre=f"Changement de statut : {declaration.numero_recepisse}",
            message=(
                f"Votre déclaration est passée de « {ancien_label} » "
                f"à « {declaration.get_statut_display()} ». {remarques}"
            )
        )

        # ── Emails Gmail si passage à RETROUVE ────────────────────────────────
        if nouveau_statut == 'RETROUVE' and ancien_statut != 'RETROUVE':
            self._envoyer_emails_retrouve(declaration, remarques)

        return Response(DeclarationDetailSerializer(declaration).data)

    # -------------------------------------------------------------------------
    # Méthode privée : envoi des emails lors d'un passage manuel à RETROUVE
    # -------------------------------------------------------------------------

    def _envoyer_emails_retrouve(self, declaration, remarques=''):
        """
        Envoie les emails Gmail aux déclarants concernés quand
        l'agent passe manuellement une déclaration au statut RETROUVE.

        Cas 1 — La déclaration a déjà une correspondance (match) :
            → Email au déclarant principal + email à la partie adverse.
        Cas 2 — Pas de correspondance (action manuelle sans match) :
            → Email au seul déclarant de la déclaration concernée.
        """
        match = declaration.declaration_correspondante  # peut être None

        # Email au déclarant de la déclaration modifiée par l'agent
        try:
            envoyer_email_retrouve(
                user=declaration.user,
                declaration=declaration,
                match=match,
                remarques=remarques,
            )
        except Exception as exc:
            logger.error(
                "Échec email RETROUVÉ (déclarant principal) %s : %s",
                declaration.numero_recepisse, exc
            )

        # Email au déclarant de la déclaration correspondante (si présent et distinct)
        if match and match.user != declaration.user:
            try:
                envoyer_email_retrouve(
                    user=match.user,
                    declaration=match,
                    match=declaration,
                    remarques=remarques,
                )
            except Exception as exc:
                logger.error(
                    "Échec email RETROUVÉ (déclarant correspondant) %s : %s",
                    match.numero_recepisse, exc
                )


# =============================================================================
# NOTIFICATIONS
# =============================================================================

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        return Response(self.get_serializer(
            self.get_queryset().filter(lue=False), many=True
        ).data)

    @action(detail=True, methods=['post'])
    def marquer_lue(self, request, pk=None):
        notif = self.get_object()
        notif.lue = True
        notif.save()
        return Response({'status': 'Notification marquée comme lue'})

    @action(detail=False, methods=['post'])
    def tout_marquer_lues(self, request):
        count = self.get_queryset().update(lue=True)
        return Response({'status': f'{count} notification(s) marquée(s) comme lue(s)'})


# =============================================================================
# STATISTIQUES
# =============================================================================

class StatistiquesView(APIView):
    permission_classes = [IsAdminOrPolice]

    def get(self, request):
        date_limite = timezone.now() - timedelta(days=7)
        data = {
            'total_declarations':    Declaration.objects.count(),
            'total_pertes':          Declaration.objects.filter(type_declaration='PERTE').count(),
            'total_trouvailles':     Declaration.objects.filter(type_declaration='TROUVAILLE').count(),
            'en_attente':            Declaration.objects.filter(statut='EN_ATTENTE').count(),
            'validees':              Declaration.objects.filter(statut='VALIDE').count(),
            'retrouvees':            Declaration.objects.filter(statut='RETROUVE').count(),
            'restituees':            Declaration.objects.filter(statut='RESTITUE').count(),
            'total_utilisateurs':    User.objects.count(),
            'total_citoyens':        User.objects.filter(role='citoyen').count(),
            'total_agents':          User.objects.filter(role__in=['police', 'admin']).count(),
            'declarations_recentes': DeclarationListSerializer(
                Declaration.objects.filter(date_declaration__gte=date_limite)
                           .order_by('-date_declaration')[:10],
                many=True
            ).data,
            'categories_populaires': list(
                CategoriePiece.objects.annotate(nombre=Count('declarations'))
                              .order_by('-nombre')[:5].values('libelle', 'nombre')
            ),
        }
        return Response(data)
    



# =============================================================================
# CHANGEMENT DE MOT DE PASSE
# =============================================================================


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_pwd = request.data.get('current_password', '')
        new_pwd = request.data.get('new_password', '')

        if not authenticate(username=user.username, password=old_pwd):
            return Response(
                {'current_password': 'Mot de passe actuel incorrect.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(new_pwd) < 8:
            return Response(
                {'new_password': 'Minimum 8 caractères.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_pwd)
        user.save()
        return Response({'message': 'Mot de passe modifié avec succès.'})
```

## File: backend/init_categories_windows.py
```python
"""
Script pour créer les catégories de pièces initiales
Exécutez avec : python init_categories_windows.py
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from declarations.models import CategoriePiece

# Liste des catégories de pièces au Togo
categories = [
    {
        'libelle': 'Pièce d\'identité',
        'description': 'Carte Nationale d\'Identité (CNI), passeport',
        'icone': 'id-card'
    },
    {
        'libelle': 'Véhicule',
        'description': 'Carte grise, permis de conduire, plaque d\'immatriculation',
        'icone': 'car'
    },
    {
        'libelle': 'Documents scolaires',
        'description': 'Diplômes, certificats, cartes d\'étudiant',
        'icone': 'graduation-cap'
    },
    {
        'libelle': 'Documents bancaires',
        'description': 'Cartes bancaires, chéquiers',
        'icone': 'credit-card'
    },
    {
        'libelle': 'Documents professionnels',
        'description': 'Badges, cartes professionnelles',
        'icone': 'briefcase'
    },
    {
        'libelle': 'Documents de santé',
        'description': 'Cartes de santé, carnets de vaccination',
        'icone': 'heart'
    },
    {
        'libelle': 'Autres documents',
        'description': 'Tout autre document administratif',
        'icone': 'file'
    }
]

print("Création des catégories de pièces...")
print("=" * 50)

for cat_data in categories:
    categorie, created = CategoriePiece.objects.get_or_create(
        libelle=cat_data['libelle'],
        defaults={
            'description': cat_data['description'],
            'icone': cat_data['icone']
        }
    )
    if created:
        print(f"✓ Créée : {categorie.libelle}")
    else:
        print(f"- Existe déjà : {categorie.libelle}")

print("=" * 50)
print(f"\nTotal : {CategoriePiece.objects.count()} catégories dans la base")
print("\n✅ Catégories créées avec succès !")
```

## File: backend/manage.py
```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

## File: frontend/.gitignore
```
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
```

## File: frontend/.vscode/extensions.json
```json
{
  "recommendations": ["Vue.volar"]
}
```

## File: frontend/index.html
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

## File: frontend/package.json
```json
{
  "name": "declatogo-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.13.5",
    "chart.js": "^4.5.1",
    "pinia": "^3.0.4",
    "vue": "^3.5.28",
    "vue-i18n": "^11.2.8",
    "vue-router": "^5.0.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^6.0.2",
    "autoprefixer": "^10.4.24",
    "postcss": "^8.5.6",
    "tailwindcss": "^3.4.19",
    "vite": "^7.3.1"
  }
}
```

## File: frontend/postcss.config.js
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

## File: frontend/public/vite.svg
```xml
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--logos" width="31.88" height="32" preserveAspectRatio="xMidYMid meet" viewBox="0 0 256 257"><defs><linearGradient id="IconifyId1813088fe1fbc01fb466" x1="-.828%" x2="57.636%" y1="7.652%" y2="78.411%"><stop offset="0%" stop-color="#41D1FF"></stop><stop offset="100%" stop-color="#BD34FE"></stop></linearGradient><linearGradient id="IconifyId1813088fe1fbc01fb467" x1="43.376%" x2="50.316%" y1="2.242%" y2="89.03%"><stop offset="0%" stop-color="#FFEA83"></stop><stop offset="8.333%" stop-color="#FFDD35"></stop><stop offset="100%" stop-color="#FFA800"></stop></linearGradient></defs><path fill="url(#IconifyId1813088fe1fbc01fb466)" d="M255.153 37.938L134.897 252.976c-2.483 4.44-8.862 4.466-11.382.048L.875 37.958c-2.746-4.814 1.371-10.646 6.827-9.67l120.385 21.517a6.537 6.537 0 0 0 2.322-.004l117.867-21.483c5.438-.991 9.574 4.796 6.877 9.62Z"></path><path fill="url(#IconifyId1813088fe1fbc01fb467)" d="M185.432.063L96.44 17.501a3.268 3.268 0 0 0-2.634 3.014l-5.474 92.456a3.268 3.268 0 0 0 3.997 3.378l24.777-5.718c2.318-.535 4.413 1.507 3.936 3.838l-7.361 36.047c-.495 2.426 1.782 4.5 4.151 3.78l15.304-4.649c2.372-.72 4.652 1.36 4.15 3.788l-11.698 56.621c-.732 3.542 3.979 5.473 5.943 2.437l1.313-2.028l72.516-144.72c1.215-2.423-.88-5.186-3.54-4.672l-25.505 4.922c-2.396.462-4.435-1.77-3.759-4.114l16.646-57.705c.677-2.35-1.37-4.583-3.769-4.113Z"></path></svg>
```

## File: frontend/README.md
```markdown
# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).
```

## File: frontend/src/App.vue
```vue
<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from './stores/auth'
import { notificationsAPI } from './services/api'

const route       = useRoute()
const { t, locale } = useI18n()
const authStore   = useAuthStore()
const mobileOpen  = ref(false)
const unreadCount = ref(0)

const toggleLang = () => {
  locale.value = locale.value === 'fr' ? 'en' : 'fr'
}

const handleLogout = () => {
  authStore.logout()
  mobileOpen.value  = false
  unreadCount.value = 0
}

const fetchUnread = async () => {
  if (!authStore.isAuthenticated) return
  try {
    const { data } = await notificationsAPI.nonLues()
    unreadCount.value = (data.results ?? data).length
  } catch { unreadCount.value = 0 }
}

// Rafraîchit le badge à chaque changement de page
watch(route, () => {
  mobileOpen.value = false
  fetchUnread()
})

// Charge le badge dès que l'utilisateur est connecté
watch(() => authStore.isAuthenticated, (auth) => {
  if (auth) fetchUnread()
  else unreadCount.value = 0
}, { immediate: true })
</script>

<template>
  <!-- ── Bandeau d'annonce ── -->
  <div class="bg-or text-vert text-xs font-semibold text-center py-2.5 px-4 flex items-center justify-center gap-2">
    ✨ {{ t('announce') }}
  </div>

  <!-- ══════════════════════════════════════════
       NAVIGATION DESKTOP
  ══════════════════════════════════════════ -->
  <nav class="sticky top-0 z-50 flex items-center justify-between px-[5%] h-[68px]
              bg-vert/95 backdrop-blur border-b-2 border-or">

    <!-- Logo -->
    <router-link :to="{ name: 'home' }"
      class="flex items-center gap-3 text-white font-serif text-xl font-bold no-underline">
      <div class="w-9 h-9 bg-or rounded-lg flex items-center justify-center text-vert font-bold text-sm">
        DT
      </div>
      Décla<span class="text-or">Togo</span>
    </router-link>

    <!-- Liens desktop -->
    <div class="hidden md:flex items-center gap-1">

      <!-- Liens publics -->
      <router-link :to="{ name: 'home' }"   class="nav-desktop-link">{{ t('nav.home') }}</router-link>
      <router-link :to="{ name: 'search' }" class="nav-desktop-link">{{ t('nav.search') }}</router-link>

      <!-- Liens connectés -->
      <template v-if="authStore.isAuthenticated">

        <router-link :to="{ name: 'declare' }" class="nav-desktop-link">
          {{ t('nav.declare') }}
        </router-link>

        <!-- ── MES DÉCLARATIONS ── -->
        <router-link :to="{ name: 'mes-declarations' }" class="nav-desktop-link">
          📋 Mes déclarations
        </router-link>

        <!-- ── NOTIFICATIONS (avec badge) ── -->
        <router-link :to="{ name: 'notifications' }" class="nav-desktop-link relative">
          🔔 Notifications
          <span v-if="unreadCount > 0"
            class="absolute -top-1 -right-1 min-w-[18px] h-[18px] bg-rouge text-white
                   text-[10px] font-bold rounded-full flex items-center justify-center
                   px-1 leading-none shadow">
            {{ unreadCount > 99 ? '99+' : unreadCount }}
          </span>
        </router-link>

        <!-- Tableau de bord admin/police -->
        <router-link v-if="authStore.isStaff" :to="{ name: 'dashboard' }" class="nav-desktop-link">
          {{ t('nav.dashboard') }}
        </router-link>

      </template>

      <!-- Sélecteur langue -->
      <button @click="toggleLang" class="lang-btn">
        🌐 {{ locale.toUpperCase() }}
      </button>

      <!-- Non connecté -->
      <template v-if="!authStore.isAuthenticated">
        <router-link :to="{ name: 'login' }"    class="nav-desktop-link">{{ t('nav.login') }}</router-link>
        <router-link :to="{ name: 'register' }" class="register-btn">{{ t('nav.register') }}</router-link>
      </template>

      <!-- Connecté — bouton déconnexion -->
      <button v-else @click="handleLogout" class="logout-btn">
        {{ t('nav.logout') }}
      </button>

    </div>

    <!-- Bouton hamburger mobile -->
    <button @click="mobileOpen = !mobileOpen"
      class="md:hidden text-white text-2xl bg-transparent border-none">
      {{ mobileOpen ? '✕' : '☰' }}
    </button>
  </nav>

  <!-- ══════════════════════════════════════════
       MENU MOBILE
  ══════════════════════════════════════════ -->
  <transition name="slide-down">
    <div v-if="mobileOpen"
      class="md:hidden fixed top-[108px] inset-x-0 z-40 bg-vert/98 backdrop-blur
             border-b border-or/30 flex flex-col gap-1 px-4 py-4">

      <router-link :to="{ name: 'home' }"   class="nav-mobile-link">{{ t('nav.home') }}</router-link>
      <router-link :to="{ name: 'search' }" class="nav-mobile-link">{{ t('nav.search') }}</router-link>

      <template v-if="authStore.isAuthenticated">

        <router-link :to="{ name: 'declare' }" class="nav-mobile-link">
          {{ t('nav.declare') }}
        </router-link>

        <!-- ── MES DÉCLARATIONS (mobile) ── -->
        <router-link :to="{ name: 'mes-declarations' }" class="nav-mobile-link">
          📋 Mes déclarations
        </router-link>

        <!-- ── NOTIFICATIONS (mobile, avec badge) ── -->
        <router-link :to="{ name: 'notifications' }"
          class="nav-mobile-link flex items-center justify-between">
          <span>🔔 Notifications</span>
          <span v-if="unreadCount > 0"
            class="min-w-[20px] h-5 bg-rouge text-white text-[10px] font-bold
                   rounded-full flex items-center justify-center px-1.5 leading-none">
            {{ unreadCount > 99 ? '99+' : unreadCount }}
          </span>
        </router-link>

        <router-link v-if="authStore.isStaff" :to="{ name: 'dashboard' }" class="nav-mobile-link">
          {{ t('nav.dashboard') }}
        </router-link>

        <div class="my-1 border-t border-white/10"></div>

        <button @click="handleLogout"
          class="nav-mobile-link text-left"
          style="color: #ff6b6b;">
          🚪 {{ t('nav.logout') }}
        </button>

      </template>

      <template v-else>
        <router-link :to="{ name: 'login' }"    class="nav-mobile-link">{{ t('nav.login') }}</router-link>
        <router-link :to="{ name: 'register' }" class="nav-mobile-link">{{ t('nav.register') }}</router-link>
      </template>

    </div>
  </transition>

  <!-- ══ Contenu des pages ══ -->
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" :key="route.fullPath" />
    </transition>
  </router-view>
</template>

<style scoped>
/* ── Navigation desktop ── */
.nav-desktop-link {
  @apply relative text-white/80 hover:text-white hover:bg-white/10
         px-3 py-2 rounded-lg text-sm font-medium transition-all no-underline;
}
/* Lien actif */
.router-link-active.nav-desktop-link {
  @apply text-white bg-white/15;
}

/* ── Boutons spéciaux ── */
.register-btn {
  @apply bg-or text-vert font-bold text-sm px-5 py-2.5 rounded-lg no-underline
         hover:bg-[#e8b220] transition-all;
}
.logout-btn {
  @apply bg-rouge text-white font-semibold text-sm px-4 py-2 rounded-lg
         border-none cursor-pointer transition-all hover:bg-[#e8192f];
}
.lang-btn {
  @apply text-xs border border-white/30 px-2.5 py-1.5 rounded-lg
         text-white/70 bg-transparent cursor-pointer hover:border-white/60
         hover:text-white transition-all;
}

/* ── Navigation mobile ── */
.nav-mobile-link {
  @apply block text-sm font-medium px-4 py-3 rounded-lg transition-all no-underline;
  color: rgba(255, 255, 255, 0.85);
}
.nav-mobile-link:hover {
  background-color: rgba(255, 255, 255, 0.10);
  color: #ffffff;
}
.router-link-active.nav-mobile-link {
  background-color: rgba(255, 255, 255, 0.15);
  color: #ffffff;
}

/* ── Transitions ── */
.fade-enter-active,
.fade-leave-active       { transition: opacity .2s ease; }
.fade-enter-from,
.fade-leave-to           { opacity: 0; }

.slide-down-enter-active,
.slide-down-leave-active { transition: all .25s ease; }
.slide-down-enter-from,
.slide-down-leave-to     { opacity: 0; transform: translateY(-10px); }
</style>
```

## File: frontend/src/assets/vue.svg
```xml
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--logos" width="37.07" height="36" preserveAspectRatio="xMidYMid meet" viewBox="0 0 256 198"><path fill="#41B883" d="M204.8 0H256L128 220.8L0 0h97.92L128 51.2L157.44 0h47.36Z"></path><path fill="#41B883" d="m0 0l128 220.8L256 0h-51.2L128 132.48L50.56 0H0Z"></path><path fill="#35495E" d="M50.56 0L128 133.12L204.8 0h-47.36L128 51.2L97.92 0H50.56Z"></path></svg>
```

## File: frontend/src/components/HelloWorld.vue
```vue
<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <button type="button" @click="count++">count is {{ count }}</button>
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p>
    Learn more about IDE Support for Vue in the
    <a
      href="https://vuejs.org/guide/scaling-up/tooling.html#ide-support"
      target="_blank"
      >Vue Docs Scaling up Guide</a
    >.
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
```

## File: frontend/src/i18n/index.js
```javascript
import { createI18n } from 'vue-i18n'

// ── Messages français ──────────────────────────────────────────────
const fr = {
  nav: {
    home:     'Accueil',
    search:   'Rechercher',
    declare:  'Déclarer',
    howto:    'Comment ça marche',
    login:    'Connexion',
    register: "S'inscrire",
    logout:   'Déconnexion',
    dashboard:'Tableau de bord',
    profile:  'Mon profil',
  },
  hero: {
    badge:    'Plateforme Officielle — République Togolaise',
    title1:   'Retrouvez vos',
    title2:   'pièces perdues',
    title3:   'en ligne',
    subtitle: 'DéclaTogo centralise les déclarations de pertes et de trouvailles de documents administratifs. Simple, rapide, officiel.',
    cta_loss: 'Déclarer une perte',
    cta_search:'Rechercher ma pièce',
  },
  search: {
    title:       'Recherche rapide',
    subtitle:    'Vérifiez si votre pièce a été signalée comme trouvée',
    placeholder: 'Numéro de pièce (ex: TG20240001)',
    all_cat:     'Toutes les catégories',
    btn:         'Lancer la recherche',
    frequent:    'Recherches fréquentes',
  },
  stats: {
    declarations: 'Déclarations enregistrées',
    found:        'Pièces retrouvées',
    citizens:     'Citoyens inscrits',
    rate:         'Taux de restitution',
  },
  steps: {
    label:  'Processus',
    title:  'Comment ça fonctionne ?',
    sub:    'Trois étapes simples pour déclarer depuis n\'importe où au Togo.',
    s1_title:'Créez votre compte',
    s1_text: 'Inscrivez-vous gratuitement avec votre numéro de téléphone et une adresse email.',
    s2_title:'Soumettez votre déclaration',
    s2_text: 'Remplissez le formulaire avec les informations sur votre pièce perdue ou trouvée.',
    s3_title:'Recevez votre récépissé',
    s3_text: 'Téléchargez votre récépissé officiel PDF. Soyez notifié si une correspondance est trouvée.',
  },
  features: {
    label:        'Fonctionnalités',
    title:        'Une plateforme complète',
    sub:          'Conçue pour les réalités togolaises, optimisée pour les réseaux 3G/4G.',
    matching:     'Matching automatique',
    matching_txt: 'Notre algorithme rapproche les déclarations de pertes et de trouvailles.',
    pdf:          'Récépissé PDF officiel',
    pdf_txt:      'Générez un document officiel reconnu, avec numéro de référence unique.',
    notif:        'Notifications en temps réel',
    notif_txt:    'Recevez une alerte dès qu\'une trouvaille correspond à votre déclaration.',
    security:     'Sécurité JWT',
    security_txt: 'Authentification sécurisée. Vos données sont chiffrées et protégées.',
    mobile:       '100% Mobile',
    mobile_txt:   'Interface responsive. Fonctionne même sur connexion 3G lente.',
    admin:        'Tableau de bord admin',
    admin_txt:    'Les agents gèrent et valident les déclarations depuis un dashboard centralisé.',
  },
  categories: {
    label:    'Catégories',
    title:    'Types de documents pris en charge',
    identity: 'Pièce d\'identité',
    vehicle:  'Véhicule',
    school:   'Documents scolaires',
    bank:     'Documents bancaires',
    pro:      'Documents professionnels',
    health:   'Documents de santé',
    other:    'Autres documents',
    suggest:  'Suggérer une catégorie',
  },
  cta: {
    title:    'Prêt à déclarer votre perte ?',
    sub:      'Rejoignez les citoyens togolais qui utilisent DéclaTogo. Inscription gratuite, récépissé immédiat.',
    loss:     'Déclarer une perte',
    found:    'Signaler une trouvaille',
  },
  footer: {
    desc:     'Plateforme officielle de déclaration de pertes de pièces administratives.',
    services: 'Services',
    info:     'Informations',
    legal:    'Légal',
    rights:   '© 2025 DéclaTogo — République Togolaise. Tous droits réservés.',
    made:     'Développé pour les citoyens togolais',
  },
  auth: {
    login_title:    'Connexion',
    login_sub:      'Accédez à votre espace citoyen',
    username:       "Nom d'utilisateur",
    password:       'Mot de passe',
    remember:       'Se souvenir de moi',
    forgot:         'Mot de passe oublié ?',
    login_btn:      'Se connecter',
    no_account:     'Pas encore de compte ?',
    register_link:  "S'inscrire",
    register_title: 'Créer un compte',
    register_sub:   'Rejoignez DéclaTogo gratuitement',
    first_name:     'Prénom',
    last_name:      'Nom de famille',
    email:          'Adresse email',
    phone:          'Numéro de téléphone',
    pwd_confirm:    'Confirmer le mot de passe',
    register_btn:   'Créer mon compte',
    have_account:   'Déjà un compte ?',
    login_link:     'Se connecter',
  },
  declaration: {
    type_loss:       'Perte',
    type_found:      'Trouvaille',
    status_waiting:  'En attente',
    status_valid:    'Validé',
    status_found:    'Retrouvé',
    status_returned: 'Restitué',
    status_rejected: 'Rejeté',
    status_closed:   'Clôturé',
  },
  common: {
    loading:   'Chargement...',
    error:     'Une erreur est survenue',
    save:      'Enregistrer',
    cancel:    'Annuler',
    confirm:   'Confirmer',
    close:     'Fermer',
    back:      'Retour',
    next:      'Suivant',
    submit:    'Soumettre',
    download:  'Télécharger',
    search:    'Rechercher',
    filter:    'Filtrer',
    all:       'Tous',
    date:      'Date',
    actions:   'Actions',
    no_result: 'Aucun résultat trouvé',
  },
  announce: 'Nouveau — Déclarez et retrouvez vos pièces en ligne | Service disponible 24h/24',
}

// ── Messages anglais ───────────────────────────────────────────────
const en = {
  nav: {
    home:     'Home',
    search:   'Search',
    declare:  'Declare',
    howto:    'How it works',
    login:    'Login',
    register: 'Register',
    logout:   'Logout',
    dashboard:'Dashboard',
    profile:  'My profile',
  },
  hero: {
    badge:    'Official Platform — Republic of Togo',
    title1:   'Find your',
    title2:   'lost documents',
    title3:   'online',
    subtitle: 'DéclaTogo centralizes loss and find declarations for official documents. Simple, fast, official.',
    cta_loss: 'Report a loss',
    cta_search:'Search my document',
  },
  search: {
    title:       'Quick search',
    subtitle:    'Check if your document has been reported as found',
    placeholder: 'Document number (e.g. TG20240001)',
    all_cat:     'All categories',
    btn:         'Search',
    frequent:    'Frequent searches',
  },
  stats: {
    declarations: 'Declarations registered',
    found:        'Documents recovered',
    citizens:     'Registered citizens',
    rate:         'Restitution rate',
  },
  steps: {
    label:  'Process',
    title:  'How does it work?',
    sub:    'Three simple steps to declare a loss or report a find anywhere in Togo.',
    s1_title:'Create your account',
    s1_text: 'Register for free with your phone number and email address.',
    s2_title:'Submit your declaration',
    s2_text: 'Fill in the form with information about your lost or found document.',
    s3_title:'Receive your receipt',
    s3_text: 'Download your official PDF receipt. Get notified if a match is found.',
  },
  features: {
    label:        'Features',
    title:        'A complete platform',
    sub:          'Built for Togolese realities, optimized for 3G/4G networks.',
    matching:     'Automatic matching',
    matching_txt: 'Our algorithm instantly matches loss and find declarations.',
    pdf:          'Official PDF receipt',
    pdf_txt:      'Generate an official document with a unique reference number.',
    notif:        'Real-time notifications',
    notif_txt:    'Get an alert when a find matches your loss declaration.',
    security:     'JWT Security',
    security_txt: 'Secure authentication. Your data is encrypted and protected.',
    mobile:       '100% Mobile',
    mobile_txt:   'Responsive interface. Works even on slow 3G connections.',
    admin:        'Admin dashboard',
    admin_txt:    'Officers manage and validate declarations from a centralized dashboard.',
  },
  categories: {
    label:    'Categories',
    title:    'Supported document types',
    identity: 'Identity document',
    vehicle:  'Vehicle',
    school:   'School documents',
    bank:     'Banking documents',
    pro:      'Professional documents',
    health:   'Health documents',
    other:    'Other documents',
    suggest:  'Suggest a category',
  },
  cta: {
    title:    'Ready to report your loss?',
    sub:      'Join Togolese citizens using DéclaTogo. Free registration, immediate receipt.',
    loss:     'Report a loss',
    found:    'Report a find',
  },
  footer: {
    desc:     'Official platform for administrative document loss declarations.',
    services: 'Services',
    info:     'Information',
    legal:    'Legal',
    rights:   '© 2025 DéclaTogo — Republic of Togo. All rights reserved.',
    made:     'Built for Togolese citizens',
  },
  auth: {
    login_title:    'Login',
    login_sub:      'Access your citizen space',
    username:       'Username',
    password:       'Password',
    remember:       'Remember me',
    forgot:         'Forgot password?',
    login_btn:      'Log in',
    no_account:     'No account yet?',
    register_link:  'Register',
    register_title: 'Create an account',
    register_sub:   'Join DéclaTogo for free',
    first_name:     'First name',
    last_name:      'Last name',
    email:          'Email address',
    phone:          'Phone number',
    pwd_confirm:    'Confirm password',
    register_btn:   'Create my account',
    have_account:   'Already have an account?',
    login_link:     'Log in',
  },
  declaration: {
    type_loss:       'Loss',
    type_found:      'Find',
    status_waiting:  'Pending',
    status_valid:    'Validated',
    status_found:    'Found',
    status_returned: 'Returned',
    status_rejected: 'Rejected',
    status_closed:   'Closed',
  },
  common: {
    loading:   'Loading...',
    error:     'An error occurred',
    save:      'Save',
    cancel:    'Cancel',
    confirm:   'Confirm',
    close:     'Close',
    back:      'Back',
    next:      'Next',
    submit:    'Submit',
    download:  'Download',
    search:    'Search',
    filter:    'Filter',
    all:       'All',
    date:      'Date',
    actions:   'Actions',
    no_result: 'No results found',
  },
  announce: 'New — Declare and find your documents online | Service available 24/7',
}

// ── Création de l'instance i18n ───────────────────────────────────
const i18n = createI18n({
  legacy: false,          // Utilise la Composition API
  locale: 'fr',           // Langue par défaut
  fallbackLocale: 'en',   // Langue de repli
  messages: { fr, en },
})

export default i18n
```

## File: frontend/src/main.js
```javascript
import { createApp }  from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios' // 1. On importe axios

import App          from './App.vue'
import router       from './router'
import i18n         from './i18n'
import './style.css' // 2. On garde précieusement ton CSS !

// 3. Configuration de l'URL de base pour Django
// Cela évitera l'erreur 404 car tous tes appels seront préfixés par /api/
axios.defaults.baseURL = 'http://localhost:8000/api/'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

app.mount('#app')
```

## File: frontend/src/router/index.js
```javascript
/**
 * Vue Router — DéclaTogo
 */

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // ── Pages publiques ─────────────────────────────────────────────
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: 'Accueil — DéclaTogo', public: true },
  },
  {
    path: '/rechercher',
    name: 'search',
    component: () => import('../views/SearchView.vue'),
    meta: { title: 'Rechercher une pièce — DéclaTogo', public: true },
  },

  // ── Authentification ─────────────────────────────────────────────
  {
    path: '/connexion',
    name: 'login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { title: 'Connexion — DéclaTogo', public: true, guestOnly: true },
  },
  {
    path: '/inscription',
    name: 'register',
    component: () => import('../views/auth/RegisterView.vue'),
    meta: { title: 'Inscription — DéclaTogo', public: true, guestOnly: true },
  },

  // ── Espace citoyen ───────────────────────────────────────────────
  {
    path: '/mes-declarations',
    name: 'mes-declarations',
    component: () => import('../views/citizen/MyDeclarationsView.vue'),
    meta: { title: 'Mes déclarations — DéclaTogo', requiresAuth: true },
  },
  {
    path: '/declarer',
    name: 'declare',
    component: () => import('../views/citizen/DeclareView.vue'),
    meta: { title: 'Déclarer — DéclaTogo', requiresAuth: true },
  },
  {
    path: '/declarations/:id',
    name: 'declaration-detail',
    component: () => import('../views/citizen/DeclarationDetailView.vue'),
    meta: { title: 'Détail — DéclaTogo', requiresAuth: true },
  },
  {
    path: '/profil',
    name: 'profile',
    component: () => import('../views/citizen/ProfileView.vue'),
    meta: { title: 'Mon profil — DéclaTogo', requiresAuth: true },
  },
  {
    path: '/notifications',
    name: 'notifications',
    component: () => import('../views/citizen/NotificationsView.vue'),
    meta: { title: 'Notifications — DéclaTogo', requiresAuth: true },
  },

  // ── Espace admin / police ────────────────────────────────────────
  {
    path: '/admin',
    name: 'dashboard',
    component: () => import('../views/admin/DashboardView.vue'),
    meta: { title: 'Tableau de bord — DéclaTogo', requiresAuth: true, requiresStaff: true },
  },
  {
    path: '/admin/declarations',
    name: 'admin-declarations',
    component: () => import('../views/admin/AdminDeclarationsView.vue'),
    meta: {
      title: 'Gestion déclarations — DéclaTogo',
      requiresAuth: true,
      requiresStaff: true,
    },
  },
  {
    path: '/admin/agents',
    name: 'admin-agents',
    component: () => import('../views/admin/ManageAgentsView.vue'),
    meta: {
      title: 'Gestion des agents — DéclaTogo',
      requiresAuth: true,
      requiresAdmin: true,
    },
  },

  // ── Gestion utilisateurs — ADMIN UNIQUEMENT ──────────────────────
  {
    path: '/admin/utilisateurs',
    name: 'admin-users',
    component: () => import('../views/admin/ManageUsersView.vue'),
    meta: {
      title: 'Gestion des utilisateurs — DéclaTogo',
      requiresAuth: true,
      requiresAdmin: true,
    },
  },

  // ── 404 ──────────────────────────────────────────────────────────
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue'),
    meta: { title: 'Page introuvable — DéclaTogo', public: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash)       return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
})

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || 'DéclaTogo'

  const { useAuthStore } = await import('../stores/auth')
  const authStore = useAuthStore()

  if (!authStore.user && authStore.accessToken) {
    await authStore.init()
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return next({ name: 'home' })
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  // Route réservée aux admins uniquement
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next({ name: 'dashboard' })
  }

  // Route réservée au staff (admin + police)
  if (to.meta.requiresStaff && !authStore.isStaff) {
    return next({ name: 'mes-declarations' })
  }

  next()
})

export default router
```

## File: frontend/src/services/api.js
```javascript
/**
 * Client HTTP Axios — DéclaTogo
 */

import axios from 'axios'
import router from '../router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
})

// ── Intercepteur REQUEST ──────────────────────────────────────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error)
)

// ── Intercepteur RESPONSE — refresh JWT ──────────────────────────
let isRefreshing = false
let failedQueue  = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((p) => (error ? p.reject(error) : p.resolve(token)))
  failedQueue = []
}

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const orig = error.config
    if (error.response?.status === 401 && !orig._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => failedQueue.push({ resolve, reject }))
          .then((token) => { orig.headers.Authorization = `Bearer ${token}`; return api(orig) })
          .catch((err) => Promise.reject(err))
      }
      orig._retry   = true
      isRefreshing  = true
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) { _logout(); return Promise.reject(error) }
      try {
        const base = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/'
        const { data } = await axios.post(`${base}token/refresh/`, { refresh })
        localStorage.setItem('access_token', data.access)
        processQueue(null, data.access)
        orig.headers.Authorization = `Bearer ${data.access}`
        return api(orig)
      } catch (e) {
        processQueue(e, null)
        _logout()
        return Promise.reject(e)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  }
)

function _logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push({ name: 'login' })
}

// ═════════════════════════════════════════════════════════════════
// Endpoints
// ═════════════════════════════════════════════════════════════════

export const authAPI = {
  login:         (d) => api.post('token/', d),
  refresh:       (d) => api.post('token/refresh/', d),
  register:      (d) => api.post('register/', d),
  profile:       ()  => api.get('profile/'),
  updateProfile: (d) => api.put('profile/', d),
}

export const declarationsAPI = {
  list:          (params)   => api.get('declarations/', { params }),
  detail:        (id)       => api.get(`declarations/${id}/`),
  create:        (data)     => api.post('declarations/', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  update:        (id, data) => api.patch(`declarations/${id}/`, data),
  /** Suppression définitive — admin uniquement */
  delete:        (id)       => api.delete(`declarations/${id}/`),
  myDeclarations:()         => api.get('declarations/mes_declarations/'),
  pertes:        ()         => api.get('declarations/pertes/'),
  trouvailles:   ()         => api.get('declarations/trouvailles/'),
  rechercher:    (data)     => api.post('declarations/rechercher/', data),
  changerStatut: (id, data) => api.patch(`declarations/${id}/changer_statut/`, data),
  downloadPDF:   (id)       => api.get(`declarations/${id}/telecharger_recepisse/`, {
    responseType: 'blob',
  }),
}

export const categoriesAPI = {
  list:   () => api.get('categories/'),
  detail: (id) => api.get(`categories/${id}/`),
}

export const notificationsAPI = {
  list:        ()   => api.get('notifications/'),
  nonLues:     ()   => api.get('notifications/non_lues/'),
  marquerLue:  (id) => api.post(`notifications/${id}/marquer_lue/`),
  toutMarquer: ()   => api.post('notifications/tout_marquer_lues/'),
}

export const statsAPI = {
  get: () => api.get('statistiques/'),
}

// ── Gestion agents (admin) ────────────────────────────────────────
export const agentsAPI = {
  list:   ()         => api.get('admin/agents/'),
  create: (data)     => api.post('admin/agents/', data),
  update: (id, data) => api.patch(`admin/agents/${id}/`, data),
  delete: (id)       => api.delete(`admin/agents/${id}/`),
}

// ── Gestion utilisateurs (admin) — NOUVEAU ───────────────────────
export const usersAPI = {
  /** Liste tous les utilisateurs (filtres : role, search) */
  list:   (params)   => api.get('admin/users/', { params }),
  /** Détail d'un utilisateur */
  detail: (id)       => api.get(`admin/users/${id}/`),
  /** Modifier (is_active, …) */
  update: (id, data) => api.patch(`admin/users/${id}/`, data),
  /** Suppression DÉFINITIVE */
  delete: (id)       => api.delete(`admin/users/${id}/`),
}

export default api
```

## File: frontend/src/stores/auth.js
```javascript
/**
 * Store Pinia — Authentification
 * Gère : login, logout, register, profil, état de connexion
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../services/api'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {

  // ── State ──────────────────────────────────────────────────────
  const user         = ref(null)
  const accessToken  = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const loading      = ref(false)
  const error        = ref(null)

  // ── Getters ────────────────────────────────────────────────────
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isAdmin  = computed(() => user.value?.role === 'admin')
  const isPolice = computed(() => user.value?.role === 'police')
  const isStaff  = computed(() => ['admin', 'police'].includes(user.value?.role))
  const userRole = computed(() => user.value?.role || 'citoyen')

  // ── Actions ────────────────────────────────────────────────────

  /** Connexion utilisateur */
  async function login(credentials) {
    loading.value = true
    error.value   = null

    try {
      const { data } = await authAPI.login(credentials)

      // Stocker les tokens
      accessToken.value  = data.access
      refreshToken.value = data.refresh
      localStorage.setItem('access_token',  data.access)
      localStorage.setItem('refresh_token', data.refresh)

      // Charger le profil
      await fetchProfile()

      // Redirection selon le rôle
      if (isStaff.value) {
        router.push({ name: 'dashboard' })
      } else {
        router.push({ name: 'mes-declarations' })
      }

      return { success: true }

    } catch (err) {
      error.value = _parseError(err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /** Inscription */
  async function register(userData) {
    loading.value = true
    error.value   = null

    try {
      await authAPI.register(userData)
      // Connexion automatique après inscription
      return await login({
        username: userData.username,
        password: userData.password,
      })
    } catch (err) {
      error.value = _parseError(err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /** Récupération du profil utilisateur */
  async function fetchProfile() {
    try {
      const { data } = await authAPI.profile()
      user.value = data
    } catch (err) {
      // Token invalide → déconnexion
      if (err.response?.status === 401) logout()
    }
  }

  /** Mise à jour du profil */
  async function updateProfile(profileData) {
    loading.value = true
    error.value   = null
    try {
      const { data } = await authAPI.updateProfile(profileData)
      user.value = data
      return { success: true }
    } catch (err) {
      error.value = _parseError(err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /** Déconnexion */
  function logout() {
    user.value         = null
    accessToken.value  = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push({ name: 'home' })
  }

  /** Initialisation au démarrage (si token présent en localStorage) */
  async function init() {
    if (accessToken.value) {
      await fetchProfile()
    }
  }

  // ── Helper privé ───────────────────────────────────────────────
  function _parseError(err) {
    if (!err.response) return 'Erreur réseau. Vérifiez votre connexion.'
    const data = err.response.data
    if (typeof data === 'string')  return data
    if (data?.detail)              return data.detail
    if (data?.non_field_errors)    return data.non_field_errors[0]
    // Erreurs de champs : retourner la première
    const firstField = Object.keys(data)[0]
    if (firstField) return `${firstField}: ${data[firstField][0]}`
    return 'Une erreur est survenue.'
  }

  return {
    // State
    user, accessToken, refreshToken, loading, error,
    // Getters
    isAuthenticated, isAdmin, isPolice, isStaff, userRole,
    // Actions
    login, register, logout, fetchProfile, updateProfile, init,
  }
})
```

## File: frontend/src/style.css
```css
/* ── 1. Directives Tailwind v3 (NE PAS TRADUIRE) ── */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ── 2. Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── 3. Variables CSS ── */
:root {
  --vert:     #005A3C;
  --vert-l:   #007A52;
  --vert-xl:  #E8F4F0;
  --rouge:    #C41230;
  --or:       #D4A017;
  --or-l:     #F5E6A8;
  --creme:    #FAF7F2;
  --texte:    #1A2E22;
  --ombre:    0 4px 24px rgba(0,90,60,.10);
  --ombre-lg: 0 12px 48px rgba(0,90,60,.16);
}

/* ── 4. Reset & Base ── */
* { box-sizing: border-box; }
body {
  font-family: 'DM Sans', system-ui, sans-serif;
  background: var(--creme);
  color: var(--texte);
  margin: 0;
}

/* ── 5. Composants ── */
@layer components {

  /* Navigation mobile */
  .nav-mobile-link {
    @apply block text-sm font-medium px-4 py-3 rounded-lg transition-all no-underline;
    color: rgba(255, 255, 255, 0.85);
  }
  .nav-mobile-link:hover {
    background-color: rgba(255, 255, 255, 0.10);
    color: #ffffff;
  }

  /* Bouton principal (vert → action primaire) */
  .btn-primary {
    @apply inline-flex items-center gap-2 bg-or text-vert font-bold
           px-6 py-3 rounded-[10px] border-none cursor-pointer
           transition-all hover:-translate-y-0.5 hover:shadow-lg;
    background-color: #D4A017;
    color: #005A3C;
  }
  .btn-primary:hover {
    background-color: #e8b220;
    box-shadow: 0 8px 24px rgba(212,160,23,.35);
  }

  /* Champ de formulaire standard */
  .form-input {
    @apply w-full border border-gray-200 rounded-[10px] px-4 py-3
           text-sm font-sans bg-white text-texte
           outline-none transition-all
           focus:border-vert focus:ring-2 focus:ring-vert/15
           placeholder:text-gray-400;
  }

  /* Carte (card) */
  .card {
    @apply bg-white rounded-[16px] p-8 shadow-card border border-gray-100;
  }

  /* Etiquette de champ */
  .form-label {
    @apply block text-xs font-semibold text-texte/70 mb-1.5 tracking-wide uppercase;
  }

  /* Message d'erreur inline */
  .form-error {
    @apply text-rouge text-xs mt-1 flex items-center gap-1;
  }

  /* Badge statut */
  .badge {
    @apply inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full;
  }
  .badge-waiting  { @apply bg-yellow-100 text-yellow-700; }
  .badge-valid    { @apply bg-blue-100 text-blue-700; }
  .badge-found    { @apply bg-green-100 text-green-700; }
  .badge-returned { @apply bg-emerald-100 text-emerald-800; }
  .badge-rejected { @apply bg-red-100 text-rouge; }
}

/* ── 6. Motif Kente (CSS pur) ── */
/* Inspiré du tissu kente togolais — damier géométrique doré */
.kente-bg {
  background-image:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 20px,
      rgba(212,160,23,.08) 20px,
      rgba(212,160,23,.08) 21px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 20px,
      rgba(212,160,23,.08) 20px,
      rgba(212,160,23,.08) 21px
    ),
    repeating-linear-gradient(
      45deg,
      rgba(255,255,255,.03) 0px,
      rgba(255,255,255,.03) 10px,
      transparent 10px,
      transparent 20px
    );
}

/* ── 7. Animations ── */
.fade-up { animation: fadeUp .5s ease both; }
.delay-200 { animation-delay: .2s; }
.delay-400 { animation-delay: .4s; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
.spin-slow { animation: spin-slow 20s linear infinite; }

/* Barre de chargement animée */
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 8px;
}

/* ── 8. Scrollbar personnalisée ── */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,90,60,.25); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,90,60,.45); }
```

## File: frontend/src/views/admin/AdminDeclarationsView.vue
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { declarationsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const router    = useRouter()
const authStore = useAuthStore()

/* ══ État ══ */
const declarations = ref([])
const loading      = ref(true)
const apiError     = ref(null)
const apiSuccess   = ref(null)
const search       = ref('')
const filterStatut = ref('')
const filterType   = ref('')

/* ══ Modale changement de statut ══ */
const statutModal    = ref(false)
const selectedDecl   = ref(null)
const nouveauStatut  = ref('')
const remarques      = ref('')
const changingStatut = ref(false)

/* ══ Modale suppression ══ */
const deleteModal  = ref(false)
const declToDelete = ref(null)
const deleting     = ref(false)

/* ══ Chargement ══ */
onMounted(loadDeclarations)

async function loadDeclarations() {
  loading.value  = true
  apiError.value = null
  try {
    const { data } = await declarationsAPI.list()
    // ✅ CORRECTION : L'API Django retourne un objet paginé avec 'results'
    declarations.value = data.results ?? data
    console.log('✅ Déclarations chargées:', declarations.value.length)
  } catch (e) {
    apiError.value = 'Impossible de charger les déclarations.'
    console.error('❌ Erreur chargement déclarations:', e)
  } finally {
    loading.value = false
  }
}

/* ══ Filtrage AMÉLIORÉ ══ */
const filtered = computed(() => {
  let list = declarations.value

  // Filtre par statut
  if (filterStatut.value) {
    list = list.filter(d => d.statut === filterStatut.value)
  }

  // Filtre par type
  if (filterType.value) {
    list = list.filter(d => d.type_declaration === filterType.value)
  }

  // Recherche textuelle améliorée
  const q = search.value.toLowerCase().trim()
  if (q) {
    list = list.filter(d => {
      // Normaliser pour la recherche (gérer les espaces multiples, etc.)
      const normalizeText = (text) => {
        return (text || '').toLowerCase().trim().replace(/\s+/g, ' ')
      }

      // Champs de recherche
      const numeroPiece   = normalizeText(d.numero_piece)
      const nomSurPiece   = normalizeText(d.nom_sur_piece)
      const numeroRecep   = normalizeText(d.numero_recepisse)
      const declarant     = normalizeText(d.declarant)
      const nomDeclarant  = normalizeText(d.nom_declarant)
      const prenomDecl    = normalizeText(d.prenom_declarant)
      const categorie     = normalizeText(d.categorie_nom)
      const lieuPerte     = normalizeText(d.lieu_perte)

      // Recherche dans tous les champs pertinents
      return numeroPiece.includes(q)   ||
             nomSurPiece.includes(q)   ||
             numeroRecep.includes(q)   ||
             declarant.includes(q)     ||
             nomDeclarant.includes(q)  ||
             prenomDecl.includes(q)    ||
             categorie.includes(q)     ||
             lieuPerte.includes(q)
    })
  }

  return list
})

/* ══ Changement de statut ══ */
function openStatut(decl) {
  selectedDecl.value  = decl
  nouveauStatut.value = decl.statut
  remarques.value     = ''
  statutModal.value   = true
}

async function handleChangerStatut() {
  if (!selectedDecl.value) return
  changingStatut.value = true
  apiError.value       = null
  try {
    const { data } = await declarationsAPI.changerStatut(selectedDecl.value.id, {
      statut: nouveauStatut.value,
      remarques: remarques.value,
    })
    const idx = declarations.value.findIndex(d => d.id === data.id)
    if (idx !== -1) {
      declarations.value[idx].statut        = data.statut
      declarations.value[idx].statut_display = data.statut_display
    }
    apiSuccess.value  = `✅ Statut mis à jour pour ${selectedDecl.value.numero_recepisse}`
    statutModal.value = false
    selectedDecl.value = null
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors du changement de statut.'
  } finally {
    changingStatut.value = false
  }
}

/* ══ Suppression ══ */
function askDelete(decl) {
  declToDelete.value = decl
  deleteModal.value  = true
}

async function confirmDelete() {
  if (!declToDelete.value) return
  deleting.value = true
  apiError.value = null
  try {
    await declarationsAPI.delete(declToDelete.value.id)
    declarations.value = declarations.value.filter(d => d.id !== declToDelete.value.id)
    apiSuccess.value = `✅ Déclaration « ${declToDelete.value.numero_recepisse} » supprimée.`
    deleteModal.value  = false
    declToDelete.value = null
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la suppression.'
  } finally {
    deleting.value = false
  }
}

/* ══ Helpers ══ */
const statusConfig = {
  EN_ATTENTE: { label: 'En attente', color: '#D97706', bg: '#FEF3C7' },
  VALIDE:     { label: 'Validé',     color: '#2563EB', bg: '#DBEAFE' },
  RETROUVE:   { label: 'Retrouvé',   color: '#059669', bg: '#D1FAE5' },
  RESTITUE:   { label: 'Restitué',   color: '#065F46', bg: '#A7F3D0' },
  REJETE:     { label: 'Rejeté',     color: '#DC2626', bg: '#FEE2E2' },
  CLOTURE:    { label: 'Clôturé',    color: '#6B7280', bg: '#F3F4F6' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const statutOptions = Object.entries(statusConfig).map(([v, c]) => ({ value: v, label: c.label }))
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-6xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Gestion des déclarations
      </h1>
      <p class="text-sm text-gray-500">
        Validez, changez le statut ou supprimez des déclarations.
      </p>
    </div>
    <router-link :to="{ name: 'dashboard' }"
      class="inline-flex items-center gap-2 text-sm font-medium text-gray-500
             bg-white border border-gray-200 px-4 py-2.5 rounded-xl no-underline
             hover:bg-gray-50 transition-all self-start">
      ← Tableau de bord
    </router-link>
  </div>

  <!-- ══ Feedback ══ -->
  <transition name="slide-msg">
    <div v-if="apiSuccess"
      class="flex items-center gap-3 bg-green-50 border border-green-200
             rounded-xl p-4 mb-5 text-sm text-green-700">
      {{ apiSuccess }}
      <button @click="apiSuccess = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-green-400">✕</button>
    </div>
  </transition>
  <transition name="slide-msg">
    <div v-if="apiError && !statutModal && !deleteModal"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      ⚠️ {{ apiError }}
      <button @click="apiError = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
    </div>
  </transition>

  <!-- ══ Filtres AMÉLIORÉS ══ -->
  <div class="flex flex-wrap gap-3 mb-5">
    <!-- Recherche avec placeholder détaillé -->
    <div class="relative flex-1 min-w-[280px]">
      <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input v-model="search" type="text"
        placeholder="Rechercher par N° pièce, nom, récépissé, déclarant, catégorie, lieu…"
        class="form-input pl-10 text-sm w-full" />
      <!-- Compteur de résultats -->
      <div v-if="search" class="absolute right-3 top-1/2 -translate-y-1/2">
        <span class="text-xs bg-[#E8F4F0] text-[#005A3C] px-2 py-1 rounded-full font-semibold">
          {{ filtered.length }}
        </span>
      </div>
    </div>
    
    <!-- Filtre type -->
    <select v-model="filterType" class="form-input text-sm w-auto min-w-[140px]">
      <option value="">Tous les types</option>
      <option value="PERTE">😟 Pertes</option>
      <option value="TROUVAILLE">🤲 Trouvailles</option>
    </select>
    
    <!-- Filtre statut -->
    <select v-model="filterStatut" class="form-input text-sm w-auto min-w-[160px]">
      <option value="">Tous les statuts</option>
      <option v-for="s in statutOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
    </select>
    
    <!-- Bouton réinitialiser filtres -->
    <button v-if="search || filterType || filterStatut"
      @click="search = ''; filterType = ''; filterStatut = ''"
      class="text-xs text-gray-400 hover:text-rouge px-3 py-2 rounded-lg
             bg-white border border-gray-200 cursor-pointer transition-all hover:border-rouge/30">
      ✕ Réinitialiser
    </button>
  </div>

  <!-- Compteur résultats détaillé -->
  <div class="flex items-center justify-between mb-3">
    <p class="text-xs text-gray-500">
      <span class="font-bold text-[#005A3C]">{{ filtered.length }}</span> déclaration(s) affichée(s)
      <span v-if="filtered.length !== declarations.length" class="text-gray-400">
        sur {{ declarations.length }} au total
      </span>
    </p>
    
    <!-- Info recherche active -->
    <div v-if="search" class="text-xs text-gray-400 flex items-center gap-2">
      <span>🔍 Recherche active :</span>
      <span class="font-mono bg-gray-100 px-2 py-0.5 rounded text-[#005A3C]">{{ search }}</span>
    </div>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 6" :key="i" class="skeleton h-24 rounded-2xl"></div>
  </div>

  <!-- ══ Vide ══ -->
  <div v-else-if="filtered.length === 0 && declarations.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-4xl mb-3">📋</div>
    <p class="font-serif text-base font-bold text-[#1A2E22] mb-1">Aucune déclaration</p>
    <p class="text-sm text-gray-400">La base de données est vide.</p>
  </div>
  
  <!-- Filtre vide -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-12 bg-white rounded-2xl border border-dashed border-gray-200">
    <div class="text-3xl mb-3">🔍</div>
    <p class="text-sm text-gray-500 mb-1">Aucune déclaration ne correspond aux critères</p>
    <p class="text-xs text-gray-400 mb-4">
      Essayez de modifier vos filtres ou votre recherche
    </p>
    <button @click="search = ''; filterType = ''; filterStatut = ''"
      class="text-xs text-[#005A3C] font-semibold bg-[#E8F4F0] px-4 py-2 rounded-lg
             border-none cursor-pointer hover:bg-[#d0ece3] transition-all">
      Réinitialiser les filtres
    </button>
  </div>

  <!-- ══ Liste ══ -->
  <div v-else class="space-y-2">
    <transition-group name="list-item">
      <div v-for="decl in filtered" :key="decl.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-card transition-all">

        <div class="p-4 flex items-start gap-4 flex-wrap">

          <!-- Icône type -->
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
            :style="{
              backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0'
            }">
            {{ decl.type_declaration === 'PERTE' ? '😟' : '🤲' }}
          </div>

          <!-- Infos déclaration -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-1">
              <span class="font-mono text-sm font-bold text-[#005A3C]">
                {{ decl.numero_recepisse }}
              </span>
              <span class="badge text-[10px] font-bold"
                :style="{ color: getStatus(decl.statut).color, backgroundColor: getStatus(decl.statut).bg }">
                {{ getStatus(decl.statut).label }}
              </span>
              <span class="badge text-[10px] font-semibold"
                :style="{
                  backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0',
                  color: decl.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
                }">
                {{ decl.type_display || decl.type_declaration }}
              </span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-x-4 gap-y-0.5 text-xs text-gray-500">
              <span>📄 {{ decl.numero_piece || '—' }}</span>
              <span>👤 {{ decl.nom_sur_piece || '—' }}</span>
              <span>👥 {{ decl.declarant || '—' }}</span>
              <span>📅 {{ formatDate(decl.date_declaration) }}</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <!-- Voir le détail -->
            <button @click="router.push({ name: 'declaration-detail', params: { id: decl.id } })"
              class="text-xs font-semibold text-[#005A3C] bg-[#E8F4F0] hover:bg-[#c8e8dc]
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              👁️ Voir
            </button>
            <!-- Changer statut -->
            <button @click="openStatut(decl)"
              class="text-xs font-semibold text-[#2563EB] bg-blue-50 hover:bg-blue-100
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              ✏️ Statut
            </button>
            <!-- Supprimer — admin uniquement -->
            <button v-if="authStore.isAdmin"
              @click="askDelete(decl)"
              class="text-xs font-semibold text-rouge bg-red-50 hover:bg-red-100
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              🗑️ Supprimer
            </button>
          </div>
        </div>

        <div class="h-0.5 rounded-b-2xl"
          :style="{ backgroundColor: getStatus(decl.statut).color, opacity: 0.25 }">
        </div>

      </div>
    </transition-group>
  </div>

</div>

<!-- ════════════════════════════════════════════
     MODALE — Changer statut
════════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="statutModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background:rgba(0,0,0,.45)"
    @click.self="statutModal = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
      <h2 class="font-serif text-lg font-bold text-[#1A2E22] mb-1">Changer le statut</h2>
      <p class="text-xs text-gray-400 mb-5">
        Déclaration : <strong class="font-mono">{{ selectedDecl?.numero_recepisse }}</strong>
      </p>

      <div v-if="apiError"
        class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-4">
        ⚠️ {{ apiError }}
      </div>

      <div class="space-y-4">
        <div>
          <label class="form-label">Nouveau statut <span class="text-rouge">*</span></label>
          <select v-model="nouveauStatut" class="form-input text-sm">
            <option v-for="s in statutOptions" :key="s.value" :value="s.value">
              {{ s.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="form-label">Remarques <span class="text-gray-400 font-normal">(optionnel)</span></label>
          <textarea v-model="remarques" rows="3" placeholder="Informations complémentaires…"
            class="form-input text-sm resize-none"></textarea>
        </div>
      </div>

      <div class="flex gap-3 mt-5">
        <button @click="statutModal = false; apiError = null"
          class="flex-1 py-2.5 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-all">
          Annuler
        </button>
        <button @click="handleChangerStatut" :disabled="changingStatut"
          class="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl
                 bg-[#005A3C] text-white font-bold text-sm border-none cursor-pointer
                 hover:bg-[#007A52] transition-all disabled:opacity-50">
          <span v-if="changingStatut" class="loader"></span>
          {{ changingStatut ? 'Sauvegarde…' : '✅ Enregistrer' }}
        </button>
      </div>
    </div>
  </div>
</transition>

<!-- ════════════════════════════════════════════
     MODALE — Confirmation suppression
════════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="deleteModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background:rgba(0,0,0,.5)"
    @click.self="deleteModal = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 text-center">
      <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center
                  text-3xl mx-auto mb-4">
        🗑️
      </div>
      <h3 class="font-serif text-lg font-bold text-[#1A2E22] mb-2">
        Supprimer cette déclaration ?
      </h3>

      <!-- Récap -->
      <div v-if="declToDelete"
        class="flex items-center gap-3 bg-gray-50 rounded-xl p-3 mb-3 text-left">
        <div class="w-9 h-9 rounded-xl flex items-center justify-center text-lg"
          :style="{ backgroundColor: declToDelete.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0' }">
          {{ declToDelete.type_declaration === 'PERTE' ? '😟' : '🤲' }}
        </div>
        <div>
          <p class="font-mono text-sm font-bold text-[#005A3C]">
            {{ declToDelete.numero_recepisse }}
          </p>
          <p class="text-xs text-gray-400">{{ declToDelete.nom_sur_piece }}</p>
        </div>
      </div>

      <div class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-5 text-left">
        ⚠️ <strong>Action irréversible.</strong> La déclaration et ses notifications
        associées seront définitivement supprimées.
      </div>

      <div v-if="apiError"
        class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-4">
        {{ apiError }}
      </div>

      <div class="flex gap-3">
        <button @click="deleteModal = false; apiError = null"
          class="flex-1 py-3 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-all">
          Annuler
        </button>
        <button @click="confirmDelete" :disabled="deleting"
          class="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl
                 bg-rouge text-white font-bold text-sm border-none cursor-pointer
                 hover:bg-[#e8192f] transition-all disabled:opacity-50">
          <span v-if="deleting" class="loader"></span>
          <span v-else>🗑️</span>
          {{ deleting ? 'Suppression…' : 'Supprimer' }}
        </button>
      </div>
    </div>
  </div>
</transition>

</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .2s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(6px); }
.list-item-leave-active { transition: all .2s ease; position: absolute; width: 100%; }
.list-item-leave-to     { opacity: 0; transform: translateX(20px); }

.modal-enter-active, .modal-leave-active { transition: opacity .2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active > div, .modal-leave-active > div { transition: transform .2s ease; }
.modal-enter-from > div, .modal-leave-to > div { transform: scale(.95); }

.slide-msg-enter-active, .slide-msg-leave-active { transition: all .25s ease; }
.slide-msg-enter-from, .slide-msg-leave-to { opacity: 0; transform: translateY(-5px); }

.loader {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

## File: frontend/src/views/admin/DashboardView.vue
```vue
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { statsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { Chart, registerables } from 'chart.js'

const router    = useRouter()
const authStore = useAuthStore()
Chart.register(...registerables)

const stats   = ref(null)
const loading = ref(true)
const error   = ref(null)

onMounted(async () => {
  try {
    const { data } = await statsAPI.get()
    stats.value = data
    await renderCharts()
  } catch (e) {
    error.value = 'Impossible de charger les statistiques.'
  } finally {
    loading.value = false
  }
})

const chartLoaded = ref(false)

const renderCharts = async () => {
  if (typeof window === 'undefined') return
  try {
    chartLoaded.value = true
    await new Promise(r => setTimeout(r, 100))
    const s = stats.value
    if (!s) return

    const donutCtx = document.getElementById('donutChart')
    if (donutCtx) {
      new Chart(donutCtx, {
        type: 'doughnut',
        data: {
          labels: ['Pertes', 'Trouvailles'],
          datasets: [{
            data: [s.total_pertes, s.total_trouvailles],
            backgroundColor: ['#C41230', '#005A3C'],
            borderWidth: 0, hoverOffset: 6,
          }]
        },
        options: {
          responsive: true, cutout: '72%',
          plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 10, padding: 14, font: { size: 11 } } }
          }
        }
      })
    }

    const barCtx = document.getElementById('barChart')
    if (barCtx) {
      new Chart(barCtx, {
        type: 'bar',
        data: {
          labels: ['En attente', 'Validées', 'Retrouvées', 'Restituées'],
          datasets: [{
            data: [s.en_attente, s.validees, s.retrouvees, s.restituees],
            backgroundColor: ['#FEF3C7', '#DBEAFE', '#D1FAE5', '#A7F3D0'],
            borderColor:     ['#D97706',  '#2563EB', '#059669', '#065F46'],
            borderWidth: 2, borderRadius: 8,
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, grid: { color: '#f3f4f6' }, ticks: { stepSize: 1 } },
            x: { grid: { display: false } }
          }
        }
      })
    }
  } catch (e) { console.warn('Chart.js:', e) }
}

const statusConfig = {
  EN_ATTENTE: { label: 'En attente', color: '#D97706', bg: '#FEF3C7' },
  VALIDE:     { label: 'Validé',     color: '#2563EB', bg: '#DBEAFE' },
  RETROUVE:   { label: 'Retrouvé',   color: '#059669', bg: '#D1FAE5' },
  RESTITUE:   { label: 'Restitué',   color: '#065F46', bg: '#A7F3D0' },
  REJETE:     { label: 'Rejeté',     color: '#DC2626', bg: '#FEE2E2' },
  CLOTURE:    { label: 'Clôturé',    color: '#6B7280', bg: '#F3F4F6' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE
const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const taux = computed(() => {
  if (!stats.value?.total_declarations) return 0
  return Math.round(
    ((stats.value.retrouvees + stats.value.restituees) / stats.value.total_declarations) * 100
  )
})

const kpiCards = computed(() => {
  if (!stats.value) return []
  const s = stats.value
  return [
    { label: 'Total déclarations', value: s.total_declarations, icon: '📋', color: '#005A3C', bg: '#E8F4F0', sub: `${s.total_pertes} pertes · ${s.total_trouvailles} trouvailles` },
    { label: 'En attente',         value: s.en_attente,         icon: '⏳', color: '#D97706', bg: '#FEF3C7', sub: 'À valider' },
    { label: 'Retrouvées',         value: s.retrouvees,         icon: '🎉', color: '#059669', bg: '#D1FAE5', sub: `Taux : ${taux.value}%` },
    { label: 'Utilisateurs',       value: s.total_utilisateurs || '—', icon: '👥', color: '#2563EB', bg: '#DBEAFE', sub: `${s.total_citoyens || 0} citoyens · ${s.total_agents || 0} agents` },
  ]
})
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-5xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-8 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full mb-3"
        :style="{
          backgroundColor: authStore.isAdmin ? '#FEE2E2' : '#DBEAFE',
          color: authStore.isAdmin ? '#C41230' : '#2563EB'
        }">
        {{ authStore.isAdmin ? '🛡️ Administrateur' : '👮 Agent de Police' }}
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">Tableau de bord</h1>
      <p class="text-sm text-gray-500">Vue d'ensemble de la plateforme DéclaTogo.</p>
    </div>

    <!-- Actions rapides ─────────────────────────── -->
    <div class="flex items-center gap-2 flex-wrap">
      <router-link v-if="authStore.isAdmin"
        :to="{ name: 'admin-users' }"
        class="inline-flex items-center gap-2 text-sm font-bold px-4 py-3 rounded-xl
               no-underline transition-all hover:-translate-y-0.5 shadow"
        style="background-color:#2563EB; color:white;">
        👥 Utilisateurs
      </router-link>
      <router-link v-if="authStore.isAdmin"
        :to="{ name: 'admin-agents' }"
        class="inline-flex items-center gap-2 text-sm font-bold px-4 py-3 rounded-xl
               no-underline transition-all hover:-translate-y-0.5 shadow"
        style="background-color:#C41230; color:white;">
        👮 Agents
      </router-link>
      <router-link :to="{ name: 'admin-declarations' }"
        class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
               text-sm px-4 py-3 rounded-xl no-underline hover:bg-[#007A52]
               hover:-translate-y-0.5 transition-all shadow">
        📋 Déclarations
      </router-link>
    </div>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-if="error"
    class="flex items-center gap-3 bg-red-50 border border-red-200
           rounded-xl p-4 mb-6 text-sm text-rouge">
    ⚠️ {{ error }}
  </div>

  <!-- ══ KPI Cards ══ -->
  <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
    <div v-if="loading" v-for="i in 4" :key="i" class="skeleton h-28 rounded-2xl"></div>
    <template v-else>
      <div v-for="card in kpiCards" :key="card.label"
        class="bg-white rounded-2xl shadow-card border border-gray-100 p-5
               hover:-translate-y-0.5 hover:shadow-card-lg transition-all">
        <div class="flex items-start justify-between mb-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
            :style="{ backgroundColor: card.bg }">{{ card.icon }}</div>
          <div class="font-serif text-3xl font-bold" :style="{ color: card.color }">
            {{ card.value }}
          </div>
        </div>
        <div class="text-xs font-semibold text-[#1A2E22]">{{ card.label }}</div>
        <div class="text-xs text-gray-400 mt-0.5">{{ card.sub }}</div>
      </div>
    </template>
  </div>

  <!-- ══ Accès rapides admin ══ -->
  <div v-if="authStore.isAdmin" class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">

    <!-- Gestion utilisateurs -->
    <div class="bg-gradient-to-r from-[#2563EB] to-[#1e40af] rounded-2xl p-5
                flex items-center justify-between gap-4 shadow-lg">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
          👥
        </div>
        <div>
          <p class="font-serif text-sm font-bold text-white">Gérer les utilisateurs</p>
          <p class="text-xs text-white/70">Supprimer citoyens, agents et admins.</p>
        </div>
      </div>
      <router-link :to="{ name: 'admin-users' }"
        class="inline-flex items-center gap-1 bg-white text-[#2563EB] font-bold
               text-xs px-4 py-2 rounded-xl no-underline flex-shrink-0
               hover:-translate-y-0.5 transition-all shadow">
        Gérer →
      </router-link>
    </div>

    <!-- Gestion agents -->
    <div class="bg-gradient-to-r from-[#C41230] to-[#8B0D22] rounded-2xl p-5
                flex items-center justify-between gap-4 shadow-lg">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
          👮
        </div>
        <div>
          <p class="font-serif text-sm font-bold text-white">Gérer les agents</p>
          <p class="text-xs text-white/70">Créer et désactiver des comptes agents.</p>
        </div>
      </div>
      <router-link :to="{ name: 'admin-agents' }"
        class="inline-flex items-center gap-1 bg-white text-[#C41230] font-bold
               text-xs px-4 py-2 rounded-xl no-underline flex-shrink-0
               hover:-translate-y-0.5 transition-all shadow">
        Gérer →
      </router-link>
    </div>
  </div>

  <!-- ══ Graphiques ══ -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4">Répartition par type</h2>
      <div v-if="loading" class="skeleton h-40 rounded-xl"></div>
      <canvas v-else id="donutChart" height="180"></canvas>
    </div>
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 lg:col-span-2">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4">Répartition par statut</h2>
      <div v-if="loading" class="skeleton h-40 rounded-xl"></div>
      <canvas v-else id="barChart" height="140"></canvas>
    </div>
  </div>

  <!-- ══ Catégories + Déclarations récentes ══ -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <h2 class="font-serif text-sm font-bold text-[#1A2E22] mb-4">Catégories actives</h2>
      <div v-if="loading" class="space-y-2">
        <div v-for="i in 5" :key="i" class="skeleton h-8 rounded-lg"></div>
      </div>
      <div v-else-if="stats?.categories_populaires?.length" class="space-y-2">
        <div v-for="(cat, i) in stats.categories_populaires" :key="cat.libelle"
          class="flex items-center gap-2">
          <span class="text-xs font-bold text-[#005A3C] w-4">{{ i + 1 }}</span>
          <div class="flex-1 min-w-0">
            <div class="text-xs font-medium text-[#1A2E22] truncate">{{ cat.libelle }}</div>
            <div class="h-1 bg-gray-100 rounded-full mt-1">
              <div class="h-full bg-[#005A3C] rounded-full"
                :style="{ width: `${Math.min(100, (cat.nombre / (stats.total_declarations || 1)) * 100)}%` }">
              </div>
            </div>
          </div>
          <span class="text-xs font-bold text-gray-500">{{ cat.nombre }}</span>
        </div>
      </div>
      <p v-else class="text-xs text-gray-400">Aucune donnée.</p>
    </div>

    <div class="lg:col-span-2 bg-white rounded-2xl shadow-card border border-gray-100 p-5">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-serif text-sm font-bold text-[#1A2E22]">Déclarations récentes</h2>
        <router-link :to="{ name: 'admin-declarations' }"
          class="text-xs text-[#005A3C] font-semibold no-underline hover:underline">
          Voir tout →
        </router-link>
      </div>
      <div v-if="loading" class="space-y-3">
        <div v-for="i in 4" :key="i" class="skeleton h-14 rounded-xl"></div>
      </div>
      <div v-else-if="stats?.declarations_recentes?.length" class="space-y-2">
        <div v-for="decl in stats.declarations_recentes.slice(0, 6)" :key="decl.id"
          @click="router.push({ name: 'declaration-detail', params: { id: decl.id } })"
          class="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition-all cursor-pointer">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0"
            :style="{ backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0' }">
            {{ decl.type_declaration === 'PERTE' ? '😟' : '🤲' }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between gap-2">
              <span class="font-mono text-xs font-bold text-[#005A3C] truncate">
                {{ decl.numero_piece }}
              </span>
              <span class="badge text-[10px] flex-shrink-0"
                :style="{ color: getStatus(decl.statut).color, backgroundColor: getStatus(decl.statut).bg }">
                {{ getStatus(decl.statut).label }}
              </span>
            </div>
            <div class="flex gap-2 text-[10px] text-gray-400 mt-0.5">
              <span>{{ decl.nom_sur_piece }}</span>
              <span>·</span>
              <span>{{ formatDate(decl.date_declaration) }}</span>
            </div>
          </div>
        </div>
      </div>
      <p v-else class="text-xs text-gray-400 py-4 text-center">Aucune déclaration récente.</p>
    </div>
  </div>

</div>
</div>
</template>
```

## File: frontend/src/views/admin/ManageAgentsView.vue
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { agentsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router    = useRouter()

/* ══ État ══ */
const agents     = ref([])
const loading    = ref(true)
const apiError   = ref(null)
const apiSuccess = ref(null)
const search     = ref('')

/* ══ Modal création ══ */
const showCreate  = ref(false)
const submitting  = ref(false)
const form = ref({
  username:         '',
  first_name:       '',
  last_name:        '',
  email:            '',
  telephone:        '',
  role:             'police',
  password:         '',
  password_confirm: '',
})
const formErrors  = ref({})
const showPwd     = ref(false)
const showPwdConf = ref(false)

/* ══ Modal désactivation ══ */
const confirmModal = ref(false)
const agentToDeactivate = ref(null)
const deactivating = ref(false)

/* ══ Chargement ══ */
onMounted(loadAgents)

async function loadAgents() {
  loading.value   = true
  apiError.value  = null
  try {
    const { data } = await agentsAPI.list()
    agents.value   = data
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Impossible de charger les agents.'
  } finally {
    loading.value = false
  }
}

/* ══ Filtrage ══ */
const filtered = computed(() => {
  const q = search.value.toLowerCase().trim()
  if (!q) return agents.value
  return agents.value.filter(a =>
    a.username.toLowerCase().includes(q)       ||
    (a.first_name || '').toLowerCase().includes(q) ||
    (a.last_name  || '').toLowerCase().includes(q) ||
    (a.email      || '').toLowerCase().includes(q)
  )
})

/* ══ Validation formulaire ══ */
function validateForm() {
  const e = {}
  if (!form.value.username.trim())   e.username   = "Nom d'utilisateur requis"
  if (form.value.username.trim().length < 3) e.username = 'Minimum 3 caractères'
  if (!/^[a-zA-Z0-9@.+\-_]+$/.test(form.value.username))
    e.username = 'Caractères invalides'
  if (!form.value.first_name.trim()) e.first_name = 'Prénom requis'
  if (!form.value.last_name.trim())  e.last_name  = 'Nom requis'
  if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email))
    e.email = 'Email invalide'
  if (form.value.telephone && !/^(\+228)?[0-9]{8}$/.test(form.value.telephone.replace(/\s/g, '')))
    e.telephone = "Format : +22890123456 ou 90123456"
  if (form.value.password.length < 8)      e.password = 'Minimum 8 caractères'
  if (!/[A-Z]/.test(form.value.password))  e.password = 'Au moins une majuscule'
  if (!/[0-9]/.test(form.value.password))  e.password = 'Au moins un chiffre'
  if (form.value.password !== form.value.password_confirm)
    e.password_confirm = 'Les mots de passe ne correspondent pas'
  formErrors.value = e
  return Object.keys(e).length === 0
}

/* ══ Créer un agent ══ */
async function handleCreate() {
  if (!validateForm()) return
  submitting.value = true
  apiError.value   = null
  try {
    const { data } = await agentsAPI.create(form.value)
    agents.value.unshift(data.agent)
    apiSuccess.value = `✅ Agent "${data.agent.username}" créé avec succès.`
    resetForm()
    showCreate.value = false
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    const d = e.response?.data
    if (typeof d === 'object') {
      // Erreurs de champs → afficher dans le formulaire
      formErrors.value = d
      apiError.value = 'Veuillez corriger les erreurs ci-dessous.'
    } else {
      apiError.value = d || 'Erreur lors de la création.'
    }
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.value = {
    username: '', first_name: '', last_name: '',
    email: '', telephone: '', role: 'police',
    password: '', password_confirm: '',
  }
  formErrors.value = {}
  showPwd.value = false
  showPwdConf.value = false
}

/* ══ Désactiver un agent ══ */
function askDeactivate(agent) {
  agentToDeactivate.value = agent
  confirmModal.value = true
}

async function confirmDeactivate() {
  if (!agentToDeactivate.value) return
  deactivating.value = true
  apiError.value     = null
  try {
    await agentsAPI.delete(agentToDeactivate.value.id)
    // Marquer comme inactif dans la liste locale
    const idx = agents.value.findIndex(a => a.id === agentToDeactivate.value.id)
    if (idx !== -1) agents.value[idx].is_active = false
    apiSuccess.value = `Le compte de "${agentToDeactivate.value.username}" a été désactivé.`
    confirmModal.value = false
    agentToDeactivate.value = null
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la désactivation.'
  } finally {
    deactivating.value = false
  }
}

/* ══ Réactiver un agent ══ */
async function reactivate(agent) {
  apiError.value = null
  try {
    await agentsAPI.update(agent.id, { is_active: true })
    const idx = agents.value.findIndex(a => a.id === agent.id)
    if (idx !== -1) agents.value[idx].is_active = true
    apiSuccess.value = `Le compte de "${agent.username}" a été réactivé.`
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la réactivation.'
  }
}

/* ══ Helpers ══ */
const roleConfig = {
  admin:  { label: 'Administrateur', icon: '🛡️', color: '#C41230', bg: '#FEE2E2' },
  police: { label: 'Agent de police', icon: '👮', color: '#2563EB', bg: '#DBEAFE' },
}
const getRole = (r) => roleConfig[r] || roleConfig.police

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const initiales = (a) => {
  if (a.first_name && a.last_name)
    return (a.first_name[0] + a.last_name[0]).toUpperCase()
  return a.username[0].toUpperCase()
}
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-4xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-red-50 text-[#C41230]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        🛡️ Réservé aux administrateurs
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Gestion des agents
      </h1>
      <p class="text-sm text-gray-500">
        Créez et gérez les comptes des agents de police et des administrateurs.
      </p>
    </div>
    <div class="flex items-center gap-2">
      <router-link :to="{ name: 'dashboard' }"
        class="inline-flex items-center gap-2 text-sm font-medium text-gray-500
               bg-white border border-gray-200 px-4 py-2.5 rounded-xl no-underline
               hover:bg-gray-50 transition-all">
        ← Tableau de bord
      </router-link>
      <button @click="showCreate = true"
        class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
               text-sm px-5 py-2.5 rounded-xl border-none cursor-pointer
               hover:bg-[#007A52] hover:-translate-y-0.5 transition-all shadow-md">
        + Créer un agent
      </button>
    </div>
  </div>

  <!-- ══ Feedback global ══ -->
  <transition name="slide-msg">
    <div v-if="apiSuccess"
      class="flex items-center gap-3 bg-green-50 border border-green-200
             rounded-xl p-4 mb-5 text-sm text-green-700">
      <span>{{ apiSuccess }}</span>
      <button @click="apiSuccess = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-green-400">✕</button>
    </div>
  </transition>
  <transition name="slide-msg">
    <div v-if="apiError && !showCreate"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      <span>⚠️ {{ apiError }}</span>
      <button @click="apiError = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
    </div>
  </transition>

  <!-- ══ Barre de recherche + stats ══ -->
  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3 mb-5">
    <div class="relative flex-1">
      <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input v-model="search" type="text"
        placeholder="Rechercher un agent par nom, prénom, username…"
        class="form-input pl-10 text-sm w-full"/>
    </div>
    <div class="flex items-center gap-3 text-xs text-gray-500 bg-white px-4 py-2.5
                rounded-xl border border-gray-200 shadow-sm flex-shrink-0">
      <span>👮 <strong class="text-[#2563EB]">{{ agents.filter(a => a.role === 'police').length }}</strong> agents</span>
      <span class="text-gray-300">·</span>
      <span>🛡️ <strong class="text-[#C41230]">{{ agents.filter(a => a.role === 'admin').length }}</strong> admins</span>
      <span class="text-gray-300">·</span>
      <span>✅ <strong class="text-[#005A3C]">{{ agents.filter(a => a.is_active).length }}</strong> actifs</span>
    </div>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 4" :key="i" class="skeleton h-20 rounded-2xl"></div>
  </div>

  <!-- ══ Liste vide ══ -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-4xl mb-3">👤</div>
    <p class="font-serif text-base font-bold text-[#1A2E22] mb-2">Aucun agent trouvé</p>
    <p class="text-sm text-gray-500 mb-4">
      {{ search ? 'Aucun résultat pour cette recherche.' : 'Créez le premier agent.' }}
    </p>
    <button v-if="!search" @click="showCreate = true"
      class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
             text-sm px-5 py-2.5 rounded-xl border-none cursor-pointer
             hover:bg-[#007A52] transition-all">
      + Créer un agent
    </button>
  </div>

  <!-- ══ Liste des agents ══ -->
  <div v-else class="space-y-3">
    <transition-group name="list-item">
      <div v-for="agent in filtered" :key="agent.id"
        :class="[
          'bg-white rounded-2xl border shadow-card transition-all',
          !agent.is_active && 'opacity-60'
        ]"
        :style="{ borderColor: agent.is_active ? '#e5e7eb' : '#fca5a5' }">

        <div class="p-5 flex items-center gap-4 flex-wrap">

          <!-- Avatar initiales -->
          <div class="w-11 h-11 rounded-full flex items-center justify-center
                      font-serif font-bold text-white text-sm flex-shrink-0 shadow"
            :style="{
              background: agent.role === 'admin'
                ? 'linear-gradient(135deg,#C41230,#8B0D22)'
                : 'linear-gradient(135deg,#2563EB,#1e40af)'
            }">
            {{ initiales(agent) }}
          </div>

          <!-- Infos principales -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-0.5">
              <span class="font-semibold text-sm text-[#1A2E22]">
                {{ agent.first_name }} {{ agent.last_name }}
              </span>
              <span class="text-xs text-gray-400">@{{ agent.username }}</span>
              <!-- Badge rôle -->
              <span class="badge text-[10px] font-bold"
                :style="{
                  color: getRole(agent.role).color,
                  backgroundColor: getRole(agent.role).bg
                }">
                {{ getRole(agent.role).icon }} {{ getRole(agent.role).label }}
              </span>
              <!-- Badge inactif -->
              <span v-if="!agent.is_active"
                class="badge text-[10px] bg-red-100 text-rouge font-bold">
                ⛔ Désactivé
              </span>
            </div>
            <div class="flex items-center gap-3 text-xs text-gray-400 flex-wrap">
              <span v-if="agent.email">✉️ {{ agent.email }}</span>
              <span v-if="agent.telephone">📞 {{ agent.telephone }}</span>
              <span>📅 Créé le {{ formatDate(agent.date_creation) }}</span>
              <span>📋 {{ agent.nombre_declarations || 0 }} déclaration(s)</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <!-- Empêcher de se modifier soi-même -->
            <template v-if="agent.id !== authStore.user?.id">
              <button v-if="agent.is_active"
                @click="askDeactivate(agent)"
                class="text-xs font-semibold text-rouge bg-red-50 hover:bg-red-100
                       px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
                ⛔ Désactiver
              </button>
              <button v-else
                @click="reactivate(agent)"
                class="text-xs font-semibold text-green-700 bg-green-50 hover:bg-green-100
                       px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
                ✅ Réactiver
              </button>
            </template>
            <!-- Compte courant — non modifiable -->
            <span v-else
              class="text-xs text-gray-400 bg-gray-100 px-3 py-2 rounded-lg">
              Votre compte
            </span>
          </div>

        </div>

        <!-- Barre colorée -->
        <div class="h-0.5 rounded-b-2xl"
          :style="{
            backgroundColor: agent.is_active ? getRole(agent.role).color : '#fca5a5',
            opacity: 0.35
          }">
        </div>

      </div>
    </transition-group>
  </div>

</div>

<!-- ═══════════════════════════════════════════
     MODAL — Créer un agent
═══════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="showCreate"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto"
    style="background:rgba(0,0,0,.45)"
    @click.self="showCreate = false; resetForm(); apiError = null">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg my-4 relative">

      <!-- En-tête modal -->
      <div class="flex items-center justify-between p-6 border-b border-gray-100">
        <div>
          <h2 class="font-serif text-xl font-bold text-[#1A2E22]">Créer un agent</h2>
          <p class="text-xs text-gray-500 mt-0.5">
            Le compte sera immédiatement actif. Communiquez le mot de passe à l'agent.
          </p>
        </div>
        <button @click="showCreate = false; resetForm(); apiError = null"
          class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center
                 text-gray-500 border-none cursor-pointer hover:bg-gray-200 transition-all">
          ✕
        </button>
      </div>

      <div class="p-6 space-y-4">

        <!-- Erreur globale -->
        <div v-if="apiError"
          class="flex items-center gap-2 bg-red-50 border border-red-200
                 rounded-xl p-3 text-sm text-rouge">
          <span>⚠️</span><span>{{ apiError }}</span>
        </div>

        <!-- Choix du rôle -->
        <div>
          <label class="form-label">Rôle <span class="text-rouge">*</span></label>
          <div class="grid grid-cols-2 gap-3">
            <button type="button"
              @click="form.role = 'police'"
              :class="[
                'flex items-center gap-3 p-3.5 rounded-xl border-2 text-left transition-all cursor-pointer',
                form.role === 'police'
                  ? 'border-[#2563EB] bg-blue-50'
                  : 'border-gray-200 bg-white hover:border-blue-200'
              ]">
              <span class="text-2xl">👮</span>
              <div>
                <div class="font-semibold text-sm text-[#1A2E22]">Agent de police</div>
                <div class="text-xs text-gray-500">Valide les déclarations</div>
              </div>
            </button>
            <button type="button"
              @click="form.role = 'admin'"
              :class="[
                'flex items-center gap-3 p-3.5 rounded-xl border-2 text-left transition-all cursor-pointer',
                form.role === 'admin'
                  ? 'border-[#C41230] bg-red-50'
                  : 'border-gray-200 bg-white hover:border-red-200'
              ]">
              <span class="text-2xl">🛡️</span>
              <div>
                <div class="font-semibold text-sm text-[#1A2E22]">Administrateur</div>
                <div class="text-xs text-gray-500">Accès complet</div>
              </div>
            </button>
          </div>
        </div>

        <!-- Prénom + Nom -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="form-label">Prénom <span class="text-rouge">*</span></label>
            <input v-model="form.first_name" type="text" placeholder="Jean"
              :class="['form-input', formErrors.first_name && 'border-rouge ring-2 ring-rouge/15']"/>
            <p v-if="formErrors.first_name" class="form-error text-xs mt-1">
              ✕ {{ formErrors.first_name }}
            </p>
          </div>
          <div>
            <label class="form-label">Nom <span class="text-rouge">*</span></label>
            <input v-model="form.last_name" type="text" placeholder="KOFFI"
              :class="['form-input', formErrors.last_name && 'border-rouge ring-2 ring-rouge/15']"/>
            <p v-if="formErrors.last_name" class="form-error text-xs mt-1">
              ✕ {{ formErrors.last_name }}
            </p>
          </div>
        </div>

        <!-- Username -->
        <div>
          <label class="form-label">
            Nom d'utilisateur <span class="text-rouge">*</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">@</span>
            <input v-model="form.username" type="text" placeholder="agent_koffi"
              :class="['form-input pl-8', formErrors.username && 'border-rouge ring-2 ring-rouge/15']"/>
          </div>
          <p v-if="formErrors.username" class="form-error text-xs mt-1">
            ✕ {{ formErrors.username }}
          </p>
        </div>

        <!-- Email + Téléphone -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="form-label">
              Email <span class="text-gray-400 normal-case font-normal">(opt.)</span>
            </label>
            <input v-model="form.email" type="email" placeholder="agent@police.tg"
              :class="['form-input', formErrors.email && 'border-rouge ring-2 ring-rouge/15']"/>
            <p v-if="formErrors.email" class="form-error text-xs mt-1">✕ {{ formErrors.email }}</p>
          </div>
          <div>
            <label class="form-label">
              Téléphone <span class="text-gray-400 normal-case font-normal">(opt.)</span>
            </label>
            <input v-model="form.telephone" type="tel" placeholder="+22890000000"
              :class="['form-input', formErrors.telephone && 'border-rouge ring-2 ring-rouge/15']"/>
            <p v-if="formErrors.telephone" class="form-error text-xs mt-1">✕ {{ formErrors.telephone }}</p>
          </div>
        </div>

        <!-- Mot de passe -->
        <div>
          <label class="form-label">
            Mot de passe initial <span class="text-rouge">*</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔒</span>
            <input v-model="form.password"
              :type="showPwd ? 'text' : 'password'"
              placeholder="Min. 8 car., 1 majuscule, 1 chiffre"
              :class="['form-input pl-10 pr-12', formErrors.password && 'border-rouge ring-2 ring-rouge/15']"/>
            <button type="button" @click="showPwd = !showPwd"
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                     bg-transparent border-none cursor-pointer hover:text-gray-600">
              {{ showPwd ? '🙈' : '👁️' }}
            </button>
          </div>
          <p v-if="formErrors.password" class="form-error text-xs mt-1">✕ {{ formErrors.password }}</p>
        </div>

        <!-- Confirmation mot de passe -->
        <div>
          <label class="form-label">
            Confirmer le mot de passe <span class="text-rouge">*</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔑</span>
            <input v-model="form.password_confirm"
              :type="showPwdConf ? 'text' : 'password'"
              placeholder="Répétez le mot de passe"
              :class="['form-input pl-10 pr-12', formErrors.password_confirm && 'border-rouge ring-2 ring-rouge/15']"/>
            <button type="button" @click="showPwdConf = !showPwdConf"
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                     bg-transparent border-none cursor-pointer hover:text-gray-600">
              {{ showPwdConf ? '🙈' : '👁️' }}
            </button>
          </div>
          <p v-if="formErrors.password_confirm" class="form-error text-xs mt-1">
            ✕ {{ formErrors.password_confirm }}
          </p>
          <p v-else-if="form.password && form.password === form.password_confirm"
            class="text-xs text-green-600 mt-1">✓ Les mots de passe correspondent</p>
        </div>

        <!-- Note sécurité -->
        <div class="bg-yellow-50 border border-yellow-200 rounded-xl p-3 text-xs text-yellow-700">
          ⚠️ <strong>Important :</strong> Communiquez ce mot de passe à l'agent de manière sécurisée.
          Il pourra le modifier depuis son profil.
        </div>

      </div>

      <!-- Pied de modal -->
      <div class="flex gap-3 p-6 border-t border-gray-100">
        <button type="button"
          @click="showCreate = false; resetForm(); apiError = null"
          class="flex-1 py-3 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 transition-all cursor-pointer">
          Annuler
        </button>
        <button type="button"
          @click="handleCreate"
          :disabled="submitting"
          class="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl
                 text-white font-bold text-sm border-none cursor-pointer
                 transition-all hover:shadow-md
                 disabled:opacity-50 disabled:cursor-not-allowed"
          :style="{
            backgroundColor: form.role === 'admin' ? '#C41230' : '#005A3C'
          }">
          <span v-if="submitting" class="loader-dot"></span>
          <span v-else>{{ form.role === 'admin' ? '🛡️' : '👮' }}</span>
          {{ submitting ? 'Création…' : 'Créer l\'agent' }}
        </button>
      </div>

    </div>
  </div>
</transition>

<!-- ═══════════════════════════════════════════
     MODAL — Confirmation désactivation
═══════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="confirmModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background:rgba(0,0,0,.45)"
    @click.self="confirmModal = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 text-center">
      <div class="text-4xl mb-3">⚠️</div>
      <h3 class="font-serif text-lg font-bold text-[#1A2E22] mb-2">
        Désactiver cet agent ?
      </h3>
      <p class="text-sm text-gray-500 mb-1">
        Le compte de
        <strong>{{ agentToDeactivate?.first_name }} {{ agentToDeactivate?.last_name }}</strong>
        sera désactivé.
      </p>
      <p class="text-xs text-gray-400 mb-6">
        L'agent ne pourra plus se connecter. Vous pourrez le réactiver ultérieurement.
      </p>
      <div class="flex gap-3">
        <button @click="confirmModal = false"
          class="flex-1 py-2.5 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-all">
          Annuler
        </button>
        <button @click="confirmDeactivate"
          :disabled="deactivating"
          class="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl
                 bg-rouge text-white font-bold text-sm border-none cursor-pointer
                 transition-all hover:bg-[#e8192f] disabled:opacity-50">
          <span v-if="deactivating" class="loader-dot"></span>
          <span v-else>⛔</span>
          {{ deactivating ? 'En cours…' : 'Désactiver' }}
        </button>
      </div>
    </div>

  </div>
</transition>

</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .25s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(8px); }

.modal-enter-active, .modal-leave-active { transition: all .2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active > div, .modal-leave-active > div { transition: all .2s ease; }
.modal-enter-from > div, .modal-leave-to > div { transform: scale(.95); }

.slide-msg-enter-active, .slide-msg-leave-active { transition: all .25s ease; }
.slide-msg-enter-from, .slide-msg-leave-to { opacity: 0; transform: translateY(-6px); }

.loader-dot {
  display: inline-block; width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.form-error { @apply text-rouge text-xs flex items-center gap-1; }
</style>
```

## File: frontend/src/views/admin/ManageUsersView.vue
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { usersAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()

/* ══ État principal ══ */
const users      = ref([])
const loading    = ref(true)
const apiError   = ref(null)
const apiSuccess = ref(null)

/* ══ Filtres ══ */
const filterRole = ref('')        // '' | 'citoyen' | 'police' | 'admin'
const search     = ref('')

/* ══ Modale confirmation suppression ══ */
const confirmModal  = ref(false)
const userToDelete  = ref(null)
const deleting      = ref(false)

/* ══ Chargement ══ */
onMounted(loadUsers)

async function loadUsers() {
  loading.value  = true
  apiError.value = null
  try {
    const { data } = await usersAPI.list()
    users.value = data
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Impossible de charger les utilisateurs.'
  } finally {
    loading.value = false
  }
}

/* ══ Filtrage côté client ══ */
const filtered = computed(() => {
  let list = users.value

  if (filterRole.value) {
    list = list.filter(u => u.role === filterRole.value)
  }

  const q = search.value.toLowerCase().trim()
  if (q) {
    list = list.filter(u =>
      u.username.toLowerCase().includes(q)          ||
      (u.first_name || '').toLowerCase().includes(q) ||
      (u.last_name  || '').toLowerCase().includes(q) ||
      (u.email      || '').toLowerCase().includes(q)
    )
  }
  return list
})

/* ══ Stats rapides ══ */
const stats = computed(() => ({
  total:    users.value.length,
  citoyens: users.value.filter(u => u.role === 'citoyen').length,
  police:   users.value.filter(u => u.role === 'police').length,
  admins:   users.value.filter(u => u.role === 'admin').length,
  actifs:   users.value.filter(u => u.is_active).length,
}))

/* ══ Suppression ══ */
function askDelete(user) {
  userToDelete.value = user
  confirmModal.value = true
}

async function confirmDelete() {
  if (!userToDelete.value) return
  deleting.value = true
  apiError.value = null
  try {
    await usersAPI.delete(userToDelete.value.id)
    users.value    = users.value.filter(u => u.id !== userToDelete.value.id)
    apiSuccess.value = `✅ L'utilisateur « ${userToDelete.value.username} » a été supprimé.`
    confirmModal.value  = false
    userToDelete.value  = null
    setTimeout(() => { apiSuccess.value = null }, 4000)
  } catch (e) {
    apiError.value = e.response?.data?.error || 'Erreur lors de la suppression.'
  } finally {
    deleting.value = false
  }
}

/* ══ Helpers ══ */
const roleConfig = {
  citoyen: { label: 'Citoyen',       icon: '👤', color: '#059669', bg: '#D1FAE5' },
  police:  { label: 'Agent police',  icon: '👮', color: '#2563EB', bg: '#DBEAFE' },
  admin:   { label: 'Administrateur',icon: '🛡️', color: '#C41230', bg: '#FEE2E2' },
}
const getRole = (r) => roleConfig[r] || roleConfig.citoyen

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const initiales = (u) =>
  u.first_name && u.last_name
    ? (u.first_name[0] + u.last_name[0]).toUpperCase()
    : u.username[0].toUpperCase()

const avatarBg = (role) =>
  role === 'admin'   ? 'linear-gradient(135deg,#C41230,#8B0D22)' :
  role === 'police'  ? 'linear-gradient(135deg,#2563EB,#1e40af)' :
                       'linear-gradient(135deg,#059669,#065F46)'

const tabRoles = [
  { value: '',        label: 'Tous',    emoji: '👥' },
  { value: 'citoyen', label: 'Citoyens',emoji: '👤' },
  { value: 'police',  label: 'Agents',  emoji: '👮' },
  { value: 'admin',   label: 'Admins',  emoji: '🛡️' },
]
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-5xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-red-50 text-[#C41230]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        🛡️ Réservé aux administrateurs
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Gestion des utilisateurs
      </h1>
      <p class="text-sm text-gray-500">
        Consultez et supprimez les comptes citoyens, agents et administrateurs.
      </p>
    </div>
    <router-link :to="{ name: 'dashboard' }"
      class="inline-flex items-center gap-2 text-sm font-medium text-gray-500
             bg-white border border-gray-200 px-4 py-2.5 rounded-xl no-underline
             hover:bg-gray-50 transition-all self-start">
      ← Tableau de bord
    </router-link>
  </div>

  <!-- ══ Feedback ══ -->
  <transition name="slide-msg">
    <div v-if="apiSuccess"
      class="flex items-center gap-3 bg-green-50 border border-green-200
             rounded-xl p-4 mb-5 text-sm text-green-700">
      {{ apiSuccess }}
      <button @click="apiSuccess = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-green-400">✕</button>
    </div>
  </transition>
  <transition name="slide-msg">
    <div v-if="apiError && !confirmModal"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      ⚠️ {{ apiError }}
      <button @click="apiError = null"
        class="ml-auto bg-transparent border-none cursor-pointer text-red-300">✕</button>
    </div>
  </transition>

  <!-- ══ Compteurs ══ -->
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
    <div v-for="c in [
        { label:'Total',    val: stats.total,    icon:'👥', color:'#005A3C', bg:'#E8F4F0' },
        { label:'Citoyens', val: stats.citoyens, icon:'👤', color:'#059669', bg:'#D1FAE5' },
        { label:'Agents',   val: stats.police,   icon:'👮', color:'#2563EB', bg:'#DBEAFE' },
        { label:'Admins',   val: stats.admins,   icon:'🛡️', color:'#C41230', bg:'#FEE2E2' },
      ]" :key="c.label"
      class="bg-white rounded-2xl border border-gray-100 shadow-card p-4 flex items-center gap-3">
      <div class="w-9 h-9 rounded-xl flex items-center justify-center text-lg"
        :style="{ backgroundColor: c.bg }">{{ c.icon }}</div>
      <div>
        <div class="font-serif text-xl font-bold" :style="{ color: c.color }">{{ c.val }}</div>
        <div class="text-xs text-gray-400">{{ c.label }}</div>
      </div>
    </div>
  </div>

  <!-- ══ Filtres ══ -->
  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3 mb-5">
    <!-- Tabs rôle -->
    <div class="flex items-center gap-1 bg-white border border-gray-200 rounded-xl p-1 shadow-sm">
      <button v-for="tab in tabRoles" :key="tab.value"
        @click="filterRole = tab.value"
        :class="[
          'px-3 py-1.5 rounded-lg text-xs font-semibold transition-all border-none cursor-pointer',
          filterRole === tab.value
            ? 'bg-[#005A3C] text-white shadow'
            : 'text-gray-500 hover:bg-gray-50 bg-transparent'
        ]">
        {{ tab.emoji }} {{ tab.label }}
      </button>
    </div>
    <!-- Recherche -->
    <div class="relative flex-1">
      <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
      <input v-model="search" type="text"
        placeholder="Rechercher par nom, username, email…"
        class="form-input pl-10 text-sm w-full" />
    </div>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 6" :key="i" class="skeleton h-20 rounded-2xl"></div>
  </div>

  <!-- ══ Vide ══ -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-4xl mb-3">🔍</div>
    <p class="font-serif text-base font-bold text-[#1A2E22] mb-1">Aucun résultat</p>
    <p class="text-sm text-gray-400">Modifiez vos filtres ou votre recherche.</p>
  </div>

  <!-- ══ Liste ══ -->
  <div v-else class="space-y-2">
    <transition-group name="list-item">
      <div v-for="user in filtered" :key="user.id"
        :class="[
          'bg-white rounded-2xl border shadow-card transition-all',
          !user.is_active ? 'opacity-60 border-red-200' : 'border-gray-100'
        ]">
        <div class="p-4 flex items-center gap-4 flex-wrap">

          <!-- Avatar -->
          <div class="w-10 h-10 rounded-full flex items-center justify-center
                      font-serif font-bold text-white text-sm flex-shrink-0 shadow"
            :style="{ background: avatarBg(user.role) }">
            {{ initiales(user) }}
          </div>

          <!-- Infos -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-0.5">
              <span class="font-semibold text-sm text-[#1A2E22]">
                {{ user.first_name }} {{ user.last_name }}
              </span>
              <span class="text-xs text-gray-400">@{{ user.username }}</span>
              <span class="badge text-[10px] font-bold"
                :style="{ color: getRole(user.role).color, backgroundColor: getRole(user.role).bg }">
                {{ getRole(user.role).icon }} {{ getRole(user.role).label }}
              </span>
              <span v-if="!user.is_active"
                class="badge text-[10px] bg-red-100 text-rouge font-bold">
                ⛔ Désactivé
              </span>
              <!-- Badge "Vous" -->
              <span v-if="user.id === authStore.user?.id"
                class="badge text-[10px] bg-yellow-100 text-yellow-700 font-bold">
                ⭐ Vous
              </span>
            </div>
            <div class="flex items-center gap-3 text-[10px] text-gray-400 flex-wrap">
              <span v-if="user.email">✉️ {{ user.email }}</span>
              <span v-if="user.telephone">📞 {{ user.telephone }}</span>
              <span>📅 {{ formatDate(user.date_creation) }}</span>
              <span>📋 {{ user.nombre_declarations || 0 }} décl.</span>
            </div>
          </div>

          <!-- Action suppression -->
          <div class="flex-shrink-0">
            <button
              v-if="user.id !== authStore.user?.id"
              @click="askDelete(user)"
              class="inline-flex items-center gap-1.5 text-xs font-semibold
                     text-rouge bg-red-50 hover:bg-red-100 px-3 py-2 rounded-lg
                     border-none cursor-pointer transition-all">
              🗑️ Supprimer
            </button>
            <span v-else class="text-xs text-gray-300 bg-gray-50 px-3 py-2 rounded-lg">
              Votre compte
            </span>
          </div>

        </div>

        <!-- Barre colorée bas -->
        <div class="h-0.5 rounded-b-2xl"
          :style="{ backgroundColor: getRole(user.role).color, opacity: 0.25 }">
        </div>

      </div>
    </transition-group>
  </div>

</div>

<!-- ════════════════════════════════════════════
     MODALE — Confirmation suppression
════════════════════════════════════════════ -->
<transition name="modal">
  <div v-if="confirmModal"
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    style="background:rgba(0,0,0,.5)"
    @click.self="confirmModal = false">

    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 text-center">

      <!-- Icône danger -->
      <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center
                  text-3xl mx-auto mb-4">
        🗑️
      </div>

      <h3 class="font-serif text-lg font-bold text-[#1A2E22] mb-2">
        Supprimer cet utilisateur ?
      </h3>

      <!-- Carte récap utilisateur -->
      <div v-if="userToDelete"
        class="flex items-center gap-3 bg-gray-50 rounded-xl p-3 mb-3 text-left">
        <div class="w-9 h-9 rounded-full flex items-center justify-center
                    font-bold text-white text-sm flex-shrink-0"
          :style="{ background: avatarBg(userToDelete.role) }">
          {{ initiales(userToDelete) }}
        </div>
        <div class="min-w-0">
          <p class="font-semibold text-sm text-[#1A2E22] truncate">
            {{ userToDelete.first_name }} {{ userToDelete.last_name }}
          </p>
          <p class="text-xs text-gray-400">@{{ userToDelete.username }} ·
            {{ getRole(userToDelete.role).label }}
          </p>
        </div>
      </div>

      <div class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-5 text-left">
        ⚠️ <strong>Action irréversible.</strong> Toutes les déclarations et notifications
        associées à ce compte seront également supprimées.
      </div>

      <!-- Erreur inline -->
      <div v-if="apiError"
        class="bg-red-50 border border-red-200 rounded-xl p-3 text-xs text-rouge mb-4">
        {{ apiError }}
      </div>

      <div class="flex gap-3">
        <button @click="confirmModal = false; apiError = null"
          class="flex-1 py-3 rounded-xl border border-gray-200 text-sm font-medium
                 text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-all">
          Annuler
        </button>
        <button @click="confirmDelete" :disabled="deleting"
          class="flex-1 flex items-center justify-center gap-2 py-3 rounded-xl
                 bg-rouge text-white font-bold text-sm border-none cursor-pointer
                 transition-all hover:bg-[#e8192f] disabled:opacity-50">
          <span v-if="deleting" class="loader"></span>
          <span v-else>🗑️</span>
          {{ deleting ? 'Suppression…' : 'Supprimer' }}
        </button>
      </div>
    </div>
  </div>
</transition>

</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .2s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(6px); }
.list-item-leave-active { transition: all .2s ease; position: absolute; width: 100%; }
.list-item-leave-to     { opacity: 0; transform: translateX(20px); }

.modal-enter-active, .modal-leave-active { transition: all .2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active > div, .modal-leave-active > div { transition: transform .2s ease; }
.modal-enter-from > div, .modal-leave-to > div { transform: scale(.95); }

.slide-msg-enter-active, .slide-msg-leave-active { transition: all .25s ease; }
.slide-msg-enter-from, .slide-msg-leave-to { opacity: 0; transform: translateY(-5px); }

.loader {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

## File: frontend/src/views/auth/LoginView.vue
```vue
<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../../stores/auth'
import { useRoute } from 'vue-router'

const { t } = useI18n()
const authStore = useAuthStore()
const route = useRoute()

/* ── État du formulaire ── */
const form = ref({
  username: '',
  password: '',
  remember: false,
})
const showPassword  = ref(false)
const submitted     = ref(false)

/* ── Validation locale ── */
const errors = computed(() => {
  if (!submitted.value) return {}
  const e = {}
  if (!form.value.username.trim())      e.username = 'Nom d\'utilisateur requis'
  if (form.value.password.length < 3)   e.password = 'Mot de passe requis'
  return e
})
const isValid = computed(() => Object.keys(errors.value).length === 0)

/* ── Soumission ── */
async function handleLogin() {
  submitted.value = true
  if (!isValid.value) return

  await authStore.login({
    username: form.value.username.trim(),
    password: form.value.password,
  })
  // La redirection est gérée par le store
}

/* ── Bulles déco animées ── */
const bubbles = [
  { size: 120, top: '10%',  left: '15%', delay: '0s',   dur: '7s'  },
  { size: 60,  top: '65%',  left: '70%', delay: '1.2s', dur: '9s'  },
  { size: 90,  top: '40%',  left: '5%',  delay: '2.5s', dur: '11s' },
  { size: 45,  top: '80%',  left: '30%', delay: '0.7s', dur: '8s'  },
  { size: 75,  top: '20%',  left: '80%', delay: '3s',   dur: '10s' },
]
</script>

<template>
  <div class="min-h-screen flex overflow-hidden" style="background:#FAF7F2">

    <!-- ══════════════════════════════════════════
         PANNEAU GAUCHE — Identité de marque
    ══════════════════════════════════════════ -->
    <aside class="hidden lg:flex lg:w-[46%] flex-col relative overflow-hidden"
           style="background-color:#005A3C">

      <!-- Motif kente + gradient -->
      <div class="absolute inset-0 kente-bg opacity-40"></div>
      <div class="absolute inset-0 bg-gradient-to-br from-[#003d29] via-transparent to-[#001a0e]/70"></div>

      <!-- Bulles décoratives flottantes -->
      <div v-for="(b, i) in bubbles" :key="i"
        class="absolute rounded-full border border-white/10 bg-white/5"
        :style="{
          width: b.size + 'px', height: b.size + 'px',
          top: b.top, left: b.left,
          animation: `floatBubble ${b.dur} ${b.delay} ease-in-out infinite alternate`
        }">
      </div>

      <!-- Bande verticale drapeau togolais -->
      <div class="absolute left-0 inset-y-0 w-1.5 flex flex-col">
        <div class="flex-[2] bg-[#005A3C]"></div>
        <div class="flex-1 bg-[#FFCE00]"></div>
        <div class="flex-[2] bg-[#C41230]"></div>
      </div>

      <div class="relative z-10 flex flex-col h-full px-12 py-14">

        <!-- Logo -->
        <div class="flex items-center gap-3 mb-auto">
          <div class="w-11 h-11 bg-[#D4A017] rounded-xl flex items-center justify-center
                      font-serif font-bold text-[#005A3C] text-sm shadow-lg">DT</div>
          <span class="font-serif text-2xl font-bold text-white tracking-tight">
            Décla<span class="text-[#D4A017]">Togo</span>
          </span>
        </div>

        <!-- Contenu central -->
        <div class="my-auto">
          <!-- Décoratif : cercle étoile -->
          <div class="w-20 h-20 rounded-full border-2 border-[#D4A017]/40 flex items-center
                      justify-center mb-8 relative">
            <div class="w-12 h-12 bg-[#D4A017]/20 rounded-full flex items-center justify-center">
              <span class="text-2xl">🔐</span>
            </div>
            <div class="absolute inset-0 rounded-full border border-[#D4A017]/20 spin-slow"></div>
          </div>

          <h2 class="font-serif text-[2.8rem] font-bold text-white leading-[1.1] mb-5">
            Votre espace<br/>
            <span class="text-[#D4A017]">citoyen</span><br/>
            vous attend.
          </h2>
          <p class="text-white/70 text-sm leading-relaxed max-w-[320px]">
            Déclarez, suivez et retrouvez vos pièces administratives
            depuis n'importe où au Togo.
          </p>

          <!-- Trois avantages -->
          <div class="mt-9 space-y-3.5">
            <div v-for="item in [
              { icon:'🛡️', text:'Données chiffrées & sécurisées' },
              { icon:'📄', text:'Récépissé PDF officiel instantané' },
              { icon:'🔔', text:'Alertes en cas de correspondance' },
            ]" :key="item.text"
              class="flex items-center gap-3">
              <span class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-sm flex-shrink-0">
                {{ item.icon }}
              </span>
              <span class="text-sm text-white/80">{{ item.text }}</span>
            </div>
          </div>
        </div>

        <!-- Pied de panneau -->
        <p class="text-xs text-white/35 mt-auto">
          © 2025 DéclaTogo — République Togolaise
        </p>
      </div>
    </aside>


    <!-- ══════════════════════════════════════════
         PANNEAU DROIT — Formulaire de connexion
    ══════════════════════════════════════════ -->
    <main class="flex-1 flex flex-col items-center justify-center px-6 py-12 relative">

      <!-- Fond décoratif subtil -->
      <div class="absolute inset-0 pointer-events-none"
           style="background:radial-gradient(ellipse 60% 50% at 80% 20%, rgba(0,90,60,.04) 0%, transparent 70%)">
      </div>

      <!-- Logo mobile uniquement -->
      <div class="lg:hidden flex items-center gap-2 mb-8">
        <div class="w-9 h-9 bg-[#005A3C] rounded-lg flex items-center justify-center
                    font-serif font-bold text-[#D4A017] text-sm">DT</div>
        <span class="font-serif text-xl font-bold text-[#1A2E22]">
          Décla<span class="text-[#005A3C]">Togo</span>
        </span>
      </div>

      <div class="w-full max-w-[420px] fade-up relative z-10">

        <!-- En-tête -->
        <div class="mb-8">
          <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                      text-xs font-bold px-3 py-1.5 rounded-full mb-4">
            🇹🇬 Plateforme officielle
          </div>
          <h1 class="font-serif text-[2rem] font-bold text-[#1A2E22] leading-tight mb-1.5">
            {{ t('auth.login_title') }}
          </h1>
          <p class="text-sm text-gray-500">{{ t('auth.login_sub') }}</p>
        </div>

        <!-- Erreur API globale -->
        <transition name="slide-error">
          <div v-if="authStore.error"
            class="flex items-start gap-3 bg-red-50 border border-red-200
                   rounded-xl p-4 mb-6 text-sm text-rouge">
            <span class="text-lg leading-none mt-0.5">⚠️</span>
            <span>{{ authStore.error }}</span>
          </div>
        </transition>

        <!-- Formulaire -->
        <form @submit.prevent="handleLogin" novalidate class="space-y-5">

          <!-- Nom d'utilisateur -->
          <div>
            <label class="form-label">{{ t('auth.username') }}</label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">👤</span>
              <input
                v-model="form.username"
                type="text"
                autocomplete="username"
                :placeholder="t('auth.username')"
                :class="['form-input pl-10', errors.username && 'border-rouge ring-2 ring-rouge/15']"
              />
            </div>
            <p v-if="errors.username" class="form-error">
              <span>✕</span> {{ errors.username }}
            </p>
          </div>

          <!-- Mot de passe -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="form-label mb-0">{{ t('auth.password') }}</label>
              <a href="#" class="text-xs text-[#005A3C] hover:underline">{{ t('auth.forgot') }}</a>
            </div>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔒</span>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                :placeholder="t('auth.password')"
                :class="['form-input pl-10 pr-12', errors.password && 'border-rouge ring-2 ring-rouge/15']"
              />
              <button type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                       hover:text-gray-600 transition-colors text-base bg-transparent border-none cursor-pointer">
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>
            <p v-if="errors.password" class="form-error">
              <span>✕</span> {{ errors.password }}
            </p>
          </div>

          <!-- Se souvenir de moi -->
          <div class="flex items-center gap-2.5">
            <button type="button"
              @click="form.remember = !form.remember"
              :class="[
                'w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0',
                'transition-all cursor-pointer border-none',
                form.remember ? 'bg-[#005A3C]' : 'bg-white border border-gray-300'
              ]"
              style="border: 2px solid; border-color: v-bind('form.remember ? \'#005A3C\' : \'#d1d5db\'')">
              <span v-if="form.remember" class="text-white text-xs leading-none">✓</span>
            </button>
            <span class="text-sm text-gray-500 cursor-pointer select-none"
              @click="form.remember = !form.remember">
              {{ t('auth.remember') }}
            </span>
          </div>

          <!-- Bouton connexion -->
          <button type="submit"
            :disabled="authStore.loading"
            class="w-full flex items-center justify-center gap-2.5
                   bg-[#005A3C] text-white font-bold py-3.5 px-6 rounded-[10px]
                   border-none cursor-pointer text-sm transition-all
                   hover:bg-[#007A52] hover:-translate-y-0.5 hover:shadow-lg
                   disabled:opacity-60 disabled:cursor-not-allowed disabled:translate-y-0"
            :style="{ boxShadow: authStore.loading ? 'none' : '0 4px 16px rgba(0,90,60,.30)' }">
            <span v-if="authStore.loading" class="loader-dot"></span>
            <span v-else>🚀</span>
            <span>{{ authStore.loading ? 'Connexion en cours...' : t('auth.login_btn') }}</span>
          </button>

        </form>

        <!-- Séparateur -->
        <div class="flex items-center gap-3 my-6">
          <span class="flex-1 h-px bg-gray-200"></span>
          <span class="text-xs text-gray-400 font-medium">ou</span>
          <span class="flex-1 h-px bg-gray-200"></span>
        </div>

        <!-- Lien inscription -->
        <p class="text-center text-sm text-gray-500">
          {{ t('auth.no_account') }}
          <router-link :to="{ name: 'register' }"
            class="text-[#005A3C] font-semibold hover:underline ml-1">
            {{ t('auth.register_link') }} →
          </router-link>
        </p>

        <!-- Retour accueil -->
        <div class="mt-6 text-center">
          <router-link :to="{ name: 'home' }"
            class="inline-flex items-center gap-1.5 text-xs text-gray-400
                   hover:text-[#005A3C] transition-colors no-underline">
            ← Retour à l'accueil
          </router-link>
        </div>

      </div>
    </main>

  </div>
</template>

<style scoped>
/* Animation bulle flottante */
@keyframes floatBubble {
  from { transform: translateY(0px) scale(1); opacity: .5; }
  to   { transform: translateY(-18px) scale(1.05); opacity: .8; }
}

/* Loader point animé */
.loader-dot {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Transition erreur */
.slide-error-enter-active,
.slide-error-leave-active { transition: all .25s ease; }
.slide-error-enter-from,
.slide-error-leave-to { opacity: 0; transform: translateY(-8px); max-height: 0; }

/* Override checkbox visuel */
button[style*="border-color"] {
  outline: none;
}
</style>
```

## File: frontend/src/views/auth/RegisterView.vue
```vue
<script setup>
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../../stores/auth'

const { t } = useI18n()
const authStore = useAuthStore()

/* ── Étape du formulaire wizard (2 étapes) ── */
const step = ref(1)
const submitted = ref(false)

/* ── État du formulaire ── */
const form = ref({
  first_name:       '',
  last_name:        '',
  username:         '',
  email:            '',
  telephone:        '',
  password:         '',
  password_confirm: '',
})
const showPassword        = ref(false)
const showPasswordConfirm = ref(false)

/* ── Validation par champ ── */
const fieldErrors = computed(() => {
  if (!submitted.value) return {}
  const e = {}

  // Étape 1
  if (!form.value.first_name.trim())  e.first_name = 'Prénom requis'
  if (!form.value.last_name.trim())   e.last_name  = 'Nom requis'
  if (!form.value.username.trim())    e.username   = 'Nom d\'utilisateur requis'
  if (form.value.username.trim().length < 3)
    e.username = 'Minimum 3 caractères'
  if (!/^[a-zA-Z0-9@.+\-_]+$/.test(form.value.username))
    e.username = 'Caractères autorisés : lettres, chiffres, @/./+/-/_'
  if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email))
    e.email = 'Adresse email invalide'
  if (form.value.telephone && !/^(\+228)?[0-9]{8}$/.test(form.value.telephone.replace(/\s/g, '')))
    e.telephone = "Format : +22890123456 ou 90123456"

  // Étape 2
  if (form.value.password.length < 8)
    e.password = 'Minimum 8 caractères'
  if (!/[A-Z]/.test(form.value.password))
    e.password = 'Doit contenir au moins une majuscule'
  if (!/[0-9]/.test(form.value.password))
    e.password = 'Doit contenir au moins un chiffre'
  if (form.value.password !== form.value.password_confirm)
    e.password_confirm = 'Les mots de passe ne correspondent pas'

  return e
})

/* ── Validation par étape ── */
const step1Valid = computed(() => {
  const e = fieldErrors.value
  return !e.first_name && !e.last_name && !e.username && !e.email && !e.telephone
})
const step2Valid = computed(() => {
  const e = fieldErrors.value
  return !e.password && !e.password_confirm
})

/* ── Forcer la validation à l'étape courante ── */
const validateStep1 = () => {
  submitted.value = true
  return step1Valid.value
}

const goToStep2 = () => {
  if (validateStep1()) step.value = 2
}

/* ── Indicateur de force du mot de passe ── */
const passwordStrength = computed(() => {
  const p = form.value.password
  if (!p) return { score: 0, label: '', color: '' }
  let score = 0
  if (p.length >= 8)  score++
  if (p.length >= 12) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++

  const levels = [
    { score: 0, label: '',             color: 'bg-gray-200' },
    { score: 1, label: 'Très faible',  color: 'bg-red-400'  },
    { score: 2, label: 'Faible',       color: 'bg-orange-400' },
    { score: 3, label: 'Moyen',        color: 'bg-yellow-400' },
    { score: 4, label: 'Fort',         color: 'bg-green-400' },
    { score: 5, label: 'Très fort',    color: 'bg-[#005A3C]' },
  ]
  return levels[score] || levels[4]
})

/* ── Soumission finale ── */
async function handleRegister() {
  submitted.value = true
  if (!step2Valid.value || !step1Valid.value) return

  await authStore.register({
    first_name:       form.value.first_name.trim(),
    last_name:        form.value.last_name.trim(),
    username:         form.value.username.trim(),
    email:            form.value.email.trim(),
    telephone:        form.value.telephone.trim(),
    password:         form.value.password,
    password_confirm: form.value.password_confirm,
  })
}

/* ── Labels des étapes ── */
const steps = [
  { num: 1, label: 'Informations personnelles', icon: '👤' },
  { num: 2, label: 'Sécurité',                  icon: '🔐' },
]
</script>

<template>
  <div class="min-h-screen flex overflow-hidden" style="background:#FAF7F2">

    <!-- ══════════════════════════════════════════
         PANNEAU GAUCHE — Identité de marque
    ══════════════════════════════════════════ -->
    <aside class="hidden lg:flex lg:w-[46%] flex-col relative overflow-hidden"
           style="background-color:#C41230">

      <div class="absolute inset-0 kente-bg opacity-30"></div>
      <div class="absolute inset-0 bg-gradient-to-bl from-[#8B0D22] via-transparent to-[#3d0010]/60"></div>

      <!-- Bande drapeau -->
      <div class="absolute left-0 inset-y-0 w-1.5 flex flex-col">
        <div class="flex-[2] bg-[#005A3C]"></div>
        <div class="flex-1 bg-[#FFCE00]"></div>
        <div class="flex-[2] bg-[#C41230]"></div>
      </div>

      <!-- Cercles décoratifs -->
      <div class="absolute top-[-60px] right-[-60px] w-64 h-64 rounded-full
                  border border-white/10 opacity-50"></div>
      <div class="absolute bottom-[-40px] left-[-40px] w-48 h-48 rounded-full
                  border border-white/10 opacity-50"></div>

      <div class="relative z-10 flex flex-col h-full px-12 py-14">

        <!-- Logo -->
        <div class="flex items-center gap-3 mb-auto">
          <div class="w-11 h-11 bg-[#D4A017] rounded-xl flex items-center justify-center
                      font-serif font-bold text-[#005A3C] text-sm shadow-lg">DT</div>
          <span class="font-serif text-2xl font-bold text-white tracking-tight">
            Décla<span class="text-[#D4A017]">Togo</span>
          </span>
        </div>

        <div class="my-auto">
          <div class="w-20 h-20 rounded-full border-2 border-[#D4A017]/40 flex items-center
                      justify-center mb-8 relative">
            <div class="w-12 h-12 bg-[#D4A017]/20 rounded-full flex items-center justify-center">
              <span class="text-2xl">🎉</span>
            </div>
          </div>

          <h2 class="font-serif text-[2.8rem] font-bold text-white leading-[1.1] mb-5">
            Rejoignez<br/>
            <span class="text-[#D4A017]">des milliers</span><br/>
            de citoyens.
          </h2>
          <p class="text-white/70 text-sm leading-relaxed max-w-[320px]">
            Inscription gratuite, récépissé immédiat. Votre espace sécurisé
            pour gérer vos déclarations administratives.
          </p>

          <!-- Chiffres clés -->
          <div class="mt-10 grid grid-cols-2 gap-4">
            <div v-for="stat in [
              { num:'2 847+', label:'Déclarations' },
              { num:'1 203+', label:'Pièces retrouvées' },
              { num:'847+',   label:'Citoyens inscrits' },
              { num:'42%',    label:'Taux de restitution' },
            ]" :key="stat.label"
              class="bg-white/10 rounded-xl p-4 border border-white/10">
              <div class="font-serif text-2xl font-bold text-[#D4A017] leading-none mb-1">
                {{ stat.num }}
              </div>
              <div class="text-xs text-white/60">{{ stat.label }}</div>
            </div>
          </div>
        </div>

        <p class="text-xs text-white/35 mt-auto">
          © 2025 DéclaTogo — République Togolaise
        </p>
      </div>
    </aside>


    <!-- ══════════════════════════════════════════
         PANNEAU DROIT — Formulaire d'inscription
    ══════════════════════════════════════════ -->
    <main class="flex-1 flex flex-col items-center justify-center px-6 py-10 relative">

      <div class="absolute inset-0 pointer-events-none"
           style="background:radial-gradient(ellipse 60% 50% at 20% 80%, rgba(196,18,48,.04) 0%, transparent 70%)">
      </div>

      <!-- Logo mobile -->
      <div class="lg:hidden flex items-center gap-2 mb-8">
        <div class="w-9 h-9 bg-[#C41230] rounded-lg flex items-center justify-center
                    font-serif font-bold text-white text-sm">DT</div>
        <span class="font-serif text-xl font-bold text-[#1A2E22]">
          Décla<span class="text-[#C41230]">Togo</span>
        </span>
      </div>

      <div class="w-full max-w-[460px] fade-up relative z-10">

        <!-- En-tête -->
        <div class="mb-6">
          <div class="inline-flex items-center gap-2 bg-red-50 text-[#C41230]
                      text-xs font-bold px-3 py-1.5 rounded-full mb-4">
            🆕 Inscription gratuite
          </div>
          <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] leading-tight mb-1">
            {{ t('auth.register_title') }}
          </h1>
          <p class="text-sm text-gray-500">{{ t('auth.register_sub') }}</p>
        </div>

        <!-- Stepper -->
        <div class="flex items-center gap-0 mb-7">
          <div v-for="(s, i) in steps" :key="s.num" class="flex items-center flex-1">
            <div class="flex items-center gap-2">
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all',
                step === s.num
                  ? 'bg-[#005A3C] text-white shadow-md'
                  : step > s.num
                    ? 'bg-[#005A3C]/20 text-[#005A3C]'
                    : 'bg-gray-200 text-gray-400'
              ]">
                <span v-if="step > s.num">✓</span>
                <span v-else>{{ s.num }}</span>
              </div>
              <span :class="[
                'text-xs font-medium hidden sm:block transition-colors',
                step === s.num ? 'text-[#1A2E22]' : 'text-gray-400'
              ]">{{ s.label }}</span>
            </div>
            <div v-if="i < steps.length - 1"
              :class="[
                'flex-1 h-px mx-3 transition-all',
                step > s.num ? 'bg-[#005A3C]' : 'bg-gray-200'
              ]">
            </div>
          </div>
        </div>

        <!-- Erreur API globale -->
        <transition name="slide-error">
          <div v-if="authStore.error"
            class="flex items-start gap-3 bg-red-50 border border-red-200
                   rounded-xl p-4 mb-5 text-sm text-rouge">
            <span class="text-lg leading-none mt-0.5">⚠️</span>
            <span>{{ authStore.error }}</span>
          </div>
        </transition>

        <!-- ═══════════════ ÉTAPE 1 ═══════════════ -->
        <transition name="step-slide" mode="out-in">
          <div v-if="step === 1" key="step1" class="space-y-4">

            <!-- Prénom + Nom (côte à côte) -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="form-label">{{ t('auth.first_name') }}</label>
                <input
                  v-model="form.first_name"
                  type="text"
                  autocomplete="given-name"
                  :placeholder="t('auth.first_name')"
                  :class="['form-input', fieldErrors.first_name && 'border-rouge ring-2 ring-rouge/15']"
                />
                <p v-if="fieldErrors.first_name" class="form-error">
                  <span>✕</span> {{ fieldErrors.first_name }}
                </p>
              </div>
              <div>
                <label class="form-label">{{ t('auth.last_name') }}</label>
                <input
                  v-model="form.last_name"
                  type="text"
                  autocomplete="family-name"
                  :placeholder="t('auth.last_name')"
                  :class="['form-input', fieldErrors.last_name && 'border-rouge ring-2 ring-rouge/15']"
                />
                <p v-if="fieldErrors.last_name" class="form-error">
                  <span>✕</span> {{ fieldErrors.last_name }}
                </p>
              </div>
            </div>

            <!-- Nom d'utilisateur -->
            <div>
              <label class="form-label">{{ t('auth.username') }}</label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">@</span>
                <input
                  v-model="form.username"
                  type="text"
                  autocomplete="username"
                  placeholder="jean_akodjo"
                  :class="['form-input pl-8', fieldErrors.username && 'border-rouge ring-2 ring-rouge/15']"
                />
              </div>
              <p v-if="fieldErrors.username" class="form-error">
                <span>✕</span> {{ fieldErrors.username }}
              </p>
            </div>

            <!-- Email -->
            <div>
              <label class="form-label">{{ t('auth.email') }} <span class="text-gray-400 normal-case font-normal">(optionnel)</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">✉️</span>
                <input
                  v-model="form.email"
                  type="email"
                  autocomplete="email"
                  :placeholder="t('auth.email')"
                  :class="['form-input pl-10', fieldErrors.email && 'border-rouge ring-2 ring-rouge/15']"
                />
              </div>
              <p v-if="fieldErrors.email" class="form-error">
                <span>✕</span> {{ fieldErrors.email }}
              </p>
            </div>

            <!-- Téléphone -->
            <div>
              <label class="form-label">{{ t('auth.phone') }} <span class="text-gray-400 normal-case font-normal">(optionnel)</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm text-nowrap">🇹🇬</span>
                <input
                  v-model="form.telephone"
                  type="tel"
                  autocomplete="tel"
                  placeholder="+22890123456"
                  :class="['form-input pl-10', fieldErrors.telephone && 'border-rouge ring-2 ring-rouge/15']"
                />
              </div>
              <p v-if="fieldErrors.telephone" class="form-error">
                <span>✕</span> {{ fieldErrors.telephone }}
              </p>
            </div>

            <!-- Bouton suivant -->
            <button type="button"
              @click="goToStep2"
              class="w-full flex items-center justify-center gap-2.5
                     bg-[#005A3C] text-white font-bold py-3.5 px-6 rounded-[10px]
                     border-none cursor-pointer text-sm transition-all mt-2
                     hover:bg-[#007A52] hover:-translate-y-0.5 hover:shadow-lg"
              style="box-shadow: 0 4px 16px rgba(0,90,60,.30)">
              Continuer →
            </button>
          </div>
        </transition>

        <!-- ═══════════════ ÉTAPE 2 ═══════════════ -->
        <transition name="step-slide" mode="out-in">
          <div v-if="step === 2" key="step2">

            <form @submit.prevent="handleRegister" novalidate class="space-y-4">

              <!-- Résumé étape 1 -->
              <div class="flex items-center gap-3 bg-[#E8F4F0] rounded-xl p-3.5 mb-2">
                <div class="w-9 h-9 bg-[#005A3C] rounded-full flex items-center justify-center
                            text-white text-base font-serif font-bold flex-shrink-0">
                  {{ form.first_name.charAt(0).toUpperCase() || '?' }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-semibold text-[#1A2E22] truncate">
                    {{ form.first_name }} {{ form.last_name }}
                  </div>
                  <div class="text-xs text-gray-500 truncate">@{{ form.username }}</div>
                </div>
                <button type="button"
                  @click="step = 1"
                  class="text-xs text-[#005A3C] font-semibold bg-transparent border-none
                         cursor-pointer hover:underline flex-shrink-0">
                  Modifier
                </button>
              </div>

              <!-- Mot de passe -->
              <div>
                <label class="form-label">{{ t('auth.password') }}</label>
                <div class="relative">
                  <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔒</span>
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    autocomplete="new-password"
                    :placeholder="t('auth.password')"
                    :class="['form-input pl-10 pr-12', fieldErrors.password && 'border-rouge ring-2 ring-rouge/15']"
                  />
                  <button type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                           hover:text-gray-600 text-base bg-transparent border-none cursor-pointer">
                    {{ showPassword ? '🙈' : '👁️' }}
                  </button>
                </div>

                <!-- Barre de force -->
                <div v-if="form.password" class="mt-2">
                  <div class="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                    <div :class="['h-full rounded-full transition-all duration-500', passwordStrength.color]"
                      :style="{ width: `${(passwordStrength.score / 5) * 100}%` }">
                    </div>
                  </div>
                  <p class="text-xs mt-1" :class="{
                    'text-red-400': passwordStrength.score <= 2,
                    'text-yellow-600': passwordStrength.score === 3,
                    'text-[#005A3C]': passwordStrength.score >= 4,
                  }">{{ passwordStrength.label }}</p>
                </div>
                <p v-if="fieldErrors.password" class="form-error">
                  <span>✕</span> {{ fieldErrors.password }}
                </p>
              </div>

              <!-- Confirmer mot de passe -->
              <div>
                <label class="form-label">{{ t('auth.pwd_confirm') }}</label>
                <div class="relative">
                  <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔑</span>
                  <input
                    v-model="form.password_confirm"
                    :type="showPasswordConfirm ? 'text' : 'password'"
                    autocomplete="new-password"
                    :placeholder="t('auth.pwd_confirm')"
                    :class="['form-input pl-10 pr-12', fieldErrors.password_confirm && 'border-rouge ring-2 ring-rouge/15']"
                  />
                  <button type="button"
                    @click="showPasswordConfirm = !showPasswordConfirm"
                    class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                           hover:text-gray-600 text-base bg-transparent border-none cursor-pointer">
                    {{ showPasswordConfirm ? '🙈' : '👁️' }}
                  </button>
                </div>

                <!-- Check visuel : les mots de passe correspondent -->
                <div v-if="form.password_confirm && form.password === form.password_confirm"
                  class="flex items-center gap-1.5 mt-1.5">
                  <span class="text-green-500 text-xs">✓ Les mots de passe correspondent</span>
                </div>
                <p v-if="fieldErrors.password_confirm" class="form-error">
                  <span>✕</span> {{ fieldErrors.password_confirm }}
                </p>
              </div>

              <!-- Critères de sécurité -->
              <ul class="text-xs text-gray-400 space-y-1 list-none pl-0 bg-gray-50 rounded-xl p-3">
                <li v-for="rule in [
                  { ok: form.password.length >= 8,          text: 'Minimum 8 caractères' },
                  { ok: /[A-Z]/.test(form.password),        text: 'Au moins une majuscule' },
                  { ok: /[0-9]/.test(form.password),        text: 'Au moins un chiffre' },
                  { ok: /[^A-Za-z0-9]/.test(form.password), text: 'Caractère spécial recommandé' },
                ]" :key="rule.text"
                  :class="['flex items-center gap-2', rule.ok ? 'text-[#005A3C]' : 'text-gray-400']">
                  <span>{{ rule.ok ? '✓' : '○' }}</span> {{ rule.text }}
                </li>
              </ul>

              <!-- Boutons -->
              <div class="flex gap-3 mt-2">
                <button type="button"
                  @click="step = 1"
                  class="flex-shrink-0 px-5 py-3.5 rounded-[10px] border border-gray-200
                         text-sm font-medium text-gray-500 bg-white hover:bg-gray-50
                         transition-all cursor-pointer">
                  ← Retour
                </button>

                <button type="submit"
                  :disabled="authStore.loading"
                  class="flex-1 flex items-center justify-center gap-2.5
                         bg-[#C41230] text-white font-bold py-3.5 px-6 rounded-[10px]
                         border-none cursor-pointer text-sm transition-all
                         hover:bg-[#e8192f] hover:-translate-y-0.5 hover:shadow-lg
                         disabled:opacity-60 disabled:cursor-not-allowed disabled:translate-y-0">
                  <span v-if="authStore.loading" class="loader-dot"></span>
                  <span v-else>🎉</span>
                  <span>{{ authStore.loading ? 'Création...' : t('auth.register_btn') }}</span>
                </button>
              </div>

            </form>
          </div>
        </transition>

        <!-- Séparateur + lien connexion -->
        <div class="flex items-center gap-3 mt-6 mb-4">
          <span class="flex-1 h-px bg-gray-200"></span>
          <span class="text-xs text-gray-400 font-medium">ou</span>
          <span class="flex-1 h-px bg-gray-200"></span>
        </div>

        <p class="text-center text-sm text-gray-500">
          {{ t('auth.have_account') }}
          <router-link :to="{ name: 'login' }"
            class="text-[#005A3C] font-semibold hover:underline ml-1">
            {{ t('auth.login_link') }} →
          </router-link>
        </p>

        <div class="mt-4 text-center">
          <router-link :to="{ name: 'home' }"
            class="inline-flex items-center gap-1.5 text-xs text-gray-400
                   hover:text-[#005A3C] transition-colors no-underline">
            ← Retour à l'accueil
          </router-link>
        </div>

      </div>
    </main>

  </div>
</template>

<style scoped>
/* Transition entre étapes */
.step-slide-enter-active,
.step-slide-leave-active { transition: all .3s ease; }
.step-slide-enter-from   { opacity: 0; transform: translateX(30px); }
.step-slide-leave-to     { opacity: 0; transform: translateX(-30px); }

/* Erreur API */
.slide-error-enter-active,
.slide-error-leave-active { transition: all .25s ease; }
.slide-error-enter-from,
.slide-error-leave-to     { opacity: 0; transform: translateY(-8px); }

/* Spinner */
.loader-dot {
  display: inline-block;
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

## File: frontend/src/views/citizen/DeclarationDetailView.vue
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { declarationsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const route     = useRoute()
const router    = useRouter()
const authStore = useAuthStore()

/* ══ État ══ */
const declaration  = ref(null)
const loading      = ref(true)
const apiError     = ref(null)
const downloading  = ref(false)

/* ══ Chargement ══ */
onMounted(async () => {
  try {
    const { data } = await declarationsAPI.detail(route.params.id)
    declaration.value = data
  } catch (e) {
    apiError.value = e.response?.status === 404
      ? 'Cette déclaration est introuvable.'
      : 'Impossible de charger la déclaration.'
  } finally {
    loading.value = false
  }
})

/* ══ PDF ══ */
const downloadPDF = async () => {
  downloading.value = true
  try {
    const { data } = await declarationsAPI.downloadPDF(declaration.value.id)
    const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `recepisse_${declaration.value.numero_recepisse}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch {
    apiError.value = 'Impossible de générer le PDF.'
  } finally {
    downloading.value = false
  }
}

/* ══ Helpers ══ */
const statusFlow = [
  { key: 'EN_ATTENTE', label: 'En attente',  icon: '⏳', desc: 'Déclaration reçue, en cours de traitement.' },
  { key: 'VALIDE',     label: 'Validée',      icon: '✅', desc: 'Validée par nos services, matching actif.' },
  { key: 'RETROUVE',   label: 'Retrouvée',    icon: '🎉', desc: 'Une correspondance a été trouvée !' },
  { key: 'RESTITUE',   label: 'Restituée',    icon: '🤝', desc: 'La pièce a été restituée à son propriétaire.' },
]
const negativeStatus = ['REJETE', 'CLOTURE']

const statusConfig = {
  EN_ATTENTE: { label: 'En attente',  color: '#D97706', bg: '#FEF3C7' },
  VALIDE:     { label: 'Validé',      color: '#2563EB', bg: '#DBEAFE' },
  RETROUVE:   { label: 'Retrouvé',    color: '#059669', bg: '#D1FAE5' },
  RESTITUE:   { label: 'Restitué',    color: '#065F46', bg: '#A7F3D0' },
  REJETE:     { label: 'Rejeté',      color: '#DC2626', bg: '#FEE2E2' },
  CLOTURE:    { label: 'Clôturé',     color: '#6B7280', bg: '#F3F4F6' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const statusIndex = computed(() => {
  if (!declaration.value) return -1
  return statusFlow.findIndex(s => s.key === declaration.value.statut)
})

const isNegative = computed(() =>
  declaration.value && negativeStatus.includes(declaration.value.statut)
)

const formatDate = (d, withTime = false) => {
  if (!d) return '—'
  const opts = { day: '2-digit', month: 'long', year: 'numeric' }
  if (withTime) Object.assign(opts, { hour: '2-digit', minute: '2-digit' })
  return new Date(d).toLocaleDateString('fr-FR', opts)
}

const hasMatch = computed(() =>
  declaration.value?.declaration_correspondante ||
  declaration.value?.correspondance_detail
)
const match = computed(() =>
  declaration.value?.correspondance_detail || declaration.value?.declaration_correspondante
)
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-3xl mx-auto">

  <!-- ══ Navigation ══ -->
  <div class="flex items-center gap-3 mb-6">
    <button @click="router.back()"
      class="flex items-center gap-1.5 text-xs text-gray-400 hover:text-[#005A3C]
             bg-transparent border-none cursor-pointer transition-colors">
      ← Retour
    </button>
    <span class="text-gray-300">·</span>
    <span class="text-xs text-gray-400">Détail de la déclaration</span>
  </div>

  <!-- ══ Chargement ══ -->
  <div v-if="loading" class="space-y-4">
    <div class="skeleton h-32 rounded-2xl"></div>
    <div class="skeleton h-64 rounded-2xl"></div>
    <div class="skeleton h-48 rounded-2xl"></div>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-else-if="apiError && !declaration"
    class="text-center py-20 bg-white rounded-2xl shadow-card">
    <div class="text-4xl mb-4">😕</div>
    <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">{{ apiError }}</p>
    <button @click="router.back()"
      class="mt-4 text-sm text-[#005A3C] font-semibold bg-transparent border-none cursor-pointer hover:underline">
      ← Retour à mes déclarations
    </button>
  </div>

  <!-- ══ Contenu ══ -->
  <template v-else-if="declaration">

    <!-- ─── Carte héro ─── -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 mb-5 overflow-hidden">

      <!-- Bande colorée en haut -->
      <div class="h-1.5"
        :style="{
          backgroundColor: isNegative ? '#DC2626'
            : declaration.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
        }">
      </div>

      <div class="p-6">
        <div class="flex items-start justify-between gap-4 flex-wrap">
          <div class="flex items-center gap-4">
            <!-- Icône type -->
            <div class="w-14 h-14 rounded-xl flex items-center justify-center text-3xl flex-shrink-0"
              :style="{
                backgroundColor: declaration.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0'
              }">
              {{ declaration.type_declaration === 'PERTE' ? '😟' : '🤲' }}
            </div>
            <div>
              <div class="flex items-center gap-2 mb-1 flex-wrap">
                <span class="font-bold text-xs px-2 py-1 rounded"
                  :style="{
                    backgroundColor: declaration.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0',
                    color: declaration.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
                  }">
                  {{ declaration.type_declaration }}
                </span>
                <span class="badge text-xs"
                  :style="{
                    color: getStatus(declaration.statut).color,
                    backgroundColor: getStatus(declaration.statut).bg
                  }">
                  {{ getStatus(declaration.statut).label }}
                </span>
              </div>
              <h1 class="font-serif text-xl font-bold text-[#1A2E22] leading-tight">
                <span v-if="declaration.nom_declarant">
                  {{ declaration.nom_declarant }}
                  <span class="font-normal">{{ declaration.prenom_declarant }}</span>
                </span>
                <span v-else>{{ declaration.nom_sur_piece }}</span>
              </h1>
              <div class="font-mono text-sm font-bold text-[#005A3C] tracking-wider mt-0.5">
                {{ declaration.numero_piece }}
              </div>
            </div>
          </div>

          <!-- Bouton PDF -->
          <button @click="downloadPDF" :disabled="downloading"
            class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                   text-xs px-4 py-2.5 rounded-xl border-none cursor-pointer
                   transition-all hover:bg-[#007A52] hover:shadow-md
                   disabled:opacity-50 flex-shrink-0">
            <span v-if="downloading" class="loader-dot-xs"></span>
            <span v-else>📄</span>
            {{ downloading ? 'Génération…' : 'Récépissé PDF' }}
          </button>
        </div>

        <!-- Numéro récépissé -->
        <div class="mt-4 pt-4 border-t border-gray-100 flex items-center gap-2 text-xs text-gray-400">
          <span>📋 Récépissé :</span>
          <span class="font-mono font-bold text-gray-600">{{ declaration.numero_recepisse }}</span>
          <span class="mx-2">·</span>
          <span>Déclaré le {{ formatDate(declaration.date_declaration, true) }}</span>
        </div>
      </div>
    </div>

    <!-- ─── Alerte match ─── -->
    <transition name="slide-in">
      <div v-if="hasMatch"
        class="bg-green-50 border-2 border-green-300 rounded-2xl p-5 mb-5">
        <div class="flex items-start gap-3">
          <span class="text-2xl">🎉</span>
          <div>
            <p class="font-bold text-green-800 mb-1">
              {{ declaration.type_declaration === 'PERTE'
                ? 'Votre pièce a peut-être été retrouvée !'
                : 'Cette trouvaille correspond à une déclaration de perte !' }}
            </p>
            <p class="text-sm text-green-700 mb-3">
              Une correspondance automatique a été détectée.
              Rapprochez-vous du commissariat pour finaliser la restitution.
            </p>
            <!-- Carte match -->
            <div class="bg-white rounded-xl p-4 border border-green-200 flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg flex items-center justify-center text-lg"
                :style="{
                  backgroundColor: match?.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0'
                }">
                {{ match?.type_declaration === 'PERTE' ? '😟' : '🤲' }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="font-mono text-xs font-bold text-[#005A3C] tracking-wider">
                  {{ match?.numero_piece }}
                </div>
                <div class="text-xs text-gray-600">{{ match?.nom_sur_piece }}</div>
                <div class="text-xs text-gray-400 mt-0.5">{{ match?.numero_recepisse }}</div>
              </div>
              <span class="text-xs text-green-600 font-semibold bg-green-100 px-2 py-1 rounded-lg">
                {{ match?.type_declaration === 'PERTE' ? 'Perte' : 'Trouvaille' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- ─── Remarques admin ─── -->
    <div v-if="declaration.remarques_admin"
      class="bg-blue-50 border border-blue-200 rounded-2xl p-4 mb-5 flex items-start gap-3">
      <span class="text-lg">💬</span>
      <div>
        <p class="text-xs font-bold text-blue-800 mb-1">Message du service</p>
        <p class="text-sm text-blue-700">{{ declaration.remarques_admin }}</p>
      </div>
    </div>

    <!-- ─── Fiche détaillée ─── -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">

      <!-- Informations pièce -->
      <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
        <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-4 flex items-center gap-2">
          <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">🪪</span>
          Pièce concernée
        </h2>
        <dl class="space-y-3 text-sm">
          <div v-for="row in [
            { label: 'Catégorie',          value: declaration.categorie_detail?.libelle || declaration.categorie_nom || '—' },
            { label: 'Numéro',             value: declaration.numero_piece || 'Non communiqué', mono: !declaration.numero_piece },
            { label: 'Nom de famille',     value: declaration.nom_declarant   || '—' },
            { label: 'Prénom(s)',          value: declaration.prenom_declarant || '—' },
            { label: 'Date de naissance',  value: declaration.date_naissance
                                                  ? new Date(declaration.date_naissance + 'T00:00:00').toLocaleDateString('fr-FR') : '—' },
            { label: 'Lieu de naissance',  value: declaration.lieu_naissance  || '—' },
            { label: 'Profession',         value: declaration.profession       || '—' },
            { label: 'Date de la ' + (declaration.type_declaration === 'PERTE' ? 'perte' : 'trouvaille'),
                                           value: formatDate(declaration.date_perte) },
            { label: 'Lieu',               value: declaration.lieu_perte       || '—' },
          ]" :key="row.label">
            <div class="flex justify-between gap-2">
              <dt class="text-xs text-gray-400 font-medium flex-shrink-0">{{ row.label }}</dt>
              <dd :class="['text-right font-medium text-[#1A2E22] break-all',
                           row.mono && 'font-mono text-[#005A3C] tracking-wide text-xs']">
                {{ row.value }}
              </dd>
            </div>
            <div class="h-px bg-gray-50"></div>
          </div>
        </dl>
      </div>

      <!-- Photo si disponible + Infos déclarant -->
      <div class="space-y-4">
        <div v-if="declaration.photo_piece"
          class="bg-white rounded-2xl shadow-card border border-gray-100 p-4 text-center">
          <p class="text-xs text-gray-400 mb-2 font-medium">Photo de la pièce</p>
          <img :src="declaration.photo_piece" alt="Photo pièce"
            class="max-h-32 w-auto mx-auto rounded-xl object-cover shadow-sm"/>
        </div>

        <!-- Description -->
        <div v-if="declaration.description"
          class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
          <h3 class="font-serif text-sm font-bold text-[#1A2E22] mb-2">Description</h3>
          <p class="text-sm text-gray-600 leading-relaxed">
            {{ declaration.description }}
          </p>
        </div>

        <!-- Dates -->
        <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5">
          <h3 class="font-serif text-sm font-bold text-[#1A2E22] mb-3">Horodatage</h3>
          <div class="space-y-2 text-xs">
            <div class="flex justify-between">
              <span class="text-gray-400">Déclaré le</span>
              <span class="font-medium text-[#1A2E22]">{{ formatDate(declaration.date_declaration, true) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Dernière mise à jour</span>
              <span class="font-medium text-[#1A2E22]">{{ formatDate(declaration.date_modification, true) }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ─── Timeline de statut ─── -->
    <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-5 mb-5">
      <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-5 flex items-center gap-2">
        <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">📊</span>
        Progression
      </h2>

      <!-- Statut négatif -->
      <div v-if="isNegative"
        class="flex items-center gap-3 bg-red-50 rounded-xl p-4 text-sm">
        <span class="text-2xl">{{ declaration.statut === 'REJETE' ? '❌' : '🔒' }}</span>
        <div>
          <p class="font-bold text-rouge">{{ getStatus(declaration.statut).label }}</p>
          <p class="text-xs text-red-600 mt-0.5">
            {{ declaration.statut === 'REJETE'
              ? 'Cette déclaration a été rejetée. Contactez le service pour plus d\'informations.'
              : 'Cette déclaration a été clôturée.' }}
          </p>
        </div>
      </div>

      <!-- Timeline normale -->
      <div v-else class="relative">
        <!-- Ligne de connexion -->
        <div class="absolute left-[18px] top-[18px] bottom-[18px] w-0.5 bg-gray-200 -z-0"></div>

        <div class="space-y-0">
          <div v-for="(s, i) in statusFlow" :key="s.key"
            class="flex items-start gap-4 relative pb-6 last:pb-0">

            <!-- Point timeline -->
            <div :class="[
              'w-9 h-9 rounded-full flex items-center justify-center text-sm flex-shrink-0 relative z-10 border-2 transition-all',
              i < statusIndex || i === statusIndex
                ? 'border-[#005A3C] bg-[#005A3C] text-white shadow-md'
                : 'border-gray-200 bg-white text-gray-400'
            ]">
              <span v-if="i < statusIndex">✓</span>
              <span v-else>{{ s.icon }}</span>
            </div>

            <!-- Contenu -->
            <div :class="['pt-1.5', i > statusIndex && 'opacity-40']">
              <p :class="[
                'text-sm font-semibold',
                i <= statusIndex ? 'text-[#1A2E22]' : 'text-gray-400'
              ]">
                {{ s.label }}
                <span v-if="i === statusIndex"
                  class="ml-2 inline-block bg-[#005A3C]/10 text-[#005A3C]
                         text-xs font-bold px-2 py-0.5 rounded-full">
                  Étape actuelle
                </span>
              </p>
              <p class="text-xs text-gray-500 mt-0.5">{{ s.desc }}</p>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- ─── Erreur ─── -->
    <div v-if="apiError"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      <span>⚠️</span><span>{{ apiError }}</span>
    </div>

    <!-- ─── Actions bas de page ─── -->
    <div class="flex items-center justify-between gap-3 flex-wrap">
      <router-link :to="{ name: 'mes-declarations' }"
        class="inline-flex items-center gap-1.5 text-sm font-medium text-gray-500
               bg-white border border-gray-200 px-5 py-3 rounded-xl no-underline
               hover:bg-gray-50 transition-all">
        ← Toutes mes déclarations
      </router-link>
      <div class="flex items-center gap-2">
        <button @click="downloadPDF" :disabled="downloading"
          class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                 text-sm px-5 py-3 rounded-xl border-none cursor-pointer
                 transition-all hover:bg-[#007A52] hover:shadow-md
                 disabled:opacity-50">
          <span v-if="downloading" class="loader-dot-xs"></span>
          <span v-else>📄</span>
          Télécharger PDF
        </button>
        <router-link :to="{ name: 'declare' }"
          class="inline-flex items-center gap-1.5 text-sm font-semibold
                 text-[#005A3C] bg-[#E8F4F0] px-5 py-3 rounded-xl no-underline
                 hover:bg-[#d0ece3] transition-all">
          + Nouvelle déclaration
        </router-link>
      </div>
    </div>

  </template>

</div>
</div>
</template>

<style scoped>
.slide-in-enter-active { transition: all .4s cubic-bezier(.175,.885,.32,1.275); }
.slide-in-enter-from   { opacity: 0; transform: translateY(-10px) scale(.97); }

.loader-dot-xs {
  display: inline-block;
  width: 12px; height: 12px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

## File: frontend/src/views/citizen/DeclareView.vue
```vue
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { declarationsAPI, categoriesAPI } from '../../services/api'

const route  = useRoute()
const router = useRouter()
const { t }  = useI18n()

/* ══════════════════════════════════════
   ÉTAT GLOBAL DU WIZARD
══════════════════════════════════════ */
const step           = ref(1)   // 1 | 2 | 3 | 4 (succès)
const submitting     = ref(false)
const apiError       = ref(null)
const createdDecl    = ref(null) // Déclaration créée après succès
const categories     = ref([])
const loadingCats    = ref(true)

/* ══════════════════════════════════════
   FORMULAIRE
══════════════════════════════════════ */
const form = ref({
  type_declaration: '',       // 'PERTE' | 'TROUVAILLE'
  categorie:        null,     // id numérique
  numero_piece:     '',       // optionnel
  nom:              '',       // Nom de famille — obligatoire
  prenom:           '',       // Prénom(s) — obligatoire
  date_naissance:   '',       // obligatoire
  lieu_naissance:   '',       // obligatoire
  profession:       '',       // obligatoire
  description:      '',
  lieu_perte:       '',
  date_perte:       '',
  photo_piece:      null,     // File object
})
const photoPreview = ref(null)
const isDragging   = ref(false)

/* ══════════════════════════════════════
   CATÉGORIES FALLBACK (si API hors ligne)
   Identiques à init_categories_windows.py
══════════════════════════════════════ */
const FALLBACK_CATEGORIES = [
  { id: 1, libelle: "Pièce d'identité",         icone: 'id-card'       },
  { id: 2, libelle: 'Véhicule',                 icone: 'car'           },
  { id: 3, libelle: 'Documents scolaires',      icone: 'graduation-cap'},
  { id: 4, libelle: 'Documents bancaires',      icone: 'credit-card'   },
  { id: 5, libelle: 'Documents professionnels', icone: 'briefcase'     },
  { id: 6, libelle: 'Documents de santé',       icone: 'heart'         },
  { id: 7, libelle: 'Autres documents',         icone: 'file'          },
]
const catsFromAPI = ref(false)

/* ══════════════════════════════════════
   PRÉ-REMPLIR LE TYPE DEPUIS LA QUERY
══════════════════════════════════════ */
onMounted(async () => {
  if (route.query.type === 'TROUVAILLE') form.value.type_declaration = 'TROUVAILLE'
  else if (route.query.type === 'PERTE') form.value.type_declaration = 'PERTE'

  try {
    const { data } = await categoriesAPI.list()
    const list = data.results ?? data
    if (list && list.length > 0) {
      categories.value = list
      catsFromAPI.value = true
    } else {
      categories.value = FALLBACK_CATEGORIES
    }
  } catch (e) {
    // API hors ligne → fallback silencieux
    categories.value = FALLBACK_CATEGORIES
  } finally {
    loadingCats.value = false
  }
})

/* ══════════════════════════════════════
   VALIDATION PAR ÉTAPE
══════════════════════════════════════ */
// Le bouton devient cliquable dès qu'un type est choisi
const step1Valid = computed(() => form.value.type_declaration !== '')
// Erreur affichée seulement si l'utilisateur clique sans catégorie
const catError = ref(false)
const step2Valid = computed(() => {
  const f = form.value
  return (
    f.nom.trim().length >= 2          &&
    f.prenom.trim().length >= 2       &&
    f.date_naissance !== ''           &&
    f.lieu_naissance.trim().length >= 2 &&
    f.profession.trim().length >= 2
  )
})

/* ══════════════════════════════════════
   NAVIGATION
══════════════════════════════════════ */
const goNext = () => {
  if (step.value === 1) {
    if (!form.value.categorie) { catError.value = true; return }
    catError.value = false
    step.value = 2
  } else if (step.value === 2 && step2Valid.value) {
    step.value = 3
  }
}
const goBack = () => {
  if (step.value > 1) step.value--
}

/* ══════════════════════════════════════
   GESTION PHOTO
══════════════════════════════════════ */
const handlePhotoChange = (e) => {
  const file = e.target.files?.[0] || e.dataTransfer?.files?.[0]
  if (!file) return
  if (file.size > 5 * 1024 * 1024) {
    apiError.value = 'La photo ne doit pas dépasser 5 MB.'
    return
  }
  if (!['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)) {
    apiError.value = 'Format non autorisé. Utilisez JPG ou PNG.'
    return
  }
  form.value.photo_piece = file
  const reader = new FileReader()
  reader.onload = (e) => { photoPreview.value = e.target.result }
  reader.readAsDataURL(file)
  apiError.value = null
}
const removePhoto = () => {
  form.value.photo_piece = null
  photoPreview.value = null
}
const handleDrop = (e) => {
  isDragging.value = false
  handlePhotoChange(e)
}

/* ══════════════════════════════════════
   SOUMISSION
══════════════════════════════════════ */
const handleSubmit = async () => {
  if (!step2Valid.value || !step1Valid.value) return
  submitting.value = true
  apiError.value   = null

  try {
    const formData = new FormData()
    // nom_sur_piece = "NOM Prénom" auto-construit côté backend
    // mais on l'envoie aussi pour compatibilité
    const nomSurPiece = `${form.value.nom.trim().toUpperCase()} ${form.value.prenom.trim()}`

    formData.append('type_declaration',  form.value.type_declaration)
    formData.append('categorie',         form.value.categorie)

    // Numéro de pièce — optionnel
    if (form.value.numero_piece.trim())
      formData.append('numero_piece', form.value.numero_piece.trim().toUpperCase())

    // nom_sur_piece : construit depuis nom + prénom
    formData.append('nom_sur_piece',     nomSurPiece)

    // Champs identité — stockés séparément en base
    formData.append('nom_declarant',     form.value.nom.trim().toUpperCase())
    formData.append('prenom_declarant',  form.value.prenom.trim())
    formData.append('date_naissance',    form.value.date_naissance)
    formData.append('lieu_naissance',    form.value.lieu_naissance.trim())
    formData.append('profession',        form.value.profession.trim())

    // Champs circonstances
    if (form.value.description) formData.append('description',  form.value.description.trim())
    if (form.value.lieu_perte)  formData.append('lieu_perte',   form.value.lieu_perte.trim())
    if (form.value.date_perte)  formData.append('date_perte',   form.value.date_perte)
    if (form.value.photo_piece) formData.append('photo_piece',  form.value.photo_piece)

    const { data } = await declarationsAPI.create(formData)
    createdDecl.value = data
    step.value = 4  // Écran de succès

  } catch (err) {
    const d = err.response?.data
    if (typeof d === 'object') {
      const keys = Object.keys(d)
      apiError.value = keys.length ? `${keys[0]} : ${d[keys[0]]}` : 'Une erreur est survenue.'
    } else {
      apiError.value = 'Erreur réseau. Vérifiez votre connexion.'
    }
    step.value = 3  // Rester sur recap
  } finally {
    submitting.value = false
  }
}

/* ══════════════════════════════════════
   TÉLÉCHARGEMENT PDF
══════════════════════════════════════ */
const downloadPDF = async () => {
  if (!createdDecl.value?.id) return
  try {
    const { data } = await declarationsAPI.downloadPDF(createdDecl.value.id)
    const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `recepisse_${createdDecl.value.numero_recepisse}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    apiError.value = 'Impossible de générer le PDF pour le moment.'
  }
}

/* ══════════════════════════════════════
   HELPERS AFFICHAGE
══════════════════════════════════════ */
const selectedCategory = computed(() =>
  categories.value.find(c => c.id === form.value.categorie)
)
const typeLabel = computed(() =>
  form.value.type_declaration === 'PERTE' ? 'Perte' : 'Trouvaille'
)
const typeColor = computed(() =>
  form.value.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
)

const today = new Date().toISOString().split('T')[0]

// Icônes par catégorie (fallback)
const iconMap = {
  'id-card': '🪪', car: '🚗', 'graduation-cap': '🎓',
  'credit-card': '💳', briefcase: '💼', heart: '🏥', file: '📂',
}
const catIcon = (cat) => iconMap[cat.icone] || '📋'

const WIZARD_STEPS = [
  { num: 1, label: 'Type & catégorie' },
  { num: 2, label: 'Détails de la pièce' },
  { num: 3, label: 'Récapitulatif' },
]
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">

  <!-- ══════════════════════
       HEADER DE PAGE
  ══════════════════════ -->
  <div v-if="step < 4" class="max-w-2xl mx-auto mb-8">
    <router-link :to="{ name: 'home' }"
      class="inline-flex items-center gap-1.5 text-xs text-gray-400
             hover:text-[#005A3C] transition-colors no-underline mb-5">
      ← Retour à l'accueil
    </router-link>

    <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                text-xs font-bold px-3 py-1.5 rounded-full mb-3">
      📋 Nouvelle déclaration
    </div>
    <h1 class="font-serif text-[2rem] font-bold text-[#1A2E22] mb-1">
      Déclarer une perte ou trouvaille
    </h1>
    <p class="text-sm text-gray-500">
      Remplissez ce formulaire — un récépissé officiel PDF vous sera remis immédiatement.
    </p>
  </div>

  <!-- ══════════════════════
       STEPPER
  ══════════════════════ -->
  <div v-if="step < 4" class="max-w-2xl mx-auto mb-8">
    <div class="flex items-center">
      <template v-for="(s, i) in WIZARD_STEPS" :key="s.num">
        <div class="flex items-center gap-2">
          <div :class="[
            'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300',
            step === s.num  ? 'bg-[#005A3C] text-white shadow-lg scale-110'
            : step > s.num  ? 'bg-[#005A3C]/20 text-[#005A3C]'
                            : 'bg-white text-gray-400 border border-gray-200'
          ]">
            <span v-if="step > s.num">✓</span>
            <span v-else>{{ s.num }}</span>
          </div>
          <span :class="[
            'text-xs font-medium hidden sm:block transition-colors',
            step === s.num ? 'text-[#1A2E22]' : 'text-gray-400'
          ]">{{ s.label }}</span>
        </div>

        <div v-if="i < WIZARD_STEPS.length - 1"
          :class="[
            'flex-1 h-px mx-3 transition-all duration-500',
            step > s.num ? 'bg-[#005A3C]' : 'bg-gray-200'
          ]">
        </div>
      </template>
    </div>

    <!-- Barre de progression -->
    <div class="mt-4 h-1 bg-gray-200 rounded-full overflow-hidden">
      <div class="h-full bg-[#005A3C] rounded-full transition-all duration-500"
        :style="{ width: `${((step - 1) / 2) * 100}%` }">
      </div>
    </div>
  </div>


  <!-- ════════════════════════════════════════
       ÉTAPE 1 — Type + Catégorie
  ════════════════════════════════════════ -->
  <transition name="fade-step" mode="out-in">
  <div v-if="step === 1" key="s1" class="max-w-2xl mx-auto fade-up">
    <div class="card">

      <!-- Choix PERTE / TROUVAILLE -->
      <h2 class="font-serif text-lg font-bold text-[#1A2E22] mb-1.5">
        Quel type de déclaration souhaitez-vous faire ?
      </h2>
      <p class="text-sm text-gray-500 mb-5">
        Choisissez selon votre situation.
      </p>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">

        <!-- PERTE -->
        <button type="button"
          @click="form.type_declaration = 'PERTE'"
          :class="[
            'relative rounded-xl p-6 border-2 text-left transition-all cursor-pointer',
            'hover:-translate-y-0.5',
            form.type_declaration === 'PERTE'
              ? 'border-[#C41230] bg-red-50 shadow-lg'
              : 'border-gray-200 bg-white hover:border-red-200'
          ]">
          <!-- Indicateur sélectionné -->
          <div v-if="form.type_declaration === 'PERTE'"
            class="absolute top-3 right-3 w-5 h-5 bg-[#C41230] rounded-full
                   flex items-center justify-center text-white text-xs">✓</div>

          <div class="w-12 h-12 rounded-xl bg-red-100 flex items-center
                      justify-center text-2xl mb-4">😟</div>
          <div class="font-serif text-lg font-bold text-[#1A2E22] mb-1">
            J'ai perdu un document
          </div>
          <p class="text-xs text-gray-500 leading-relaxed">
            Vous avez perdu une pièce administrative et souhaitez en faire la déclaration officielle.
          </p>
          <div class="mt-3 inline-block bg-[#C41230]/10 text-[#C41230]
                      text-xs font-bold px-2 py-1 rounded">PERTE</div>
        </button>

        <!-- TROUVAILLE -->
        <button type="button"
          @click="form.type_declaration = 'TROUVAILLE'"
          :class="[
            'relative rounded-xl p-6 border-2 text-left transition-all cursor-pointer',
            'hover:-translate-y-0.5',
            form.type_declaration === 'TROUVAILLE'
              ? 'border-[#005A3C] bg-[#E8F4F0] shadow-lg'
              : 'border-gray-200 bg-white hover:border-green-200'
          ]">
          <div v-if="form.type_declaration === 'TROUVAILLE'"
            class="absolute top-3 right-3 w-5 h-5 bg-[#005A3C] rounded-full
                   flex items-center justify-center text-white text-xs">✓</div>

          <div class="w-12 h-12 rounded-xl bg-[#E8F4F0] flex items-center
                      justify-center text-2xl mb-4">🤲</div>
          <div class="font-serif text-lg font-bold text-[#1A2E22] mb-1">
            J'ai trouvé un document
          </div>
          <p class="text-xs text-gray-500 leading-relaxed">
            Vous avez trouvé une pièce administrative et souhaitez aider son propriétaire à la récupérer.
          </p>
          <div class="mt-3 inline-block bg-[#005A3C]/10 text-[#005A3C]
                      text-xs font-bold px-2 py-1 rounded">TROUVAILLE</div>
        </button>
      </div>

      <!-- Catégorie -->
      <h2 class="font-serif text-lg font-bold text-[#1A2E22] mb-1.5">
        Quelle est la catégorie du document ?
      </h2>
      <div class="flex items-center gap-2 mb-5">
        <p class="text-sm text-gray-500">Sélectionnez le type de pièce concernée.</p>
        <span v-if="!catsFromAPI && categories.length > 0"
          class="text-xs bg-yellow-100 text-yellow-700 font-medium px-2 py-0.5 rounded-full flex-shrink-0">
          ⚡ Mode hors ligne
        </span>
      </div>

      <div v-if="loadingCats" class="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
        <div v-for="i in 6" :key="i" class="skeleton h-20 rounded-xl"></div>
      </div>

      <!-- Grille catégories (erreur surlignée si oubliée) -->
      <div v-else
        :class="['grid grid-cols-2 sm:grid-cols-3 gap-3 mb-2', catError && !form.categorie && 'ring-2 ring-rouge/30 rounded-xl p-1']">
        <button type="button"
          v-for="cat in categories" :key="cat.id"
          @click="form.categorie = cat.id; catError = false"
          :class="[
            'rounded-xl p-4 border-2 text-left transition-all cursor-pointer',
            'hover:-translate-y-0.5',
            form.categorie === cat.id
              ? 'border-[#005A3C] bg-[#E8F4F0] shadow-md'
              : catError && !form.categorie
                ? 'border-rouge/30 bg-white'
                : 'border-gray-200 bg-white hover:border-gray-300'
          ]">
          <span class="text-2xl block mb-2">{{ catIcon(cat) }}</span>
          <div :class="[
            'text-xs font-semibold leading-tight',
            form.categorie === cat.id ? 'text-[#005A3C]' : 'text-[#1A2E22]'
          ]">{{ cat.libelle }}</div>
        </button>
      </div>

      <!-- Message d'erreur catégorie -->
      <transition name="slide-error">
        <p v-if="catError && !form.categorie"
          class="flex items-center gap-1.5 text-xs text-rouge font-medium mb-4 mt-1">
          ⚠️ Veuillez sélectionner une catégorie pour continuer.
        </p>
        <div v-else class="mb-4"></div>
      </transition>

      <!-- Pied de carte -->
      <div class="flex items-center justify-between pt-4 border-t border-gray-100">
        <div class="text-xs text-gray-400">
          <span v-if="!form.type_declaration">← Choisissez un type</span>
          <span v-else-if="!form.categorie" class="text-[#D97706] font-medium">⬆ Choisissez aussi une catégorie</span>
          <span v-else class="text-[#005A3C] font-semibold">✓ Prêt à continuer</span>
        </div>
        <button type="button"
          @click="goNext"
          :disabled="!step1Valid"
          class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                 text-sm px-6 py-3 rounded-[10px] border-none cursor-pointer
                 transition-all hover:bg-[#007A52] hover:-translate-y-0.5
                 disabled:opacity-40 disabled:cursor-not-allowed disabled:translate-y-0">
          Continuer →
        </button>
      </div>

    </div>
  </div>
  </transition>


  <!-- ════════════════════════════════════════
       ÉTAPE 2 — Détails de la pièce
  ════════════════════════════════════════ -->
  <transition name="fade-step" mode="out-in">
  <div v-if="step === 2" key="s2" class="max-w-2xl mx-auto fade-up">
    <div class="card">

      <!-- Badge type sélectionné -->
      <div class="flex items-center gap-2 mb-6">
        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold"
          :style="{
            backgroundColor: form.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0',
            color: typeColor
          }">
          {{ form.type_declaration === 'PERTE' ? '😟' : '🤲' }} {{ typeLabel }}
        </div>
        <div class="flex items-center gap-1.5 bg-gray-100 text-gray-600 px-3 py-1.5 rounded-full text-xs font-bold">
          {{ catIcon(selectedCategory || {}) }} {{ selectedCategory?.libelle }}
        </div>
        <button type="button" @click="goBack"
          class="ml-auto text-xs text-gray-400 hover:text-[#005A3C] bg-transparent
                 border-none cursor-pointer transition-colors">
          Modifier
        </button>
      </div>

      <h2 class="font-serif text-lg font-bold text-[#1A2E22] mb-5">
        Informations sur la pièce
      </h2>

      <div class="space-y-5">

        <!-- Numéro de pièce (optionnel) -->
        <div>
          <label class="form-label">
            Numéro de la pièce
            <span class="text-gray-400 normal-case font-normal ml-1">(optionnel)</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔢</span>
            <input
              v-model="form.numero_piece"
              type="text"
              placeholder="Ex : TG20240001, AB-1234-CD"
              maxlength="100"
              class="form-input pl-10 uppercase"
              style="font-family: 'DM Mono', monospace, sans-serif; letter-spacing: 0.04em;"
            />
          </div>
          <p class="text-xs text-gray-400 mt-1.5">
            Si vous ne connaissez pas le numéro, laissez ce champ vide.
          </p>
        </div>

        <!-- Séparateur identité -->
        <div class="flex items-center gap-3">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Identité sur la pièce</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Nom + Prénom séparés -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">

          <!-- NOM DE FAMILLE -->
          <div>
            <label class="form-label">
              Nom de famille <span class="text-rouge">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">👤</span>
              <input
                v-model="form.nom"
                type="text"
                placeholder="Ex : AKODJO"
                maxlength="100"
                class="form-input pl-10 uppercase"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
              <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
              Saisissez exactement comme indiqué sur votre pièce (majuscules incluses).
            </p>
          </div>

          <!-- PRÉNOM(S) -->
          <div>
            <label class="form-label">
              Prénom(s) <span class="text-rouge">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">✍️</span>
              <input
                v-model="form.prenom"
                type="text"
                placeholder="Ex : Jean Kofi"
                maxlength="100"
                class="form-input pl-10"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
              <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
              Saisissez exactement comme indiqué sur votre pièce.
            </p>
          </div>

        </div>

        <!-- Séparateur infos complémentaires -->
        <div class="flex items-center gap-3">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Informations complémentaires</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Date de naissance + Lieu de naissance -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="form-label">
              Date de naissance <span class="text-rouge">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🎂</span>
              <input
                v-model="form.date_naissance"
                type="date"
                :max="today"
                class="form-input pl-10"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
              <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
              Telle qu'indiquée sur la pièce.
            </p>
          </div>
          <div>
            <label class="form-label">
              Lieu de naissance <span class="text-rouge">*</span>
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🏙️</span>
              <input
                v-model="form.lieu_naissance"
                type="text"
                placeholder="Ex : Lomé, Kpalimé, Sokodé"
                maxlength="100"
                class="form-input pl-10"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
              <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
              Tel qu'indiqué sur la pièce.
            </p>
          </div>
        </div>

        <!-- Profession -->
        <div>
          <label class="form-label">
            Profession <span class="text-rouge">*</span>
          </label>
          <div class="relative">
            <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">💼</span>
            <input
              v-model="form.profession"
              type="text"
              placeholder="Ex : Commerçant, Enseignant, Étudiant, Fonctionnaire"
              maxlength="100"
              class="form-input pl-10"
            />
          </div>
          <p class="text-xs text-gray-400 mt-1.5 flex items-start gap-1">
            <span class="text-[#D97706] flex-shrink-0">ℹ️</span>
            Telle qu'indiquée sur votre pièce d'identité.
          </p>
        </div>

        <!-- Séparateur circonstances -->
        <div class="flex items-center gap-3">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Circonstances</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- Date + Lieu de la perte/trouvaille -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="form-label">
              Date de la {{ form.type_declaration === 'PERTE' ? 'perte' : 'trouvaille' }}
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">📅</span>
              <input
                v-model="form.date_perte"
                type="date"
                :max="today"
                class="form-input pl-10"
              />
            </div>
          </div>
          <div>
            <label class="form-label">
              Lieu de la {{ form.type_declaration === 'PERTE' ? 'perte' : 'trouvaille' }}
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">📍</span>
              <input
                v-model="form.lieu_perte"
                type="text"
                placeholder="Ex : Marché de Lomé, Avenue de la Paix"
                maxlength="300"
                class="form-input pl-10"
              />
            </div>
          </div>
        </div>

        <!-- Description -->
        <div>
          <label class="form-label">
            Description <span class="text-gray-400 normal-case font-normal">(optionnel)</span>
          </label>
          <textarea
            v-model="form.description"
            rows="3"
            placeholder="Décrivez les circonstances de la perte ou trouvaille, signes particuliers de la pièce…"
            maxlength="1000"
            class="form-input resize-none"
          ></textarea>
          <p class="text-xs text-gray-400 mt-1 text-right">
            {{ form.description.length }}/1000
          </p>
        </div>

        <!-- Upload Photo -->
        <div>
          <label class="form-label">
            Photo de la pièce <span class="text-gray-400 normal-case font-normal">(optionnel — max 5 MB)</span>
          </label>

          <!-- Aperçu photo -->
          <div v-if="photoPreview" class="relative mb-3 inline-block">
            <img :src="photoPreview" alt="Aperçu"
              class="h-28 w-auto rounded-xl object-cover border-2 border-[#005A3C]/30 shadow-md"/>
            <button type="button"
              @click="removePhoto"
              class="absolute -top-2 -right-2 w-6 h-6 bg-[#C41230] text-white rounded-full
                     flex items-center justify-center text-xs border-2 border-white cursor-pointer
                     shadow-md hover:bg-[#e8192f] transition-colors">✕</button>
          </div>

          <!-- Zone de drop -->
          <div v-if="!photoPreview"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            :class="[
              'border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer',
              isDragging
                ? 'border-[#005A3C] bg-[#E8F4F0]'
                : 'border-gray-200 bg-gray-50 hover:border-gray-300'
            ]"
            @click="$refs.photoInput.click()">
            <span class="text-3xl block mb-2">📷</span>
            <p class="text-sm text-gray-500 mb-1">Cliquez ou glissez une image</p>
            <p class="text-xs text-gray-400">JPG, PNG — max 5 MB</p>
          </div>
          <input ref="photoInput" type="file" accept="image/jpeg,image/jpg,image/png"
            class="hidden" @change="handlePhotoChange"/>
        </div>

      </div>

      <!-- Pied de carte -->
      <div class="flex items-center justify-between pt-6 mt-6 border-t border-gray-100">
        <button type="button" @click="goBack"
          class="flex items-center gap-2 text-sm font-medium text-gray-500 bg-white
                 border border-gray-200 px-5 py-3 rounded-[10px] cursor-pointer
                 hover:bg-gray-50 transition-all">
          ← Retour
        </button>
        <div class="flex items-center gap-3">
          <span v-if="!step2Valid" class="text-xs text-gray-400">
            Nom, prénom et informations d'identité requis
          </span>
          <button type="button"
            @click="goNext"
            :disabled="!step2Valid"
            class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                   text-sm px-6 py-3 rounded-[10px] border-none cursor-pointer
                   transition-all hover:bg-[#007A52] hover:-translate-y-0.5
                   disabled:opacity-40 disabled:cursor-not-allowed disabled:translate-y-0">
            Vérifier →
          </button>
        </div>
      </div>

    </div>
  </div>
  </transition>


  <!-- ════════════════════════════════════════
       ÉTAPE 3 — Récapitulatif + Confirmation
  ════════════════════════════════════════ -->
  <transition name="fade-step" mode="out-in">
  <div v-if="step === 3" key="s3" class="max-w-2xl mx-auto fade-up">

    <!-- Erreur API -->
    <transition name="slide-error">
      <div v-if="apiError"
        class="flex items-start gap-3 bg-red-50 border border-red-200
               rounded-xl p-4 mb-5 text-sm text-rouge">
        <span class="text-lg leading-none mt-0.5">⚠️</span>
        <span>{{ apiError }}</span>
      </div>
    </transition>

    <div class="card">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-10 h-10 bg-[#E8F4F0] rounded-full flex items-center justify-center text-lg">
          👁️
        </div>
        <div>
          <h2 class="font-serif text-lg font-bold text-[#1A2E22]">
            Vérifiez votre déclaration
          </h2>
          <p class="text-xs text-gray-500">Relisez avant de confirmer — aucune modification possible après soumission.</p>
        </div>
      </div>

      <!-- Bloc type -->
      <div class="rounded-xl p-4 mb-4 border-l-4"
        :style="{
          borderColor: typeColor,
          backgroundColor: form.type_declaration === 'PERTE' ? '#FEF2F2' : '#F0FDF4'
        }">
        <div class="flex items-center gap-2 mb-1">
          <span class="text-lg">{{ form.type_declaration === 'PERTE' ? '😟' : '🤲' }}</span>
          <span class="font-bold text-sm" :style="{ color: typeColor }">
            Déclaration de {{ typeLabel.toUpperCase() }}
          </span>
        </div>
        <p class="text-xs text-gray-500">
          Catégorie : <strong>{{ selectedCategory?.libelle }}</strong>
        </p>
      </div>

      <!-- Tableau récap -->
      <div class="rounded-xl border border-gray-200 overflow-hidden mb-6">
        <div v-for="(row, i) in [
          { label: 'Numéro de la pièce',  value: form.numero_piece.trim().toUpperCase() || 'Non communiqué', mono: true },
          { label: 'Nom de famille',       value: form.nom.trim().toUpperCase() },
          { label: 'Prénom(s)',            value: form.prenom.trim() },
          { label: 'Date de naissance',    value: form.date_naissance || '—' },
          { label: 'Lieu de naissance',    value: form.lieu_naissance || '—' },
          { label: 'Profession',           value: form.profession || '—' },
          { label: 'Date de la ' + (form.type_declaration === 'PERTE' ? 'perte' : 'trouvaille'), value: form.date_perte || '—' },
          { label: 'Lieu',                 value: form.lieu_perte || '—' },
          { label: 'Description',          value: form.description || '—' },
          { label: 'Photo',                value: form.photo_piece ? form.photo_piece.name : 'Non fournie' },
        ]" :key="row.label"
          :class="[
            'flex items-start gap-3 px-4 py-3 text-sm',
            i % 2 === 0 ? 'bg-gray-50' : 'bg-white'
          ]">
          <span class="text-xs text-gray-500 font-medium w-36 flex-shrink-0 pt-0.5">
            {{ row.label }}
          </span>
          <span :class="['text-[#1A2E22] break-all', row.mono && 'font-mono font-bold tracking-wider text-[#005A3C]']">
            {{ row.value }}
          </span>
        </div>
      </div>

      <!-- Aperçu photo si dispo -->
      <div v-if="photoPreview" class="mb-6">
        <p class="text-xs text-gray-500 mb-2 font-medium">Aperçu de la photo jointe :</p>
        <img :src="photoPreview" alt="Photo de la pièce"
          class="h-24 w-auto rounded-xl object-cover border border-gray-200 shadow-sm"/>
      </div>

      <!-- Note légale -->
      <div class="bg-[#FFFBEB] border border-yellow-200 rounded-xl p-4 mb-6">
        <p class="text-xs text-yellow-700 leading-relaxed">
          ⚠️ <strong>Déclaration sur l'honneur.</strong> Toute fausse déclaration est punissable par la loi togolaise.
          En soumettant ce formulaire, vous certifiez l'exactitude des informations fournies.
        </p>
      </div>

      <!-- Boutons -->
      <div class="flex items-center justify-between">
        <button type="button" @click="goBack"
          :disabled="submitting"
          class="flex items-center gap-2 text-sm font-medium text-gray-500 bg-white
                 border border-gray-200 px-5 py-3 rounded-[10px] cursor-pointer
                 hover:bg-gray-50 transition-all disabled:opacity-50">
          ← Modifier
        </button>
        <button type="button"
          @click="handleSubmit"
          :disabled="submitting"
          class="flex items-center gap-2.5 font-bold text-sm px-8 py-3.5
                 rounded-[10px] border-none cursor-pointer transition-all
                 hover:-translate-y-0.5 hover:shadow-lg
                 disabled:opacity-60 disabled:cursor-not-allowed disabled:translate-y-0"
          :style="{
            backgroundColor: typeColor,
            color: 'white',
            boxShadow: submitting ? 'none' : `0 4px 16px ${typeColor}50`
          }">
          <span v-if="submitting" class="loader-dot"></span>
          <span v-else>✅</span>
          <span>{{ submitting ? 'Envoi en cours...' : 'Confirmer la déclaration' }}</span>
        </button>
      </div>

    </div>
  </div>
  </transition>


  <!-- ════════════════════════════════════════
       ÉTAPE 4 — SUCCÈS 🎉
  ════════════════════════════════════════ -->
  <transition name="zoom-in" mode="out-in">
  <div v-if="step === 4" key="s4" class="max-w-xl mx-auto text-center py-4 fade-up">

    <!-- Cercle animé succès -->
    <div class="relative inline-flex items-center justify-center mb-6">
      <div class="w-24 h-24 rounded-full flex items-center justify-center text-4xl
                  shadow-xl"
        :style="{
          backgroundColor: form.type_declaration === 'PERTE' ? '#C41230' : '#005A3C'
        }">
        🎉
      </div>
      <!-- Cercle pulsant -->
      <div class="absolute inset-0 rounded-full animate-ping opacity-20"
        :style="{ backgroundColor: form.type_declaration === 'PERTE' ? '#C41230' : '#005A3C' }">
      </div>
    </div>

    <div class="inline-block bg-[#E8F4F0] text-[#005A3C] text-xs font-bold
                px-4 py-1.5 rounded-full mb-3">
      ✓ Déclaration enregistrée
    </div>

    <h2 class="font-serif text-[2rem] font-bold text-[#1A2E22] mb-3 leading-tight">
      Votre déclaration<br/>a bien été reçue !
    </h2>
    <p class="text-sm text-gray-500 max-w-sm mx-auto mb-6 leading-relaxed">
      Votre récépissé officiel est disponible. Vous serez notifié dès qu'une
      correspondance sera trouvée dans notre base de données.
    </p>

    <!-- Numéro de récépissé -->
    <div v-if="createdDecl" class="bg-white rounded-xl border-2 border-[#005A3C]/20
                                   p-5 mb-6 shadow-card">
      <p class="text-xs text-gray-500 mb-1">Numéro de récépissé</p>
      <div class="font-mono text-xl font-bold text-[#005A3C] tracking-wider">
        {{ createdDecl.numero_recepisse }}
      </div>
      <p class="text-xs text-gray-400 mt-2">
        Conservez ce numéro pour suivre votre déclaration.
      </p>
    </div>

    <!-- Erreur PDF -->
    <transition name="slide-error">
      <div v-if="apiError"
        class="flex items-start gap-3 bg-red-50 border border-red-200
               rounded-xl p-3 mb-4 text-sm text-rouge text-left">
        <span>⚠️</span><span>{{ apiError }}</span>
      </div>
    </transition>

    <!-- Actions -->
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <button type="button"
        @click="downloadPDF"
        class="inline-flex items-center justify-center gap-2.5 bg-[#005A3C] text-white
               font-bold px-6 py-3.5 rounded-[10px] border-none cursor-pointer
               transition-all hover:bg-[#007A52] hover:-translate-y-0.5 hover:shadow-lg text-sm">
        📄 Télécharger mon récépissé PDF
      </button>

      <router-link :to="{ name: 'mes-declarations' }"
        class="inline-flex items-center justify-center gap-2.5 bg-white text-[#005A3C]
               font-semibold px-6 py-3.5 rounded-[10px] border border-[#005A3C]/30
               transition-all hover:bg-[#E8F4F0] hover:-translate-y-0.5 text-sm no-underline">
        📋 Voir mes déclarations
      </router-link>
    </div>

    <!-- Lien nouvelle déclaration -->
    <div class="mt-6">
      <button type="button"
        @click="() => { step = 1; form = { type_declaration: '', categorie: null, numero_piece: '', nom: '', prenom: '', date_naissance: '', lieu_naissance: '', profession: '', description: '', lieu_perte: '', date_perte: '', photo_piece: null }; photoPreview = null; createdDecl = null; apiError = null }"
        class="text-xs text-gray-400 hover:text-[#005A3C] bg-transparent
               border-none cursor-pointer transition-colors">
        + Faire une nouvelle déclaration
      </button>
    </div>

  </div>
  </transition>

</div>
</template>

<style scoped>
/* Transitions wizard */
.fade-step-enter-active,
.fade-step-leave-active { transition: all .3s ease; }
.fade-step-enter-from   { opacity: 0; transform: translateX(24px); }
.fade-step-leave-to     { opacity: 0; transform: translateX(-24px); }

/* Zoom succès */
.zoom-in-enter-active { transition: all .4s cubic-bezier(.175,.885,.32,1.275); }
.zoom-in-enter-from   { opacity: 0; transform: scale(.85); }

/* Erreur */
.slide-error-enter-active,
.slide-error-leave-active { transition: all .25s ease; }
.slide-error-enter-from,
.slide-error-leave-to { opacity: 0; transform: translateY(-8px); }

/* Spinner */
.loader-dot {
  display: inline-block;
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Input uppercase trick */
input.uppercase { text-transform: uppercase; }
input.uppercase::placeholder { text-transform: none; }
</style>
```

## File: frontend/src/views/citizen/MyDeclarationsView.vue
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { declarationsAPI } from '../../services/api'
import { useAuthStore } from '../../stores/auth'

const router    = useRouter()
const authStore = useAuthStore()

/* ══ État ══ */
const declarations = ref([])
const loading      = ref(true)
const apiError     = ref(null)
const filterType   = ref('ALL')    // ALL | PERTE | TROUVAILLE
const filterStatut = ref('ALL')
const downloading  = ref(null)     // id en cours de download

/* ══ Chargement ══ */
onMounted(async () => {
  try {
    const { data } = await declarationsAPI.myDeclarations()
    declarations.value = data.results ?? data
  } catch (e) {
    apiError.value = 'Impossible de charger vos déclarations.'
  } finally {
    loading.value = false
  }
})

/* ══ Filtrage ══ */
const filtered = computed(() => {
  let list = declarations.value
  if (filterType.value !== 'ALL')
    list = list.filter(d => d.type_declaration === filterType.value)
  if (filterStatut.value !== 'ALL')
    list = list.filter(d => d.statut === filterStatut.value)
  return list
})

/* ══ Statistiques ══ */
const stats = computed(() => {
  const d = declarations.value
  return {
    total:     d.length,
    pertes:    d.filter(x => x.type_declaration === 'PERTE').length,
    attente:   d.filter(x => x.statut === 'EN_ATTENTE').length,
    retrouve:  d.filter(x => x.statut === 'RETROUVE').length,
    restitue:  d.filter(x => x.statut === 'RESTITUE').length,
  }
})

/* ══ Téléchargement PDF ══ */
const downloadPDF = async (decl) => {
  downloading.value = decl.id
  try {
    const { data } = await declarationsAPI.downloadPDF(decl.id)
    const url = URL.createObjectURL(new Blob([data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `recepisse_${decl.numero_recepisse}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch {
    apiError.value = 'Erreur lors de la génération du PDF.'
  } finally {
    downloading.value = null
  }
}

/* ══ Helpers ══ */
const statusConfig = {
  EN_ATTENTE: { label: 'En attente',  color: '#D97706', bg: '#FEF3C7', icon: '⏳' },
  VALIDE:     { label: 'Validé',      color: '#2563EB', bg: '#DBEAFE', icon: '✅' },
  RETROUVE:   { label: 'Retrouvé',    color: '#059669', bg: '#D1FAE5', icon: '🎉' },
  RESTITUE:   { label: 'Restitué',    color: '#065F46', bg: '#A7F3D0', icon: '🤝' },
  REJETE:     { label: 'Rejeté',      color: '#DC2626', bg: '#FEE2E2', icon: '❌' },
  CLOTURE:    { label: 'Clôturé',     color: '#6B7280', bg: '#F3F4F6', icon: '🔒' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

const statuts = Object.entries(statusConfig).map(([k, v]) => ({ key: k, ...v }))
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-4xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-8 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        👤 Espace citoyen
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] mb-1">
        Bonjour, {{ authStore.user?.first_name || authStore.user?.username }} 👋
      </h1>
      <p class="text-sm text-gray-500">
        Suivez l'état de vos déclarations et téléchargez vos récépissés.
      </p>
    </div>
    <router-link :to="{ name: 'declare' }"
      class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
             text-sm px-5 py-3 rounded-xl no-underline hover:bg-[#007A52]
             hover:-translate-y-0.5 transition-all shadow-md flex-shrink-0">
      + Nouvelle déclaration
    </router-link>
  </div>

  <!-- ══ Statistiques ══ -->
  <div v-if="!loading" class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
    <div class="bg-white rounded-xl p-4 shadow-card border border-gray-100 text-center">
      <div class="font-serif text-2xl font-bold text-[#005A3C]">{{ stats.total }}</div>
      <div class="text-xs text-gray-500 mt-0.5">Total</div>
    </div>
    <div class="bg-white rounded-xl p-4 shadow-card border border-gray-100 text-center">
      <div class="font-serif text-2xl font-bold text-yellow-600">{{ stats.attente }}</div>
      <div class="text-xs text-gray-500 mt-0.5">En attente</div>
    </div>
    <div class="bg-white rounded-xl p-4 shadow-card border border-gray-100 text-center">
      <div class="font-serif text-2xl font-bold text-green-600">{{ stats.retrouve }}</div>
      <div class="text-xs text-gray-500 mt-0.5">Retrouvées</div>
    </div>
    <div class="bg-white rounded-xl p-4 shadow-card border border-gray-100 text-center">
      <div class="font-serif text-2xl font-bold text-emerald-700">{{ stats.restitue }}</div>
      <div class="text-xs text-gray-500 mt-0.5">Restituées</div>
    </div>
  </div>

  <!-- Squelettes stats -->
  <div v-else class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
    <div v-for="i in 4" :key="i" class="skeleton h-20 rounded-xl"></div>
  </div>

  <!-- ══ Erreur ══ -->
  <div v-if="apiError"
    class="flex items-center gap-3 bg-red-50 border border-red-200
           rounded-xl p-4 mb-6 text-sm text-rouge">
    <span>⚠️</span><span>{{ apiError }}</span>
  </div>

  <!-- ══ Filtres ══ -->
  <div class="flex items-center gap-2 mb-5 flex-wrap">
    <!-- Type -->
    <div class="flex items-center gap-1 bg-white rounded-xl p-1 border border-gray-200 shadow-sm">
      <button v-for="opt in [
        { key: 'ALL',       label: 'Tous'        },
        { key: 'PERTE',     label: '😟 Pertes'   },
        { key: 'TROUVAILLE',label: '🤲 Trouvailles'},
      ]" :key="opt.key"
        @click="filterType = opt.key"
        :class="[
          'text-xs font-semibold px-3 py-1.5 rounded-lg transition-all cursor-pointer border-none',
          filterType === opt.key
            ? 'bg-[#005A3C] text-white shadow-sm'
            : 'bg-transparent text-gray-500 hover:text-[#1A2E22]'
        ]">
        {{ opt.label }}
      </button>
    </div>

    <!-- Statut -->
    <select v-model="filterStatut"
      class="bg-white border border-gray-200 rounded-xl px-3 py-2 text-xs
             text-gray-600 outline-none cursor-pointer shadow-sm">
      <option value="ALL">Tous les statuts</option>
      <option v-for="s in statuts" :key="s.key" :value="s.key">
        {{ s.icon }} {{ s.label }}
      </option>
    </select>

    <span class="ml-auto text-xs text-gray-400">
      {{ filtered.length }} résultat{{ filtered.length !== 1 ? 's' : '' }}
    </span>
  </div>

  <!-- ══ Liste squelette ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 4" :key="i" class="skeleton h-28 rounded-2xl"></div>
  </div>

  <!-- ══ Liste vide ══ -->
  <div v-else-if="filtered.length === 0 && declarations.length === 0"
    class="text-center py-16 bg-white rounded-2xl border border-gray-100 shadow-card">
    <div class="text-5xl mb-4">📂</div>
    <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">Aucune déclaration</p>
    <p class="text-sm text-gray-500 mb-6">
      Vous n'avez pas encore fait de déclaration.
    </p>
    <router-link :to="{ name: 'declare' }"
      class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
             text-sm px-6 py-3 rounded-xl no-underline hover:bg-[#007A52] transition-all">
      📋 Faire ma première déclaration
    </router-link>
  </div>

  <!-- Filtre vide -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-12 bg-white rounded-2xl border border-dashed border-gray-200">
    <div class="text-3xl mb-3">🔍</div>
    <p class="text-sm text-gray-500">Aucune déclaration ne correspond aux filtres.</p>
    <button @click="filterType = 'ALL'; filterStatut = 'ALL'"
      class="mt-3 text-xs text-[#005A3C] font-semibold bg-transparent border-none cursor-pointer hover:underline">
      Réinitialiser les filtres
    </button>
  </div>

  <!-- ══ Cartes déclarations ══ -->
  <div v-else class="space-y-3">
    <transition-group name="list-item">
      <div v-for="decl in filtered" :key="decl.id"
        class="bg-white rounded-2xl border border-gray-100 shadow-card
               hover:shadow-card-lg hover:-translate-y-0.5 transition-all">

        <div class="p-5 flex flex-col sm:flex-row items-start gap-4">

          <!-- Icône type -->
          <div class="w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
            :style="{
              backgroundColor: decl.type_declaration === 'PERTE' ? '#FEE2E2' : '#E8F4F0'
            }">
            {{ decl.type_declaration === 'PERTE' ? '😟' : '🤲' }}
          </div>

          <!-- Contenu principal -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-2 flex-wrap mb-1.5">
              <div>
                <span class="font-mono font-bold text-[#005A3C] text-sm tracking-wider">
                  {{ decl.numero_piece }}
                </span>
                <span class="mx-2 text-gray-300">·</span>
                <span class="text-sm font-semibold text-[#1A2E22]">
                  {{ decl.nom_sur_piece }}
                </span>
              </div>
              <span class="badge text-xs flex-shrink-0"
                :style="{
                  color: getStatus(decl.statut).color,
                  backgroundColor: getStatus(decl.statut).bg
                }">
                {{ getStatus(decl.statut).icon }} {{ getStatus(decl.statut).label }}
              </span>
            </div>

            <div class="flex items-center gap-3 text-xs text-gray-400 flex-wrap">
              <span>📅 {{ formatDate(decl.date_declaration) }}</span>
              <span v-if="decl.categorie_nom">📁 {{ decl.categorie_nom }}</span>
              <span v-if="decl.lieu_perte">📍 {{ decl.lieu_perte }}</span>
              <span class="font-mono text-[10px] text-gray-300">{{ decl.numero_recepisse }}</span>
            </div>

            <!-- Alerte match -->
            <div v-if="decl.statut === 'RETROUVE'"
              class="mt-2 inline-flex items-center gap-1.5 bg-green-50 text-green-700
                     text-xs font-semibold px-3 py-1.5 rounded-lg">
              🎉 Correspondance trouvée — Voir les détails
            </div>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0 sm:self-center">
            <!-- Télécharger PDF -->
            <button @click="downloadPDF(decl)"
              :disabled="downloading === decl.id"
              class="flex items-center gap-1.5 text-xs font-semibold
                     text-[#005A3C] bg-[#E8F4F0] hover:bg-[#d0ece3]
                     px-3 py-2 rounded-lg border-none cursor-pointer
                     transition-all disabled:opacity-50 disabled:cursor-wait">
              <span v-if="downloading === decl.id" class="loader-dot-xs"></span>
              <span v-else>📄</span>
              PDF
            </button>
            <!-- Voir détail -->
            <button @click="router.push({ name: 'declaration-detail', params: { id: decl.id } })"
              class="flex items-center gap-1.5 text-xs font-semibold
                     text-gray-600 bg-gray-100 hover:bg-gray-200
                     px-3 py-2 rounded-lg border-none cursor-pointer transition-all">
              Détails →
            </button>
          </div>

        </div>

        <!-- Barre de statut en bas de carte (couleur) -->
        <div class="h-0.5 rounded-b-2xl transition-all"
          :style="{ backgroundColor: getStatus(decl.statut).color, opacity: 0.4 }">
        </div>

      </div>
    </transition-group>
  </div>

</div>
</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .25s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(10px); }

.loader-dot-xs {
  display: inline-block;
  width: 12px; height: 12px;
  border: 2px solid rgba(0,90,60,.2);
  border-top-color: #005A3C;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

## File: frontend/src/views/citizen/NotificationsView.vue
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { notificationsAPI } from '../../services/api'

const router = useRouter()

/* ══ État ══ */
const notifications = ref([])
const loading       = ref(true)
const markingAll    = ref(false)
const filterType    = ref('ALL')   // ALL | MATCH | STATUT | INFO | ADMIN

/* ══ Chargement ══ */
onMounted(async () => {
  try {
    const { data } = await notificationsAPI.list()
    notifications.value = data.results ?? data
  } catch {}
  finally { loading.value = false }
})

/* ══ Filtrage ══ */
const filtered = computed(() => {
  if (filterType.value === 'ALL') return notifications.value
  return notifications.value.filter(n => n.type_notification === filterType.value)
})

const unreadCount = computed(() =>
  notifications.value.filter(n => !n.lue).length
)

/* ══ Actions ══ */
const markOne = async (notif) => {
  if (notif.lue) return
  try {
    await notificationsAPI.marquerLue(notif.id)
    notif.lue = true
  } catch {}
}

const markAll = async () => {
  if (!unreadCount.value) return
  markingAll.value = true
  try {
    await notificationsAPI.toutMarquer()
    notifications.value.forEach(n => { n.lue = true })
  } catch {}
  finally { markingAll.value = false }
}

/* ══ Naviguer vers la déclaration liée ══ */
const openNotif = (notif) => {
  markOne(notif)
  if (notif.declaration) {
    router.push({ name: 'declaration-detail', params: { id: notif.declaration } })
  }
}

/* ══ Helpers ══ */
const typeConfig = {
  MATCH:  { label: 'Correspondance', icon: '🎉', color: '#059669', bg: '#D1FAE5' },
  STATUT: { label: 'Statut',         icon: '📊', color: '#2563EB', bg: '#DBEAFE' },
  INFO:   { label: 'Information',    icon: 'ℹ️',  color: '#6B7280', bg: '#F3F4F6' },
  ADMIN:  { label: 'Administrateur', icon: '💬',  color: '#D97706', bg: '#FEF3C7' },
}
const getType = (t) => typeConfig[t] || typeConfig.INFO

const formatDate = (d) => {
  if (!d) return '—'
  const date = new Date(d)
  const now  = new Date()
  const diff = Math.floor((now - date) / 1000)

  if (diff < 60)   return 'À l\'instant'
  if (diff < 3600) return `Il y a ${Math.floor(diff / 60)} min`
  if (diff < 86400)return `Il y a ${Math.floor(diff / 3600)} h`
  if (diff < 604800) return `Il y a ${Math.floor(diff / 86400)} j`
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}

const typeFilters = [
  { key: 'ALL',   label: 'Toutes' },
  { key: 'MATCH', label: '🎉 Correspondances' },
  { key: 'STATUT',label: '📊 Statuts' },
  { key: 'INFO',  label: 'ℹ️ Infos' },
  { key: 'ADMIN', label: '💬 Admin' },
]
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-2xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="flex items-start justify-between gap-4 mb-6 flex-wrap">
    <div>
      <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                  text-xs font-bold px-3 py-1.5 rounded-full mb-3">
        🔔 Notifications
      </div>
      <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22] flex items-center gap-3">
        Mes notifications
        <span v-if="unreadCount > 0"
          class="text-sm font-bold bg-[#C41230] text-white px-2.5 py-0.5 rounded-full">
          {{ unreadCount }}
        </span>
      </h1>
    </div>
    <button v-if="unreadCount > 0"
      @click="markAll"
      :disabled="markingAll"
      class="flex items-center gap-2 text-xs font-semibold text-[#005A3C]
             bg-[#E8F4F0] border border-[#005A3C]/20 px-4 py-2.5 rounded-xl
             cursor-pointer hover:bg-[#d0ece3] transition-all disabled:opacity-50 border-none">
      <span v-if="markingAll" class="loader-dot-sm"></span>
      <span v-else>✓✓</span>
      Tout marquer comme lu
    </button>
  </div>

  <!-- ══ Filtres ══ -->
  <div class="flex items-center gap-1 bg-white rounded-xl p-1 border border-gray-200
              shadow-sm mb-5 overflow-x-auto">
    <button v-for="f in typeFilters" :key="f.key"
      @click="filterType = f.key"
      :class="[
        'text-xs font-semibold px-3 py-2 rounded-lg whitespace-nowrap transition-all cursor-pointer border-none flex-shrink-0',
        filterType === f.key
          ? 'bg-[#005A3C] text-white shadow-sm'
          : 'bg-transparent text-gray-500 hover:text-[#1A2E22]'
      ]">
      {{ f.label }}
    </button>
  </div>

  <!-- ══ Squelettes ══ -->
  <div v-if="loading" class="space-y-3">
    <div v-for="i in 5" :key="i" class="skeleton h-20 rounded-2xl"></div>
  </div>

  <!-- ══ Vide ══ -->
  <div v-else-if="notifications.length === 0"
    class="text-center py-20 bg-white rounded-2xl shadow-card border border-gray-100">
    <div class="text-5xl mb-4">🔕</div>
    <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">Aucune notification</p>
    <p class="text-sm text-gray-500">
      Vous serez notifié dès qu'une correspondance sera trouvée.
    </p>
  </div>

  <!-- Filtre vide -->
  <div v-else-if="filtered.length === 0"
    class="text-center py-12 bg-white rounded-2xl border border-dashed border-gray-200">
    <div class="text-3xl mb-3">🔍</div>
    <p class="text-sm text-gray-500">Aucune notification dans cette catégorie.</p>
    <button @click="filterType = 'ALL'"
      class="mt-2 text-xs text-[#005A3C] font-semibold bg-transparent border-none cursor-pointer hover:underline">
      Voir toutes les notifications
    </button>
  </div>

  <!-- ══ Liste ══ -->
  <div v-else class="space-y-2">
    <transition-group name="list-item">
      <div v-for="notif in filtered" :key="notif.id"
        @click="openNotif(notif)"
        :class="[
          'rounded-2xl border transition-all cursor-pointer',
          'hover:-translate-y-0.5 hover:shadow-card-lg',
          notif.lue
            ? 'bg-white border-gray-100 shadow-sm'
            : 'bg-white border-[#005A3C]/20 shadow-card'
        ]">
        <div class="p-4 flex items-start gap-4">

          <!-- Icône type -->
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-lg
                      flex-shrink-0 relative"
            :style="{ backgroundColor: getType(notif.type_notification).bg }">
            {{ getType(notif.type_notification).icon }}
            <!-- Pastille non-lue -->
            <div v-if="!notif.lue"
              class="absolute -top-1 -right-1 w-3 h-3 bg-[#C41230] rounded-full
                     border-2 border-white">
            </div>
          </div>

          <!-- Contenu -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between gap-2">
              <p :class="['text-sm leading-snug', notif.lue ? 'text-gray-600' : 'font-semibold text-[#1A2E22]']">
                {{ notif.titre }}
              </p>
              <span class="text-xs text-gray-400 flex-shrink-0 mt-0.5">
                {{ formatDate(notif.date_creation) }}
              </span>
            </div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed line-clamp-2">
              {{ notif.message }}
            </p>

            <!-- Badge type + lien si déclaration liée -->
            <div class="flex items-center gap-2 mt-2">
              <span class="badge text-[10px]"
                :style="{
                  color: getType(notif.type_notification).color,
                  backgroundColor: getType(notif.type_notification).bg
                }">
                {{ getType(notif.type_notification).label }}
              </span>
              <span v-if="notif.declaration" class="text-[10px] text-gray-400">
                → Voir la déclaration
              </span>
              <span v-if="notif.lue" class="text-[10px] text-gray-300 ml-auto">Lu</span>
            </div>
          </div>

        </div>

        <!-- Barre colorée bas si non lue -->
        <div v-if="!notif.lue" class="h-0.5 rounded-b-2xl"
          :style="{ backgroundColor: getType(notif.type_notification).color, opacity: 0.35 }">
        </div>

      </div>
    </transition-group>
  </div>

</div>
</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .25s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(8px); }
.line-clamp-2 {
  display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden;
}
.loader-dot-sm {
  display: inline-block; width: 12px; height: 12px;
  border: 2px solid rgba(0,90,60,.2); border-top-color: #005A3C;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

## File: frontend/src/views/citizen/ProfileView.vue
```vue
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()

/* ══ État ══ */
const tab          = ref('info')   // 'info' | 'password'
const submitting   = ref(false)
const success      = ref(null)
const apiError     = ref(null)
const submitted    = ref(false)

/* ══ Formulaire infos ══ */
const form = ref({
  first_name: '',
  last_name:  '',
  email:      '',
  telephone:  '',
})

/* ══ Formulaire mot de passe ══ */
const pwdForm = ref({
  current_password: '',
  new_password:     '',
  confirm_password: '',
})
const showPwd = ref({ current: false, new: false, confirm: false })

/* ══ Pré-remplir depuis le store ══ */
onMounted(() => {
  const u = authStore.user
  if (!u) return
  form.value = {
    first_name: u.first_name || '',
    last_name:  u.last_name  || '',
    email:      u.email      || '',
    telephone:  u.telephone  || '',
  }
})

/* ══ Validation ══ */
const infoErrors = computed(() => {
  if (!submitted.value) return {}
  const e = {}
  if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email))
    e.email = 'Adresse email invalide'
  if (form.value.telephone && !/^(\+228)?[0-9]{8}$/.test(form.value.telephone.replace(/\s/g, '')))
    e.telephone = "Format : +22890123456 ou 90123456"
  return e
})

const pwdErrors = computed(() => {
  if (!submitted.value) return {}
  const e = {}
  if (!pwdForm.value.current_password)       e.current = 'Requis'
  if (pwdForm.value.new_password.length < 8) e.new = 'Minimum 8 caractères'
  if (!/[A-Z]/.test(pwdForm.value.new_password)) e.new = 'Au moins une majuscule'
  if (!/[0-9]/.test(pwdForm.value.new_password)) e.new = 'Au moins un chiffre'
  if (pwdForm.value.new_password !== pwdForm.value.confirm_password)
    e.confirm = 'Les mots de passe ne correspondent pas'
  return e
})

/* ══ Sauvegarde infos ══ */
const saveInfo = async () => {
  submitted.value = true
  if (Object.keys(infoErrors.value).length) return
  submitting.value = true
  success.value    = null
  apiError.value   = null
  const result = await authStore.updateProfile(form.value)
  if (result.success) {
    success.value = 'Profil mis à jour avec succès !'
  } else {
    apiError.value = result.error
  }
  submitting.value = false
  submitted.value  = false
}

/* ══ Changer mot de passe (via updateProfile) ══ */
const savePassword = async () => {
  submitted.value = true
  if (Object.keys(pwdErrors.value).length) return
  submitting.value = true
  success.value    = null
  apiError.value   = null
  try {
    await api.post('change-password/', {
      current_password: pwdForm.value.current_password,
      new_password:     pwdForm.value.new_password,
    })
    success.value = 'Mot de passe modifié avec succès !'
    pwdForm.value = { current_password: '', new_password: '', confirm_password: '' }
  } catch (e) {
    apiError.value = e.response?.data?.current_password
                  || e.response?.data?.new_password
                  || 'Erreur lors du changement.'
  } finally {
    submitting.value = false
    submitted.value  = false
  }
}

/* ══ Initiale avatar ══ */
const initials = computed(() => {
  const u = authStore.user
  if (!u) return '?'
  if (u.first_name && u.last_name)
    return (u.first_name[0] + u.last_name[0]).toUpperCase()
  return u.username?.[0]?.toUpperCase() || '?'
})

const roleLabel = {
  citoyen: { text: 'Citoyen',          bg: '#E8F4F0', color: '#005A3C' },
  police:  { text: 'Agent de Police',  bg: '#DBEAFE', color: '#2563EB' },
  admin:   { text: 'Administrateur',   bg: '#FEE2E2', color: '#C41230' },
}
const role = computed(() => roleLabel[authStore.user?.role] || roleLabel.citoyen)

const clearMessages = () => { success.value = null; apiError.value = null; submitted.value = false }
</script>

<template>
<div class="min-h-screen py-10 px-4" style="background:#FAF7F2">
<div class="max-w-2xl mx-auto">

  <!-- ══ En-tête ══ -->
  <div class="mb-8">
    <div class="inline-flex items-center gap-2 bg-[#E8F4F0] text-[#005A3C]
                text-xs font-bold px-3 py-1.5 rounded-full mb-3">
      👤 Mon profil
    </div>
    <h1 class="font-serif text-[1.9rem] font-bold text-[#1A2E22]">
      Gérer mon compte
    </h1>
  </div>

  <!-- ══ Carte avatar ══ -->
  <div class="bg-white rounded-2xl shadow-card border border-gray-100 p-6 mb-5
              flex items-center gap-5 flex-wrap">
    <!-- Avatar -->
    <div class="w-16 h-16 rounded-full flex items-center justify-center
                font-serif text-2xl font-bold text-white flex-shrink-0 shadow-lg"
      style="background: linear-gradient(135deg, #005A3C 0%, #007A52 100%)">
      {{ initials }}
    </div>
    <div class="flex-1 min-w-0">
      <h2 class="font-serif text-xl font-bold text-[#1A2E22] truncate">
        {{ authStore.user?.first_name }} {{ authStore.user?.last_name }}
        <span v-if="!authStore.user?.first_name" class="text-gray-400 font-sans font-normal text-base">
          {{ authStore.user?.username }}
        </span>
      </h2>
      <div class="flex items-center gap-2 flex-wrap mt-1">
        <span class="text-sm text-gray-500">@{{ authStore.user?.username }}</span>
        <span class="text-gray-300">·</span>
        <span class="text-xs font-bold px-2 py-0.5 rounded-full"
          :style="{ backgroundColor: role.bg, color: role.color }">
          {{ role.text }}
        </span>
      </div>
    </div>
    <div class="text-right text-xs text-gray-400">
      <div>{{ authStore.user?.nombre_declarations || 0 }} déclaration(s)</div>
      <div class="mt-0.5">Membre depuis {{ authStore.user?.date_creation
        ? new Date(authStore.user.date_creation).toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
        : '—' }}</div>
    </div>
  </div>

  <!-- ══ Onglets ══ -->
  <div class="flex gap-1 bg-white rounded-xl p-1 border border-gray-200 shadow-sm mb-5 w-fit">
    <button v-for="t in [
      { key: 'info',     label: '✏️ Informations' },
      { key: 'password', label: '🔐 Mot de passe' },
    ]" :key="t.key"
      @click="tab = t.key; clearMessages()"
      :class="[
        'text-xs font-semibold px-4 py-2 rounded-lg transition-all cursor-pointer border-none',
        tab === t.key
          ? 'bg-[#005A3C] text-white shadow-sm'
          : 'bg-transparent text-gray-500 hover:text-[#1A2E22]'
      ]">
      {{ t.label }}
    </button>
  </div>

  <!-- ══ Feedback ══ -->
  <transition name="slide-msg">
    <div v-if="success"
      class="flex items-center gap-3 bg-green-50 border border-green-200
             rounded-xl p-4 mb-5 text-sm text-green-700">
      <span>✅</span><span>{{ success }}</span>
      <button @click="success = null" class="ml-auto bg-transparent border-none cursor-pointer text-green-400 hover:text-green-600">✕</button>
    </div>
  </transition>
  <transition name="slide-msg">
    <div v-if="apiError"
      class="flex items-center gap-3 bg-red-50 border border-red-200
             rounded-xl p-4 mb-5 text-sm text-rouge">
      <span>⚠️</span><span>{{ apiError }}</span>
      <button @click="apiError = null" class="ml-auto bg-transparent border-none cursor-pointer text-red-300 hover:text-rouge">✕</button>
    </div>
  </transition>

  <!-- ══ Onglet Informations ══ -->
  <transition name="fade-tab" mode="out-in">
  <div v-if="tab === 'info'" key="info" class="bg-white rounded-2xl shadow-card border border-gray-100 p-6">
    <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-5 flex items-center gap-2">
      <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">✏️</span>
      Informations personnelles
    </h2>

    <form @submit.prevent="saveInfo" novalidate class="space-y-4">

      <!-- Prénom / Nom -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="form-label">Prénom</label>
          <input v-model="form.first_name" type="text"
            placeholder="Jean" class="form-input"/>
        </div>
        <div>
          <label class="form-label">Nom de famille</label>
          <input v-model="form.last_name" type="text"
            placeholder="AKODJO" class="form-input"/>
        </div>
      </div>

      <!-- Email -->
      <div>
        <label class="form-label">Adresse email</label>
        <div class="relative">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">✉️</span>
          <input v-model="form.email" type="email"
            placeholder="jean@example.tg"
            :class="['form-input pl-10', infoErrors.email && 'border-rouge ring-2 ring-rouge/15']"/>
        </div>
        <p v-if="infoErrors.email" class="form-error"><span>✕</span> {{ infoErrors.email }}</p>
      </div>

      <!-- Téléphone -->
      <div>
        <label class="form-label">Numéro de téléphone</label>
        <div class="relative">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-sm">🇹🇬</span>
          <input v-model="form.telephone" type="tel"
            placeholder="+22890123456"
            :class="['form-input pl-10', infoErrors.telephone && 'border-rouge ring-2 ring-rouge/15']"/>
        </div>
        <p v-if="infoErrors.telephone" class="form-error"><span>✕</span> {{ infoErrors.telephone }}</p>
      </div>

      <!-- Username (readonly) -->
      <div>
        <label class="form-label">Nom d'utilisateur <span class="text-gray-400 normal-case font-normal">(non modifiable)</span></label>
        <div class="relative">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">@</span>
          <input :value="authStore.user?.username" type="text"
            disabled class="form-input pl-8 bg-gray-50 text-gray-400 cursor-not-allowed"/>
        </div>
      </div>

      <!-- Bouton -->
      <div class="flex items-center justify-end pt-2">
        <button type="submit" :disabled="submitting"
          class="flex items-center gap-2 bg-[#005A3C] text-white font-bold
                 text-sm px-6 py-3 rounded-xl border-none cursor-pointer
                 transition-all hover:bg-[#007A52] hover:shadow-md
                 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="submitting" class="loader-dot"></span>
          <span v-else>💾</span>
          {{ submitting ? 'Enregistrement…' : 'Enregistrer' }}
        </button>
      </div>

    </form>
  </div>
  </transition>

  <!-- ══ Onglet Mot de passe ══ -->
  <transition name="fade-tab" mode="out-in">
  <div v-if="tab === 'password'" key="password" class="bg-white rounded-2xl shadow-card border border-gray-100 p-6">
    <h2 class="font-serif text-base font-bold text-[#1A2E22] mb-5 flex items-center gap-2">
      <span class="w-7 h-7 bg-[#E8F4F0] rounded-lg flex items-center justify-center text-sm">🔐</span>
      Changer le mot de passe
    </h2>

    <form @submit.prevent="savePassword" novalidate class="space-y-4">

      <div v-for="field in [
        { key: 'current', model: 'current_password', label: 'Mot de passe actuel',    show: 'current' },
        { key: 'new',     model: 'new_password',     label: 'Nouveau mot de passe',   show: 'new'     },
        { key: 'confirm', model: 'confirm_password', label: 'Confirmer le mot de passe', show: 'confirm' },
      ]" :key="field.key">
        <label class="form-label">{{ field.label }}</label>
        <div class="relative">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-sm">🔒</span>
          <input v-model="pwdForm[field.model]"
            :type="showPwd[field.show] ? 'text' : 'password'"
            :placeholder="field.label"
            :class="['form-input pl-10 pr-12', pwdErrors[field.key] && 'border-rouge ring-2 ring-rouge/15']"/>
          <button type="button"
            @click="showPwd[field.show] = !showPwd[field.show]"
            class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400
                   hover:text-gray-600 text-base bg-transparent border-none cursor-pointer">
            {{ showPwd[field.show] ? '🙈' : '👁️' }}
          </button>
        </div>
        <p v-if="pwdErrors[field.key]" class="form-error"><span>✕</span> {{ pwdErrors[field.key] }}</p>
      </div>

      <!-- Critères -->
      <ul class="text-xs bg-gray-50 rounded-xl p-3 space-y-1 list-none pl-0">
        <li v-for="rule in [
          { ok: pwdForm.new_password.length >= 8,            text: 'Minimum 8 caractères' },
          { ok: /[A-Z]/.test(pwdForm.new_password),          text: 'Au moins une majuscule' },
          { ok: /[0-9]/.test(pwdForm.new_password),          text: 'Au moins un chiffre' },
          { ok: pwdForm.new_password === pwdForm.confirm_password && pwdForm.new_password.length > 0,
            text: 'Mots de passe identiques' },
        ]" :key="rule.text"
          :class="['flex items-center gap-2', rule.ok ? 'text-[#005A3C]' : 'text-gray-400']">
          <span>{{ rule.ok ? '✓' : '○' }}</span> {{ rule.text }}
        </li>
      </ul>

      <div class="flex items-center justify-end pt-2">
        <button type="submit" :disabled="submitting"
          class="flex items-center gap-2 bg-[#C41230] text-white font-bold
                 text-sm px-6 py-3 rounded-xl border-none cursor-pointer
                 transition-all hover:bg-[#e8192f] hover:shadow-md
                 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="submitting" class="loader-dot"></span>
          <span v-else>🔐</span>
          {{ submitting ? 'Mise à jour…' : 'Changer le mot de passe' }}
        </button>
      </div>

    </form>
  </div>
  </transition>

  <!-- ══ Zone danger ══ -->
  <div class="mt-5 bg-white rounded-2xl shadow-card border border-gray-100 p-5">
    <h3 class="font-serif text-sm font-bold text-rouge mb-3">Zone de déconnexion</h3>
    <p class="text-xs text-gray-500 mb-3">
      Votre session sera terminée et vous serez redirigé vers la page d'accueil.
    </p>
    <button @click="authStore.logout()"
      class="flex items-center gap-2 bg-red-50 text-rouge font-semibold
             text-xs px-5 py-2.5 rounded-xl border border-red-200
             cursor-pointer hover:bg-red-100 transition-all">
      🚪 Se déconnecter
    </button>
  </div>

</div>
</div>
</template>

<style scoped>
.fade-tab-enter-active, .fade-tab-leave-active { transition: all .2s ease; }
.fade-tab-enter-from, .fade-tab-leave-to { opacity: 0; transform: translateX(10px); }
.slide-msg-enter-active, .slide-msg-leave-active { transition: all .25s ease; }
.slide-msg-enter-from, .slide-msg-leave-to { opacity: 0; transform: translateY(-6px); }
.loader-dot {
  display: inline-block; width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3); border-top-color: #fff;
  border-radius: 50%; animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

## File: frontend/src/views/HomeView.vue
```vue
<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()

const searchQuery    = ref('')
const searchCategory = ref('')

const handleSearch = () => {
  router.push({ name: 'search', query: {
    q:  searchQuery.value,
    cat: searchCategory.value,
  }})
}

const stats = [
  { num: '2 847', suffix: '+', key: 'declarations' },
  { num: '1 203', suffix: '+', key: 'found' },
  { num: '847',   suffix: '+', key: 'citizens' },
  { num: '42',    suffix: '%', key: 'rate' },
]

const features = [
  { icon: '🤝', key: 'matching' },
  { icon: '📄', key: 'pdf' },
  { icon: '🔔', key: 'notif' },
  { icon: '🔒', key: 'security' },
  { icon: '📱', key: 'mobile' },
  { icon: '🗂️', key: 'admin' },
]

const categories = [
  { icon: '🪪', key: 'identity', sub: 'CNI, Passeport' },
  { icon: '🚗', key: 'vehicle',  sub: 'Carte grise, Permis' },
  { icon: '🎓', key: 'school',   sub: 'Diplômes, Certificats' },
  { icon: '💳', key: 'bank',     sub: 'Cartes, Chéquiers' },
  { icon: '💼', key: 'pro',      sub: 'Badges, Cartes pro' },
  { icon: '🏥', key: 'health',   sub: 'Carnet, Assurance' },
  { icon: '📂', key: 'other',    sub: 'Tout document admin' },
]

const chips = ['CNI', 'Passeport', 'Carte grise', 'Permis', 'Diplôme']
</script>

<template>
  <section class="relative min-h-[92vh] grid grid-cols-1 md:grid-cols-2
                  items-center px-[5%] gap-12 overflow-hidden"
           style="background-color: var(--vert)">

    <div class="absolute inset-0 kente-bg opacity-30"></div>
    <div class="absolute inset-0 bg-gradient-to-br from-transparent to-[#001a0e]/60"></div>

    <div class="relative z-10 py-20 fade-up">
      <div class="inline-block bg-[#D4A017]/20 text-[#D4A017] px-4 py-1.5 rounded-full border border-[#D4A017]/30 mb-7 text-sm font-bold">
        🇹🇬 {{ t('hero.badge') }}
      </div>
      
      <h1 class="font-serif text-[clamp(2.6rem,4.5vw,4rem)] font-bold
                 leading-[1.1] text-white mb-6">
        {{ t('hero.title1') }}<br/>
        <span class="text-[#D4A017] relative inline-block">
          {{ t('hero.title2') }}
          <span class="absolute bottom-1 left-0 right-0 h-[3px]
                       bg-[#D4A017] rounded-sm"></span>
        </span><br/>
        {{ t('hero.title3') }}
      </h1>
      
      <p class="text-white/90 text-lg leading-relaxed max-w-[500px] mb-10">
        {{ t('hero.subtitle') }}
      </p>
      
      <div class="flex gap-4 flex-wrap">
        <router-link :to="{ name: 'declare' }" class="btn-primary text-base px-7 py-3.5 no-underline">
          📋 {{ t('hero.cta_loss') }}
        </router-link>
        
        <router-link :to="{ name: 'search' }"
          class="inline-flex items-center gap-2 px-7 py-3.5 rounded-[10px]
                 bg-white/10 backdrop-blur text-white font-semibold text-base
                 border border-white/25 transition-all hover:bg-white/20
                 hover:-translate-y-0.5 no-underline">
          🔍 {{ t('hero.cta_search') }}
        </router-link>
      </div>
    </div>

    <div class="relative z-10 py-20 flex justify-end fade-up delay-200">
      <div class="bg-white/95 backdrop-blur-sm rounded-[20px] p-9 w-full max-w-[420px]
                  shadow-2xl">
        <h3 class="font-serif text-xl font-bold text-[#1A2E22] mb-1.5">
          {{ t('search.title') }}
        </h3>
        <p class="text-sm text-gray-500 mb-6 leading-relaxed">
          {{ t('search.subtitle') }}
        </p>

        <div class="relative mb-3">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          <input v-model="searchQuery" type="text"
            :placeholder="t('search.placeholder')"
            @keyup.enter="handleSearch"
            class="form-input pl-10"/>
        </div>

        <select v-model="searchCategory"
          class="form-input mb-4 cursor-pointer">
          <option value="">{{ t('search.all_cat') }}</option>
          <option value="1">{{ t('categories.identity') }}</option>
          <option value="2">{{ t('categories.vehicle') }}</option>
          <option value="3">{{ t('categories.school') }}</option>
          <option value="4">{{ t('categories.bank') }}</option>
          <option value="5">{{ t('categories.pro') }}</option>
          <option value="6">{{ t('categories.health') }}</option>
        </select>

        <button @click="handleSearch"
          class="w-full bg-[#005A3C] text-white font-bold py-3 rounded-[10px]
                 border-none cursor-pointer transition-all text-sm font-sans
                 hover:bg-[#007A52] hover:-translate-y-px flex items-center justify-center gap-2">
          🔍 {{ t('search.btn') }}
        </button>

        <div class="flex items-center gap-3 my-4">
          <span class="flex-1 h-px bg-gray-200"></span>
          <span class="text-xs text-gray-400">{{ t('search.frequent') }}</span>
          <span class="flex-1 h-px bg-gray-200"></span>
        </div>
        <div class="flex gap-2 flex-wrap">
          <span v-for="chip in chips" :key="chip"
            @click="searchQuery = chip; handleSearch()"
            class="bg-[#E8F4F0] text-[#005A3C] text-xs font-semibold px-3 py-1.5
                   rounded-full cursor-pointer transition-all
                   hover:bg-[#005A3C] hover:text-white">
            {{ chip }}
          </span>
        </div>
      </div>
    </div>
  </section>

  <div class="bg-white border-t-4 border-[#D4A017] border-b border-gray-200
              px-[5%] py-8 grid grid-cols-2 md:grid-cols-4 gap-6">
    <div v-for="stat in stats" :key="stat.key" class="text-center">
      <div class="font-serif text-[2.2rem] font-bold text-[#005A3C] leading-none mb-1">
        {{ stat.num }}<span class="text-[#C41230] text-xl">{{ stat.suffix }}</span>
      </div>
      <div class="text-xs text-gray-500 font-medium">{{ t(`stats.${stat.key}`) }}</div>
    </div>
  </div>

  <section class="px-[5%] py-20" style="background-color: var(--creme)">
    <div class="text-xs font-bold tracking-widest text-[#005A3C] uppercase mb-2">📖 {{ t('steps.label') }}</div>
    <h2 class="font-serif text-[clamp(1.8rem,3vw,2.5rem)] font-bold
               text-[#1A2E22] leading-snug mb-4 max-w-xl">
      {{ t('steps.title') }}
    </h2>
    <p class="text-gray-500 leading-relaxed max-w-md mb-14">{{ t('steps.sub') }}</p>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
      <div class="hidden md:block absolute top-[28px] left-[calc(16.6%+28px)]
                  right-[calc(16.6%+28px)] h-0.5
                  bg-gradient-to-r from-[#005A3C] via-[#D4A017] to-[#005A3C]"></div>

      <div class="bg-white p-6 rounded-xl shadow-lg hover:-translate-y-1.5 transition-all border-t-4 border-transparent hover:border-[#005A3C]">
        <div class="w-14 h-14 bg-[#005A3C] text-white rounded-full flex items-center
                    justify-center font-serif text-2xl font-bold mb-6
                    border-4 border-[#FAF7F2] relative z-10 shadow-md">1</div>
        <h3 class="font-serif text-lg font-bold mb-3 text-[#1A2E22]">{{ t('steps.s1_title') }}</h3>
        <p class="text-sm text-gray-500 leading-relaxed">{{ t('steps.s1_text') }}</p>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-lg hover:-translate-y-1.5 transition-all border-t-4 border-transparent hover:border-[#C41230]">
        <div class="w-14 h-14 bg-[#C41230] text-white rounded-full flex items-center
                    justify-center font-serif text-2xl font-bold mb-6
                    border-4 border-[#FAF7F2] relative z-10 shadow-md">2</div>
        <h3 class="font-serif text-lg font-bold mb-3 text-[#1A2E22]">{{ t('steps.s2_title') }}</h3>
        <p class="text-sm text-gray-500 leading-relaxed">{{ t('steps.s2_text') }}</p>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-lg hover:-translate-y-1.5 transition-all border-t-4 border-transparent hover:border-[#D4A017]">
        <div class="w-14 h-14 bg-[#D4A017] text-[#005A3C] rounded-full flex items-center
                    justify-center font-serif text-2xl font-bold mb-6
                    border-4 border-[#FAF7F2] relative z-10 shadow-md">3</div>
        <h3 class="font-serif text-lg font-bold mb-3 text-[#1A2E22]">{{ t('steps.s3_title') }}</h3>
        <p class="text-sm text-gray-500 leading-relaxed">{{ t('steps.s3_text') }}</p>
      </div>
    </div>
  </section>

  <section class="px-[5%] py-20 relative overflow-hidden" 
           style="background-color: var(--vert)">
    
    <div class="absolute inset-0 kente-bg opacity-20"></div>

    <div class="relative z-10">
      <div class="inline-block bg-white/10 text-[#D4A017] border border-white/20 px-3 py-1 rounded text-xs font-bold mb-4">
        ✦ {{ t('features.label') }}
      </div>
      <h2 class="font-serif text-[clamp(1.8rem,3vw,2.5rem)] font-bold
                 text-white leading-snug mb-4 max-w-lg">
        {{ t('features.title') }}
      </h2>
      <p class="text-white/80 leading-relaxed max-w-md mb-12">{{ t('features.sub') }}</p>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 relative z-10">
        <div v-for="f in features" :key="f.key"
          class="bg-white/10 border border-white/10 rounded-xl p-7 backdrop-blur-sm
                 transition-all hover:bg-white/20 hover:-translate-y-1">
          <span class="text-3xl block mb-4">{{ f.icon }}</span>
          <h3 class="font-serif text-base font-bold text-white mb-2">
            {{ t(`features.${f.key}`) }}
          </h3>
          <p class="text-sm text-white/80 leading-relaxed">
            {{ t(`features.${f.key}_txt`) }}
          </p>
        </div>
      </div>
    </div>
  </section>

  <section class="bg-white px-[5%] py-20">
    <div class="text-xs font-bold tracking-widest text-[#005A3C] uppercase mb-2">📁 {{ t('categories.label') }}</div>
    <h2 class="font-serif text-[clamp(1.8rem,3vw,2.5rem)] font-bold
               text-[#1A2E22] leading-snug mb-10">
      {{ t('categories.title') }}
    </h2>
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div v-for="cat in categories" :key="cat.key"
        class="bg-white rounded-xl p-6 text-center shadow-md cursor-pointer
               transition-all hover:border-[#005A3C] hover:-translate-y-1 hover:shadow-xl
               border-2 border-transparent"
        @click="router.push({ name: 'search', query: { cat: cat.key }})">
        <span class="text-3xl block mb-3">{{ cat.icon }}</span>
        <div class="text-sm font-semibold text-[#1A2E22] mb-1">{{ t(`categories.${cat.key}`) }}</div>
        <div class="text-xs text-gray-400">{{ cat.sub }}</div>
      </div>

      <div class="rounded-xl p-6 text-center border-2 border-dashed border-gray-200
                  bg-gray-50 cursor-default flex flex-col items-center justify-center">
        <span class="text-3xl block mb-3">➕</span>
        <div class="text-sm font-semibold text-gray-400 mb-1">{{ t('categories.suggest') }}</div>
        <div class="text-xs text-gray-300">Contactez-nous</div>
      </div>
    </div>
  </section>

  <section class="relative overflow-hidden px-[5%] py-20 text-center
                  bg-gradient-to-br from-[#C41230] to-[#8B0D22]">
    <div class="absolute inset-0"
      style="background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.04) 0 1px,transparent 1px 20px)">
    </div>
    <h2 class="font-serif text-[clamp(2rem,3.5vw,3rem)] font-bold
               text-white mb-4 relative z-10">
      {{ t('cta.title') }}
    </h2>
    <p class="text-white/80 max-w-lg mx-auto mb-9 leading-relaxed relative z-10">
      {{ t('cta.sub') }}
    </p>
    <div class="flex gap-4 justify-center flex-wrap relative z-10">
      <router-link :to="{ name: 'declare' }"
        class="bg-white text-[#C41230] font-bold px-8 py-3.5 rounded-[10px]
               no-underline inline-flex items-center gap-2 transition-all
               hover:-translate-y-0.5 hover:shadow-xl">
        📋 {{ t('cta.loss') }}
      </router-link>
      <router-link :to="{ name: 'declare', query: { type: 'TROUVAILLE' }}"
        class="bg-transparent text-white font-semibold px-8 py-3.5 rounded-[10px]
               border-2 border-white/40 no-underline inline-flex items-center gap-2
               transition-all hover:border-white hover:bg-white/10 hover:-translate-y-0.5">
        📦 {{ t('cta.found') }}
      </router-link>
    </div>
  </section>

  <footer class="bg-[#1A2E22] px-[5%] pt-14 pb-6 text-white/60">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
      <div class="md:col-span-2">
        <div class="font-serif text-xl font-bold text-white mb-3">
          Décla<span class="text-[#D4A017]">Togo</span>
        </div>
        <p class="text-sm leading-relaxed max-w-xs">{{ t('footer.desc') }}</p>
        <div class="flex mt-4 h-1.5 w-20 rounded overflow-hidden">
          <div class="flex-[2] bg-[#005A3C]"></div>
          <div class="flex-1 bg-[#FFCE00]"></div>
          <div class="flex-[2] bg-[#C41230]"></div>
        </div>
      </div>
      <div>
        <div class="text-xs font-bold uppercase tracking-widest text-white mb-4">
          {{ t('footer.services') }}
        </div>
        <ul class="space-y-2.5 pl-0">
          <li class="list-none"><router-link :to="{ name: 'declare' }"
            class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">
            {{ t('hero.cta_loss') }}
          </router-link></li>
          <li class="list-none"><router-link :to="{ name: 'search' }"
            class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">
            {{ t('nav.search') }}
          </router-link></li>
        </ul>
      </div>
      <div>
        <div class="text-xs font-bold uppercase tracking-widest text-white mb-4">
          {{ t('footer.info') }}
        </div>
        <ul class="space-y-2.5 pl-0">
          <li class="list-none"><a href="#" class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">FAQ</a></li>
          <li class="list-none"><a href="#" class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">Contact</a></li>
          <li class="list-none"><a href="#" class="text-sm text-white/50 hover:text-[#D4A017] transition-colors no-underline">
            {{ t('footer.legal') }}
          </a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-white/10 pt-6 flex flex-col md:flex-row
                items-center justify-between gap-3 text-xs">
      <span>{{ t('footer.rights') }}</span>
      <span>{{ t('footer.made') }} ❤️</span>
    </div>
  </footer>
</template>
```

## File: frontend/src/views/NotFoundView.vue
```vue
<template>
    <div class="text-center py-32">
        <h1 class="font-serif text-4xl text-vert mb-4">404</h1>
        <p class="text-gray-500">Page introuvable</p>
        <router-link to="/" class="text-vert underline mt-4 block">Retour à l'accueil</router-link>
    </div>
</template>
```

## File: frontend/src/views/SearchView.vue
```vue
<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { declarationsAPI, categoriesAPI } from '../services/api'

const route  = useRoute()
const router = useRouter()

/* ══ État ══ */
// AJOUT : Mode de recherche et champs nom/prénom
const searchMode = ref(route.query.mode || 'numero') // 'numero' ou 'nom'
const query      = ref(route.query.q    || '')       // Numéro de pièce
const nom        = ref(route.query.nom  || '')       // Nom de famille
const prenom     = ref(route.query.prenom || '')     // Prénom

const catFilter  = ref(route.query.cat  || '')
const results    = ref([])
const categories = ref([])
const loading    = ref(false)
const searched   = ref(false)
let   debounce   = null

/* ══ Chargement catégories ══ */
onMounted(async () => {
  try {
    const { data } = await categoriesAPI.list()
    categories.value = data.results ?? data
  } catch {}
  
  // Lancer la recherche si des paramètres sont présents dans l'URL
  if (query.value || nom.value || prenom.value) doSearch()
})

/* ══ Recherche debounced ══ */
const doSearch = async () => {
  // AJOUT : Vérification conditionnelle selon le mode
  const isNumeroMode = searchMode.value === 'numero'
  const hasInput = isNumeroMode 
    ? query.value.trim() 
    : (nom.value.trim() || prenom.value.trim())

  if (!hasInput) { results.value = []; searched.value = false; return }

  loading.value = true
  searched.value = true
  
  try {
    // AJOUT : Construction dynamique du payload
    const payload = {}
    
    if (isNumeroMode) {
      payload.numero_piece = query.value.trim()
    } else {
      payload.nom_declarant = nom.value.trim()
      payload.prenom_declarant = prenom.value.trim()
    }

    if (catFilter.value) payload.categorie = Number(catFilter.value)
    
    const { data } = await declarationsAPI.rechercher(payload)
    results.value = data.correspondances ?? []
  } catch {
    results.value = []
  } finally {
    loading.value = false
  }
  
  // Sync URL (Mise à jour pour inclure les nouveaux champs)
  router.replace({ query: { 
    mode: searchMode.value,
    q: query.value || undefined, 
    nom: nom.value || undefined,
    prenom: prenom.value || undefined,
    cat: catFilter.value || undefined 
  }})
}

// AJOUT : Watch sur les nouvelles variables
watch([query, nom, prenom, catFilter, searchMode], () => {
  clearTimeout(debounce)
  debounce = setTimeout(doSearch, 420)
})

/* ══ Helpers ══ */
const statusConfig = {
  EN_ATTENTE: { label: 'En attente', color: '#D97706', bg: '#FEF3C7' },
  VALIDE:     { label: 'Validé',     color: '#2563EB', bg: '#DBEAFE' },
  RETROUVE:   { label: 'Retrouvé',   color: '#059669', bg: '#D1FAE5' },
  RESTITUE:   { label: 'Restitué',   color: '#065F46', bg: '#A7F3D0' },
  REJETE:     { label: 'Rejeté',     color: '#DC2626', bg: '#FEE2E2' },
  CLOTURE:    { label: 'Clôturé',    color: '#6B7280', bg: '#F3F4F6' },
}
const getStatus = (s) => statusConfig[s] || statusConfig.EN_ATTENTE

const formatDate = (d) => d
  ? new Date(d).toLocaleDateString('fr-FR', { day:'2-digit', month:'short', year:'numeric' })
  : '—'

const popular = ['CNI', 'Passeport', 'Carte grise', 'Permis', 'Diplôme']
</script>

<template>
<div class="min-h-screen" style="background:#FAF7F2">

  <section class="relative overflow-hidden py-16 px-[5%]"
           style="background-color:#005A3C">
    <div class="absolute inset-0 kente-bg opacity-30"></div>
    <div class="absolute inset-0 bg-gradient-to-br from-transparent to-[#001a0e]/50"></div>

    <div class="relative z-10 max-w-2xl mx-auto text-center">
      <div class="inline-flex items-center gap-2 bg-white/10 text-[#D4A017]
                  border border-white/20 px-3 py-1.5 rounded-full text-xs font-bold mb-4">
        🔍 Recherche publique
      </div>
      <h1 class="font-serif text-[clamp(1.8rem,3vw,2.6rem)] font-bold text-white mb-3 leading-tight">
        Votre pièce a peut-être<br/>
        <span class="text-[#D4A017]">été retrouvée</span>
      </h1>
      <p class="text-white/75 text-sm mb-6 leading-relaxed">
        Recherchez par numéro ou par nom dans notre base de trouvailles.
      </p>

      <div class="flex justify-center mb-4">
        <div class="inline-flex bg-black/20 p-1 rounded-xl border border-white/10">
          <button 
            @click="searchMode = 'numero'"
            class="px-4 py-2 rounded-lg text-xs font-bold transition-all border-none cursor-pointer"
            :class="searchMode === 'numero' ? 'bg-white text-[#005A3C]' : 'bg-transparent text-white/70 hover:text-white'">
            🔢 Par Numéro
          </button>
          <button 
            @click="searchMode = 'nom'"
            class="px-4 py-2 rounded-lg text-xs font-bold transition-all border-none cursor-pointer"
            :class="searchMode === 'nom' ? 'bg-white text-[#005A3C]' : 'bg-transparent text-white/70 hover:text-white'">
            👤 Par Nom
          </button>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-2 shadow-2xl flex flex-col sm:flex-row gap-2">
        
        <div v-if="searchMode === 'numero'" class="relative flex-1">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          <input
            v-model="query"
            type="text"
            placeholder="Numéro de pièce (ex: TG20240001)"
            class="w-full border-0 outline-none bg-transparent pl-10 pr-4 py-3
                   text-sm text-[#1A2E22] placeholder:text-gray-400"
            @keyup.enter="doSearch"
          />
        </div>

        <div v-else class="flex-1 flex flex-col sm:flex-row gap-0 sm:gap-2">
            <div class="relative flex-1">
                <input
                    v-model="nom"
                    type="text"
                    placeholder="Nom"
                    class="w-full border-0 outline-none bg-transparent px-4 py-3
                        text-sm text-[#1A2E22] placeholder:text-gray-400"
                    @keyup.enter="doSearch"
                />
            </div>
            <div class="hidden sm:block w-[1px] bg-gray-200 my-2"></div>
            <div class="relative flex-1">
                <input
                    v-model="prenom"
                    type="text"
                    placeholder="Prénom(s)"
                    class="w-full border-0 outline-none bg-transparent px-4 py-3
                        text-sm text-[#1A2E22] placeholder:text-gray-400"
                    @keyup.enter="doSearch"
                />
            </div>
        </div>

        <select v-model="catFilter"
          class="border-0 outline-none bg-gray-50 rounded-xl text-sm text-gray-600
                 px-3 py-3 cursor-pointer min-w-[160px]">
          <option value="">Toutes catégories</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.libelle }}</option>
        </select>
        
        <button @click="doSearch"
          class="bg-[#005A3C] text-white font-bold text-sm px-6 py-3 rounded-xl
                 border-none cursor-pointer transition-all hover:bg-[#007A52]
                 flex items-center gap-2">
          <span v-if="loading" class="loader-dot-sm"></span>
          <span v-else>🔍</span>
          Rechercher
        </button>
      </div>

      <div v-if="searchMode === 'numero'" class="flex items-center justify-center gap-2 flex-wrap mt-4">
        <span class="text-xs text-white/40">Fréquents :</span>
        <button v-for="chip in popular" :key="chip"
          @click="query = chip"
          class="bg-white/10 text-white/70 hover:bg-white/20 hover:text-white
                 text-xs px-3 py-1.5 rounded-full border border-white/15
                 transition-all cursor-pointer border-none">
          {{ chip }}
        </button>
      </div>
    </div>
  </section>


  <section class="max-w-3xl mx-auto px-4 py-10">

    <div v-if="!searched && !loading" class="text-center py-16">
      <div class="text-5xl mb-4">🗂️</div>
      <p class="text-gray-400 text-sm">
        Remplissez les informations ci-dessus pour lancer la recherche.
      </p>
      <p class="text-xs text-gray-400 mt-2">
        La recherche porte sur toutes les trouvailles validées dans notre base.
      </p>
    </div>

    <div v-else-if="loading" class="space-y-3">
      <div class="flex items-center gap-3 mb-6">
        <div class="loader-ring"></div>
        <span class="text-sm text-gray-500">Recherche en cours…</span>
      </div>
      <div v-for="i in 3" :key="i" class="skeleton h-24 rounded-xl"></div>
    </div>

    <template v-else-if="searched">
      <div class="flex items-center justify-between mb-5">
        <div>
          <span class="font-serif text-lg font-bold text-[#1A2E22]">
            {{ results.length }} résultat{{ results.length !== 1 ? 's' : '' }}
          </span>
          <span class="text-sm text-gray-400 ml-2">
              pour « {{ searchMode === 'numero' ? query : (nom + ' ' + prenom).trim() }} »
          </span>
        </div>
        <button v-if="results.length || query || nom || prenom"
          @click="{ query = ''; nom = ''; prenom = ''; results = []; searched = false }"
          class="text-xs text-gray-400 hover:text-[#C41230] bg-transparent
                 border-none cursor-pointer transition-colors">
          ✕ Effacer
        </button>
      </div>

      <div v-if="results.length === 0"
        class="text-center py-14 bg-white rounded-2xl border border-gray-100 shadow-card">
        <div class="text-4xl mb-4">😕</div>
        <p class="font-serif text-lg font-bold text-[#1A2E22] mb-2">
          Aucune trouvaille correspondante
        </p>
        <p class="text-sm text-gray-500 max-w-sm mx-auto mb-6 leading-relaxed">
          Votre pièce n'a pas encore été signalée. Déclarez votre perte pour être notifié
          dès qu'une correspondance apparaît.
        </p>
        <router-link :to="{ name: 'declare', query: { type: 'PERTE' } }"
          class="inline-flex items-center gap-2 bg-[#005A3C] text-white font-bold
                 text-sm px-6 py-3 rounded-xl no-underline hover:bg-[#007A52] transition-all">
          📋 Déclarer ma perte
        </router-link>
      </div>

      <div v-else class="space-y-3">
        <transition-group name="list-item">
          <div v-for="decl in results" :key="decl.id"
            class="bg-white rounded-2xl border border-gray-100 shadow-card
                   hover:shadow-card-lg hover:-translate-y-0.5 transition-all p-5
                   flex flex-col sm:flex-row items-start gap-4">

            <div class="w-12 h-12 bg-[#E8F4F0] rounded-xl flex items-center
                        justify-center text-2xl flex-shrink-0">
              🤲
            </div>

            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2 flex-wrap mb-1">
                <div>
                  <span class="font-mono font-bold text-[#005A3C] text-sm tracking-wider">
                    {{ decl.numero_piece }}
                  </span>
                  <span class="mx-2 text-gray-300">·</span>
                  <span class="text-sm font-semibold text-[#1A2E22]">
                    {{ decl.nom_sur_piece }}
                  </span>
                </div>
                <span class="badge text-xs flex-shrink-0"
                  :style="{
                    color: getStatus(decl.statut).color,
                    backgroundColor: getStatus(decl.statut).bg
                  }">
                  {{ getStatus(decl.statut).label }}
                </span>
              </div>

              <div class="flex items-center gap-4 text-xs text-gray-400 flex-wrap mt-2">
                <span v-if="decl.categorie_nom">📁 {{ decl.categorie_nom }}</span>
                <span v-if="decl.lieu_perte">📍 {{ decl.lieu_perte }}</span>
                <span>📅 {{ formatDate(decl.date_declaration) }}</span>
              </div>
            </div>

            <div class="flex-shrink-0 sm:self-center">
              <router-link :to="{ name: 'declare', query: { type: 'PERTE' } }"
                class="inline-flex items-center gap-1.5 bg-[#005A3C] text-white
                       font-semibold text-xs px-4 py-2.5 rounded-xl no-underline
                       hover:bg-[#007A52] transition-all">
                ✅ C'est la mienne
              </router-link>
            </div>

          </div>
        </transition-group>

        <div class="mt-6 bg-[#FFFBEB] border border-yellow-200 rounded-2xl p-5
                    flex items-start gap-3">
          <span class="text-xl">💡</span>
          <div>
            <p class="text-sm font-semibold text-yellow-800 mb-1">
              Vous ne trouvez pas votre pièce ?
            </p>
            <p class="text-xs text-yellow-700 leading-relaxed mb-3">
              Déclarez votre perte maintenant. Si votre pièce est signalée ultérieurement,
              vous recevrez une notification automatique.
            </p>
            <router-link :to="{ name: 'declare', query: { type: 'PERTE' } }"
              class="inline-flex items-center gap-1.5 bg-yellow-600 text-white font-semibold
                     text-xs px-4 py-2 rounded-lg no-underline hover:bg-yellow-700 transition-all">
              📋 Déclarer ma perte
            </router-link>
          </div>
        </div>

      </div>
    </template>

  </section>

</div>
</template>

<style scoped>
.list-item-enter-active { transition: all .3s ease; }
.list-item-enter-from   { opacity: 0; transform: translateY(12px); }

.loader-dot-sm {
  display: inline-block;
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
.loader-ring {
  width: 20px; height: 20px;
  border: 2px solid #e5e7eb;
  border-top-color: #005A3C;
  border-radius: 50%;
  animation: spin .8s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
```

## File: frontend/tailwind.config.js
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Palette officielle DéclaTogo — inspirée du drapeau togolais
        vert: {
          DEFAULT: '#005A3C',
          light:   '#007A52',
          xl:      '#E8F4F0',
        },
        rouge: {
          DEFAULT: '#C41230',
          light:   '#E8192F',
        },
        or: {
          DEFAULT: '#D4A017',
          light:   '#F5E6A8',
        },
        creme: '#FAF7F2',
        texte: '#1A2E22',
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        sans:  ['"DM Sans"', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'card':    '0 4px 24px rgba(0,90,60,.10)',
        'card-lg': '0 12px 48px rgba(0,90,60,.16)',
      },
      borderRadius: {
        'card': '12px',
      },
    },
  },
  plugins: [],
}
```

## File: frontend/vite.config.js
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
})
```

## File: package.json
```json
{
  "dependencies": {
    "axios": "^1.13.5",
    "pinia": "^3.0.4",
    "vue-router": "^4.6.4"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.24",
    "init": "^0.1.2",
    "npx": "^10.2.2",
    "postcss": "^8.5.6",
    "tailwindcss": "^4.1.18"
  }
}
```

## File: README.md
```markdown
# Gestion_Perte
```

## File: repomix.config.json
```json
{
  "output": {
    "filePath": "repomix-output.md",
    "style": "markdown"
  },
  "ignore": {
    "customPatterns": [
      "**/node_modules/**",
      "**/dist/**",
      "**/.nuxt/**",
      "**/.vuepress/.temp/**",
      "**/venv/**",
      "**/.venv/**",
      "**/env/**",
      "**/*.pyc",
      "**/__pycache__/**",
      "**/db.sqlite3",
      "**/.git/**",
      "**/package-lock.json",
      "**/yarn.lock"
    ]
  }
}
```

## File: requirements.txt
```
certifi==2025.11.12
cffi==2.0.0
charset-normalizer==3.4.4
colorama==0.4.6
filelock==3.20.0
fsspec==2025.10.0
idna==3.11
Jinja2==3.1.6
llvmlite==0.45.1
MarkupSafe==3.0.3
more-itertools==10.8.0
mpmath==1.3.0
networkx==3.5
numba==0.62.1
numpy==2.3.5
openai-whisper==20250625
pycparser==2.23
pydub==0.25.1
regex==2025.11.3
requests==2.32.5
sounddevice==0.5.3
sympy==1.14.0
tiktoken==0.12.0
torch==2.9.1
tqdm==4.67.1
typing_extensions==4.15.0
urllib3==2.5.0
```
