import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pandas as pd
from core.infrastructure.database import get_connection
from core.domain.feedback import Feedback  # Import the domain class


def get_feedback_for_station(station_id):
    """
    Retrieves feedback for a given station ID and returns a list of Feedback objects.
    """
    conn = get_connection()
    query = '''
     SELECT 
        f.user_id,
        f.station_id,
        f.rating,
        f.comments,
        f.timestamp
    FROM Feedback f
    WHERE f.station_id = ?;
    '''
    df = pd.read_sql_query(query, conn, params=(station_id,))
    conn.close()

    # Convert the DataFrame rows into a list of Feedback objects
    feedback_list = [
        Feedback(
            user_id=row["user_id"],
            station_id=row["station_id"],
            rating=row["rating"],
            comments=row["comments"],
            timestamp=row["timestamp"],
        )
        for _, row in df.iterrows()
    ]
    return feedback_list


def insert_feedback(station_id, user_id, rating, comments):
    """
    Inserts a new feedback record into the database.
    """
    conn = get_connection()
    query = '''
    INSERT INTO Feedback (station_id, user_id, rating, comments, timestamp)
    VALUES (?, ?, ?, ?, datetime('now'))
    '''
    cursor = conn.cursor()
    cursor.execute(query, (station_id, user_id, rating, comments))
    conn.commit()
    conn.close()

conn = get_connection()
query = '''select* from Users'''

df= pd.read_sql_query(query, conn)
print(df)
conn.close()