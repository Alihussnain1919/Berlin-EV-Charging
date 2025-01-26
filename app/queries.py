# Reusable functions or classes for database queries
import sqlite3
import pandas as pd

# Function to fetch charging stations by postal code
def get_stations_by_postal_code(postal_code):
    conn = sqlite3.connect('charging_stations.db')
    query = '''
    SELECT station_id, operator, street, house_number, city, state, latitude, longitude
    FROM ChargingStations
    WHERE postal_code = ?
    '''
    df = pd.read_sql_query(query, conn, params=(postal_code,))
    conn.close()
    return df

# Function to fetch feedback for a charging station
def get_feedback_for_station(station_id):
    conn = sqlite3.connect('charging_stations.db')
    query = '''
     SELECT 
        f.user_id,
        cs.operator AS station_name,
        f.rating,
        f.comments,
        f.timestamp
    FROM Feedback f
    JOIN ChargingStations cs 
        ON f.station_id = cs.station_id
    WHERE f.station_id = ?;
    '''
    df = pd.read_sql_query(query, conn, params=(station_id,))
    conn.close()
    return df

# Function to insert feedback
def insert_feedback(station_id, user_id, rating, comments):
    conn = sqlite3.connect('charging_stations.db')
    query = '''
    INSERT INTO Feedback (station_id, user_id, rating, comments, timestamp)
    VALUES (?, ?, ?, ?, datetime('now'))
    '''
    cursor = conn.cursor()
    cursor.execute(query, (station_id, user_id, rating, comments))
    conn.commit()
    conn.close()

