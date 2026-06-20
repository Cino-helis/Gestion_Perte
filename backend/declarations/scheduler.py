from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


def verifier_remplacements():
    from declarations.models import Declaration, DemandeRemplacement, Notification
    from declarations.email_remplacement import envoyer_email_remplacement

    limite = timezone.now() - timedelta(days=7)

    pertes_eligibles = Declaration.objects.filter(
        type_declaration='PERTE',
        statut='VALIDE',
        date_declaration__lte=limite,
        declaration_correspondante__isnull=True,
    ).exclude(
        demande_remplacement__isnull=False
    ).select_related('user', 'categorie')

    nb = pertes_eligibles.count()
    if nb == 0:
        logger.info("[Scheduler] Aucune perte éligible au remplacement.")
        return

    logger.info(f"[Scheduler] {nb} perte(s) éligible(s) trouvée(s).")

    for perte in pertes_eligibles:
        try:
            demande = DemandeRemplacement.objects.create(
                declaration=perte,
                date_echeance_match=perte.date_declaration + timedelta(days=7),
            )
            Declaration.objects.filter(pk=perte.pk).update(statut='REMPLACEMENT')
            Notification.objects.create(
                user=perte.user,
                declaration=perte,
                type_notification='REMPLACEMENT',
                titre='📂 Dossier de remplacement ouvert',
                message=(
                    f"Votre déclaration de perte {perte.numero_recepisse} "
                    f"({perte.nom_sur_piece}) n'a pas eu de correspondance "
                    f"après 7 jours. Un dossier de remplacement "
                    f"N° {demande.numero_dossier} a été ouvert automatiquement."
                ),
            )
            envoyer_email_remplacement('ouverture', perte.user, demande)
            logger.info(f"[Scheduler] Dossier {demande.numero_dossier} créé pour {perte.numero_recepisse}")

        except Exception as exc:
            logger.error(f"[Scheduler] Erreur pour {perte.numero_recepisse} : {exc}")


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        verifier_remplacements,
        trigger='interval',
        hours=24,
        id='verifier_remplacements',
        replace_existing=True,
    )

    logger.info("[Scheduler] Démarré — vérification toutes les 24h.")
    scheduler.start()