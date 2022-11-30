import os
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from geopy import distance
from geographiclib.geodesic import Geodesic
import math
import gmplot
INTERVAL = 10 #Interval in meters
# define the WGS84 ellipsoid
geod = Geodesic.WGS84
#AIzaSyBjPNqn2j9--iKKrqvJAcQ0rnh4ZyH2vkg
def geodesic_interpolate(lat1, lon1, lat2, lon2, end=False):
    g = geod.Inverse(lat1, lon1, lat2, lon2)
    l = geod.InverseLine(lat1, lon1, lat2, lon2)
    print("The distance is {:.3f} m.".format(g['s12']))
    # interval in m for interpolated line between locations
    step = int(math.ceil(l.s13 / INTERVAL))
    coList = []
    oldS = -1
    for i in range(step + 1):
        if i == 0:
            print("distance latitude longitude azimuth")
        if end:
            s = min(INTERVAL * i, l.s13)
        else:
            s = min(INTERVAL * i, max(l.s13 - INTERVAL, 0))
        loc = l.Position(s, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        print("{:.0f} {:.5f} {:.5f} {:.5f}".format(
            loc['s12'], loc['lat2'], loc['lon2'], loc['azi2']))
        if s <= oldS:
            break
        coList.append((loc['lat2'], loc['lon2']))
        oldS = s
    return coList

file = open("/Users/anirbanbanerjee/Downloads/Sample.kml", 'r')
contents = file.read()
soup = BeautifulSoup(contents, 'xml')
placemarks = soup.findAll("Placemark")
for placemark in placemarks:
    cordinates = placemark.coordinates
    coList = cordinates.text.strip('\t \n').split()
    lons = [float(item.split(',')[0].strip()) for item in coList]
    lats = [float(item.split(',')[1].strip()) for item in coList]
    lat_lon = [f"{item.split(',')[1].strip()}, {item.split(',')[0].strip()}" for item in coList]
    df = pd.DataFrame({"Latitude": lats, "Longitude": lons})

    df['distance'] = 0
    co2 = np.array(list(zip(df.loc[df.index[:-1], 'Latitude'].values.astype(float), df.loc[df.index[:-1], 'Longitude'].values.astype(float))))
    co1 = np.array(list(zip(df.loc[df.index[1:], 'Latitude'].values.astype(float), df.loc[df.index[1:], 'Longitude'].values.astype(float))))
    df.loc[df.index[1:], 'distance'] = np.array([distance.distance(item1, item2) for (item1, item2) in zip(co1, co2)])
    coList = []
    for index, row in df.iterrows():
        end = False
        if index == df.index[-2]:
            end = True
        l = geodesic_interpolate(row['Latitude'], row['Longitude'], df.loc[index+1, 'Latitude'], df.loc[index+1, 'Longitude'], end=end)
        coList.extend(l)
        if end:
            break

    df = pd.DataFrame(coList, columns=['Latitude', 'Longitude'])
    df['distance'] = 0
    co2 = np.array(list(zip(df.loc[df.index[:-1], 'Latitude'].values.astype(float),
                            df.loc[df.index[:-1], 'Longitude'].values.astype(float))))
    co1 = np.array(list(zip(df.loc[df.index[1:], 'Latitude'].values.astype(float),
                            df.loc[df.index[1:], 'Longitude'].values.astype(float))))
    df.loc[df.index[1:], 'distance'] = np.array([distance.distance(item1, item2) for (item1, item2) in zip(co1, co2)])
    print(df)

    gmap3 = gmplot.GoogleMapPlotter(df.iat[0,0],
                                    df.iat[0,1], 10)
    gmap3.scatter(df['Latitude'].values, df['Longitude'].values, '# FF0000',
                  size=40, marker=True)
    gmap3.plot(df['Latitude'].values, df['Longitude'].values,
               'cornflowerblue', edge_width=2.5)
    gmap3.apikey = "AIzaSyBjPNqn2j9--iKKrqvJAcQ0rnh4ZyH2vkg"
    gmap3.draw("track_map.html")
    print(co1)
#
# L->U
# R->D