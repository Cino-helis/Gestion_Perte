"""
Commande Django : check_remplacements
Détecte les déclarations de PERTE sans correspondance après 7 jours
et ouvre automatiquement un dossier de remplacement.

Usage :
    python manage.py check_remplacements

Planification recommandée (cron, tous les jours à 8h) :
    0 8 * * * /chemin/vers/env/bin/python /chemin/vers/manage.py check_remplacements >> /var/log/declatogo_remplacements.log 2>&1
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from declarations.models import Declaration, DemandeRemplacement, Notification
from declarations.email_remplacement import envoyer_email_remplacement


class Command(BaseCommand):
    help = (
        "Détecte les déclarations de perte sans match après 7 jours "
        "et ouvre un dossier de remplacement."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Simule sans créer de dossiers ni envoyer d'emails.",
        )
        parser.add_argument(
            '--delai-jours',
            type=int,
            default=7,
            help="Délai en jours avant ouverture du dossier (défaut : 7).",
        )

    def handle(self, *args, **options):
        dry_run     = options['dry_run']
        delai_jours = options['delai_jours']
        limite      = timezone.now() - timedelta(days=delai_jours)

        self.stdout.write(
            f"\n{'[DRY-RUN] ' if dry_run else ''}Recherche des pertes sans match "
            f"depuis plus de {delai_jours} jour(s)...\n"
        )

        # Déclarations de perte :
        #   - validées (statut VALIDE)
        #   - déclarées il y a plus de `delai_jours` jours
        #   - sans correspondance trouvée
        #   - sans dossier de remplacement déjà ouvert
        pertes_eligibles = Declaration.objects.filter(
            type_declaration='PERTE',
            statut='VALIDE',
            date_declaration__lte=limite,
            declaration_correspondante__isnull=True,
        ).exclude(
            demande_remplacement__isnull=False   # exclure celles qui ont déjà un dossier
        ).select_related('user', 'categorie')

        nb = pertes_eligibles.count()
        self.stdout.write(f"→ {nb} déclaration(s) éligible(s) trouvée(s).\n")

        if nb == 0:
            self.stdout.write(self.style.SUCCESS("Aucune action requise.\n"))
            return

        created_count = 0
        error_count   = 0

        for perte in pertes_eligibles:
            self.stdout.write(
                f"  • {perte.numero_recepisse} — "
                f"{perte.nom_sur_piece} "
                f"(déclarée le {perte.date_declaration.strftime('%d/%m/%Y')})"
            )

            if dry_run:
                self.stdout.write("    [DRY-RUN] Dossier NON créé.\n")
                continue

            try:
                # Créer le dossier de remplacement
                demande = DemandeRemplacement.objects.create(
                    declaration=perte,
                    date_echeance_match=perte.date_declaration + timedelta(days=delai_jours),
                )

                # Passer la déclaration au statut REMPLACEMENT
                Declaration.objects.filter(pk=perte.pk).update(statut='REMPLACEMENT')

                # Notification in-app
                Notification.objects.create(
                    user=perte.user,
                    declaration=perte,
                    type_notification='REMPLACEMENT',
                    titre='📂 Dossier de remplacement ouvert',
                    message=(
                        f"Votre déclaration de perte {perte.numero_recepisse} "
                        f"({perte.nom_sur_piece}) n'a pas eu de correspondance "
                        f"après {delai_jours} jours. "
                        f"Un dossier de remplacement N° {demande.numero_dossier} "
                        f"a été ouvert automatiquement. Un agent va traiter votre dossier."
                    ),
                )

                # Email
                envoyer_email_remplacement('ouverture', perte.user, demande)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"    ✓ Dossier {demande.numero_dossier} créé — "
                        f"email envoyé à {perte.user.email or 'N/A'}"
                    )
                )
                created_count += 1

            except Exception as exc:
                self.stderr.write(
                    self.style.ERROR(
                        f"    ✗ Erreur pour {perte.numero_recepisse} : {exc}"
                    )
                )
                error_count += 1

        self.stdout.write(
            f"\n{'[DRY-RUN] ' if dry_run else ''}"
            f"Terminé : {created_count} dossier(s) créé(s), {error_count} erreur(s).\n"
        )
