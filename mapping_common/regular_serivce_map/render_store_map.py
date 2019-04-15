# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:30:11 2019

@author: Reeves

Proof of concept for plotting order distributions on a point by point basis
2 weeks of data are used
"""

import pandas as pd
import folium as fm
import folium.plugins
from datetime import datetime

#%%

stores = pd.read_csv(r'file:///D:/honestbee/operational/script_files/mapping_common/regular_serivce_map/regular_service_store_list.csv')
grouped_stores = pd.read_csv(r'file:///D:/honestbee/operational/script_files/mapping_common/regular_serivce_map/store_groups.csv')

#%%

stores.rename(columns={'Stores Name' : 'store_name',
                       'Store Address Details Address Location' : 'store_loc'},
                        inplace=True)

#%%

stores.store_name = stores.store_name.str.strip()
grouped_stores.grouped_name = grouped_stores.grouped_name.str.strip()

grouped_stores.set_index('store_name', inplace=True)
grouped_stores_dict = grouped_stores.grouped_name.to_dict()

stores = stores.assign(grouped_name = stores.store_name.map(grouped_stores_dict))
stores.loc[stores.grouped_name.isnull(), 'grouped_name'] = stores.store_name

stores.drop_duplicates(subset='grouped_name', inplace=True)

#%%

store_map = fm.Map(location =[35.6762, 139.6503],
                   tiles='Stamen Toner',
                   zoom_start=11,
                   min_zoom=11,
                   max_zoom=15)

store_cluster = folium.plugins.MarkerCluster().add_to(store_map)

for store in reduced_stores.itertuples(index=False, name=None):
    fm.Marker(location=[float(store[1].split(',')[0]), float(store[1].split(',')[1])],
                        popup=store[2],
                        icon=fm.Icon(icon='cart-plus', color='green', prefix='fa')).add_to(store_cluster)
    
#%%
    
store_map.save(r'D:/honestbee/operational/script_files/mapping_common/regular_serivce_map/store_map_{0}.html'.format(datetime.now().strftime('%Y-%m-%d')))