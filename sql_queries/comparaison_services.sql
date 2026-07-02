/* Calcule le taux de talon nocturne de chaque service pour identifier immédiatement les zones qui restent allumées la nuit. */
SELECT 
    service,
    ROUND(MIN(consommation_kw), 2) as puissance_minimale_nuit_kw,
    ROUND(AVG(consommation_kw), 2) as puissance_moyenne_totale_kw,
    ROUND(MIN(consommation_kw) / AVG(consommation_kw) * 100, 1) as taux_talon_pourcentage
FROM consommations_courbes
GROUP BY service
ORDER BY taux_talon_pourcentage DESC;