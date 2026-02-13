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