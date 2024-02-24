
from opensky_api import OpenSkyApi
from datetime import datetime
api = OpenSkyApi()

states = api.get_states(0)
flag = False

"""
#Airport'a göre flight data veriyor
arrivals = api.get_arrivals_by_airport("EDDF", 1517227200, 1517230800)
departures = api.get_departures_by_airport("EDDF", 1517227200, 1517230800)
print("Arrivals:")
for flight in arrivals:
    print(flight)
print("Departures:")
for flight in departures:
    print(flight)


"""

for s in states.states:
    if s.time_position :
        date = datetime.utcfromtimestamp(s.time_position)
        #print("%r %r %r %r %r %r" % (date.day, date.month, date.year, date.hour, date.minute, date.second))
        #print("(%r, %r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude, s.velocity, s.icao24))

        if s.icao24 and flag==False:
            ft = api.get_track_by_aircraft(s.icao24,0) #flight track
            if ft is not None and ft.path is not None:
                flag = True;
                print(len(ft.path)) #waypoint listesi



















