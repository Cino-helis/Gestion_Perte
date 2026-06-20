"""
Service d'emails pour le workflow de remplacement de pièce — DéclaTogo.

Étapes couvertes :
  'ouverture'       → Dossier ouvert (7j sans match)
  'recepisse_emis'  → Autorisation prête à télécharger + commissariat désigné
  'en_traitement'   → Dossier reçu au commissariat
  'document_pret'   → Nouvelle pièce prête à retirer
  'retire'          → Procédure terminée

Usage :
    from declarations.email_remplacement import envoyer_email_remplacement
    envoyer_email_remplacement('ouverture', user, demande)
"""

import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


# ── Contenu par étape ────────────────────────────────────────────────────────

_ETAPES = {
    'ouverture': {
        'sujet_tpl':   "[DéclaTogo] Dossier de remplacement ouvert — {num_dossier}",
        'titre':       "Dossier de remplacement ouvert",
        'couleur':     '#D97706',
        'emoji':       '📂',
        'texte_intro': (
            "Votre déclaration de perte <b>{num_recepisse}</b> n'a pas eu de correspondance "
            "dans le délai de 7 jours. Un dossier de remplacement <b>{num_dossier}</b> "
            "a été ouvert automatiquement."
        ),
        'instructions': [
            "Un agent va examiner votre dossier très prochainement.",
            "Vous recevrez une autorisation officielle à présenter au commissariat.",
            "Aucune action de votre part n'est requise pour l'instant.",
        ],
    },
    'recepisse_emis': {
        'sujet_tpl':   "[DéclaTogo] Votre autorisation est prête — {num_dossier}",
        'titre':       "Autorisation officielle disponible",
        'couleur':     '#2563EB',
        'emoji':       '📄',
        'texte_intro': (
            "Votre autorisation de remplacement pour le dossier <b>{num_dossier}</b> "
            "est prête. Connectez-vous à DéclaTogo pour la télécharger et rendez-vous "
            "au commissariat désigné."
        ),
        'instructions': [
            "Connectez-vous à DéclaTogo et téléchargez votre autorisation PDF.",
            "Rendez-vous au commissariat indiqué dans l'autorisation.",
            "Apportez les pièces justificatives listées dans le document.",
            "Conservez votre récépissé de dépôt remis par le commissariat.",
        ],
    },
    'en_traitement': {
        'sujet_tpl':   "[DéclaTogo] Votre dossier est en cours de traitement — {num_dossier}",
        'titre':       "Dossier en traitement au commissariat",
        'couleur':     '#7C3AED',
        'emoji':       '⚙️',
        'texte_intro': (
            "Votre dossier <b>{num_dossier}</b> a bien été pris en charge par le commissariat. "
            "La fabrication de votre nouvelle pièce est en cours. "
            "Vous serez notifié dès qu'elle sera disponible."
        ),
        'instructions': [
            "Patientez — vous recevrez un email dès que votre pièce sera prête.",
            "Conservez votre récépissé de dépôt du commissariat.",
            "En cas de question, contactez directement le commissariat désigné.",
        ],
    },
    'document_pret': {
        'sujet_tpl':   "[DéclaTogo] 🎉 Votre nouvelle pièce est prête ! — {num_dossier}",
        'titre':       "Votre nouvelle pièce est prête à retirer !",
        'couleur':     '#059669',
        'emoji':       '🎉',
        'texte_intro': (
            "Excellente nouvelle ! Votre nouvelle pièce est prête. "
            "Rendez-vous au commissariat désigné pour le retrait "
            "(dossier <b>{num_dossier}</b>)."
        ),
        'instructions': [
            "Rendez-vous au commissariat désigné dans vos horaires d'ouverture.",
            "Apportez votre récépissé de dépôt ET votre autorisation DéclaTogo.",
            "Apportez une pièce d'identité valide (ou document officiel).",
            "Après retrait, votre dossier sera clôturé sur DéclaTogo.",
        ],
    },
    'retire': {
        'sujet_tpl':   "[DéclaTogo] Procédure terminée — {num_dossier}",
        'titre':       "Procédure de remplacement terminée",
        'couleur':     '#065F46',
        'emoji':       '✅',
        'texte_intro': (
            "Votre procédure de remplacement (<b>{num_dossier}</b>) est terminée. "
            "Merci d'avoir utilisé DéclaTogo !"
        ),
        'instructions': [
            "Conservez précieusement votre nouvelle pièce.",
            "En cas de perte future, revenez sur DéclaTogo pour déclarer.",
        ],
    },
}


