-- Tabella Data
CREATE TABLE dim_date (
    id_date SERIAL PRIMARY KEY,
    sale_date DATE,
    month INTEGER,
    year INTEGER
);

-- Tabella Indirizzo
CREATE TABLE dim_address (
    id_address SERIAL PRIMARY KEY,
    address TEXT,
    neighborhood TEXT,
    borough TEXT,
    median_income NUMERIC,
    poverty_rate NUMERIC,
    perc_white NUMERIC,
    perc_black NUMERIC,
    crime_index NUMERIC
);

-- Tabella Categoria Edificio
CREATE TABLE dim_build_category (
    id_build_category SERIAL PRIMARY KEY,
    macro_class_category TEXT,
    class_category TEXT
);

-- Tabella Categoria Dimensione Terreno
CREATE TABLE dim_land_square_category (
    id_land_square_category SERIAL PRIMARY KEY,
    land_square_category TEXT
);

-- Tabella Anno di Costruzione
CREATE TABLE dim_year_built (
    id_year_built SERIAL PRIMARY KEY,
    year_built INTEGER
);

-- Tabella Fatto Vendite
CREATE TABLE fact_sales (
    id_fact SERIAL PRIMARY KEY,
    id_build_category INTEGER REFERENCES dim_build_category(id_build_category),
    id_date INTEGER REFERENCES dim_date(id_date),
    id_address INTEGER REFERENCES dim_address(id_address),
    id_land_square_category INTEGER REFERENCES dim_land_square_category(id_land_square_category),
    id_year_built INTEGER REFERENCES dim_year_built(id_year_built)
    price NUMERIC,
    total_units INTEGER,
    land_square_feet NUMERIC,
);

--ALTER TABLE fact_sales
--DROP COLUMN commercial_units;
