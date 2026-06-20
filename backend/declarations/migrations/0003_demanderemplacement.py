# Generated migration — 0003_demanderemplacement

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declarations', '0002_declaration_date_naissance_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Ajout du statut REMPLACEMENT sur Declaration
        migrations.AlterField(
            model_name='declaration',
            name='statut',
            field=models.CharField(
                choices=[
                    ('EN_ATTENTE',   'En attente de validation'),
                    ('VALIDE',       'Validé'),
                    ('RETROUVE',     'Retrouvé/Correspondance trouvée'),
                    ('RESTITUE',     'Restitué au propriétaire'),
                    ('REJETE',       'Rejeté'),
                    ('CLOTURE',      'Clôturé'),
                    ('REMPLACEMENT', 'En cours de remplacement'),
                ],
                default='EN_ATTENTE',
                max_length=20,
                verbose_name='Statut'
            ),
        ),

        # Création du modèle DemandeRemplacement
        migrations.CreateModel(
            name='DemandeRemplacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(
                    choices=[
                        ('EN_ATTENTE',     "En attente de traitement par un agent"),
                        ('RECEPISSE_EMIS', "Autorisation officielle émise — à déposer au commissariat"),
                        ('EN_TRAITEMENT',  "Dossier en traitement au commissariat"),
                        ('DOCUMENT_PRET',  "Nouvelle pièce prête à retirer"),
                        ('RETIRE',         "Document retiré — dossier clôturé"),
                        ('ANNULE',         "Annulé"),
                    ],
                    default='EN_ATTENTE',
                    max_length=20,
                    verbose_name='Statut du dossier'
                )),
                ('numero_dossier', models.CharField(
                    blank=True, max_length=50, null=True,
                    unique=True, verbose_name='Numéro de dossier'
                )),
                ('commissariat',          models.CharField(blank=True, max_length=300, null=True, verbose_name='Commissariat agréé')),
                ('adresse_commissariat',  models.TextField(blank=True, null=True, verbose_name='Adresse du commissariat')),
                ('horaires_commissariat', models.CharField(blank=True, max_length=200, null=True, verbose_name="Horaires d'ouverture")),
                ('remarques',             models.TextField(blank=True, null=True, verbose_name='Remarques agent')),
                ('date_creation',           models.DateTimeField(auto_now_add=True, verbose_name='Date de création du dossier')),
                ('date_echeance_match',     models.DateTimeField(verbose_name='Échéance du matching (J+7)')),
                ('date_emission_recepisse', models.DateTimeField(blank=True, null=True, verbose_name="Date d'émission de l'autorisation")),
                ('date_depot_commissariat', models.DateTimeField(blank=True, null=True, verbose_name='Date de dépôt au commissariat')),
                ('date_document_pret',      models.DateTimeField(blank=True, null=True, verbose_name='Date de disponibilité du document')),
                ('date_retrait',            models.DateTimeField(blank=True, null=True, verbose_name='Date de retrait')),
                ('declaration', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='demande_remplacement',
                    to='declarations.declaration',
                    verbose_name='Déclaration de perte'
                )),
                ('traite_par', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='remplacements_traites',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Traité par'
                )),
            ],
            options={
                'verbose_name': 'Demande de remplacement',
                'verbose_name_plural': 'Demandes de remplacement',
                'ordering': ['-date_creation'],
            },
        ),

        # Ajout du type REMPLACEMENT dans Notification
        migrations.AlterField(
            model_name='notification',
            name='type_notification',
            field=models.CharField(
                choices=[
                    ('INFO',         'Information'),
                    ('MATCH',        'Correspondance trouvée'),
                    ('STATUT',       'Changement de statut'),
                    ('ADMIN',        'Message administrateur'),
                    ('REMPLACEMENT', 'Remplacement de pièce'),
                ],
                max_length=20,
                verbose_name='Type'
            ),
        ),
    ]
