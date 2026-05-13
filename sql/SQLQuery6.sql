SELECT 
    d.anio,
    d.mes,
    SUM(f.CANT_CONEXIONES) AS total_conexiones
FROM fact_conexiones_import f
JOIN dim_fecha_import d
    ON f.id_fecha = d.id_fecha
GROUP BY d.anio, d.mes
ORDER BY d.anio, d.mes;