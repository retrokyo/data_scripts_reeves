# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 13:18:48 2019

@author: froni
"""

import pandas as pd
import random
import folium as fm
import folium.plugins
import numpy as np
from collections import namedtuple

def set_points(bee_df):
    try:
        point_array = []
        for row in bee_df.itertuples(index=False, name=None):
            point_array.append([row[5], row[6]])
    except:
        print('Something went wrong')
    return point_array

def get_arrow(locations, color='black', size=6, n_arrows=5):
    arrow_map = fm.Map(location=[35.6895, 139.6917])
    Point = namedtuple('Point', field_names=['lat' ,'long'])
    
    p1 = Point(locations[0][0], locations[0][1])
    p2 = Point(locations[1][0], locations[1][1])
    
    rotation = get_bearing(p1, p2) - 90.0
    arrow_lats = np.linspace(p1.lat, p2.lat, n_arrows + 2)
    arrow_longs = np.linspace(p1.long, p2.long, n_arrows + 2)
    
    arrows = []
    for points in zip(arrow_lats, arrow_longs):
        arrows.append(fm.RegularPolygonMarker(location=points,
                                              fill_color=color,
                                              number_of_sides=3,
                                              radius=size,
                                              rotation=rotation).add_to(arrow_map))
    return arrows

def get_bearing(p1, p2):
    long_diff = np.radians(p2.long - p1.long)
    
    lat1 = np.radians(p1.lat)
    lat2 = np.radians(p2.lat)
    
    x= np.sin(long_diff) * np.cos(lat2)
    y= np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) * np.cos(long_diff))
    
    bearing = np.degrees(np.arctan2(x, y))
    
    if bearing < 0:
        return bearing + 360
    return bearing
#%%
df = pd.read_csv(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Grocery Driver Path/driver_info_d2d.csv')

#%%
df.rename(columns={'Fulfillments Local Deliverer Ends Week of Year' : 'week_num',
                   'Fulfillments Local Deliverer Ends Date' : 'rdate',
                   'Fulfillments Local Deliverer Ends Time of Day': 'tod',
                   'Stores Hub Name': 'hub_name',
                   'Deliverers Name' : 'bee_name',
                   'Store Addresses Address Location' : 'store_loc',
                   'Shipping Address Address Location' : 'drop_loc'},
                    inplace=True)

#%%

rand_bee1 = df.loc[random.randint(0, len(df)), ['bee_name', 'rdate']].tolist()

#%%

bee1_jobs = df.loc[(df['bee_name'] == rand_bee1[0]) & (df['rdate'] == rand_bee1[1])]

#%%

bee1_jobs.sort_values(by=['tod'], inplace=True)

#%%

bee1_points = set_points(bee1_jobs)

#%%
tokyo_coords = [35.6895, 139.6917]
bee1_map = fm.Map(location=tokyo_coords, zoom_start=10, tiles='Stamen Toner')

arrow_array = []
arrow_between = []
store_cluster = folium.plugins.MarkerCluster().add_to(bee1_map)
drop_cluster = folium.plugins.MarkerCluster().add_to(bee1_map)
i = 1
for path in bee1_points:
    start = list(map(float, path[0].split(',')))
    try:
        fm.PolyLine(locations=[end, start]).add_to(bee1_map)
        arrow_between.append(get_arrow([end, start], color='red'))
    except:
        pass
    end = list(map(float, path[1].split(',')))
    arrow_array.append(get_arrow([start, end], color='green'))
    fm.Marker(location=start, popup=str(i), icon=fm.Icon(icon='cart-plus', color='green', prefix='fa')).add_to(store_cluster)
    fm.Marker(location=end, popup=str(i), icon=fm.Icon(icon='cart-arrow-down', color='red', prefix='fa')).add_to(drop_cluster)
    fm.PolyLine(locations=[start, end]).add_to(bee1_map)
    i += 1


for i in range(len(arrow_array)):
    for arrow in arrow_array[i]:
        arrow.add_to(bee1_map)

for i in range(len(arrow_between)):
    for arrow in arrow_between[i]:
        arrow.add_to(bee1_map)
#%%
    
bee1_map.save(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Grocery Driver Path/bee1_map.html')