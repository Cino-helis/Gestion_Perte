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