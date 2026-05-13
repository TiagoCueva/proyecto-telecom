USE Proyecto_Telecom;
GO

-- =========================
-- DIMENSION FECHA
-- =========================

CREATE TABLE dim_fecha (
    id_fecha INT PRIMARY KEY,
    periodo DATE,
    anio INT,
    mes INT
);

-- =========================
-- DIMENSION EMPRESA
-- =========================

CREATE TABLE dim_empresa (
    id_empresa INT PRIMARY KEY,
    empresa VARCHAR(200)
);

-- =========================
-- DIMENSION UBICACION
-- =========================

CREATE TABLE dim_ubicacion (
    id_ubicacion INT PRIMARY KEY,
    ubigeo_distrito BIGINT,
    departamento VARCHAR(100),
    provincia VARCHAR(100),
    distrito VARCHAR(100)
);

-- =========================
-- DIMENSION TECNOLOGIA
-- =========================

CREATE TABLE dim_tecnologia (
    id_tecnologia INT PRIMARY KEY,
    tecnologia VARCHAR(100),
    rango_velocidad VARCHAR(100)
);

-- =========================
-- TABLA HECHOS
-- =========================

CREATE TABLE fact_conexiones (
    id_hecho INT IDENTITY(1,1) PRIMARY KEY,
    id_fecha INT,
    id_empresa INT,
    id_ubicacion INT,
    id_tecnologia INT,
    cant_conexiones INT,

    FOREIGN KEY (id_fecha)
    REFERENCES dim_fecha(id_fecha),

    FOREIGN KEY (id_empresa)
    REFERENCES dim_empresa(id_empresa),

    FOREIGN KEY (id_ubicacion)
    REFERENCES dim_ubicacion(id_ubicacion),

    FOREIGN KEY (id_tecnologia)
    REFERENCES dim_tecnologia(id_tecnologia)
);