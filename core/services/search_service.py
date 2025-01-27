import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from core.domain.charging_stations import ChargingStation
import pandas as pd
from core.infrastructure.database import get_connection

def get_stations_by_postal_code(postal_code):
    conn = get_connection()
    query = '''
    SELECT station_id, operator, street, house_number, city, state, latitude, longitude
    FROM ChargingStations
    WHERE postal_code = ?
    ORDER BY station_id
    '''
    df = pd.read_sql_query(query, conn, params=(postal_code,))
    conn.close()
    print(df) # delete it after debugging
    # Convert rows to ChargingStation objects
    stations = [
        ChargingStation(
            station_id=row['station_id'],
            operator=row['operator'],
            street=row['street'],
            house_number=row['house_number'],
            city=row['city'],
            state=row['state'],
            latitude=row['latitude'],
            longitude=row['longitude']
        )
        for _, row in df.iterrows()
    ]

    return stations


''''
conn = get_connection()
query= n\''' SELECT * FROM ChargingStations where postal_code=13593 n\'''

df = pd.read_sql_query(query, conn)
print(df)
conn.close()

'''