/* Analyse des pics de puissance maximaux par service */
SELECT 
    service,
    ROUND(MAX(consommation_kw), 2) as puissance_pointe_max_kw,
    ROUND(AVG(consommation_kw), 2) as puissance_moyenne_kw,
    ROUND(MAX(consommation_kw) / AVG(consommation_kw), 1) as ratio_pic_moyenne,
    horodatage as date_et_heure_du_pic
FROM consommations_courbes
GROUP BY service
ORDER BY puissance_pointe_max_kw DESC;