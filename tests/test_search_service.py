import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


import pytest
from core.services.search_service import get_stations_by_postal_code
from core.domain.charging_stations import ChargingStation
import sqlite3
import pandas as pd
@pytest.fixture
def test_get_stations_by_postal_code(setup_database, monkeypatch):
    conn = setup_database

    # Mock the get_connection method in the search service
    def mock_get_connection():
        return conn

    monkeypatch.setattr("core.infrastructure.database.get_connection", mock_get_connection)

    # Test the function
    postal_code = "10115"
    stations = get_stations_by_postal_code(postal_code)

    # Check that the correct number of stations is returned
    assert len(stations) == 3

    # Validate each station
    expected_stations = [
        {"operator": "Operator A", "street": "Main St", "latitude": 52.52, "longitude": 13.405},
        {"operator": "Operator B", "street": "Second St", "latitude": 52.53, "longitude": 13.406},
        {"operator": "Operator C", "street": "Third St", "latitude": 52.54, "longitude": 13.407},
    ]

    for i, expected in enumerate(expected_stations):
        assert stations[i].operator == expected["operator"]
        assert stations[i].street == expected["street"]
        assert stations[i].latitude == expected["latitude"]
        assert stations[i].longitude == expected["longitude"]
