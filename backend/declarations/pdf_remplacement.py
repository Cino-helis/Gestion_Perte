"""
Générateur PDF — Autorisation officielle de remplacement de pièce.

Ce document est remis au citoyen par l'agent après 7 jours sans match.
Le citoyen le présente au commissariat agréé pour obtenir sa nouvelle pièce.

Usage :
    from declarations.pdf_remplacement import generate_autorisation_pdf
    buffer = generate_autorisation_pdf(demande)
"""

import io
from datetime import datetime, timedelta

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)

# ── Palette drapeau togolais ────────────────────────────────────────────────
VERT_TOGO    = colors.HexColor('#006A4E')
ROUGE_TOGO   = colors.HexColor('#D21034')
JAUNE_TOGO   = colors.HexColor('#FFCE00')
GRIS_CLAIR   = colors.HexColor('#F5F5F5')
GRIS_BORDURE = colors.HexColor('#CCCCCC')
BLEU_TAMPON  = colors.HexColor('#0D47A1')
NOIR         = colors.black
BLANC        = colors.white


def _get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('Entete',        fontSize=9,  textColor=GRIS_CLAIR, alignment=TA_CENTER, spaceAfter=2))
    styles.add(ParagraphStyle('TitreRepub',    fontSize=11, fontName='Helvetica-Bold', textColor=BLANC, alignment=TA_CENTER, spaceAfter=2))
    styles.add(ParagraphStyle('TitreDoc',      fontSize=15, fontName='Helvetica-Bold', textColor=VERT_TOGO, alignment=TA_CENTER, spaceBefore=10, spaceAfter=4))
    styles.add(ParagraphStyle('SousTitreDoc',  fontSize=11, fontName='Helvetica-Bold', textColor=ROUGE_TOGO, alignment=TA_CENTER, spaceAfter=6))
    styles.add(ParagraphStyle('SectionTitre',  fontSize=10, fontName='Helvetica-Bold', textColor=BLANC, alignment=TA_LEFT, leftIndent=6, spaceAfter=0))
    styles.add(ParagraphStyle('Corps',         fontSize=9,  textColor=NOIR, alignment=TA_LEFT, spaceAfter=3))
    styles.add(ParagraphStyle('CorpsCentre',   fontSize=9,  textColor=NOIR, alignment=TA_CENTER, spaceAfter=3))
    styles.add(ParagraphStyle('CorpsJustifie', fontSize=9,  textColor=NOIR, alignment=TA_JUSTIFY, spaceAfter=4, leading=14))
    styles.add(ParagraphStyle('Note',          fontSize=7.5,textColor=colors.HexColor('#555555'), alignment=TA_LEFT, spaceAfter=3))
    styles.add(ParagraphStyle('Alerte',        fontSize=9,  fontName='Helvetica-Bold', textColor=ROUGE_TOGO, alignment=TA_CENTER, spaceAfter=3))
    styles.add(ParagraphStyle('NumDossier',    fontSize=14, fontName='Helvetica-Bold', textColor=VERT_TOGO, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4))
    styles.add(ParagraphStyle('Validite',      fontSize=8,  textColor=colors.HexColor('#777777'), alignment=TA_CENTER, spaceAfter=2))
    return styles


def _ligne_section(titre, styles):
    cell = Paragraph(f"  {titre.upper()}", styles['SectionTitre'])
    t = Table([[cell]], colWidths=[17 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), VERT_TOGO),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return t


def _tableau_infos(donnees, styles):
    rows = [[
        Paragraph(f"<b>{label}</b>", styles['Corps']),
        Paragraph(str(val) if val else '—', styles['Corps'])
    ] for label, val in donnees]

    t = Table(rows, colWidths=[6 * cm, 11 * cm])
    style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_BORDURE),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    for i in range(len(rows)):
        style.add('BACKGROUND', (0, i), (-1, i), GRIS_CLAIR if i % 2 == 0 else BLANC)
    t.setStyle(style)
    return t


