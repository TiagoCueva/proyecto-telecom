import pandas as pd
from scipy.stats import ttest_ind

# =========================
# CARGAR DATASET
# =========================

df = pd.read_csv("data_processed/conexiones_limpio.csv")

print("Dataset cargado")

# =========================
# GRUPOS
# =========================

fibra = df[
    df["TECNOLOGÍA"] == "FIBRA ÓPTICA"
]["CANT_CONEXIONES"]

otras = df[
    df["TECNOLOGÍA"] != "FIBRA ÓPTICA"
]["CANT_CONEXIONES"]

# =========================
# HIPOTESIS
# =========================

print("\nH0: No existe diferencia significativa")
print("H1: Sí existe diferencia significativa")

# =========================
# PRUEBA T
# =========================

estadistico, p_value = ttest_ind(
    fibra,
    otras,
    equal_var=False
)

print("\nRESULTADOS")

print(f"Estadístico t: {estadistico}")
print(f"p-value: {p_value}")

# =========================
# DECISION
# =========================

alpha = 0.05

if p_value < alpha:
    print("\nSe rechaza H0")
    print("Existe diferencia significativa")
else:
    print("\nNo se rechaza H0")
    print("No existe diferencia significativa")

print("\nValidación estadística completada")