SELECT 
    e.empresa,
    SUM(f.CANT_CONEXIONES) AS total_conexiones
FROM fact_conexiones_import f
JOIN dim_empresa_import e
    ON f.id_empresa = e.id_empresa
GROUP BY e.empresa
ORDER BY total_conexiones DESC;