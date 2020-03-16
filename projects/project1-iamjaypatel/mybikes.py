# Name: Jay Patel(jjp107)
# CS 1656: Data Science
import sys
import pandas as pd
from math import cos, asin, sqrt
import math


def read_statusURL():
    df = pd.read_json(station_statusURL)
    temp = df['data']
    return pd.DataFrame(temp['stations'])


def read_infoURL():
    df = pd.read_json(station_infoURL)
    temp = df['data']
    temp1 = pd.DataFrame(temp['stations'])
    return temp1.sort_values(by=['lat', 'lon'])


def total_bikes():
    data = read_statusURL()
    total = data['num_bikes_available'].sum()
    print("Output: ", total)
    sys.exit()


def total_docks():
    data = read_statusURL()
    total = data['num_docks_available'].sum()
    print("Output: ", total)
    sys.exit()


def percent_avail(id):  # parameter: id is station_id.
    data = read_statusURL()
    array = [id]
    df_i = data.loc[data['station_id'].isin(array)]
    bikes = df_i.iloc[0]['num_bikes_available']
    docks = df_i.iloc[0]['num_docks_available']
    #print("bikes: ", bikes)
    #print("docks: ", docks)
    calc = (docks/(bikes+docks)) * 100
    final_total = math.floor(calc)
    print("Output: ", final_total, "%")
    sys.exit()


def distance(lat1, lon1, lat2, lon2):
    # print("In Distance()")
    # print("lat 1, lon 1", lat1, lon1)
    # print("lat 2, lon 2", lat2, lon2)
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * \
        cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))


def closest_stations(lat, lon):  # parameter: lat is latitude, lon is longitude
    data = read_infoURL()
    lat1 = float(lat)
    long1 = float(lon)
    distance_arr = []
    station_arr = []
    name_arr = []
    for i, loc in data.iterrows():
        calc_dist = distance(lat1, long1, loc['lat'], loc['lon'])
        distance_arr.append(calc_dist)
        station_arr.append(loc['station_id'])
        name_arr.append(loc['name'])
        #print(i, pp)
    li = {'li_stationid': station_arr,
          'li_name': name_arr, 'Distance': distance_arr}
    d = pd.DataFrame(li)
    new_d = d.sort_values(by=['Distance'])
    print("Output: ")
    # Location 1
    loc1_station = new_d.iloc[0]['li_stationid']
    loc1_name = new_d.iloc[0]['li_name']
    print("%s," % loc1_station, loc1_name)
    # Location 2
    loc2_station = new_d.iloc[1]['li_stationid']
    loc2_name = new_d.iloc[1]['li_name']
    print("%s," % loc2_station, loc2_name)
    # Location 3
    loc3_station = new_d.iloc[2]['li_stationid']
    loc3_name = new_d.iloc[2]['li_name']
    print("%s," % loc3_station, loc3_name)
    sys.exit()


def closest_bike(lat, lon):  # parameter: lat is latitude, lon is longitude
    data_info = read_infoURL()
    data_status = read_statusURL()
    lat1 = float(lat)
    long1 = float(lon)
    distance_arr = []
    station_arr = []
    name_arr = []
    for i, loc in data_info.iterrows():
        calc_dist = distance(lat1, long1, loc['lat'], loc['lon'])
        distance_arr.append(calc_dist)
        station_arr.append(loc['station_id'])
        name_arr.append(loc['name'])
        #print(i, pp)
    li = {'station_id': station_arr,
          'name': name_arr, 'Distance': distance_arr}
    df_info = pd.DataFrame(li)
    merged_df = pd.merge(df_info, data_status, on='station_id')
    chk_bikes = merged_df[merged_df['num_bikes_available'] > 0]
    df_bikes_available = chk_bikes.sort_values(by=['Distance'])
    print("Output: ")
    # Location 1
    loc_station = df_bikes_available.iloc[0]['station_id']
    loc_name = df_bikes_available.iloc[0]['name']
    print("%s," % loc_station, loc_name)
    sys.exit()


if len(sys.argv) < 3:
    sys.exit("Usage: \n python3 mybikes.py baseURL command [parameters]")
else:
    baseURL = sys.argv[1]  # Get base URL from the user.
    #print("baseURL: ", baseURL)
    command = sys.argv[2]


# Data Feeds
# Provides docking station_id, name, latitude and longitude, and the total capacity.
station_infoURL = baseURL+'/station_information.json'
#print("station_infoURL: ", station_infoURL)
# For each station_id, this provides how many bikes and docks are available at any given time.
station_statusURL = baseURL+'/station_status.json'
#print("station_statusURL: ", station_statusURL)

if command == "total_bikes":
    print("Command: total_bikes")
    print("Parameters: ")
    total_bikes()
elif command == "total_docks":
    print("Command: total_docks")
    print("Parameters: ")
    total_docks()
elif command == "percent_avail":
    if (len(sys.argv) < 4):
        sys.exit("Usage: \n python3 mybikes.py baseURL percent_avail station_id")
    else:
        print("Command: percent_avail")
        station_id = sys.argv[3]
        print("Parameters: ", station_id)
        percent_avail(station_id)
elif command == "closest_stations":
    if (len(sys.argv) < 5):
        sys.exit(
            "Usage: \n python3 mybikes.py baseURL closest_stations latitude longitude")
    else:
        print("Command: closest_stations")
        latitude = sys.argv[3]
        longitude = sys.argv[4]
        print("Parameters: ", latitude, longitude)
        closest_stations(latitude, longitude)
elif command == "closest_bike":
    if (len(sys.argv) < 5):
        sys.exit(
            "Usage: \n python3 mybikes.py baseURL closest_bike latitude longitude")
    else:
        print("Command: closest_bike")
        latitude = sys.argv[3]
        longitude = sys.argv[4]
        print("Parameters: ", latitude, longitude)
        closest_bike(latitude, longitude)
else:
    sys.exit("Usage: \n python3 mybikes.py baseURL command [parameters]")
