from datetime import datetime

class PlaneData:

    def __init__(self, icao24, callsign=None, time_position=0, longitude=0,
                 latitude=0, on_ground=False, velocity=0, true_track=0):
        self.icao24 = icao24
        self.callsign = callsign
        self.time_position = time_position
        self.longitude = longitude
        self.latitude = latitude
        self.on_ground = on_ground
        self.velocity = velocity
        self.true_track = true_track
        self.location_history = []


    def update_data(self, longitude, latitude, on_ground, velocity, true_track):
        if self.latitude != latitude and self.longitude != longitude:
            self.latitude = latitude
            self.longitude = longitude
            self.location_history.append((latitude, longitude))

        self.on_ground = on_ground
        self.velocity = velocity
        self.true_track = true_track


    def __str__(self):
        a = datetime.utcfromtimestamp(self.time_position).strftime("%Y-%m-%d %H:%M:%S UTC")
        return f"ICAO24: {self.icao24}, Callsign: {self.callsign}, Latitude: {self.latitude}, Longitude: {self.longitude}, Time_position: {a}"
