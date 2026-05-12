import pandas as pd
import numpy as np

# Cargar datasets
conexiones = pd.read_csv("conexiones.csv", sep=";", encoding="latin1")
muestra = pd.read_csv("muestra.csv", sep=";", encoding="latin1")

cobertura = pd.read_excel("cobertura.xls")
reclamos = pd.read_excel("reclamos.xls")

# Guardar datasets en diccionario
datasets = {
    "conexiones": conexiones,
    "cobertura": cobertura,
    "reclamos": reclamos,
    "muestra": muestra
}

# PERFILADO
for nombre, df in datasets.items():

    print("\n")
    print("=" * 60)
    print("DATASET:", nombre.upper())
    print("=" * 60)

    # Filas y columnas
    print("\nCantidad de filas y columnas")
    print(df.shape)

    # Tipos de datos
    print("\nTipos de datos")
    print(df.dtypes)

    # Nulos
    print("\nValores nulos")
    nulos = df.isnull().sum()

    porcentaje_nulos = (
        df.isnull().mean() * 100
    ).round(2)

    tabla_nulos = pd.DataFrame({
        "Nulos": nulos,
        "% Nulos": porcentaje_nulos
    })

    print(tabla_nulos)

    # Duplicados
    print("\nDuplicados")
    print(df.duplicated().sum())

    # Estadísticas descriptivas
    print("\nEstadísticas descriptivas")
    print(df.describe(include="all"))

    # Outliers
    print("\nOutliers detectados")

    columnas_numericas = df.select_dtypes(
        include=np.number
    ).columns

    for columna in columnas_numericas:

        Q1 = df[columna].quantile(0.25)
        Q3 = df[columna].quantile(0.75)

        IQR = Q3 - Q1

        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        outliers = df[
            (df[columna] < limite_inferior)
            |
            (df[columna] > limite_superior)
        ]

        print(
            f"{columna}: {outliers.shape[0]} outliers"
        )