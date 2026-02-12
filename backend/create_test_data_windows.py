"""
Script pour créer des données de test
Exécutez avec : python create_test_data_windows.py
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from declarations.models import CategoriePiece, Declaration
from datetime import datetime, timedelta

User = get_user_model()

print("=" * 60)
print("Création des données de test")
print("=" * 60)
print()

# 1. Créer des utilisateurs de test
print("1. Création des utilisateurs...")

# Admin
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@declarations.tg',
        'first_name': 'Administrateur',
        'last_name': 'Système',
        'role': 'admin',
        'telephone': '+22890000001',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"✓ Admin créé : {admin.username}")
else:
    print(f"- Admin existe : {admin.username}")

# Agent de police
police, created = User.objects.get_or_create(
    username='police',
    defaults={
        'email': 'police@declarations.tg',
        'first_name': 'Agent',
        'last_name': 'KOFFI',
        'role': 'police',
        'telephone': '+22890000002',
        'is_staff': True
    }
)
if created:
    police.set_password('police123')
    police.save()
    print(f"✓ Agent police créé : {police.username}")

# Citoyens
citoyens_data = [
    {
        'username': 'jean_akodjo',
        'email': 'jean@example.tg',
        'first_name': 'Jean',
        'last_name': 'AKODJO',
        'telephone': '+22890123456'
    },
    {
        'username': 'marie_eklou',
        'email': 'marie@example.tg',
        'first_name': 'Marie',
        'last_name': 'EKLOU',
        'telephone': '+22890123457'
    },
    {
        'username': 'kofi_mensah',
        'email': 'kofi@example.tg',
        'first_name': 'Kofi',
        'last_name': 'MENSAH',
        'telephone': '+22890123458'
    }
]

citoyens = []
for data in citoyens_data:
    citoyen, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'telephone': data['telephone'],
            'role': 'citoyen'
        }
    )
    if created:
        citoyen.set_password('citoyen123')
        citoyen.save()
        print(f"✓ Citoyen créé : {citoyen.username}")
    citoyens.append(citoyen)

# 2. Récupérer les catégories
print("\n2. Récupération des catégories...")
categories = list(CategoriePiece.objects.all())
if not categories:
    print("⚠️ Aucune catégorie trouvée. Exécutez d'abord init_categories_windows.py")
    sys.exit(1)
print(f"✓ {len(categories)} catégories disponibles")

# 3. Créer des déclarations de PERTE
print("\n3. Création de déclarations de PERTE...")

pertes_data = [
    {
        'user': citoyens[0],
        'categorie': categories[0],  # Pièce d'identité
        'numero_piece': 'TG20240001',
        'nom_sur_piece': 'AKODJO Jean',
        'description': 'CNI perdue lors d\'un déplacement à Lomé',
        'lieu_perte': 'Marché de Lomé',
        'date_perte': datetime.now() - timedelta(days=3),
        'statut': 'VALIDE'
    },
    {
        'user': citoyens[1],
        'categorie': categories[1],  # Véhicule
        'numero_piece': 'AB-1234-CD',
        'nom_sur_piece': 'EKLOU Marie',
        'description': 'Carte grise perdue',
        'lieu_perte': 'Boulevard du 13 Janvier',
        'date_perte': datetime.now() - timedelta(days=5),
        'statut': 'VALIDE'
    },
    {
        'user': citoyens[2],
        'categorie': categories[0],  # Pièce d'identité
        'numero_piece': 'TG20240002',
        'nom_sur_piece': 'MENSAH Kofi',
        'description': 'Passeport perdu à l\'aéroport',
        'lieu_perte': 'Aéroport de Lomé',
        'date_perte': datetime.now() - timedelta(days=1),
        'statut': 'EN_ATTENTE'
    },
    {
        'user': citoyens[0],
        'categorie': categories[2],  # Documents scolaires
        'numero_piece': 'DIPLOME-2023-001',
        'nom_sur_piece': 'AKODJO Jean',
        'description': 'Diplôme de licence perdu',
        'lieu_perte': 'Université de Lomé',
        'date_perte': datetime.now() - timedelta(days=10),
        'statut': 'VALIDE'
    }
]

for perte in pertes_data:
    declaration, created = Declaration.objects.get_or_create(
        type_declaration='PERTE',
        numero_piece=perte['numero_piece'],
        defaults=perte
    )
    if created:
        print(f"✓ Perte créée : {declaration.numero_recepisse}")

# 4. Créer des déclarations de TROUVAILLE
print("\n4. Création de déclarations de TROUVAILLE...")

trouvailles_data = [
    {
        'user': citoyens[1],
        'categorie': categories[0],  # Pièce d'identité
        'numero_piece': 'TG20240001',  # Correspond à la perte de Jean
        'nom_sur_piece': 'AKODJO Jean',
        'description': 'CNI trouvée près du marché',
        'lieu_perte': 'Avenue de la Paix, Lomé',
        'date_perte': datetime.now() - timedelta(days=2),
        'statut': 'VALIDE'
    },
    {
        'user': citoyens[2],
        'categorie': categories[3],  # Documents bancaires
        'numero_piece': '1234-5678-9012-3456',
        'nom_sur_piece': 'DUPONT Pierre',
        'description': 'Carte bancaire trouvée',
        'lieu_perte': 'Supermarché Casino',
        'date_perte': datetime.now() - timedelta(days=1),
        'statut': 'VALIDE'
    }
]

for trouvaille in trouvailles_data:
    declaration, created = Declaration.objects.get_or_create(
        type_declaration='TROUVAILLE',
        numero_piece=trouvaille['numero_piece'],
        nom_sur_piece=trouvaille['nom_sur_piece'],
        defaults=trouvaille
    )
    if created:
        print(f"✓ Trouvaille créée : {declaration.numero_recepisse}")

# 5. Créer une correspondance
print("\n5. Création d'une correspondance...")
try:
    perte_jean = Declaration.objects.get(
        type_declaration='PERTE',
        numero_piece='TG20240001'
    )
    trouvaille_jean = Declaration.objects.get(
        type_declaration='TROUVAILLE',
        numero_piece='TG20240001'
    )
    
    perte_jean.declaration_correspondante = trouvaille_jean
    perte_jean.statut = 'RETROUVE'
    perte_jean.save()
    
    trouvaille_jean.declaration_correspondante = perte_jean
    trouvaille_jean.statut = 'RETROUVE'
    trouvaille_jean.save()
    
    print(f"✓ Correspondance créée entre {perte_jean.numero_recepisse} et {trouvaille_jean.numero_recepisse}")
except:
    print("⚠️ Impossible de créer la correspondance")

# Résumé
print("\n" + "=" * 60)
print("RÉSUMÉ")
print("=" * 60)
print(f"Utilisateurs : {User.objects.count()}")
print(f"Catégories : {CategoriePiece.objects.count()}")
print(f"Déclarations : {Declaration.objects.count()}")
print(f"  - Pertes : {Declaration.objects.filter(type_declaration='PERTE').count()}")
print(f"  - Trouvailles : {Declaration.objects.filter(type_declaration='TROUVAILLE').count()}")
print(f"  - Retrouvées : {Declaration.objects.filter(statut='RETROUVE').count()}")

print("\n" + "=" * 60)
print("IDENTIFIANTS DE CONNEXION")
print("=" * 60)
print("Admin :")
print("  Username: admin")
print("  Password: admin123")
print("\nAgent de police :")
print("  Username: police")
print("  Password: police123")
print("\nCitoyens :")
print("  Username: jean_akodjo, marie_eklou, kofi_mensah")
print("  Password: citoyen123")

print("\n✅ Données de test créées avec succès !")