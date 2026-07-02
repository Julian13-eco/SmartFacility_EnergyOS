/* Analyse du profil horaire du service Numérisation */
SELECT 
    SUBSTR(horodatage, 12, 2) as heure,
    ROUND(AVG(consommation_kw), 2) as conso_moyenne_kw
FROM consommations_courbes
WHERE service = 'Numérisation'
GROUP BY heure
ORDER BY heure ASC;