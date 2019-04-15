# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 11:45:40 2019

@author: reeves
"""

import getpass
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import Point, shape
import folium as fm
from branca.element import Template, MacroElement

#%%
chosen = False
while chosen == False:
    service_type = input('''
                     Please choose service type
                     1 : groceries
                     2 : food
                     ''')
    
    if service_type == '1':
        df = pd.read_excel(r'file:///C:/Users/reeves/Desktop/operational/apartment_mapping/grocery_ff.xlsx')
        chosen = True
        
    elif service_type == '2':
        df = pd.read_excel(r'file:///C:/Users/reeves/Desktop/operational/apartment_mapping/food_ff.xlsx')
        chosen = True
    else:
        print('Incorrect input. Please try again.')
        

zones = pd.read_csv(r'file:///C:/Users/reeves/Desktop/operational/zone_poly/zone_polygons.csv')
apartments = pd.read_csv(r'file:///C:/Users/reeves/Desktop/operational/apartment_mapping/apartment_coords.csv')
stores = pd.read_csv('file:///C:/Users/reeves/Desktop/operational/apartment_mapping/priority_store_list.csv')

df.rename(columns={'Shipping Address Address Location' : 'drop_loc',
                   'Fulfillments Net Fulfillments' : 'net_ff'},
            inplace=True)

apartments.rename(columns={'Shipping Address Address Location': 'loc'},
                  inplace=True)

zones.rename(columns={'Zones Zone ID' : 'zone_id',
                      'Zones Zone Name' : 'zone_name',
                      'Zones Zone Area' : 'zone_polygon'},
                inplace=True)

zones.dropna(inplace=True)
zones.reset_index(drop=True, inplace=True)

#%%
r_zone_poly_list = []
zone_poly_list = []
print('Creating shapely Shapes...')
for i in range(len(zones.zone_polygon)):
    polygon = json.loads(zones.zone_polygon[i])
    zone_poly_list.append(shape(polygon))
    
    for j in range(len(polygon['coordinates'][0])):
        long = polygon['coordinates'][0][j][0]
        lat = polygon['coordinates'][0][j][1]
        polygon['coordinates'][0][j][0] = lat
        polygon['coordinates'][0][j][1] = long
        
    r_zone_poly_list.append(shape(polygon))
    print(i)

zones = zones.assign(r_zone_polygon=r_zone_poly_list,
                      zone_polygon=zone_poly_list)

#%%

drop_zone_id_list = []
print('Appending Zone IDs..')
for i in range(len(df.drop_loc)):
    p1, p2 = df.drop_loc[i].split(',')[0], df.drop_loc[i].split(',')[1]
    p1 = float(p1)
    p2 = float(p2)
    point = Point(p1, p2)
    check = False
    
    for j in range(len(zones.r_zone_polygon)):
        if zones.r_zone_polygon[j].contains(point) == True:
            drop_zone_id_list.append(zones.zone_id[j])
            print(i, point, zones.zone_id[j])
            check = True
            
    if check == False:
        drop_zone_id_list.append(None)
        print(i, point)
            
            
df = df.assign(zone_id = drop_zone_id_list)
#%%
print('Left Join!')

df.drop(columns=['drop_loc',
                 'drop_zone',
                 'Fulfillments Operation Local Delivery Timeslot Starts Week of Year',
                 'Fulfillments Service Type'],
    inplace=True)
df.reset_index(drop=True, inplace=True)

df = df.groupby(['zone_id'], as_index=False).net_ff.sum()
zones = zones.merge(df, how='left', on='zone_id')

zones.drop(columns=['r_zone_polygon'], inplace=True)
zones.fillna(0, inplace=True)
gdf = gpd.GeoDataFrame(zones, geometry='zone_polygon')
#%%
print('Creating Map')            
dist_map = fm.Map(location=[35.6762, 139.6503],
             zoom_start=10,
             tiles='StamenToner')

fm.GeoJson(data=gdf.to_json(),
           style_function= lambda x :{'fillColor':'#FF2A1C' if \
                                      x['properties']['net_ff']>=250 \
                                  else '#FFC133' if x['properties']['net_ff']>=100 \
                                  else '#80FF00' if x['properties']['net_ff']>=50 \
                                  else '#00FFCF' if x['properties']['net_ff']>=10 \
                                  else '#00CFFF' if x['properties']['net_ff']>0 \
                                  else '#A09898',
                                  'fillOpacity': 0.7,
                                  'color': 'black',
                                  'weight' : 1},
            name='Order Distribution',
            tooltip=fm.GeoJsonTooltip(['zone_name', 'zone_id', 'net_ff'],
                                  aliases=['Zone Name', 'Zone ID', 'Net FF'])).add_to(dist_map)

layer = fm.FeatureGroup(name='Apartments')

for apartment in apartments.itertuples(index=False, name=None):
    apartment_coords = [float(apartment[4].split(',')[0]),
                        float(apartment[4].split(',')[1])]
    fm.Marker(location=apartment_coords,
              popup=apartment[0],
              icon=fm.Icon(icon='archway',
                           color='black',
                           prefix='fa')).add_to(layer)

store_points = fm.FeatureGroup(name='Stores')

for store in stores.itertuples(index=False, name=None):
    store_coords = [float(store[1].split(',')[0]),
                    float(store[1].split(',')[1])]
    fm.Marker(location=store_coords,
              popup=store[0],
              icon=fm.Icon(icon='cart-plus',
                           color='pink',
                           prefix='fa')).add_to(store_points)
template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Grocery - 3 Months</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legend</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:#FF2A1C;opacity:0.7;'></span>&gt; 250</li>
    <li><span style='background:#FFC133;opacity:0.7;'></span>&gt; 100</li>
    <li><span style='background:#80FF00;opacity:0.7;'></span>&gt; 50</li>
    <li><span style='background:#00FFCF;opacity:0.7;'></span>&gt; 10</li>
    <li><span style='background:#00CFFF;opacity:0.7;'></span>&gt; 0</li>
  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

dist_map.get_root().add_child(macro)
dist_map.add_child(layer)
dist_map.add_child(store_points)
fm.LayerControl().add_to(dist_map)
print('Saving Map...')
#%%

if service_type == 1:
    dist_map.save(r'C:/Users/{0}/Desktop/grocery_output.html'.format(getpass.getuser()))
    
else:
    dist_map.save(r'c:/Users/{0}/Desktop/food_output.html'.format(getpass.getuser()))
    
print('Map Saved!')
