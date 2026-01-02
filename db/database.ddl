CREATE TABLE IF NOT EXISTS batch (
    id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batch(id),
    timestamp TIMESTAMP,
    temperature DOUBLE PRECISION,
    relative_humidity INT,
    apparent_temperature DOUBLE PRECISION,
    is_day BOOLEAN,
    surface_pressure DOUBLE PRECISION,
    pressure_msl DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    rain DOUBLE PRECISION,
    snowfall DOUBLE PRECISION,
    showers DOUBLE PRECISION,
    cloud_cover INT,
    wind_speed DOUBLE PRECISION,
    wind_direction DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS bike_stations (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(256),
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    slots INT
);

CREATE TABLE IF NOT EXISTS bike_stations_status (
    id SERIAL PRIMARY KEY,
    batch_id INT REFERENCES batch(id),
    timestamp TIMESTAMP,
    station_id VARCHAR(32) REFERENCES bike_stations(id),
    free_bikes INT,
    empty_slots INT
);
