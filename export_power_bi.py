import sqlite3
import pandas as pd
import os

def exporter_pour_powerbi():
    db_path = 'projet_energie.db'
    
    # On se connecte et on récupère la requête d'évaluation économique
    sql_path = os.path.join('sql_queries', 'evaluation_economique.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        query = f.read()
        
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Export en CSV (séparateur point-virgule pour Excel/Power BI français)
    output_path = 'export_analyse_energetique.csv'
    df.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')
    
    print(f"✅ Fichier '{output_path}' généré avec succès !")
    print("Tu peux maintenant le glisser-déposer dans Power BI.")

if __name__ == "__main__":
    exporter_pour_powerbi()