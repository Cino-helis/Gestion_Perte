"""
Script pour créer les catégories de pièces initiales
Exécutez avec : python init_categories_windows.py
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from declarations.models import CategoriePiece

# Liste des catégories de pièces au Togo
categories = [
    {
        'libelle': 'Pièce d\'identité',
        'description': 'Carte Nationale d\'Identité (CNI), passeport',
        'icone': 'id-card'
    },
    {
        'libelle': 'Véhicule',
        'description': 'Carte grise, permis de conduire, plaque d\'immatriculation',
        'icone': 'car'
    },
    {
        'libelle': 'Documents scolaires',
        'description': 'Diplômes, certificats, cartes d\'étudiant',
        'icone': 'graduation-cap'
    },
    {
        'libelle': 'Documents bancaires',
        'description': 'Cartes bancaires, chéquiers',
        'icone': 'credit-card'
    },
    {
        'libelle': 'Documents professionnels',
        'description': 'Badges, cartes professionnelles',
        'icone': 'briefcase'
    },
    {
        'libelle': 'Documents de santé',
        'description': 'Cartes de santé, carnets de vaccination',
        'icone': 'heart'
    },
    {
        'libelle': 'Autres documents',
        'description': 'Tout autre document administratif',
        'icone': 'file'
    }
]

print("Création des catégories de pièces...")
print("=" * 50)

for cat_data in categories:
    categorie, created = CategoriePiece.objects.get_or_create(
        libelle=cat_data['libelle'],
        defaults={
            'description': cat_data['description'],
            'icone': cat_data['icone']
        }
    )
    if created:
        print(f"✓ Créée : {categorie.libelle}")
    else:
        print(f"- Existe déjà : {categorie.libelle}")

print("=" * 50)
print(f"\nTotal : {CategoriePiece.objects.count()} catégories dans la base")
print("\n✅ Catégories créées avec succès !")