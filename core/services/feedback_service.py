import pandas as pd
from core.infrastructure.database import get_connection


def get_feedback_for_station(station_id):
    conn = get_connection()
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

def insert_feedback(station_id, user_id, rating, comments):
    conn = get_connection()
    query = '''
    INSERT INTO Feedback (station_id, user_id, rating, comments, timestamp)
    VALUES (?, ?, ?, ?, datetime('now'))
    '''
    cursor = conn.cursor()
    cursor.execute(query, (station_id, user_id, rating, comments))
    conn.commit()
    conn.close()
