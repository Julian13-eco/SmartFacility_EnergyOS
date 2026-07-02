/* Analyse globale des périodes d'inoccupation (Nuits + Week-ends) */
WITH donnees_formatees AS (
    SELECT 
        service,
        consommation_kw,
        horodatage,
        -- Extraction de l'heure
        CAST(SUBSTR(horodatage, 12, 2) AS INTEGER) as heure,
        -- Reconstruction de la date au format YYYY-MM-DD pour SQLite
        SUBSTR(horodatage, 7, 4) || '-' || SUBSTR(horodatage, 4, 2) || '-' || SUBSTR(horodatage, 1, 2) as date_iso
    FROM consommations_courbes
),
donnees_avec_jours AS (
    SELECT 
        *,
        -- strftime('%w') renvoie '0' pour le dimanche, '6' pour le samedi
        strftime('%w', date_iso) as jour_semaine
    FROM donnees_formatees
)
SELECT 
    service,
    ROUND(MIN(consommation_kw), 2) as talon_inoccupation_kw,
    -- Calcul du potentiel d'économie basé sur 4 836 heures d'inoccupation par an (9h/nuit en semaine + 48h le week-end)
    ROUND(MAX(0, MIN(consommation_kw) - 0.2), 2) as kwh_economisables_par_heure,
    ROUND(MAX(0, MIN(consommation_kw) - 0.2) * 4836 * 0.20, 2) as economie_annuelle_inoccupation_euros
FROM donnees_avec_jours
WHERE 
    jour_semaine IN ('0', '6') -- Tout le week-end (Samedi = 6, Dimanche = 0)
    OR heure >= 21             -- Ou en semaine après 21h
    OR heure < 6               -- Ou en semaine avant 6h
GROUP BY service
ORDER BY economie_annuelle_inoccupation_euros DESC;