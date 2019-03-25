# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 10:37:32 2019

@author: froni
"""

import pandas as pd
import folium as fm
import json
from shapely.geometry import shape
import geopandas as gpd

#%%

df = pd.read_excel(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Grocery Driver Path/bucketed.xlsx')
zones = pd.read_csv(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Grocery Driver Path/zone_polygons.csv')
#%%

costco = df.loc[df['hub_name'] == 'B:COSTCOkawasaki']

zones.rename(columns={'Zones Zone ID' : 'zone_id',
                      'Zones Zone Name' : 'zone_name',
                      'Zones Zone Area' : 'zone_polygon'},
                        inplace=True)

zones.dropna(inplace=True)
zones.reset_index(drop=True, inplace=True)
#%%
non_coscto2 = [i for i in df.itertuples(index=False, name=None) if ((i[3] != 'B:COSTCOkawasaki') & ('TOKYO' in i[3]))]

#%%
non_costco = df.loc[(df['hub_name'] != 'B:COSTCOkawasaki')]    
#%%

non_costco_count = non_costco.groupby('drop_zone', as_index=False)['ff_ends_tod'].count()

costco_count = costco.groupby('drop_zone', as_index=False)['ff_ends_tod'].count()

non_costco_count.rename(columns={'ff_ends_tod' : 'count'},
                        inplace=True)

costco_count.rename(columns={'ff_ends_tod' : 'count'},
                    inplace=True)
#%%

for i in range(len(zones.zone_polygon)):
    poly = json.loads(zones.zone_polygon[i])
    zones.zone_polygon[i] = shape(poly) 
    
#%%
    
zone_geometry = gpd.GeoDataFrame(zones, crs={'init' : 'epsg:3395'})
zone_geometry.set_geometry('zone_polygon', inplace=True)


#%%

order_dist_costco = fm.Map(location=[35.6895, 139.6917],
                           zoom_start=10,
                           tiles='StamenToner')

fm.Choropleth(geo_data=zone_geometry.to_json(),
              data=costco_count,
              columns=['drop_zone', 'count'],
              key_on='feature.properties.zone_name',
              fill_color='YlOrRd',
              fill_opacity=0.7,
              nan_fill_opacity=0.2,
              line_opacity=1,
              smooth_factor=1.2,
              name='Costco Kawasaki Distribution',
              legend_name='Order Count').add_to(order_dist_costco)

fm.LayerControl().add_to(order_dist_costco)
order_dist_costco.save(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Grocery Driver Path/test.html')

#%%

order_dist_non_costco = fm.Map(location=[35.6895, 139.6917],
                               zoom_start=10,
                               tiles='StamenToner')

fm.Choropleth(geo_data=zone_geometry.to_json(),
              data=non_costco_count,
              columns=['drop_zone', 'count'],
              key_on='feature.properties.zone_name',
              fill_color='YlOrRd',
              fill_opacity=0.7,
              nan_fill_opacity=0.2,
              line_opacity=1,
              smooth_factor=1.2,
              legend_name='Order Count').add_to(order_dist_non_costco)

fm.LayerControl().add_to(order_dist_non_costco)
order_dist_non_costco.save(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Grocery Driver Path/test2.html')
