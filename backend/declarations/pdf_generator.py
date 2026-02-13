"""
Générateur de récépissés PDF avec ReportLab
Produit un document officiel de style administratif togolais.

Installation requise :
    pip install reportlab pillow

Usage :
    from declarations.pdf_generator import generer_recepisse_pdf
    buffer = generer_recepisse_pdf(declaration)
    # buffer est un BytesIO prêt à être envoyé en réponse HTTP
"""

import io
from datetime import datetime

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)


# =============================================================================
# COULEURS DU DRAPEAU TOGOLAIS (rouge, vert, blanc)
# =============================================================================
VERT_TOGO    = colors.HexColor('#006A4E')
ROUGE_TOGO   = colors.HexColor('#D21034')
JAUNE_TOGO   = colors.HexColor('#FFCE00')
GRIS_CLAIR   = colors.HexColor('#F5F5F5')
GRIS_BORDURE = colors.HexColor('#CCCCCC')
NOIR         = colors.black
BLANC        = colors.white


# =============================================================================
# STYLES TYPOGRAPHIQUES
# =============================================================================

def _get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name='Entete',
        fontSize=9,
        textColor=GRIS_CLAIR,
        alignment=TA_CENTER,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='TitreRepublique',
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=BLANC,
        alignment=TA_CENTER,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='TitreDocument',
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=VERT_TOGO,
        alignment=TA_CENTER,
        spaceBefore=12,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name='SousTitre',
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=ROUGE_TOGO,
        alignment=TA_CENTER,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name='SectionTitre',
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=BLANC,
        alignment=TA_LEFT,
        leftIndent=6,
        spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        name='Corps',
        fontSize=9,
        textColor=NOIR,
        alignment=TA_LEFT,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name='CorpsCentre',
        fontSize=9,
        textColor=NOIR,
        alignment=TA_CENTER,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name='Note',
        fontSize=8,
        textColor=colors.HexColor('#555555'),
        alignment=TA_LEFT,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name='NumeroBold',
        fontSize=13,
        fontName='Helvetica-Bold',
        textColor=VERT_TOGO,
        alignment=TA_CENTER,
        spaceBefore=6,
        spaceAfter=6,
    ))

    return styles


# =============================================================================
# FONCTIONS HELPERS
# =============================================================================

def _ligne_section(titre, styles):
    """Retourne un tableau d'une ligne faisant office de titre de section."""
    cell = Paragraph(f"  {titre.upper()}", styles['SectionTitre'])
    table = Table([[cell]], colWidths=[17 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), VERT_TOGO),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
    ]))
    return table


def _tableau_infos(donnees, styles):
    """
    Crée un tableau à deux colonnes (label | valeur) avec style alternance.
    donnees : liste de (str label, str valeur)
    """
    rows = []
    for label, valeur in donnees:
        rows.append([
            Paragraph(f"<b>{label}</b>", styles['Corps']),
            Paragraph(str(valeur) if valeur else '—', styles['Corps'])
        ])

    table = Table(rows, colWidths=[6 * cm, 11 * cm])
    style = TableStyle([
        ('GRID',          (0, 0), (-1, -1), 0.5, GRIS_BORDURE),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ])

    # Alternance de couleurs sur les lignes
    for i in range(len(rows)):
        bg = GRIS_CLAIR if i % 2 == 0 else BLANC
        style.add('BACKGROUND', (0, i), (-1, i), bg)

    table.setStyle(style)
    return table


# =============================================================================
# GENERATEUR PRINCIPAL
# =============================================================================

