import pandas as pd


# du 15/04/2019 au 17/11/2024
# Lire le fichier CSV
df = pd.read_csv('datas/all/FacebookAdLibraryReport_cleaned.csv')

# Liste étendue de mots-clés liés au RN et ses personnalités
mots_cles_rn = [
    # Noms officiels du parti
    'rassemblement national',
    'front national',
    
    # Famille Le Pen
    'le pen',
    'marine le pen',
    'jean-marie le pen',
    
    # Direction actuelle et cadres
    'jordan bardella',
    'bardella',
    'jérôme rivière',
    'jean-lin lacapelle',
    'virginie joron',
    'julie lechanteux',
    'hélène laporte',
    'philippe vardon',
    'catherine griset',
    'mathilde androuët',
    'julien leonardelli',
    'philippe olivier',
    'gilles lebreton',
    'stéphane blanchon',
    
    # Groupes politiques européens
    'identité et démocratie',
    'groupe identité et démocratie',
    
    # Cadres et personnalités importantes
    'louis aliot',
    'steeve briois',
    'nicolas bay',
    'gilbert collard',
    'thierry mariani',
    'philippe olivier',
    'hervé juvin',
    'jean-paul garraud',
    'nicolas meizonnet',
    'edwige diaz',
    'julien odoul',
    'laurent jacobelli',
    'gilles pennelle',
    'sébastien chenu',
    'bruno bilde',
    'wallerand de saint-just',
    
    # Jeunes du RN
    'génération nation',
    'front national de la jeunesse',
    'génération rn',
    'jeunes avec marine',
    'collectif racine',
    
    # Slogans et expressions associées
    'marine présidente',
    'au nom du peuple',
    'priorité nationale',
    'bleu marine',
    'mariniste',
    
    # Médias et plateformes proches
    'nations presse info',
    'fn infos',
    'rn infos',
]

# Créer un DataFrame vide pour stocker les résultats
df_rn_final = pd.DataFrame()

# Traiter chaque mot-clé séparément
for mot_cle in mots_cles_rn:
    # Créer une copie explicite du DataFrame filtré
    mask = df['Page name'].str.lower().str.contains(mot_cle, na=False, regex=False)
    df_temp = df[mask].copy()  # Utilisation de .copy() pour créer une copie explicite
    
    # Vérifier si df_temp n'est pas vide avant d'ajouter la colonne
    if not df_temp.empty:
        df_temp['mot_cle_trouve'] = mot_cle
        df_rn_final = pd.concat([df_rn_final, df_temp])

# Supprimer les doublons basés sur l'identifiant unique de la publicité
df_rn_final = df_rn_final.drop_duplicates(subset=['Page name', 'Amount spent (EUR)', 'Number of ads in Library'])

# Remplacer l'ancien df_rn par le nouveau
df_rn = df_rn_final

# Sauvegarder le nouveau DataFrame dans un CSV
df_rn.to_csv('datas/all/FacebookAdLibraryReport_RN_complet.csv', index=False)

# Afficher des statistiques au format markdown
print("\n# Statistiques des publicités RN")
print("\n## Statistiques globales")
print(f"| Métrique | Valeur |")
print("|----------|---------|")
print(f"| Nombre total d'entrées | {len(df_rn):,} |")
print(f"| Nombre de pages uniques | {df_rn['Page name'].nunique():,} |")
print(f"| Montant total dépensé | {df_rn['Amount spent (EUR)'].sum():,.2f} € |")

# Calculer les métriques pour les statistiques détaillées
total_ads = df_rn['Number of ads in Library'].sum()
montant_total = df_rn['Amount spent (EUR)'].sum()
cout_moyen_par_pub = montant_total / total_ads if total_ads > 0 else 0

print("\n## Statistiques détaillées des publicités")
print(f"| Métrique | Valeur |")
print("|----------|---------|")
print(f"| Nombre total de publicités | {total_ads:,} |")
print(f"| Montant total dépensé | {montant_total:,.2f} € |")
print(f"| Coût moyen par publicité | {cout_moyen_par_pub:.2f} € |")

# Créer l'analyse par page
analyse_par_page = df_rn.groupby('Page name').agg({
    'Number of ads in Library': 'sum',
    'Amount spent (EUR)': 'sum'
}).reset_index()

# Calculer le coût moyen par pub
analyse_par_page['Coût moyen par pub'] = analyse_par_page['Amount spent (EUR)'] / analyse_par_page['Number of ads in Library']

# Trier par montant dépensé décroissant
analyse_par_page = analyse_par_page.sort_values('Amount spent (EUR)', ascending=False)

# Afficher le top 50 en format markdown
print("\n## Top 50 des pages avec les plus grandes dépenses")
print("| Nom de la page | Nombre de pubs | Montant dépensé (€) | Coût moyen par pub (€) |")
print("|----------------|----------------|-------------------|---------------------|")
for idx, row in analyse_par_page.head(50).iterrows():
    print(f"| {row['Page name']} | {int(row['Number of ads in Library']):,} | {row['Amount spent (EUR)']:,.2f} | {row['Coût moyen par pub']:.2f} |")

