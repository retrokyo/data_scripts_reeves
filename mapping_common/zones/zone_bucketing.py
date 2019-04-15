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
def drop_zone_bucketing(df_file_path):

    df = pd.read_csv(df_file_path)
    zones = pd.read_csv(r'file:///C:/Users/reeves/Desktop/operational/zone_poly/zone_polygons.csv')

    df.rename(columns={'Shipping Address Address Location' : 'drop_loc'},
                    inplace=True)

    zones.rename(columns={'Zones Zone ID' : 'zone_id',
                          'Zones Zone Name' : 'zone_name',
                          'Zones Zone Area' : 'zone_polygon'},
                            inplace=True)
    zones.dropna(inplace=True)
    zones.reset_index(drop=True, inplace=True)

#%%
    zones = zones.assign(r_zone_polygon='')
    for i in range(len(zones.zone_polygon)):
        polygon = json.loads(zones.zone_polygon[i])
    
        for j in range(len(polygon['coordinates'][0])):
            long = polygon['coordinates'][0][j][0]
            lat = polygon['coordinates'][0][j][1]
            polygon['coordinates'][0][j][0] = lat
            polygon['coordinates'][0][j][1] = long
    
        zones.r_zone_polygon[i] = (shape(polygon))
        print(i)
        
#%%
    df = df.assign(drop_zone='')
    for k in range(len(df.drop_loc)):
        p1, p2 = df.drop_loc[k].split(',')[0], df.drop_loc[k].split(',')[1]
        p1 = float(p1)
        p2 = float(p2)
        point = Point(p1, p2)
    
        for l in range(len(zones.r_zone_polygon)):
            try:
                if zones.r_zone_polygon[l].contains(point) == True:
                    df.drop_zone[k] = zones.zone_name[l]
                    print(k, point, zones.zone_name[l])
            except:
                pass
    
#%%
            
    df.to_excel(r'C:/Users/reeves/Desktop/output.xlsx', index=False)