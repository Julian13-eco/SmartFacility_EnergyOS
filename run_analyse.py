import sqlite3
import pandas as pd
import os

# Fichier qui me permet de lancer mes requêtes SQL
def lancer_analyse(fichier_sql):
    db_path = 'projet_energie.db'
    sql_path = os.path.join('sql_queries', fichier_sql)
    
    # Vérification que le fichier existe avant de tenter de l'ouvrir
    if not os.path.exists(sql_path):
        print(f"❌ Erreur : Impossible de trouver le fichier {sql_path}")
        return

    with open(sql_path, 'r', encoding='utf-8') as f:
        query = f.read()
    
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(query, conn)
        # CORRECTION : Ajout des guillemets autour du nom du fichier dans le print
        print(f"\n📊 Résultat de l'analyse ('{fichier_sql}') :")
        print(df.to_string(index=False))
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de la requête : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    lancer_analyse("analyse_pics.sql")