def _html_email(etape_data, nom, num_dossier, num_recepisse,
                commissariat=None, adresse=None, horaires=None,
                remarques=None):
    """Génère le corps HTML de l'email."""
    date_envoi = timezone.localtime(timezone.now()).strftime('%d/%m/%Y à %H:%M')
    titre   = etape_data['titre']
    couleur = etape_data['couleur']
    emoji   = etape_data['emoji']

    intro = etape_data['texte_intro'].format(
        num_dossier=num_dossier, num_recepisse=num_recepisse
    )

    # Bloc commissariat
    bloc_comm = ''
    if commissariat:
        bloc_comm = f"""
        <tr><td style="padding:0 32px 20px;">
          <table width="100%" cellpadding="0" cellspacing="0"
                 style="background:#EFF6FF;border:2px solid #BFDBFE;border-radius:10px;">
            <tr><td style="padding:14px 18px;">
              <p style="margin:0 0 4px;font-size:11px;font-weight:700;color:#1D4ED8;
                         text-transform:uppercase;letter-spacing:.06em;">Commissariat agréé</p>
              <p style="margin:0 0 3px;font-size:14px;font-weight:700;color:#1E3A5F;">🏛️ {commissariat}</p>
              {"<p style='margin:0 0 2px;font-size:12px;color:#374151;'>📍 " + adresse + "</p>" if adresse else ''}
              {"<p style='margin:0;font-size:12px;color:#374151;'>🕐 " + horaires + "</p>" if horaires else ''}
            </td></tr>
          </table>
        </td></tr>"""

    # Instructions
    lignes = ''.join(
        f"""<tr><td style="padding:4px 0;">
          <table cellpadding="0" cellspacing="0"><tr>
            <td style="width:24px;height:24px;background:{couleur};border-radius:50%;
                        color:white;font-weight:700;font-size:11px;text-align:center;
                        vertical-align:middle;">{i}</td>
            <td style="padding-left:10px;font-size:13px;color:#374151;">{instr}</td>
          </tr></table></td></tr>"""
        for i, instr in enumerate(etape_data['instructions'], 1)
    )

    # Remarques
    bloc_rem = ''
    if remarques:
        bloc_rem = f"""
        <tr><td style="padding:0 32px 18px;">
          <table width="100%" cellpadding="0" cellspacing="0"
                 style="background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;">
            <tr><td style="padding:10px 14px;font-size:13px;color:#92400e;">
              <strong>Note de l'agent :</strong> {remarques}
            </td></tr>
          </table>
        </td></tr>"""

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"/>
<title>DéclaTogo — {titre}</title></head>
<body style="margin:0;padding:0;background:#FAF7F2;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#FAF7F2">
<tr><td align="center" style="padding:28px 14px;">
<table width="600" cellpadding="0" cellspacing="0"
       style="max-width:600px;background:#fff;border-radius:16px;overflow:hidden;
              box-shadow:0 4px 24px rgba(0,90,60,.12);">

  <tr><td style="height:6px;padding:0;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td style="background:#005A3C;width:40%;height:6px;"></td>
      <td style="background:#D4A017;width:20%;height:6px;"></td>
      <td style="background:#C41230;width:40%;height:6px;"></td>
    </tr></table></td></tr>

  <tr><td style="background:#005A3C;padding:20px 28px;text-align:center;">
    <table cellpadding="0" cellspacing="0" align="center"><tr>
      <td style="background:#D4A017;width:38px;height:38px;border-radius:8px;
                  text-align:center;vertical-align:middle;font-weight:700;
                  font-size:13px;color:#005A3C;">DT</td>
      <td style="padding-left:10px;font-size:20px;font-weight:700;color:#fff;vertical-align:middle;">
        Décla<span style="color:#D4A017;">Togo</span></td>
    </tr></table>
    <p style="margin:8px 0 0;font-size:10px;color:rgba(255,255,255,.55);
               text-transform:uppercase;letter-spacing:.1em;">
      Plateforme officielle — République Togolaise</p>
  </td></tr>

  <tr><td style="background:{couleur};padding:16px 28px;text-align:center;">
    <p style="margin:0;font-size:19px;font-weight:700;color:#fff;">{emoji} {titre}</p>
  </td></tr>

  <tr><td style="padding:22px 32px 8px;">
    <p style="margin:0;font-size:15px;color:#374151;line-height:1.6;">
      Bonjour <strong>{nom}</strong>,</p>
  </td></tr>

  <tr><td style="padding:12px 32px 18px;">
    <table width="100%" cellpadding="0" cellspacing="0"
           style="background:#f8fafc;border:2px solid {couleur};border-radius:12px;">
      <tr><td style="padding:14px 18px;">
        <p style="margin:0 0 4px;font-size:11px;font-weight:700;color:#6b7280;
                   text-transform:uppercase;letter-spacing:.06em;">Numéro de dossier</p>
        <p style="margin:0;font-family:monospace;font-size:18px;font-weight:700;
                   color:{couleur};letter-spacing:.1em;">{num_dossier}</p>
        <p style="margin:4px 0 0;font-size:12px;color:#374151;">
          Réf. perte : {num_recepisse}</p>
      </td></tr>
    </table>
  </td></tr>

  <tr><td style="padding:0 32px 18px;">
    <p style="margin:0;font-size:13px;color:#374151;line-height:1.65;">{intro}</p>
  </td></tr>

  {bloc_comm}
  {bloc_rem}

  <tr><td style="padding:0 32px 22px;">
    <p style="margin:0 0 10px;font-size:13px;font-weight:700;color:#1A2E22;">
      📋 Étapes à suivre :</p>
    <table width="100%" cellpadding="0" cellspacing="0">{lignes}</table>
  </td></tr>

  <tr><td style="padding:0 32px 22px;">
    <table width="100%" cellpadding="0" cellspacing="0"
           style="background:#fffbeb;border-left:4px solid #D4A017;border-radius:0 8px 8px 0;">
      <tr><td style="padding:11px 14px;font-size:12px;color:#92400e;line-height:1.6;">
        ⚠️ <strong>Conservez</strong> cet email et votre autorisation PDF.
        Ils sont indispensables pour le retrait de votre nouvelle pièce.
      </td></tr>
    </table>
  </td></tr>

  <tr><td style="background:#f8fafc;padding:16px 28px;border-top:1px solid #e5e7eb;text-align:center;">
    <p style="margin:0;font-size:10px;color:#9ca3af;line-height:1.6;">
      Email envoyé le {date_envoi}<br/>
      DéclaTogo — Plateforme officielle, République Togolaise<br/>
      <em>Cet email est automatique, merci de ne pas y répondre.</em></p>
  </td></tr>

  <tr><td style="height:5px;padding:0;">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td style="background:#C41230;width:40%;height:5px;"></td>
      <td style="background:#D4A017;width:20%;height:5px;"></td>
      <td style="background:#005A3C;width:40%;height:5px;"></td>
    </tr></table></td></tr>

