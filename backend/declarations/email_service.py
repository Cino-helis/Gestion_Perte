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