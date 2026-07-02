import pandas as pd
import glob
import os

def compiler_quotidiens():
    # Cible les fichiers dans le dossier quotidien
    fichiers = glob.glob("raw_data/quotidient/*.csv")
    all_dfs = []

    if not fichiers:
        print("❌ Aucun fichier trouvé dans raw_data/quotidient/")
        return

    for f in fichiers:
        print(f"📄 Traitement : {os.path.basename(f)}")
        
        # Le header est à la ligne 15 (index 14), on saute donc les 14 premières lignes
        df = pd.read_csv(f, skiprows=14, sep=',')
        
        # Sélection des colonnes : 
        # Index 1 = Date, Index 2 = Valeur (selon la structure constatée)
        df_clean = df.iloc[:, [1, 2]].copy()
        df_clean.columns = ['horodatage', 'consommation_kwh']
        
        # Nettoyage : suppression des guillemets et transformation de la virgule en point
        df_clean['consommation_kwh'] = df_clean['consommation_kwh'].astype(str).str.replace('"', '').str.replace(',', '.')
        
        # Conversion forcée en nombre (les erreurs deviennent NaN)
        df_clean['consommation_kwh'] = pd.to_numeric(df_clean['consommation_kwh'], errors='coerce')
        
        # Suppression des lignes vides (ex: lignes d'en-tête résiduelles)
        df_clean = df_clean.dropna()
        
        # Extraction du PRM (nom du fichier : prm_25212879756250_daily.csv)
        nom_fichier = os.path.basename(f)
        df_clean['compteur_id'] = nom_fichier.split('_')[1]
        
        all_dfs.append(df_clean)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        # Sauvegarde format Excel France (séparateur point-virgule et virgule décimale)
        final_df.to_csv("master_quotidient.csv", index=False, sep=';', decimal=',')
        print("\n✅ Succès ! 'master_quotidient.csv' est prêt.")
    else:
        print("❌ Aucune donnée n'a pu être extraite.")

if __name__ == "__main__":
    compiler_quotidiens()