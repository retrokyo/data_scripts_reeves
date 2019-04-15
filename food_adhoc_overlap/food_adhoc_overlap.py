# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:46:27 2019

@author: reeves
"""

import pandas as pd
import json
from shapely.geometry import Point, shape
import geopandas as gpd
import folium as fm
#%%

df = pd.read_csv(r'file:///C:/Users/reeves/Desktop/operational/food_grocery_overlap/food_grocery_wk9_10.csv')

df.rename(columns={'Fulfillments Operation Local Delivery Timeslot Starts Week of Year': 'week_', 
                   'Fulfillments Operation Local Delivery Timeslot Starts Date' : 'date_',
                       'Shipping Address Address Location' : 'drop_loc',
                       'Fulfillments Service Type' : 'service_type',
                       'Fulfillments Net Fulfillments' : 'net_ff'}, inplace=True)

df.drop(len(df)-1, inplace=True, axis=0)
#%%

zones = pd.read_csv(r'file:///C:/Users/reeves/Desktop/operational/zone_poly/zone_polygons.csv')

zones.rename(columns={'Zones Zone ID' : 'zone_id',
                      'Zones Zone Name' : 'zone_name',
                      'Zones Zone Area' : 'zone_geometry'},
inplace=True)

zones.dropna(inplace=True)
zones.reset_index(drop=True, inplace=True)
#%%
zones = zones.assign(r_zone_polygon = '')
for i in range(len(zones.zone_geometry)):
    polygon = json.loads(zones.zone_geometry[i])
    
    for j in range(len(polygon['coordinates'][0])):
        long = polygon['coordinates'][0][j][0]
        lat = polygon['coordinates'][0][j][1]
        polygon['coordinates'][0][j][0] = lat
        polygon['coordinates'][0][j][1] = long
        
    zones.r_zone_polygon[i] = shape(polygon)
    print(i)
#%%

df = df.assign(drop_poly = '')
df = df.assign(zone_name = '')
for k in range(len(df.drop_loc)):
    p1, p2 = df.drop_loc[k].split(',')[0], df.drop_loc[k].split(',')[1]
    p1 = float(p1)
    p2 = float(p2)
    point = Point(p1, p2)
    
    for l in range(len(zones.r_zone_polygon)):
        if zones.r_zone_polygon[l].contains(point) == True:
            temp_zone_name = zones.zone_name[l]
            temp_zone_poly = zones.r_zone_polygon[l]
            df.drop_poly[k] = temp_zone_poly
            df.zone_name[k] = temp_zone_name
            print(k, temp_zone_name)
            
#%%
for i in range(len(zones.zone_geometry)):
    polygon = json.loads(zones.zone_geometry[i])
    zones.zone_geometry[i] = shape(polygon)
    print(i)
    
#%%
    
gf = gpd.GeoDataFrame(zones, crs={'init' : 'epsg:3395'})
gf.set_geometry('zone_geometry', inplace=True)
gf.drop('r_zone_polygon', axis=1, inplace=True)

#%%

food_df = df[df.service_type == 'food']
food_df.drop('drop_poly', axis=1, inplace=True)
food_df.reset_index(drop=True, inplace=True)

grocery_df = df[df.service_type == 'groceries']
grocery_df.drop('drop_poly', axis=1, inplace=True)
grocery_df.reset_index(drop=True, inplace=True)

combined_df = food_df.append(grocery_df, ignore_index=True)

#%%

zone_df = food_df.groupby('zone_name').apply(sum)
#%%

dist_map = fm.Map(location=[35.6762, 139.6503],
                   zoom_start=10,
                   tiles='StamenToner')

food_choro = fm.Choropleth(geo_data=gf.to_json(),
              data=food_df,
              columns=['zone_name', 'net_ff'],
              key_on='feature.properties.zone_name',
              fill_color='YlOrRd',
              fill_opacity=0.5,
              nan_fill_opacity=0.2,
              line_opacity=1,
              smooth_factor=1.2,
              name='Food Distribution',
              highlight=True,
              legend_name='Food Volume',
              bins=3)

grocery_choro = fm.Choropleth(geo_data=gf.to_json(),
                              data=grocery_df,
                              columns=['zone_name', 'net_ff'],
                              key_on='feature.properties.zone_name',
                              fill_color='BuGn',
                              fill_opacity=0.5,
                              nan_fill_opacity=0.2,
                              line_opacity=1,
                              smooth_factor=1.2,
                              name='Grocery Distribution',
                              highlight=True,
                              legend_name='Grocery Volume',
                              bins=3)

combined_choro = fm.Choropleth(geo_data=gf.to_json(),
                                data=combined_df,
                                columns=['zone_name', 'net_ff'],
                                key_on='feature.properties.zone_name',
                                fill_color='PuRd',
                                fill_opacity=0.7,
                                nan_fill_opacity=0.2,
                                line_opacity=1,
                                smooth_factor=1.2,
                                name='Combined Distribution',
                                highlight=True,
                                legend_name='Combined Volume',
                                bins=3)

dist_map.add_child(food_choro)
dist_map.add_child(grocery_choro)
dist_map.add_child(combined_choro)
fm.LayerControl().add_to(dist_map)

#%%

dist_map.save('C:/Users/reeves/Desktop/operational/food_grocery_overlap/food_v_grocery_wk9_10.html')

#%%
