# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 22:41:38 2019

@author: Reeves
"""

import pandas as pd
import folium as fm
import folium.plugins
from datetime import datetime
from shapely.geometry import Polygon, Point


#%%
'''
Main function
'''

def render_map(map_obj, df_name, group_list):
    
    color_list = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen',
                  'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    
    dates_list = df_name.ff_date.unique().tolist()
    dates_list.sort()
    
    store_list = df_name.grouped_name.unique().tolist()
    
    i = 0
    for store in store_list:
        
        store_coords = [float(group_list[i][1].split(',')[0]), float(group_list[i][1].split(',')[1])]
        
        fm.Marker(location=store_coords,
                  popup=store,
                  icon=fm.Icon(icon='certificate', color=color_list[i], prefix='fa')).add_to(map_obj)
        
        for n_date in dates_list:
            
            layer = fm.FeatureGroup(name=store + ' ' +n_date + ' ' + datetime.strptime(n_date, '%Y-%m-%d').strftime('%a'),
                                    show=False)
            order_cluster = folium.plugins.MarkerCluster().add_to(layer)
        
            for order in df_name[(df_name.ff_date == n_date) & (df_name.grouped_name == store)].itertuples(index=False, name=None):
                
                fm.Marker(location=[float(order[2].split(',')[0]), float(order[2].split(',')[1])],
                                    icon=fm.Icon(icon='cart-plus',
                                                 color=color_list[i],
                                                 prefix='fa')).add_to(order_cluster)
                
            map_obj.add_child(layer)
        
        for j in range(2,6,3):
            
            layer = fm.FeatureGroup(name='{0}-{1}km Radius'.format(store,str(j)), show=False)
            
            fm.Circle(location=store_coords,
                                popup=str(j),
                                radius=float(j * 1000)).add_to(layer)
            
            map_obj.add_child(layer)
            
        i += 1
    
    fm.LayerControl().add_to(map_obj)
    map_obj.save(r'D:/honestbee/operational/script_files/point_dist_viz/output/{0}.html'.format(df_name.name))

#%%

def group_info(group_name):
    
    group_array = []
    group_unique_store = group_name.grouped_name.unique().tolist()
    
    for store in group_unique_store:
        group_array.append(stores.loc[stores.grouped_name == store, ['grouped_name', 'store_loc']].to_numpy()[0].tolist())
        
    return group_array
#%%

stores = pd.read_csv(r'file:///D:/honestbee/operational/script_files/mapping_common/regular_serivce_map/regular_service_store_list.csv')
grouped_stores = pd.read_csv(r'file:///D:/honestbee/operational/script_files/mapping_common/regular_serivce_map/store_groups.csv')
tokyo_coords = [35.6762, 139.6503]

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

master_ff = pd.read_csv(r'file:///D:/honestbee/operational/script_files/point_dist_viz/order_locations.csv')

#%%

master_ff.rename(columns={'Fulfillments Local Delivered Date' : 'ff_date',
                          'Stores Name' : 'store_name',
                          'Shipping Address Address Location' : 'drop_loc'},
                        inplace=True)

#%%

master_ff.store_name = master_ff.store_name.str.strip()

master_ff = master_ff.assign(grouped_name = master_ff.store_name.map(grouped_stores_dict))

master_ff.loc[master_ff.grouped_name.isnull(), 'grouped_name'] = master_ff.store_name

#%%

aeon_ozeki = master_ff[(master_ff.grouped_name == 'Ozeki【碑文谷】') | (master_ff.grouped_name == 'AEON【碑文谷】')]
aeon_ozeki.name = 'aeon_ozeki'

sancha = master_ff[(master_ff.grouped_name == 'Seiyu【三軒茶屋】') | (master_ff.grouped_name == 'Tokyu Store【三軒茶屋】')]
sancha.name= 'sancha'

national_azabu = master_ff[(master_ff.grouped_name == 'National Azabu')]
national_azabu.name ='national_azabu'

lincos_daiei = master_ff[(master_ff.grouped_name == 'Lincos【六本木】') | (master_ff.grouped_name == 'Daiei 【麻布十番】')]
lincos_daiei.name = 'lincos_daiei'

preece_naka = master_ff[(master_ff.grouped_name == 'Precce【中目黒】')]
preece_naka.name = 'preece_naka'

nissin = master_ff[(master_ff.grouped_name == 'Nissin World Delicatessen') | (master_ff.grouped_name == 'Azabu Garden')]
nissin.name = 'nissin'


#%%

unique_store_list = master_ff.grouped_name.unique().tolist()

aeon_ozeki_info = [[unique_store_list.pop(unique_store_list.index('AEON【碑文谷】')), 
        stores.loc[stores.store_name == 'AEON【碑文谷】', 'store_loc'].unique().item()],
        [unique_store_list.pop(unique_store_list.index('Ozeki【碑文谷】')), 
         stores.loc[stores.store_name == 'Ozeki【碑文谷】', 'store_loc'].unique().item()]]

sancha_info = [[unique_store_list.pop(unique_store_list.index('Seiyu【三軒茶屋】')), 
         stores.loc[stores.store_name == 'Seiyu【三軒茶屋】', 'store_loc'].unique().item()],
        [unique_store_list.pop(unique_store_list.index('Tokyu Store【三軒茶屋】')), 
         stores.loc[stores.store_name == 'Tokyu Store【三軒茶屋】', 'store_loc'].unique().item()]]

national = [[unique_store_list.pop(unique_store_list.index('National Azabu')), 
         stores.loc[stores.store_name == 'National Azabu', 'store_loc'].unique().item()]]

lincos_daiei_info = [[unique_store_list.pop(unique_store_list.index('Lincos【六本木】')), 
         stores.loc[stores.store_name == 'Lincos【六本木】', 'store_loc'].unique().item()],
        [unique_store_list.pop(unique_store_list.index('Daiei 【麻布十番】')), 
         stores.loc[stores.store_name == 'Daiei 【麻布十番】', 'store_loc'].unique().item()]]

preece_naka_info = [[unique_store_list.pop(unique_store_list.index('Precce【中目黒】')), 
         stores.loc[stores.store_name == 'Precce【中目黒】', 'store_loc'].unique().item()]]

nissin_info = [[unique_store_list.pop(unique_store_list.index('Nissin World Delicatessen')), 
         stores.loc[stores.store_name == 'Nissin World Delicatessen', 'store_loc'].unique().item()],
        [unique_store_list.pop(unique_store_list.index('Azabu Garden')),
         stores.loc[stores.store_name == 'Azabu Garden', 'store_loc'].unique().item()]]

#%%

master_ff.drop(index=aeon_ozeki.index.to_list(), inplace=True)
master_ff.drop(index=sancha.index.to_list(), inplace=True)
master_ff.drop(index=national_azabu.index.to_list(), inplace=True)
master_ff.drop(index=lincos_daiei.index.to_list(), inplace=True)
master_ff.drop(index=preece_naka.index.to_list(), inplace=True)
master_ff.drop(index=nissin.index.to_list(), inplace=True)

master_ff.reset_index(drop=True, inplace=True)

aeon_ozeki.reset_index(drop=True, inplace=True)
sancha.reset_index(drop=True, inplace=True)
national_azabu.reset_index(drop=True, inplace=True)
lincos_daiei.reset_index(drop=True, inplace=True)
preece_naka.reset_index(drop=True, inplace=True)
nissin.reset_index(drop=True, inplace=True)

#%% 
    
national_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(national_map, national_azabu, national)

#%%

aeon_ozeki_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(aeon_ozeki_map, aeon_ozeki, aeon_ozeki_info)

#%%

sancha_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(sancha_map, sancha, sancha_info)

#%%

lincos_daiei_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(lincos_daiei_map, lincos_daiei, lincos_daiei_info)

#%%

preece_naka_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(preece_naka_map, preece_naka, preece_naka_info)

#%%

nissin_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(nissin_map, nissin, nissin_info)

#%%

northeast = Polygon([(139.7539174,35.6864208),
              (139.7721135,35.6451397),
              (139.916309,35.6479296),
              (139.8751103,35.7831245),
              (139.7539174,35.6864208)])

northwest = Polygon([(139.6938359,35.6814012),
              (139.7669636,35.7173676),
              (139.7707402,35.7967706),
              (139.6478306,35.7761613),
              (139.6128117,35.7176463),
              (139.6938359,35.6814012)])

south = Polygon([(139.6475949,35.6331418),
              (139.5641675,35.5940666),
              (139.6407285,35.4996493),
              (139.7372022,35.5622342),
              (139.6475949,35.6331418)])

center = Polygon([(139.7430386,35.6900458),
              (139.703896,35.6798736),
              (139.6633878,35.674708),
              (139.6342053,35.6484876),
              (139.7251859,35.5809443),
              (139.775311,35.5971375),
              (139.7430386,35.6900458)])

#%%%

store_zones = pd.DataFrame([['northeast', northeast], ['northwest', northwest], ['south', south], ['center', center]],
                           columns=['zone_name', 'zone_polygon'])

#%%
store_zones = store_zones.assign(group = [1, 2, 3, 4])

group_dict = stores.drop(columns=['store_name']).set_index('grouped_name').store_loc.to_dict()
master_ff = master_ff.assign(store_loc = master_ff.grouped_name.map(group_dict))

master_ff = master_ff.assign(group = '')

for i in range(len(master_ff.store_loc)):
    p1 = float(master_ff.store_loc[i].split(',')[1])
    p2 = float(master_ff.store_loc[i].split(',')[0])
    point = Point(p1, p2)
    
    for j in range(len(store_zones.zone_polygon)):
        
        if store_zones.zone_polygon[j].contains(point):
            master_ff.group[i] = store_zones.group[j]
            
#%%
            
group1 = master_ff[master_ff.group == 1]
group1.name = 'group1'

group2 = master_ff[master_ff.group == 2]
group2.name = 'group2'

group3 = master_ff[master_ff.group == 3]
group3.name = 'group3'

group4 = master_ff[master_ff.group == 4]
group4.name = 'group4'

#%%

group1_info = group_info(group1)
group2_info = group_info(group2)
group3_info = group_info(group3)
group4_info = group_info(group4)

#%%

group1.reset_index(drop=True, inplace=True)
group2.reset_index(drop=True, inplace=True)
group3.reset_index(drop=True, inplace=True)
group4.reset_index(drop=True, inplace=True)

#%%

group1_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(group1_map, group1, group1_info)

#%%

group2_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(group2_map, group2, group2_info)

#%%

group3_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(group3_map, group3, group3_info)

#%%

group4_map = fm.Map(location=tokyo_coords,
                      tiles='Stamen Toner',
                      zoom_start=11,
                      min_zoom=11,
                      max_zoom=15)

render_map(group4_map, group4, group4_info)

#%%