def generate_recepisse_pdf(declaration) -> io.BytesIO:
    """
    Génère le PDF de récépissé pour une déclaration.

    Args:
        declaration : instance du modèle Declaration

    Returns:
        io.BytesIO : buffer contenant le PDF prêt à l'envoi
    """
    buffer = io.BytesIO()
    styles = _get_styles()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.5 * cm,
        bottomMargin=2 * cm,
        title=f"Récépissé {declaration.numero_recepisse}",
        author="Plateforme Déclarations Togo",
    )

    elements = []

    # ------------------------------------------------------------------
    # 1. EN-TÊTE OFFICIEL
    # ------------------------------------------------------------------
    entete_data = [[
        Paragraph("REPUBLIQUE TOGOLAISE<br/>Travail – Liberté – Patrie", styles['TitreRepublique']),
        Paragraph(
            "MINISTÈRE DE LA SÉCURITÉ ET DE LA PROTECTION CIVILE<br/>"
            "Direction Générale de la Police Nationale",
            styles['Entete']
        ),
    ]]
    entete_table = Table(entete_data, colWidths=[8.5 * cm, 8.5 * cm])
    entete_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), VERT_TOGO),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEAFTER',     (0, 0), (0, 0), 1, JAUNE_TOGO),
    ]))
    elements.append(entete_table)
    elements.append(Spacer(1, 0.4 * cm))

    # Bande rouge décorative
    elements.append(HRFlowable(width="100%", thickness=4, color=ROUGE_TOGO, spaceAfter=6))

    # ------------------------------------------------------------------
    # 2. TITRE PRINCIPAL
    # ------------------------------------------------------------------
    type_display = declaration.get_type_declaration_display().upper()
    elements.append(Paragraph(
        f"RÉCÉPISSÉ DE DÉCLARATION DE {type_display}",
        styles['TitreDocument']
    ))
    elements.append(Paragraph(
        f"Pièces et Documents Administratifs",
        styles['SousTitre']
    ))

    # Numéro de récépissé encadré
    num_data = [[Paragraph(
        f"N° {declaration.numero_recepisse}",
        styles['NumeroBold']
    )]]
    num_table = Table(num_data, colWidths=[17 * cm])
    num_table.setStyle(TableStyle([
        ('BOX',           (0, 0), (-1, -1), 2, VERT_TOGO),
        ('BACKGROUND',    (0, 0), (-1, -1), GRIS_CLAIR),
        ('TOPPADDING',    (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(num_table)
    elements.append(Spacer(1, 0.4 * cm))

    # ------------------------------------------------------------------
    # 3. INFORMATIONS DU DÉCLARANT
    # ------------------------------------------------------------------
    elements.append(_ligne_section("Informations du déclarant", styles))
    elements.append(Spacer(1, 0.15 * cm))

    user = declaration.user
    infos_declarant = [
        ("Nom complet",    f"{user.last_name} {user.first_name}".strip() or user.username),
        ("Nom d'utilisateur", user.username),
        ("Téléphone",      user.telephone or "Non renseigné"),
        ("Email",          user.email or "Non renseigné"),
    ]
    elements.append(_tableau_infos(infos_declarant, styles))
    elements.append(Spacer(1, 0.4 * cm))

    # ------------------------------------------------------------------
    # 4. INFORMATIONS SUR LA PIÈCE
    # ------------------------------------------------------------------
    elements.append(_ligne_section("Informations sur la pièce", styles))
    elements.append(Spacer(1, 0.15 * cm))

    date_perte_str = (
        declaration.date_perte.strftime('%d/%m/%Y')
        if declaration.date_perte else "Non renseignée"
    )

    infos_piece = [
        ("Catégorie",          declaration.categorie.libelle),
        ("Numéro de la pièce", declaration.numero_piece),
        ("Nom sur la pièce",   declaration.nom_sur_piece),
        ("Date de la perte",   date_perte_str),
        ("Lieu",               declaration.lieu_perte or "Non renseigné"),
        ("Description",        declaration.description or "Aucune description"),
    ]
    elements.append(_tableau_infos(infos_piece, styles))
    elements.append(Spacer(1, 0.4 * cm))

    # ------------------------------------------------------------------
    # 5. INFORMATIONS ADMINISTRATIVES
    # ------------------------------------------------------------------
    elements.append(_ligne_section("Informations administratives", styles))
    elements.append(Spacer(1, 0.15 * cm))

    date_declaration_str = timezone.localtime(declaration.date_declaration).strftime(
        '%d/%m/%Y à %H:%M'
    )
    statut_display = declaration.get_statut_display()

    infos_admin = [
        ("Numéro de récépissé", declaration.numero_recepisse),
        ("Type de déclaration", declaration.get_type_declaration_display()),
        ("Statut actuel",       statut_display),
        ("Date de déclaration", date_declaration_str),
    ]

    if declaration.remarques_admin:
        infos_admin.append(("Remarques", declaration.remarques_admin))

    if declaration.declaration_correspondante:
        infos_admin.append((
            "Correspondance",
            f"Déclaration {declaration.declaration_correspondante.numero_recepisse}"
        ))

    elements.append(_tableau_infos(infos_admin, styles))
    elements.append(Spacer(1, 0.5 * cm))

    # ------------------------------------------------------------------
    # 6. ZONE DE SIGNATURE
    # ------------------------------------------------------------------
    date_impression = datetime.now().strftime('%d/%m/%Y à %H:%M')

    signature_data = [[
        Paragraph(
            f"Fait à Lomé, le {date_impression}<br/><br/><br/>"
            "<b>Le Déclarant</b><br/>(Signature)",
            styles['CorpsCentre']
        ),
        Paragraph(
            "<br/><br/><br/>"
            "<b>Le Responsable du Service</b><br/>(Cachet et Signature)",
            styles['CorpsCentre']
        ),
    ]]
    sig_table = Table(signature_data, colWidths=[8.5 * cm, 8.5 * cm])
    sig_table.setStyle(TableStyle([
        ('BOX',        (0, 0), (-1, -1), 0.5, GRIS_BORDURE),
        ('LINEAFTER',  (0, 0), (0, -1), 0.5, GRIS_BORDURE),
        ('TOPPADDING',    (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLAIR),
    ]))
    elements.append(sig_table)
    elements.append(Spacer(1, 0.3 * cm))

    # ------------------------------------------------------------------
    # 7. PIED DE PAGE
    # ------------------------------------------------------------------
    elements.append(HRFlowable(width="100%", thickness=1, color=VERT_TOGO, spaceAfter=6))
    elements.append(Paragraph(
        "⚠️  <b>Ce document est un récépissé de déclaration et ne constitue pas une pièce d'identité.</b><br/>"
        "Plateforme officielle de déclaration de pertes de pièces administratives — République Togolaise<br/>"
        f"Document généré le {date_impression} — Réf : {declaration.numero_recepisse}",
        styles['Note']
    ))

    # ------------------------------------------------------------------
    # CONSTRUCTION DU PDF
    # ------------------------------------------------------------------
    doc.build(elements)
    buffer.seek(0)
    return buffer