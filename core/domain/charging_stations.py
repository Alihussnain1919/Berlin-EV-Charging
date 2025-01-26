class ChargingStation:
    def __init__(self, station_id, operator, street, house_number, city, state, latitude, longitude):
        self.station_id = station_id
        self.operator = operator
        self.street = street
        self.house_number = house_number
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude

    def get_full_address(self):
        return f"{self.street} {self.house_number}, {self.city}, {self.state}"
