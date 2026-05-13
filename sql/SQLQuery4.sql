SELECT 
    u.departamento,
    SUM(f.CANT_CONEXIONES) AS total_conexiones
FROM fact_conexiones_import f
JOIN dim_ubicacion_import u
    ON f.id_ubicacion = u.id_ubicacion
GROUP BY u.departamento
ORDER BY total_conexiones DESC;