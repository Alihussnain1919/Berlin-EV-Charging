import sqlite3

DATABASE_PATH = "charging_stations.db"

def get_connection():
    return sqlite3.connect(DATABASE_PATH)
