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
        import declarations.signals  # noqa: F401

        import os
        if os.environ.get('RUN_MAIN') != 'true':
            from declarations.scheduler import start
            start()