import pandas as pd
from core.infrastructure.database import get_connection

def get_stations_by_postal_code(postal_code):
    conn = get_connection()
    query = '''
    SELECT station_id, operator, street, house_number, city, state, latitude, longitude
    FROM ChargingStations
    WHERE postal_code = ?
    '''
    df = pd.read_sql_query(query, conn, params=(postal_code,))
    conn.close()
    return df
