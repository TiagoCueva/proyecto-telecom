import pandas as pd
import numpy as np

# =========================
# CARGAR DATASETS
# =========================

conexiones = pd.read_csv(
    "conexiones.csv",
    sep=";",
    encoding="latin1"
)

muestra = pd.read_csv(
    "muestra.csv",
    sep=";",
    encoding="latin1"
)

cobertura = pd.read_excel(
    "cobertura.xls"
)

reclamos = pd.read_excel(
    "reclamos.xls"
)

print("Datasets cargados correctamente")


# =========================
# LIMPIEZA RECLAMOS
# =========================

print("\nLimpieza de reclamos")

print("Antes:", reclamos.shape)

# eliminar columna vacía
reclamos = reclamos.drop(
    columns=["Unnamed: 0"]
)

# renombrar columnas
reclamos.columns = [
    "empresa",
    "fecha",
    "departamento",
    "provincia",
    "tipo_servicio",
    "tipo_reclamo",
    "cantidad"
]

# eliminar duplicados
reclamos = reclamos.drop_duplicates()

print("Después:", reclamos.shape)


# =========================
# LIMPIEZA MUESTRA
# =========================

print("\nLimpieza de muestra")

# corregir encoding
muestra.columns = (
    muestra.columns
    .str.encode("latin1")
    .str.decode("utf-8")
)

# eliminar espacios
muestra.columns = (
    muestra.columns
    .str.strip()
)

print("Encoding corregido")


# =========================
# LIMPIEZA CONEXIONES
# =========================

print("\nLimpieza de conexiones")

# convertir periodo a fecha
conexiones["PERIODO"] = pd.to_datetime(
    conexiones["PERIODO"].astype(str),
    format="%Y%m"
)

# normalizar texto
columnas_texto = [
    "EMPRESA",
    "DEPARTAMENTO",
    "PROVINCIA",
    "DISTRITO",
    "TECNOLOGÍA"
]

for col in columnas_texto:

    conexiones[col] = (
        conexiones[col]
        .str.upper()
        .str.strip()
    )

print("Texto normalizado")


# =========================
# OUTLIERS
# =========================

print("\nTratamiento de outliers")

Q1 = conexiones["CANT_CONEXIONES"].quantile(0.25)

Q3 = conexiones["CANT_CONEXIONES"].quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR

limite_superior = Q3 + 1.5 * IQR

conexiones_limpio = conexiones[
    (
        conexiones["CANT_CONEXIONES"]
        >= limite_inferior
    )
    &
    (
        conexiones["CANT_CONEXIONES"]
        <= limite_superior
    )
]

print("Antes:", conexiones.shape)

print("Después:", conexiones_limpio.shape)


# =========================
# EXPORTAR
# =========================

conexiones_limpio.to_csv(
    "data_processed/conexiones_limpio.csv",
    index=False
)

cobertura.to_csv(
    "data_processed/cobertura_limpio.csv",
    index=False
)

reclamos.to_csv(
    "data_processed/reclamos_limpio.csv",
    index=False
)

muestra.to_csv(
    "data_processed/muestra_limpio.csv",
    index=False
)

print("\nArchivos exportados correctamente")