import pandas as pd

# =========================
# CARGAR DATASET
# =========================

df = pd.read_csv("data_processed/conexiones_limpio.csv")

print("Dataset cargado")

# =========================
# KPI 1
# TOTAL CONEXIONES
# =========================

total_conexiones = df["CANT_CONEXIONES"].sum()

print("\nKPI 1 - Total conexiones")
print(total_conexiones)

# =========================
# KPI 2
# CONEXIONES POR EMPRESA
# =========================

kpi_empresa = (
    df.groupby("EMPRESA")["CANT_CONEXIONES"]
    .sum()
    .sort_values(ascending=False)
)

print("\nKPI 2 - Conexiones por empresa")
print(kpi_empresa.head())

# =========================
# KPI 3
# CONEXIONES POR DEPARTAMENTO
# =========================

kpi_departamento = (
    df.groupby("DEPARTAMENTO")["CANT_CONEXIONES"]
    .sum()
    .sort_values(ascending=False)
)

print("\nKPI 3 - Conexiones por departamento")
print(kpi_departamento.head())

# =========================
# KPI 4
# CONEXIONES POR TECNOLOGIA
# =========================

kpi_tecnologia = (
    df.groupby("TECNOLOGÍA")["CANT_CONEXIONES"]
    .sum()
    .sort_values(ascending=False)
)

print("\nKPI 4 - Conexiones por tecnología")
print(kpi_tecnologia)

# =========================
# KPI 5
# ANALISIS TEMPORAL
# =========================

df["PERIODO"] = pd.to_datetime(df["PERIODO"])

kpi_mensual = (
    df.groupby("PERIODO")["CANT_CONEXIONES"]
    .sum()
    .reset_index()
)

kpi_mensual["MoM_%"] = (
    kpi_mensual["CANT_CONEXIONES"]
    .pct_change() * 100
)

print("\nKPI 5 - Variación mensual")
print(kpi_mensual)

# =========================
# KPI 6
# PARTICIPACION MERCADO
# =========================

participacion = (
    df.groupby("EMPRESA")["CANT_CONEXIONES"]
    .sum()
    .reset_index()
)

participacion["Participacion_%"] = (
    participacion["CANT_CONEXIONES"]
    / participacion["CANT_CONEXIONES"].sum()
) * 100

participacion = participacion.sort_values(
    by="Participacion_%",
    ascending=False
)

print("\nKPI 6 - Participación de mercado")
print(participacion.head())

print("\nProceso KPI completado")