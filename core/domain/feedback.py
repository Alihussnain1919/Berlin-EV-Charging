class Feedback:
    def __init__(self, user_id, station_id, rating, comments, timestamp=None):
        self.user_id = user_id
        self.station_id = station_id
        self.rating = rating
        self.comments = comments
        self.timestamp = timestamp