</table></td></tr></table>
</body></html>"""


def envoyer_email_remplacement(type_etape: str, user, demande) -> bool:
    """
    Envoie un email de notification pour le workflow de remplacement.

    Args:
        type_etape : clé parmi 'ouverture', 'recepisse_emis', 'en_traitement',
                     'document_pret', 'retire'
        user       : instance User destinataire
        demande    : instance DemandeRemplacement

    Returns:
        True si envoi réussi, False sinon.
    """
    if not user.email:
        logger.info("Email remplacement non envoyé à %s : pas d'adresse.", user.username)
        return False

    etape = _ETAPES.get(type_etape)
    if not etape:
        logger.warning("Type d'étape inconnu : %s", type_etape)
        return False

    nom = f"{user.first_name} {user.last_name}".strip() or user.username
    decl = demande.declaration

    sujet = etape['sujet_tpl'].format(num_dossier=demande.numero_dossier)

    # Texte brut
    texte = (
        f"Bonjour {nom},\n\n"
        f"Dossier N° {demande.numero_dossier}\n"
        f"Réf. perte : {decl.numero_recepisse}\n\n"
        + etape['texte_intro'].replace('<b>', '').replace('</b>', '').format(
            num_dossier=demande.numero_dossier,
            num_recepisse=decl.numero_recepisse
        )
        + "\n\nÉtapes :\n"
        + "\n".join(f"  {i}. {instr}" for i, instr in enumerate(etape['instructions'], 1))
        + "\n\n— L'équipe DéclaTogo\nPlateforme officielle — République Togolaise"
    )

    # HTML
    html = _html_email(
        etape_data=etape,
        nom=nom,
        num_dossier=demande.numero_dossier,
        num_recepisse=decl.numero_recepisse,
        commissariat=demande.commissariat,
        adresse=demande.adresse_commissariat,
        horaires=demande.horaires_commissariat,
        remarques=demande.remarques,
    )

    try:
        expediteur = (
            getattr(settings, 'DEFAULT_FROM_EMAIL', None)
            or getattr(settings, 'EMAIL_HOST_USER', 'noreply@declatogo.tg')
        )
        msg = EmailMultiAlternatives(
            subject=sujet,
            body=texte,
            from_email=f"DéclaTogo <{expediteur}>",
            to=[user.email],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send(fail_silently=False)
        logger.info("Email '%s' envoyé à %s <%s> — dossier %s",
                    type_etape, user.username, user.email, demande.numero_dossier)
        return True
    except Exception as exc:
        logger.error("Échec email '%s' à %s — dossier %s : %s",
                     type_etape, user.username, demande.numero_dossier, exc)
        return False
