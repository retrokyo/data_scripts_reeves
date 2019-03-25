# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import json
from shapely.geometry import Point
from shapely.geometry import shape

#%%

master_df = pd.read_csv(r'C:/Users/froni/Desktop/honestbee/operational/script_files/adhoc_order_distribution/fulfillment_bucketing_grocery_adhoc.csv')
zones = pd.read_csv(r'C:/Users/froni/Desktop/honestbee/operational/script_files/mapping_common/zone_polygons.csv')

#%%

master_df.rename(columns={'Fulfillments Local Delivery Timeslot Starts Week of Year' : 'ff_woy',
                          'Fulfillments Local Delivery Timeslot Starts Date' : 'ff_date',
                          'Fulfillments Local Delivery Timeslot Starts Day of Week' : 'ff_dow',
                          'Fulfillments Fulfillment Number' : 'ff_num',
                          'Deliverers Name' : 'bee_name',
                          'Stores Name' : 'store_name',
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
zones = zones.assign(r_zone_polygon = '')
for i in range(len(zones.zone_polygon)):
    polygon = json.loads(zones.zone_polygon[i])
    for j in range(len(polygon['coordinates'][0])):
        long = polygon['coordinates'][0][j][0]
        lat = polygon['coordinates'][0][j][1]
        polygon['coordinates'][0][j][1] = long
        polygon['coordinates'][0][j][0] = lat
        
    zones.r_zone_polygon[i] = shape(polygon)
        
        
#%%
 
master_df = master_df.assign(drop_zone_id = '')
for k in range(len(master_df.drop_loc)):
    p1, p2 = master_df.drop_loc[k].split(',')[0], master_df.drop_loc[k].split(',')[1]
    p1 = float(p1)
    p2 = float(p2)
    point = Point(p1,p2)
    for l in range(len(zones.r_zone_polygon)):
        try:
            if zones.r_zone_polygon[l].contains(point) == True:
                temp_zone_id = zones.zone_id[l]
                master_df.drop_zone_id[k] = temp_zone_id
                print(k, point, temp_zone_id)
        except:
            pass
        
#%%
            
master_df = master_df.assign(store_zone_id = '')
for m in range(len(master_df.store_loc)):
    p1, p2 = master_df.store_loc[m].split(',')[0], master_df.store_loc[m].split(',')[1]
    p1 = float(p1)
    p2 = float(p2)
    point = Point(p1, p2)
    
    for n in range(len(zones.r_zone_polygon)):
        try:
            if zones.r_zone_polygon[n].contains(point) == True:
                temp_zone_id = zones.zone_id[n]
                master_df.store_zone_id[m] = temp_zone_id
                print(m, point, temp_zone_id)
        except:
            pass
        
#%%
            
master_df.to_csv(r'C:/Users/froni/Desktop/honestbee/operational/script_files/adhoc_order_distribution/bucketed_fulfillment.csv',
                 index=False)