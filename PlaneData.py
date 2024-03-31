from datetime import datetime
import numpy as np
import Simdemo
simVal = 0.1
class PlaneData:

    def __init__(self, icao24, callsign=None, time_position=0, longitude=0,
                 latitude=0, on_ground=False, velocity=0, true_track=0, category=0):
        self.icao24 = icao24
        self.callsign = callsign
        self.time_position = time_position
        self.longitude = longitude
        self.latitude = latitude
        self.on_ground = on_ground
        self.velocity = velocity
        self.true_track = true_track
        self.idx =0 # use as array index
        #alternative 1# self.location_history = [longitude,latitude]


        #self.location_history = np.empty((50,2),int) # use empty so that contents are unitilised. saves time
        self.location_history = np.zeros((50,2),float) # use empty so that contents are unitilised. saves time
        self.simulation_history = np.zeros((50,2),float)

        # cift idxs are latitudes tek idxs are longtitudes
        #self.location_history = (latitude,longitude)
        self.location_history[self.idx][0] = latitude
        self.location_history[self.idx][1] = longitude
        self.simulatedLatitude = Simdemo.SimulatorInVal(latitude,latitude,simVal)
        self.simulatedLongitude = Simdemo.SimulatorInVal(longitude,longitude,simVal)
        self.simulation_history[self.idx][0] = self.simulatedLatitude 
        self.simulation_history[self.idx][1] = self.simulatedLongitude 
        self.idx+=1
        self.category = category


    def update_data(self, longitude, latitude, on_ground, velocity, true_track):
        if self.latitude != latitude or self.longitude != longitude:
            self.latitude = latitude
            self.longitude = longitude
            self.simulatedLatitude = Simdemo.SimulatorInVal(latitude,self.simulation_history[self.idx-1][0],simVal)
            self.simulatedLongitude = Simdemo.SimulatorInVal(longitude,self.simulation_history[self.idx-1][1],simVal)
            # cift idxs are latitudes tek idxs are longtitudes
            # self.location_history = (latitude,longitude)
            self.location_history[self.idx][0] = latitude
            self.location_history[self.idx][1] = longitude
            self.simulation_history[self.idx][0] = self.simulatedLatitude
            self.simulation_history[self.idx][1] = self.simulatedLongitude
            self.idx += 1
        #alternative1    #self.location_history.append((latitude, longitude))
        #self.location_history = ((latitude, longitude))

        self.on_ground = on_ground
        self.velocity = velocity
        self.true_track = true_track


    def __str__(self):
        a = datetime.utcfromtimestamp(self.time_position).strftime("%Y-%m-%d %H:%M:%S UTC")
        return f"ICAO24: {self.icao24}, Callsign: {self.callsign}, Latitude: {self.latitude}, Longitude: {self.longitude}, Time_position: {a}"
