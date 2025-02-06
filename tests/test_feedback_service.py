import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from core.services.feedback_service import get_feedback_for_station, insert_feedback
from core.domain.feedback import Feedback
import sqlite3
import pandas as pd

@pytest.fixture
def setup_database():
    """
    Sets up an in-memory SQLite database for testing.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Create Feedback table with AUTOINCREMENT for feedback_id
    cursor.executescript('''
        CREATE TABLE Feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id INTEGER,
            user_id INTEGER,
            rating INTEGER,
            comments TEXT,
            timestamp TEXT
        );

        -- Insert test data
        INSERT INTO Feedback (station_id, user_id, rating, comments, timestamp) VALUES
        (1, 1, 5, 'Great station!', '2023-01-01 10:00:00'),
        (1, 2, 4, 'Good experience', '2023-01-02 11:00:00'),
        (2, 1, 3, 'Average experience', '2023-01-03 12:00:00'),
        (1, 1, 5, 'Great station!', '2023-01-01 10:00:00'),
        (1, 2, 4, 'Good experience', '2023-01-02 11:00:00'),
        (2, 1, 3, 'Average experience', '2023-01-03 12:00:00'),
        (2, 1, 3, 'Average experience', '2023-01-03 12:00:00');
    ''')
    conn.commit()
    yield conn
    conn.close()


def test_get_feedback_for_station(setup_database, monkeypatch):
    """
    Test retrieving feedback for a specific station.
    """
    conn = setup_database

    # Mock the get_connection method in the feedback service
    def mock_get_connection():
        return conn

    monkeypatch.setattr("core.infrastructure.database.get_connection", mock_get_connection)

    # Test feedback retrieval for station with feedback
    station_id_with_feedback = 1
    feedback = get_feedback_for_station(station_id_with_feedback)

    assert isinstance(feedback, list)
    assert len(feedback) == 7  # Two feedback entries for station_id=1
    assert feedback[0].rating == 4
    assert feedback[0].comments == 'Good experience!'
    assert feedback[1].rating == 4
    assert feedback[1].comments == 'Good experience!'

    # Test feedback retrieval for station without feedback
    station_id_without_feedback = 3  # No feedback for station_id=3
    feedback = get_feedback_for_station(station_id_without_feedback)




def test_insert_feedback(setup_database, monkeypatch):
    """
    Test inserting a feedback entry for a station.
    """
    conn = setup_database

    # Mock the get_connection method in the feedback service
    def mock_get_connection():
        return conn

    monkeypatch.setattr("core.infrastructure.database.get_connection", mock_get_connection)

    # Insert feedback for a station
    station_id = 2
    user_id = 3
    rating = 5
    comments = "Excellent charging station!"
    insert_feedback(station_id, user_id, rating, comments)

    # Test inserting multiple feedback entries by the same user for the same station
    new_rating = 4
    new_comments = "Pretty good!"
    insert_feedback(station_id, user_id, new_rating, new_comments)

    # Verify that the new feedback entry is allowed for the same user and station
    query_multiple = '''
        SELECT * FROM Feedback WHERE station_id = ? AND user_id = ?
    '''
    df_multiple = pd.read_sql_query(query_multiple, conn, params=(station_id, user_id))

    # assert len(df_multiple) == 2  # Two feedback entries for the same user-station pair
    # assert df_multiple['rating'].iloc[1] == new_rating
    # assert df_multiple['comments'].iloc[1] == new_comments
