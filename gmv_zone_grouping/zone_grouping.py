# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 12:30:28 2019

@author: froni
"""

import pandas as pd
import json
from shapely.geometry import Point
from shapely.geometry import shape
#%%
orders = pd.read_csv(r'C:\Users\froni\Desktop\honestbee\Operational\Script Files\GMV Zone Grouping\store_gmv_data.csv')
zones = pd.read_csv(r'C:\Users\froni\Desktop\honestbee\Operational\Script Files\GMV Zone Grouping\zone_polygons.csv')

zones.dropna(inplace=True)
zones.reset_index(drop=True, inplace=True)

#%%
for i in range(len(zones.zone_polygon)):
    poly = json.loads(zones.zone_polygon[i])
    
    for j in range(len(poly['coordinates'][0])):
        long = poly['coordinates'][0][j][0]
        lat = poly['coordinates'][0][j][1]
        poly['coordinates'][0][j][0] = lat
        poly['coordinates'][0][j][1] = long
    zones.zone_polygon[i] = shape(poly)
 
#%%
orders = orders.assign(zone_name = '')
for k in range(len(orders.address_coords)):
    
    p1, p2 = orders.address_coords[k].split(',')[0], orders.address_coords[k].split(',')[1]  
    p1= float(p1)
    p2 = float(p2)
    point = Point(p1, p2)
    
    for l in range(len(zones.zone_polygon)):
        try:
            if zones.zone_polygon[l].contains(point) == True:
                temp_zone_name = ''
                temp_zone_name = zones.zone_name[l]
                orders.zone_name[k] = temp_zone_name
                print(k, point, temp_zone_name)
        except:
            pass
        
#%%
            
orders.to_excel(r'C:\Users\froni\Desktop\honestbee\Operational\Script Files\GMV Zone Grouping\zone.xlsx', index=False)