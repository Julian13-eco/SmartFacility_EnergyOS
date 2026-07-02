import pandas as pd
import glob
import os  # <--- C'est cette ligne qui manquait !

def compiler_courbes():
    fichiers = glob.glob("raw_data/courbes_charge/*.csv")
    all_dfs = []

    if not fichiers:
        print("❌ Aucun fichier trouvé dans raw_data/courbes_charge/")
        return

    for f in fichiers:
        print(f"📄 Traitement : {os.path.basename(f)}")
        
        # Lecture en sautant les 16 premières lignes
        df = pd.read_csv(f, skiprows=16, sep=',')
        
        # Sélection des colonnes [Début, Valeur (en kW)]
        df_clean = df.iloc[:, [2, 4]].copy()
        df_clean.columns = ['horodatage', 'consommation_kw']
        
        # Nettoyage et conversion
        df_clean['consommation_kw'] = df_clean['consommation_kw'].astype(str).str.replace('"', '').str.replace(',', '.')
        df_clean['consommation_kw'] = pd.to_numeric(df_clean['consommation_kw'])
        
        # Extraction du PRM (le bloc avant le premier '_')
        nom_fichier = os.path.basename(f)
        df_clean['compteur_id'] = nom_fichier.split('_')[0]
        
        all_dfs.append(df_clean)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        # Sauvegarde format Excel France
        final_df.to_csv("master_courbes.csv", index=False, sep=';', decimal=',')
        print("\n✅ Succès ! 'master_courbes.csv' est prêt avec le PRM correct.")
    else:
        print("❌ Aucune donnée n'a pu être extraite.")

if __name__ == "__main__":
    compiler_courbes()