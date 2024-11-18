import pandas as pd

# Lire le fichier CSV
df = pd.read_csv('datas/all/FacebookAdLibraryReport_2024-11-14_FR_lifelong_advertisers.csv')

# Afficher les statistiques avant nettoyage
print(f"Nombre de lignes original : {len(df)}")

# Filtrer les lignes où "Amount spent (EUR)" n'est pas égal à "≤100"
df_cleaned = df[df['Amount spent (EUR)'] != '≤100']

# Convertir la colonne "Amount spent (EUR)" en numérique
df_cleaned['Amount spent (EUR)'] = df_cleaned['Amount spent (EUR)'].str.replace(',', '').astype(float)

# Afficher les statistiques après nettoyage
print(f"Nombre de lignes après nettoyage : {len(df_cleaned)}")
print(f"Nombre de lignes supprimées : {len(df) - len(df_cleaned)}")
somme_totale = df_cleaned['Amount spent (EUR)'].sum()
print(f"Somme totale dépensée : {somme_totale:.2f} EUR")
print(f"Différence avec 59 316 580 : {59_316_580 - somme_totale:.2f} EUR")

# Définir les tranches
bins = [100, 1000, 3000, 5000, 10000, 20000, 50000, 100000, 200000, float('inf')]
labels = ['100-1000', '1000-3000', '3000-5000', '5000-10000', '10000-20000', 
          '20000-50000', '50000-100000', '100000-200000', '>200000']

# Créer les catégories et compter
categories = pd.cut(df_cleaned['Amount spent (EUR)'], bins=bins, labels=labels)
distribution = categories.value_counts().sort_index()

# Afficher les résultats
print("\nDistribution des dépenses:")
for categorie, count in distribution.items():
    print(f"Annonceurs dépensant {categorie} EUR: {count}")

# Afficher le pourcentage pour chaque catégorie
print("\nPourcentage par catégorie:")
pourcentages = (distribution / len(df_cleaned) * 100).round(2)
for categorie, pourcentage in pourcentages.items():
    print(f"Catégorie {categorie} EUR: {pourcentage}%")

# Sauvegarder le fichier nettoyé
df_cleaned.to_csv('datas/all/FacebookAdLibraryReport_cleaned.csv', index=False)
