/* Estimation des économies annuelles par service (Cible talon = 0.2 kW) */
SELECT 
    service,
    MIN(consommation_kw) as talon_actuel_kw,
    ROUND(MAX(0, MIN(consommation_kw) - 0.2), 2) as kwh_economisables_par_heure,
    ROUND(MAX(0, MIN(consommation_kw) - 0.2) * 9 * 365 * 0.20, 2) as economie_annuelle_estimee_euros
FROM consommations_courbes
GROUP BY service
ORDER BY economie_annuelle_estimee_euros DESC;