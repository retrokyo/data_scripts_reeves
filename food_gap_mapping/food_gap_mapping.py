# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 12:48:48 2019

@author: reeves
"""

import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape
import folium as fm
import numpy as np
from branca.element import Template, MacroElement

#%%
'''
Get data from sources, and prep the dataframes from manipulation
'''

df = pd.read_excel(r'file:///C:/Users/reeves/Desktop/dc_ff_table_v0.2.xlsx',
                   sheet_name='values',
                   header=1)

df.drop(columns={'Gap Percentage', 'Food', 'Grocery', 'Total'},
        index=39,
        inplace=True)

df.rename(columns={'Zone': 'zone_name',
                   'Sum of Grocery FF': 'grocery_ff',
                   'Sum of Grocery FF Percentage': 'grocery_ff_per',
                   'Sum of Food FF': 'food_ff',
                   'Sum of Food FF Percentage': 'food_ff_per',
                   'Gap': 'gap',
                   'Total FF': 'total_ff_per'},
            inplace=True)

zones = pd.read_csv(r'file:///C:/Users/reeves/Desktop/operational/zone_poly/zone_polygons.csv')

zones.rename(columns={'Zones Zone ID': 'zone_id',
                      'Zones Zone Name':'zone_name',
                      'Zones Zone Area': 'zone_polygon'},
                inplace=True)

zones.dropna(inplace=True)
zones.reset_index(drop=True, inplace=True)

#%%
'''
Change zone polygon from json to shapely geometry for geopandas
'''

for i in range(len(zones.zone_id)):
    polygon = json.loads(zones.zone_polygon[i])
    zones.zone_polygon[i] = shape(polygon)
    print(i)
    
#%%
'''
Left Join Zones on df
'''
intensity_df = df.merge(zones, how='left', on='zone_name') 
map_df = zones.merge(df, how='left', on='zone_name')
map_df.fillna(0, inplace=True)
#%%
'''
Transform DataFrame to GeoDataFrame
'''

map_gdf = gpd.GeoDataFrame(map_df, geometry='zone_polygon')

#%%
percentile_25 = np.percentile(intensity_df.gap, 25)
percentile_50 = np.percentile(intensity_df.gap, 50)
percentile_75 = np.percentile(intensity_df.gap, 75)

style_function = lambda x: {'fillColor': '#FF2A22' if \
                            x['properties']['food_ff']>=133 \
                            else '#FFBD22' if x['properties']['food_ff']>=percentile_75 \
                            else '#FFE954' if x['properties']['food_ff']>=percentile_50 \
                            else '#F5FF97' if x['properties']['food_ff']>percentile_25 \
                            else '#000000',
                            'fillOpacity': 0.7,
                            'color': 'black',
                            'weight': 1}

style_function2 = lambda x: {'fillColor': '#BDFFF3' if \
                             x['properties']['food_ff']>0 \
                             else '#000000',
                             'fillOpacity': 0.7,
                             'color': 'black',
                             'weight': 1}
#%%
info_list = ['zone_name', 'zone_id', 'food_ff', 'food_ff_per', 'grocery_ff', 'grocery_ff_per']
 
alias_list = ['Zone', 'Zone ID', 'Food FF', 'Food FF Percentage',
              'Grocery FF', 'Grocery FF Percentage']

tooltip = fm.GeoJsonTooltip(info_list, 
                            aliases=alias_list)

#%%

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Food Percentile</title>
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
    <li><span style='background:#FF2A22;opacity:0.7;'></span>75-100% (>174)</li>
    <li><span style='background:#FFBD22;opacity:0.7;'></span>50-75% (100-174)</li>
    <li><span style='background:#FFE954;opacity:0.7;'></span>25-50% (75-99)</li>
    <li><span style='background:#F5FF97;opacity:0.7;'></span>0-25% (0-74)</li>
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

#%%
dist_map = fm.Map(location=[35.6762, 139.6503],
                  tiles='Stamen Toner',
                  zoom_start=10)

fm.GeoJson(data=map_gdf.to_json(),
           style_function=style_function,
           name='Order Distribution',
           tooltip=tooltip).add_to(dist_map)

fm.GeoJson(data=map_gdf.to_json(),
           style_function=style_function2,
           name='Focus').add_to(dist_map)

dist_map.get_root().add_child(macro)
fm.LayerControl().add_to(dist_map)

dist_map.save(r'C:/Users/reeves/Desktop/food_bd.html')