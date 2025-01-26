import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# tests/test_services.py
import pytest
from core.services.search_service import get_stations_by_postal_code
from core.services.feedback_service import get_feedback_for_station, insert_feedback
import sqlite3
import pandas as pd

@pytest.fixture
def setup_database():
    # Setup an in-memory SQLite database for testing
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Create test tables
    cursor.executescript('''
        CREATE TABLE ChargingStations (
            station_id INTEGER PRIMARY KEY,
            postal_code TEXT,
            operator TEXT,
            street TEXT,
            house_number TEXT,
            city TEXT,
            state TEXT,
            latitude REAL,
            longitude REAL
        );

        INSERT INTO ChargingStations VALUES
        (1, '10115', 'Operator A', 'Main St', '1', 'Berlin', 'Berlin', 52.52, 13.405);

        CREATE TABLE Feedback (
            feedback_id INTEGER PRIMARY KEY,
            station_id INTEGER,
            user_id INTEGER,
            rating INTEGER,
            comments TEXT,
            timestamp TEXT
        );

        INSERT INTO Feedback VALUES
        (1, 1, 1, 5, 'Great station!', '2023-01-01 10:00:00');
    ''')
    conn.commit()
    yield conn
    conn.close()

def test_get_stations_by_postal_code(setup_database):
    conn = setup_database
    query = '''
        SELECT station_id, operator, street, house_number, city, state, latitude, longitude
        FROM ChargingStations
        WHERE postal_code = ?
    '''
    postal_code = "10115"
    df = pd.read_sql_query(query, conn, params=(postal_code,))
    assert not df.empty
    assert len(df) == 1
    assert df['operator'].iloc[0] == 'Operator A'

def test_get_feedback_for_station(setup_database):
    conn = setup_database
    station_id = 1
    query = '''
        SELECT user_id, rating, comments, timestamp
        FROM Feedback
        WHERE station_id = ?
    '''
    df = pd.read_sql_query(query, conn, params=(station_id,))
    assert not df.empty
    assert len(df) == 1
    assert df['rating'].iloc[0] == 5
    assert df['comments'].iloc[0] == 'Great station!'

def test_insert_feedback(setup_database):
    conn = setup_database
    cursor = conn.cursor()
    query = '''
        INSERT INTO Feedback (station_id, user_id, rating, comments, timestamp)
        VALUES (?, ?, ?, ?, datetime('now'))
    '''
    cursor.execute(query, (1, 2, 4, 'Good experience!',))
    conn.commit()

    # Check that the new feedback was inserted
    df = pd.read_sql_query('SELECT * FROM Feedback WHERE user_id = 2', conn)
    assert not df.empty
    assert df['comments'].iloc[0] == 'Good experience!'
