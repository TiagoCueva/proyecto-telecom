SELECT 
    t.[TECNOLOGÍA],
    SUM(f.CANT_CONEXIONES) AS total_conexiones
FROM fact_conexiones_import f
JOIN dim_tecnologia_import t
    ON f.id_tecnologia = t.id_tecnologia
GROUP BY t.[TECNOLOGÍA]
ORDER BY total_conexiones DESC;