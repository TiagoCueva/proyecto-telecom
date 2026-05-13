import pandas as pd
import sqlite3

# =========================
# CARGAR DATASET LIMPIO
# =========================

conexiones = pd.read_csv("data_processed/conexiones_limpio.csv")

# Convertir PERIODO a fecha desde el inicio
conexiones["PERIODO"] = pd.to_datetime(conexiones["PERIODO"])

print("Dataset cargado correctamente")


# =========================
# DIMENSION FECHA
# =========================

dim_fecha = conexiones[["PERIODO"]].drop_duplicates().reset_index(drop=True)
dim_fecha["id_fecha"] = dim_fecha.index + 1
dim_fecha["anio"] = dim_fecha["PERIODO"].dt.year
dim_fecha["mes"] = dim_fecha["PERIODO"].dt.month

print("Dimensión fecha creada")


# =========================
# DIMENSION EMPRESA
# =========================

dim_empresa = conexiones[["EMPRESA"]].drop_duplicates().reset_index(drop=True)
dim_empresa["id_empresa"] = dim_empresa.index + 1

print("Dimensión empresa creada")


# =========================
# DIMENSION UBICACION
# =========================

dim_ubicacion = conexiones[
    ["UBIGEO_DISTRITO", "DEPARTAMENTO", "PROVINCIA", "DISTRITO"]
].drop_duplicates().reset_index(drop=True)

dim_ubicacion["id_ubicacion"] = dim_ubicacion.index + 1

print("Dimensión ubicación creada")


# =========================
# DIMENSION TECNOLOGIA
# =========================

dim_tecnologia = conexiones[
    ["TECNOLOGÍA", "RANGO_VELOC_BAJADA"]
].drop_duplicates().reset_index(drop=True)

dim_tecnologia["id_tecnologia"] = dim_tecnologia.index + 1

print("Dimensión tecnología creada")


# =========================
# TABLA DE HECHOS
# =========================

fact_conexiones = conexiones.merge(
    dim_fecha,
    on="PERIODO",
    how="left"
)

fact_conexiones = fact_conexiones.merge(
    dim_empresa,
    on="EMPRESA",
    how="left"
)

fact_conexiones = fact_conexiones.merge(
    dim_ubicacion,
    on=["UBIGEO_DISTRITO", "DEPARTAMENTO", "PROVINCIA", "DISTRITO"],
    how="left"
)

fact_conexiones = fact_conexiones.merge(
    dim_tecnologia,
    on=["TECNOLOGÍA", "RANGO_VELOC_BAJADA"],
    how="left"
)

fact_conexiones = fact_conexiones[
    [
        "id_fecha",
        "id_empresa",
        "id_ubicacion",
        "id_tecnologia",
        "CANT_CONEXIONES"
    ]
]

print("Tabla de hechos creada")


# =========================
# ORDENAR COLUMNAS
# =========================

dim_fecha = dim_fecha[
    ["id_fecha", "PERIODO", "anio", "mes"]
]

dim_empresa = dim_empresa[
    ["id_empresa", "EMPRESA"]
]

dim_ubicacion = dim_ubicacion[
    ["id_ubicacion", "UBIGEO_DISTRITO", "DEPARTAMENTO", "PROVINCIA", "DISTRITO"]
]

dim_tecnologia = dim_tecnologia[
    ["id_tecnologia", "TECNOLOGÍA", "RANGO_VELOC_BAJADA"]
]


# =========================
# EXPORTAR CSV
# =========================

dim_fecha.to_csv("data_processed/dim_fecha.csv", index=False)
dim_empresa.to_csv("data_processed/dim_empresa.csv", index=False)
dim_ubicacion.to_csv("data_processed/dim_ubicacion.csv", index=False)
dim_tecnologia.to_csv("data_processed/dim_tecnologia.csv", index=False)
fact_conexiones.to_csv("data_processed/fact_conexiones.csv", index=False)

print("Archivos CSV exportados correctamente")


# =========================
# CREAR BASE SQLITE
# =========================

conn = sqlite3.connect("data_processed/modelo_estrella.db")

dim_fecha.to_sql("dim_fecha", conn, if_exists="replace", index=False)
dim_empresa.to_sql("dim_empresa", conn, if_exists="replace", index=False)
dim_ubicacion.to_sql("dim_ubicacion", conn, if_exists="replace", index=False)
dim_tecnologia.to_sql("dim_tecnologia", conn, if_exists="replace", index=False)
fact_conexiones.to_sql("fact_conexiones", conn, if_exists="replace", index=False)

print("Base modelo_estrella.db creada correctamente")


# =========================
# CONSULTAS SQL
# =========================

consulta1 = """
SELECT
    e.EMPRESA,
    SUM(f.CANT_CONEXIONES) AS total_conexiones
FROM fact_conexiones f
JOIN dim_empresa e
ON f.id_empresa = e.id_empresa
GROUP BY e.EMPRESA
ORDER BY total_conexiones DESC;
"""

consulta2 = """
SELECT
    u.DEPARTAMENTO,
    SUM(f.CANT_CONEXIONES) AS total_conexiones
FROM fact_conexiones f
JOIN dim_ubicacion u
ON f.id_ubicacion = u.id_ubicacion
GROUP BY u.DEPARTAMENTO
ORDER BY total_conexiones DESC;
"""

consulta3 = """
SELECT
    t."TECNOLOGÍA",
    SUM(f.CANT_CONEXIONES) AS total_conexiones
FROM fact_conexiones f
JOIN dim_tecnologia t
ON f.id_tecnologia = t.id_tecnologia
GROUP BY t."TECNOLOGÍA"
ORDER BY total_conexiones DESC;
"""

consulta4 = """
SELECT
    d.anio,
    d.mes,
    SUM(f.CANT_CONEXIONES) AS total_conexiones
FROM fact_conexiones f
JOIN dim_fecha d
ON f.id_fecha = d.id_fecha
GROUP BY d.anio, d.mes
ORDER BY d.anio, d.mes;
"""

print("\nConsulta 1: conexiones por empresa")
print(pd.read_sql_query(consulta1, conn).head())

print("\nConsulta 2: conexiones por departamento")
print(pd.read_sql_query(consulta2, conn).head())

print("\nConsulta 3: conexiones por tecnología")
print(pd.read_sql_query(consulta3, conn).head())

print("\nConsulta 4: conexiones por fecha")
print(pd.read_sql_query(consulta4, conn).head())

conn.close()

print("\nProceso de modelado dimensional completado correctamente")