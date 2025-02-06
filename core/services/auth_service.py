import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.infrastructure.database import get_connection
from core.domain.auth import verify_password

def authenticate_user(name, password):
    """
    Authenticate user credentials from the database.
    Returns True if the username and password match.
    """
    conn = get_connection()
    query = "SELECT password_hash FROM Users WHERE name = ?"
    cursor = conn.cursor()
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hashed_password = result[0]
        return verify_password(password, stored_hashed_password)
    return False

