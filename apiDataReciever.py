#IMPORTING LIBRARY
import requests
import json
import pandas as pd

#AREA EXTENT COORDINATE WGS4
lon_min,lat_min=-125.974,30.038
lon_max,lat_max=-68.748,52.214

#REST API QUERY
user_name=''
password=''
#url_data='https://'+user_name+':'+password+'@opensky-network.org/api/states/all?'+'lamin='+str(lat_min)+'&lomin='+str(lon_min)+'&lamax='+str(lat_max)+'&lomax='+str(lon_max)
url_data= "https://opensky-network.org/api/states/all?lamin=30.038&lomin=-125.974&lamax=52.214&lomax=-68.748"
response=requests.get(url_data).json()

#LOAD TO PANDAS DATAFRAME
col_name=['icao24','callsign','origin_country','time_position','last_contact','long','lat','baro_altitude','on_ground','velocity',
'true_track','vertical_rate','sensors','geo_altitude','squawk','spi','position_source']
flight_df=pd.DataFrame(response['states'])
flight_df=flight_df.loc[:,0:16]
flight_df.columns=col_name
flight_df=flight_df.fillna('No Data') #replace NAN with No Data
flight_df.head()
print(flight_df)