def generate_autorisation_pdf(demande) -> io.BytesIO:
    """
    Génère l'autorisation officielle de remplacement de pièce.

    Args:
        demande : instance DemandeRemplacement

    Returns:
        io.BytesIO : buffer PDF prêt à l'envoi
    """
    buffer = io.BytesIO()
    styles = _get_styles()
    decl   = demande.declaration
    user   = decl.user

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2 * cm, leftMargin=2 * cm,
        topMargin=1.5 * cm, bottomMargin=2 * cm,
        title=f"Autorisation de remplacement — {demande.numero_dossier}",
        author="Plateforme Déclarations Togo",
    )

    elems = []
    now   = datetime.now()
    validite = now + timedelta(days=60)

    # ── 1. EN-TÊTE OFFICIEL ──────────────────────────────────────────────────
    entete = Table([[
        Paragraph("REPUBLIQUE TOGOLAISE<br/>Travail – Liberté – Patrie", styles['TitreRepub']),
        Paragraph(
            "MINISTÈRE DE LA SÉCURITÉ ET DE LA PROTECTION CIVILE<br/>"
            "Direction Générale de la Police Nationale<br/>"
            "Service des Pièces Administratives",
            styles['Entete']
        ),
    ]], colWidths=[8.5 * cm, 8.5 * cm])
    entete.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), VERT_TOGO),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEAFTER', (0, 0), (0, 0), 1, JAUNE_TOGO),
    ]))
    elems.append(entete)
    elems.append(Spacer(1, 0.3 * cm))
    elems.append(HRFlowable(width="100%", thickness=4, color=ROUGE_TOGO, spaceAfter=6))

    # ── 2. TITRE ─────────────────────────────────────────────────────────────
    elems.append(Paragraph("AUTORISATION OFFICIELLE DE REMPLACEMENT", styles['TitreDoc']))
    elems.append(Paragraph("Pièce Administrative Perdue — Procédure Accélérée", styles['SousTitreDoc']))

    # Numéro de dossier
    num = Table([[Paragraph(f"N° Dossier : {demande.numero_dossier}", styles['NumDossier'])]],
                colWidths=[17 * cm])
    num.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 2, VERT_TOGO),
        ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLAIR),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elems.append(num)

    # Validité
    elems.append(Paragraph(
        f"Document valable jusqu'au {validite.strftime('%d/%m/%Y')} — "
        f"Émis le {now.strftime('%d/%m/%Y à %H:%M')}",
        styles['Validite']
    ))
    elems.append(Spacer(1, 0.4 * cm))

    # ── 3. ATTESTATION TEXTUELLE ─────────────────────────────────────────────
    nom_agent = f"{demande.traite_par.first_name} {demande.traite_par.last_name}".strip() if demande.traite_par else "l'agent responsable"
    nom_complet = f"{decl.nom_declarant or ''} {decl.prenom_declarant or ''}".strip() or decl.nom_sur_piece

    elems.append(Paragraph(
        f"Nous, soussignés, agents de la Direction Générale de la Police Nationale, "
        f"via la plateforme officielle <b>DéclaTogo</b>, attestons que "
        f"<b>{nom_complet}</b> a déclaré la perte de sa pièce administrative "
        f"sous la référence <b>{decl.numero_recepisse}</b>, "
        f"le <b>{decl.date_declaration.strftime('%d/%m/%Y')}</b>, "
        f"et qu'aucune trouvaille correspondante n'a été signalée dans le délai réglementaire de 7 jours. "
        f"En conséquence, le présent document autorise l'intéressé(e) à engager la procédure "
        f"de remplacement auprès du commissariat désigné ci-dessous.",
        styles['CorpsJustifie']
    ))
    elems.append(Spacer(1, 0.3 * cm))

    # ── 4. INFORMATIONS DU DÉCLARANT ─────────────────────────────────────────
    elems.append(_ligne_section("Identité du déclarant", styles))
    elems.append(Spacer(1, 0.15 * cm))
    elems.append(_tableau_infos([
        ("Nom complet",       f"{user.last_name} {user.first_name}".strip() or user.username),
        ("Nom sur la pièce",  nom_complet),
        ("Date de naissance", decl.date_naissance.strftime('%d/%m/%Y') if decl.date_naissance else "—"),
        ("Lieu de naissance", decl.lieu_naissance or "—"),
        ("Profession",        decl.profession or "—"),
        ("Téléphone",         user.telephone or "—"),
        ("Email",             user.email or "—"),
    ], styles))
    elems.append(Spacer(1, 0.4 * cm))

    # ── 5. PIÈCE PERDUE ──────────────────────────────────────────────────────
    elems.append(_ligne_section("Pièce perdue à remplacer", styles))
    elems.append(Spacer(1, 0.15 * cm))
    elems.append(_tableau_infos([
        ("Catégorie",           decl.categorie.libelle),
        ("Numéro de la pièce",  decl.numero_piece or "Non communiqué"),
        ("Date de perte",       decl.date_perte.strftime('%d/%m/%Y') if decl.date_perte else "—"),
        ("Lieu de perte",       decl.lieu_perte or "—"),
        ("Récépissé de perte",  decl.numero_recepisse),
        ("N° dossier remplacement", demande.numero_dossier),
    ], styles))
    elems.append(Spacer(1, 0.4 * cm))

    # ── 6. COMMISSARIAT DÉSIGNÉ ──────────────────────────────────────────────
    elems.append(_ligne_section("Commissariat agréé pour le remplacement", styles))
    elems.append(Spacer(1, 0.15 * cm))

    if demande.commissariat:
        elems.append(_tableau_infos([
            ("Commissariat",   demande.commissariat),
            ("Adresse",        demande.adresse_commissariat or "—"),
            ("Horaires",       demande.horaires_commissariat or "Lun.–Ven. 08h–16h"),
        ], styles))
    else:
        box = Table([[Paragraph(
            "⚠️  Le commissariat agréé sera communiqué par l'agent. "
            "Veuillez vous rapprocher du service DéclaTogo.",
            styles['Corps']
        )]], colWidths=[17 * cm])
        box.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, JAUNE_TOGO),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFBEB')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elems.append(box)
    elems.append(Spacer(1, 0.4 * cm))

    # ── 7. PIÈCES À FOURNIR ───────────────────────────────────────────────────
    elems.append(_ligne_section("Documents à présenter au commissariat", styles))
    elems.append(Spacer(1, 0.15 * cm))
    docs = [
        ["1", "Ce document (Autorisation de remplacement DéclaTogo)"],
        ["2", f"Le récépissé de perte original N° {decl.numero_recepisse}"],
        ["3", "Une pièce d'identité en cours de validité (ou tout document officiel)"],
        ["4", "Une photo d'identité récente (format passeport)"],
        ["5", "Le timbre fiscal réglementaire (se renseigner au commissariat)"],
    ]
    t_docs = Table(docs, colWidths=[1 * cm, 16 * cm])
    t_docs.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, GRIS_BORDURE),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (0, -1), VERT_TOGO),
        ('TEXTCOLOR', (0, 0), (0, -1), BLANC),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    for i in range(len(docs)):
        if i % 2 == 0:
            t_docs.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), GRIS_CLAIR)]))
    elems.append(t_docs)
    elems.append(Spacer(1, 0.5 * cm))

    # ── 8. SIGNATURE ─────────────────────────────────────────────────────────
    sig = Table([[
        Paragraph(
            f"Lomé, le {now.strftime('%d/%m/%Y')}<br/><br/><br/>"
            "<b>Le Déclarant</b><br/>(Signature)",
            styles['CorpsCentre']
        ),
        Paragraph(
            "<br/><br/><br/>"
            "<b>L'Agent Responsable</b><br/>"
            f"{nom_agent}<br/>"
            "(Cachet et Signature)",
            styles['CorpsCentre']
        ),
    ]], colWidths=[8.5 * cm, 8.5 * cm])
    sig.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, GRIS_BORDURE),
        ('LINEAFTER', (0, 0), (0, -1), 0.5, GRIS_BORDURE),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLAIR),
    ]))
    elems.append(sig)
    elems.append(Spacer(1, 0.3 * cm))

    # ── 9. AVERTISSEMENT ─────────────────────────────────────────────────────
    elems.append(HRFlowable(width="100%", thickness=1, color=VERT_TOGO, spaceAfter=5))
    elems.append(Paragraph(
        "⚠️  <b>Ce document est strictement personnel et non cessible.</b> "
        f"Il est valable uniquement jusqu'au {validite.strftime('%d/%m/%Y')} et "
        f"doit être présenté au commissariat agréé ci-dessus. "
        "Toute falsification est passible de poursuites judiciaires conformément au droit togolais.<br/>"
        f"DéclaTogo — Plateforme officielle — Réf. {demande.numero_dossier} — "
        f"Généré le {now.strftime('%d/%m/%Y à %H:%M')}",
        styles['Note']
    ))

    doc.build(elems)
    buffer.seek(0)
    return buffer
