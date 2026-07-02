import sqlite3
import pandas as pd

# OCalcule les limites de consommation de chaque service (le percentile 95 pour la maintenance et la règle des 85% pour la sécurité) grâce à la puissance statistique de la bibliothèque Pandas.
def calculer_seuils_critiques():
    db_path = '../projet_energie.db'
    conn = sqlite3.connect(db_path)
    
    # Exécute la requête des pics de puissance en base de données, affiche le bilan dans le terminal et génère automatiquement le fichier CSV associé.
    query = "SELECT service, consommation_kw FROM consommations_courbes;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Calcul des indicateurs par service
    rapport_seuils = []
    for service, group in df.groupby('service'):
        max_historique = group['consommation_kw'].max()
        
        # Méthode A : 85% du max
        seuil_vigilance = max_historique * 0.85
        
        # Méthode B : 95ème percentile
        seuil_statistique = group['consommation_kw'].quantile(0.95)
        
        rapport_seuils.append({
            'Service': service,
            'Max Historique (kW)': round(max_historique, 2),
            'Seuil Vigilance (85% du Max)': round(seuil_vigilance, 2),
            'Seuil Normal Haut (Percentile 95)': round(seuil_statistique, 2)
        })
    
    # Affichage du tableau de synthèse
    df_seuils = pd.DataFrame(rapport_seuils)
    print("\n🛡️ SEUILS DE PUISSANCE CALCULÉS POUR LES ALERTES :")
    print(df_seuils.to_string(index=False))
    
    # Sauvegarde pour Power BI ou ton futur script d'alerte API
    df_seuils.to_csv('seuils_alertes_services.csv', sep=';', index=False, encoding='utf-8-sig')
    print("\n💾 Fichier 'seuils_alertes_services.csv' enregistré.")

if __name__ == "__main__":
    calculer_seuils_critiques()