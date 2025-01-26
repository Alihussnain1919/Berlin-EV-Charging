import pandas as pd
# Load the residents dataset
residents_df = pd.read_csv("datasets/plz_einwohner.csv")

# Load the charging stations dataset
stations_df = pd.read_csv("datasets/Ladesaeulenregister.csv")

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('charging_stations.db')
cursor = conn.cursor()

# Create Residents table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Residents (
    postal_code INTEGER PRIMARY KEY,
    note TEXT,
    population INTEGER,
    area_km2 REAL,
    latitude FLOAT,
    longitude FLOAT
)
''')

# Create ChargingStations table //
cursor.execute('''
CREATE TABLE IF NOT EXISTS ChargingStations (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator TEXT,
    street TEXT,
    house_number TEXT,
    postal_code INTEGER,
    city TEXT,
    state TEXT,
    district TEXT,
    latitude FLOAT,
    longitude FLOAT,
    installation_date TEXT,
    nominal_power REAL,
    charging_type TEXT,
    number_of_points INTEGER
)
''')

# Create ChargingPoints table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ChargingPoints (
    point_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER,
    plug_type TEXT,
    power_kw REAL,
    public_key TEXT,
    FOREIGN KEY (station_id) REFERENCES ChargingStations(station_id)
)
''')

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password_hash TEXT
)
''')

# Create Feedback table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER,
    user_id INTEGER,
    rating INTEGER,
    comments TEXT,
    timestamp TEXT,
    FOREIGN KEY (station_id) REFERENCES ChargingStations(station_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
''')

conn.commit()

# Insert residents data
residents_df.to_sql('Residents', conn, if_exists='replace', index=False)

stations_df = stations_df.rename(columns={
    "Betreiber": "operator",
    "Straße": "street",
    "Hausnummer": "house_number",
    "Postleitzahl": "postal_code",
    "Ort": "city",
    "Bundesland": "state",
    "Kreis/kreisfreie Stadt": "district",
    "Breitengrad": "latitude",
    "Längengrad": "longitude",
    "Inbetriebnahmedatum": "installation_date",
    "Nennleistung Ladeeinrichtung [kW]": "nominal_power",
    "Art der Ladeeinrichung": "charging_type",
    "Anzahl Ladepunkte": "number_of_points"
})
stations_df.to_sql('ChargingStations', conn, if_exists='replace', index=False)

charging_points = []
for index, row in stations_df.iterrows():
    station_id = index + 1
    for i in range(1, 5):  # Assuming up to 4 plug types
        plug_type = row.get(f'Steckertypen{i}', None)
        power_kw = row.get(f'P{i} [kW]', None)
        public_key = row.get(f'Public Key{i}', None)
        
        if pd.notna(plug_type):  # Only add if plug type exists
            charging_points.append((station_id, plug_type, power_kw, public_key))

cursor.executemany('''
INSERT INTO ChargingPoints (station_id, plug_type, power_kw, public_key)
VALUES (?, ?, ?, ?)
''', charging_points)

conn.commit()

# Step 1: Create a new table with the corrected schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS ChargingStations_New (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator TEXT,
    street TEXT,
    house_number TEXT,
    postal_code INTEGER,
    city TEXT,
    state TEXT,
    district TEXT,
    latitude FLOAT,
    longitude FLOAT,
    installation_date TEXT,
    nominal_power REAL,
    charging_type TEXT,
    number_of_points INTEGER
);
''')

# Step 2: Copy data from the old table to the new table
cursor.execute('''
INSERT INTO ChargingStations_New (
    operator, street, house_number, postal_code, city, state, district,
    latitude, longitude, installation_date, nominal_power, charging_type,
    number_of_points
)
SELECT 
    operator, street, house_number, postal_code, city, state, district,
    latitude, longitude, installation_date, nominal_power, charging_type,
    number_of_points
FROM ChargingStations;
''')

# Step 3: Drop the old table
cursor.execute('DROP TABLE ChargingStations;')

# Step 4: Rename the new table to replace the old one
cursor.execute('ALTER TABLE ChargingStations_New RENAME TO ChargingStations;')

# Commit changes
conn.commit()
