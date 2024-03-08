from datetime import datetime

class PlaneData:

    def __init__(self, icao24, callsign=None, time_position=0, last_contact=0, longitude=0,
                 latitude=0, baro_altitude=0, on_ground=False, velocity=0, vertical_rate=0, category=0):
        self.icao24 = icao24
        self.callsign = callsign
        self.time_position = time_position
        self.last_contact = last_contact
        self.longitude = longitude
        self.latitude = latitude
        self.baro_altitude = baro_altitude
        self.on_ground = on_ground
        self.velocity = velocity
        self.vertical_rate = vertical_rate
        self.category = category
        self.location_history = []

    def update_position(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.location_history.append((latitude, longitude))

    def update_altitude(self, altitude):
        self.altitude = altitude

    def update_velocity(self, velocity):
        self.velocity = velocity

    def __str__(self):
        a = datetime.utcfromtimestamp(self.time_position).strftime("%Y-%m-%d %H:%M:%S UTC")
        return f"ICAO24: {self.icao24}, Callsign: {self.callsign}, Latitude: {self.latitude}, Longitude: {self.longitude}, Time_position: {a}"