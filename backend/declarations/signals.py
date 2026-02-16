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
        # Lier les deux déclarations
        instance.declaration_correspondante = match
        instance.statut = 'RETROUVE'
        # Utiliser update_fields pour éviter de redéclencher le signal à l'infini
        Declaration.objects.filter(pk=instance.pk).update(
            declaration_correspondante=match,
            statut='RETROUVE'
        )

        Declaration.objects.filter(pk=match.pk).update(
            declaration_correspondante=instance,
            statut='RETROUVE'
        )

        # --- Notification + email pour le déclarant de l'instance ---
        _creer_notification_match(
            user=instance.user,
            declaration_propre=instance,
            declaration_match=match
        )

        # --- Notification + email pour le déclarant du match ---
        _creer_notification_match(
            user=match.user,
            declaration_propre=match,
            declaration_match=instance
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