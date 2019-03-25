# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:26:22 2019

@author: froni
"""

import pandas as pd
import json
from shapely.geometry import shape
import geopandas as gpd
import folium as fm

#%%
'''
Create and setup the Pandas DataFrames that we will use for drawing the map
'''

df = pd.read_csv(r'file:///H:/honestbee/operational/script_files/adhoc_order_distribution/bucketed_fulfillment.csv')
zones = pd.read_csv(r'file:///H:/honestbee/operational/script_files/mapping_common/zone_polygons.csv')
store_name_correction = pd.read_csv(r'file:///H:/honestbee/operational/script_files/adhoc_order_distribution/store_name_correction.csv')

zones.rename(columns={'Zones Zone ID' : 'zone_id',
                      'Zones Zone Name' : 'zone_name',
                      'Zones Zone Area' : 'zone_polygon'},
                        inplace=True)

zones.dropna(inplace=True)
zones.reset_index(drop=True, inplace=True)


#%%
'''
Assign a count so we have values with which to use. 
Since this data is order-level each row is 1 order.
We also create a grouped name category since one store is represented by multiple in the system.
'''
 
df = df.assign(count ='')
df = df.assign(grouped_name = '')

for i in range(len(df.store_name)):
    for j in range(len(store_name_correction.previous_store_name)):
        
        if df.store_name[i] == store_name_correction.previous_store_name[j]:
            df.grouped_name[i] = store_name_correction.current_store_name[j]
            print(i, df.grouped_name[i])
            
    if df.grouped_name[i] == '':
        df.grouped_name[i] = df.store_name[i]
        print(i, df.grouped_name[i])
    df['count'][i] = 1
#%%
'''
Get unique values for the two columns that we are going to create categories on
''' 

store_list = df.grouped_name.unique().tolist()
date_list = df.ff_date.unique().tolist()

#%%
'''
Create shapely opbecjts in Pandas DataFrame
This is needed for transformation to a GeoPandas GeoDataFrame
'''

for i in range(len(zones.zone_polygon)):
    polygon = json.loads(zones.zone_polygon[i])
    zones.zone_polygon[i] = shape(polygon)
    
#%%
'''
Create goepandas DataFrame for drawing the polygons on the map, and bucketing
''' 

gpd_zones = gpd.GeoDataFrame(zones, crs={'init' : 'epsg:3395'})
gpd_zones.set_geometry('zone_polygon', inplace=True)

#%%
'''
Create the folium map object
'''

adhoc_distribution = fm.Map(location=[35.6895, 139.6917],
                            zoom_start=10,
                            tiles='StamenToner')

'''
Create a map layer for every day, and every store within that day
'''
for store in store_list[2:3]:
    for date_ in date_list:
        
        draw_df = df.loc[(df.ff_date == date_) & (df.grouped_name == store)]
        df.dropna(inplace=True)
        draw_df.reset_index(drop=True, inplace=True)
        
        fm.Choropleth(geo_data=gpd_zones.to_json(),
                      data=draw_df,
                      columns=['drop_zone_id', 'count'],
                      key_on='feature.properties.zone_id',
                      fill_color='YlOrRd',
                      fill_opacity=0.7,
                      nan_fill_opacity=0.2,
                      line_opacity=1,
                      smooth_factor=1.2,
                      name='{0} : {1}'.format(date_, store),
                      legend_name='Week {0}: Order Count'.format(date_),
                      overlay=True,
                      show=False,).add_to(adhoc_distribution)
        fm.LayerControl().add_to(adhoc_distribution)
        adhoc_distribution.save(r'H:\honestbee\operational\script_files\adhoc_order_distribution\{0}_{1}.html'.format(date_, store))
        print(store)
    print(date_)
    
#%%
    

