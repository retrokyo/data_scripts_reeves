# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 16:47:13 2019

@author: froni
"""

import pandas as pd
import json
from shapely.geometry import Point
from shapely.geometry import shape

#%%

#df = pd.read_csv(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Grocery Driver Path/driver_info_d2d.csv')
#zones = pd.read_csv(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Grocery Driver Path/zone_polygons.csv')
df = pd.read_csv(r'H:/honestbee/Operational/Script Files/Grocery Driver Path/driver_info_d2d.csv')
zones = pd.read_csv(r'H:/honestbee/Operational/Script Files/Grocery Driver Path/zone_polygons.csv')

df.rename(columns={'Fulfillments Local Deliverer Ends Week of Year' : 'ff_ends_week',
                   'Fulfillments Local Deliverer Ends Date' : 'ff_ends_date',
                   'Fulfillments Local Deliverer Ends Time of Day' : 'ff_ends_tod',
                   'Stores Hub Name' : 'hub_name',
                   'Deliverers Name' : 'bee_name',
                   'Store Addresses Address Location' : 'store_loc',
                   'Shipping Address Address Location' : 'drop_loc'},
                    inplace=True)

zones.rename(columns={'Zones Zone ID' : 'zone_id',
                     'Zones Zone Name' : 'zone_name',
                     'Zones Zone Area' : 'zone_polygon'},
                        inplace=True)
zones.dropna(inplace=True)
zones.reset_index(drop=True, inplace=True)

#%%
for i in range(len(zones.zone_polygon)):
    polygon = json.loads(zones.zone_polygon[i])
    
    for j in range(len(polygon['coordinates'][0])):
        long = polygon['coordinates'][0][j][0]
        lat = polygon['coordinates'][0][j][1]
        polygon['coordinates'][0][j][0] = lat
        polygon['coordinates'][0][j][1] = long
    
    zones.zone_polygon[i] = shape(polygon)
    
#%%
df = df.assign(store_zone = '')
for k in range(len(df.store_loc)):
    p1, p2 = df.store_loc[k].split(',')[0], df.store_loc[k].split(',')[1]
    p1 = float(p1)
    p2 = float(p2)
    point = Point(p1, p2)
    
    for l in range(len(zones.zone_polygon)):
        try:
            if zones.zone_polygon[l].contains(point) == True:
                temp_zone_name = ''
                temp_zone_name = zones.zone_name[l]
                df.store_zone[k] = temp_zone_name
                print(k, point, temp_zone_name)
        except:
            pass
        
#%%
df = df.assign(drop_zone = '')
for m in range(len(df.drop_loc)):
    p1, p2 = df.drop_loc[m].split(',')[0], df.drop_loc[m].split(',')[1]
    p1 = float(p1)
    p2 = float(p2)
    point = Point(p1, p2)
    
    for n in range(len(zones.zone_polygon)):
        try:
            if zones.zone_polygon[n].contains(point) == True:
                temp_zone_name = ''
                temp_zone_name = zones.zone_name[n]
                df.drop_zone[m] = temp_zone_name
                print(m, point, temp_zone_name)
        except:
            pass
        
#%%
            
df.to_excel(r'H:/honestbee/Operational/Script Files/Grocery Driver Path/bucketed.xlsx')