import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# tests/test_infrastructure.py
import pytest
from core.infrastructure.database import get_connection

def test_get_db_connection():
    conn = get_connection()
    assert conn is not None

    # Test if connection allows queries
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    result = cursor.fetchone()
    assert result[0] == 1
    conn.close()
