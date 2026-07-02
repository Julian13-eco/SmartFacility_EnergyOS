import streamlit as st
import sqlite3
import pandas as pd
import os

# Configuration de l'application
st.set_page_config(page_title="Smart Facility Energy OS", layout="wide", page_icon="⚡")

# Fonction pour exécuter les requêtes SQL du projet
def executer_requete(nom_fichier_sql):
    chemin_sql = os.path.join('sql_queries', nom_fichier_sql)
    if not os.path.exists(chemin_sql):
        st.error(f"Fichier introuvable : {chemin_sql}")
        return None
    with open(chemin_sql, 'r', encoding='utf-8') as f:
        query = f.read()
    conn = sqlite3.connect("projet_energie.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- BARRE LATÉRALE : NAVIGATION ENTRE LES 5 PROTOTYPES ---
st.sidebar.title("🎮 Energy OS Navigation")
st.sidebar.write("Sélectionnez l'un des 5 prototypes web :")
page = st.sidebar.radio(
    "Vues de l'application :",
    [
        "1. Hub Énergétique (Dashboard)",
        "2. Chasse au Talon (Gaspillomètre)",
        "3. Planificateur de Contacteurs",
        "4. Superviseur des Pics & Seuils",
        "5. Registre des Équipements"
    ]
)

st.sidebar.write("---")
st.sidebar.info("💡 Objectif : Cibler la pose des contacteurs sur les vrais circuits dérivés en incluant les nuits et les week-ends.")

# ==============================================================================
# PROTOTYPE 1 : HUB ÉNERGÉTIQUE
# ==============================================================================
if page == "1. Hub Énergétique (Dashboard)":
    st.title("📊 Hub Énergétique Global")
    st.write("Vue d'ensemble de la performance du bâtiment.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Alerte Gaspillage", "72.3 %", "Courrier", delta_color="inverse")
    col2.metric("Talon Serveurs", "44.4 %", "PGCC Droite (Stable)")
    col3.metric("Zone Optimisée", "2.9 %", "Salle de réunion (Top)")
    
    df_talon = executer_requete("comparaison_services.sql")
    if df_talon is not None:
        st.subheader("Classement général des consommations (Taux de Talon %)")
        st.bar_chart(data=df_talon, x="service", y="taux_talon_pourcentage")

# ==============================================================================
# PROTOTYPE 2 : CHASSE AU TALON (Mis à jour : Nuits + Week-ends)
# ==============================================================================
elif page == "2. Chasse au Talon (Gaspillomètre)":
    st.title("🦹 Le Gaspillomètre global (Nuits + Week-ends)")
    st.write("Analyse des périodes d'inoccupation totales (Semaine après 21h + Samedi et Dimanche complets).")
    
    # On utilise la requête globale d'inoccupation
    df_inoccupation = executer_requete("analyse_inoccupation.sql")
    
    if df_inoccupation is not None:
        # Renommer proprement les colonnes pour l'affichage web
        df_affichage = df_inoccupation.rename(columns={
            "service": "Service / Départ",
            "talon_inoccupation_kw": "Talon mesuré (kW)",
            "kwh_economisables_par_heure": "kWh économisables / heure",
            "economie_annuelle_inoccupation_euros": "Économie potentielle (€/an)"
        })
        st.dataframe(df_affichage, use_container_width=True)
        st.info("Cette analyse se base sur un volume de 4 836 heures d'inoccupation par an.")

# ==============================================================================
# PROTOTYPE 3 : PLANIFICATEUR DE CONTACTEURS (Mis à jour : Nuits + Week-ends)
# ==============================================================================
elif page == "3. Planificateur de Contacteurs":
    st.title("🔌 Simulateur d'Installation de Contacteurs")
    st.write("Coche les départs de ton tableau électrique pour simuler la pose d'un contacteur programmable (Coupure Nuits + Week-ends).")
    
    # Utilisation des données réelles Nuits + Week-ends
    df_inoccupation = executer_requete("analyse_inoccupation.sql")
    
    if df_inoccupation is not None:
        st.write("### Sélection des circuits à couper hors occupation :")
        services_a_couper = []
        
        for index, row in df_inoccupation.iterrows():
            # Configuration par défaut
            par_defaut = False
            if row['service'] == "Courrier":
                par_defaut = True  # Flagrant, on le pré-coche
                
            # Sécurité visuelle pour empêcher de couper les serveurs
            label_affichage = f"Coupure sur : {row['service']} ➔ Gain : {row['economie_annuelle_inoccupation_euros']} €/an"
            if "PGCC" in row['service'] or "RESPI" in row['service']:
                label_affichage += " ⚠️ (Infrastructure Critique)"
            
            if st.checkbox(label_affichage, value=par_defaut):
                services_a_couper.append(row['economie_annuelle_inoccupation_euros'])
        
        # Calcul du ROI réel combiné
        total_economise = sum(services_a_couper)
        st.write("---")
        st.subheader("💰 Rapport financier du plan de déploiement")
        
        if total_economise > 0:
            st.success(f"En installant des contacteurs sur les circuits sélectionnés, l'entreprise économise **{round(total_economise, 2)} € / an** (Nuits + Week-ends inclus).")
            
            # Petit calcul de coin de table pour le coût du matériel
            cout_estime_unitaire_contacteur = 120  # Prix moyen matériel + pose d'un contacteur modulaire
            nb_contacteurs = len(services_a_couper)
            cout_total_travaux = nb_contacteurs * cout_estime_unitaire_contacteur
            
            col_roi1, col_roi2 = st.columns(2)
            col_roi1.metric("Coût estimé des travaux", f"{cout_total_travaux} €", "Matériel & Main d'œuvre")
            
            roi_mois = (cout_total_travaux / total_economise) * 12
            col_roi2.metric("Retour sur Investissement (ROI)", f"{round(roi_mois, 1)} Mois", "Temps de rentabilisation")
        else:
            st.info("Cochez un ou plusieurs circuits pour calculer les gains cumulés.")

# ==============================================================================
# PROTOTYPE 4 : SUPERVISEUR DES PICS & MAINTENANCE
# ==============================================================================
elif page == "4. Superviseur des Pics & Seuils":
    st.title("⚡ Surveillance des Pics de Puissance (J+1)")
    st.write("Analyse des pointes pour la maintenance préventive.")
    
    df_pics = executer_requete("analyse_pics.sql")
    if df_pics is not None:
        st.write("### Historique des records constatés :")
        st.dataframe(df_pics, use_container_width=True)
        st.warning("Rappel : Les pics majeurs ont lieu en Janvier entre 8h et 10h (Relance matinale d'hiver).")

# ==============================================================================
# PROTOTYPE 5 : REGISTRE DES ÉQUIPEMENTS
# ==============================================================================
elif page == "5. Registre des Équipements":
    st.title("📦 Registre des Équipements et criticité")
    st.write("Inventaire technique pour éviter les coupures accidentelles lors de la pose des contacteurs.")
    
    data_assets = {
        "Départ Tableau": ["Courrier", "PGCC Droite", "RESPI Gauche", "Cafétéria", "Salle de réunion"],
        "Type de charge": ["Machines de mise sous pli / Ventilation", "Serveurs principaux", "Baie de brassage réseau", "Frigos / Machines à café", "Éclairage / Écrans"],
        "Criticité": ["Basse (Coupure possible)", "CRITIQUE (Ne jamais couper)", "CRITIQUE (Ne jamais couper)", "Moyenne (Prises uniquement)", "Basse"]
    }
    st.table(pd.DataFrame(data_assets))