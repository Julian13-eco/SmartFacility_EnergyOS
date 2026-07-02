import sqlite3
import pandas as pd
import os

def analyser_consommation_services():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'projet_energie.db')
    
    conn = sqlite3.connect(db_path)
    
    # Requête SQL pour analyser les consommations quotidiennes par service
    query = """
    SELECT 
        service,
        ROUND(SUM(consommation_kwh), 2) as consommation_totale_kwh,
        ROUND(AVG(consommation_kwh), 2) as moyenne_journaliere_kwh,
        COUNT(horodatage) as jours_enregistres
    FROM consommations_quotidiennes
    GROUP BY service
    ORDER BY consommation_totale_kwh DESC;
    """
    
    df_analyse = pd.read_sql_query(query, conn)
    conn.close()
    
    print("\n📊 --- RAPPORT ÉNERGÉTIQUE PAR SERVICE ---")
    print(df_analyse.to_string(index=False))

if __name__ == "__main__":
    analyser_consommation_services()