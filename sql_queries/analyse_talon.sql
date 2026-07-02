/* Analyse du talon de consommation sur la période d'inoccupation (21h - 06h) */
SELECT 
    service,
    ROUND(MIN(consommation_kw), 2) as puissance_minimale_nuit_kw,
    ROUND(AVG(consommation_kw), 2) as puissance_moyenne_nuit_kw
FROM consommations_courbes
WHERE 
    CAST(SUBSTR(horodatage, 12, 2) AS INTEGER) >= 21  -- Après 21h
    OR 
    CAST(SUBSTR(horodatage, 12, 2) AS INTEGER) < 6   -- Avant 6h
GROUP BY service
ORDER BY puissance_moyenne_nuit_kw ASC;