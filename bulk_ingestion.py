import sqlite3
import pandas as pd
import os

def injecter_donnees():
    # Définit le dossier où se trouve ce script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'projet_energie.db')
    
    # 1. Connexion (crée le fichier .db automatiquement s'il n'existe pas)
    conn = sqlite3.connect(db_path)
    
    # 2. Chargement de la configuration
    config_path = os.path.join(base_dir, 'config_compteurs.csv')
    if not os.path.exists(config_path):
        print(f"❌ Erreur : Fichier {config_path} introuvable.")
        return
    df_config = pd.read_csv(config_path)
    
    # 3. Liste des fichiers à injecter
    fichiers = {
        'master_courbes.csv': 'consommations_courbes',
        'master_quotidient.csv': 'consommations_quotidiennes'
    }

    for fichier, table in fichiers.items():
        chemin_fichier = os.path.join(base_dir, fichier)
        
        if os.path.exists(chemin_fichier):
            print(f"📥 Injection de {fichier}...")
            df = pd.read_csv(chemin_fichier, sep=';', decimal=',')
            
            # Jointure avec la config
            # On s'assure que les colonnes sont bien en type 'int64' pour le merge
            df['compteur_id'] = df['compteur_id'].astype('int64')
            df_config['prm'] = df_config['prm'].astype('int64')
            
            df = df.merge(df_config, left_on='compteur_id', right_on='prm', how='left')
            df = df.drop(columns=['prm'])
            
            # Injection
            df.to_sql(table, conn, if_exists='replace', index=False)
            print(f"✅ {table} injectée.")
        else:
            print(f"⚠️ Fichier {fichier} introuvable, passé.")

    conn.close()
    print("\n🏁 Base de données 'projet_energie.db' recréée et remplie avec succès !")

if __name__ == "__main__":
    injecter_donnees()