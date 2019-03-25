# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 15:23:42 2019

@author: reeves
"""

import pandas as pd
import folium as fm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#%%
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.fullscreen_window()

orders = pd.read_excel(r'file:///C:/Users/reeves/Desktop/operational/d2d_adhoc_vs_others/adhoc_vs_other.xlsx',
                       sheet_name='national_azabu')

#%%

orders = orders.assign(date_str = '')

for i in range(len(orders.timeslot_date)):
    orders.date_str[i] = orders.timeslot_date[i].date()
    
#%%
    
date_array = orders.date_str.unique().tolist()

#%%
for i in range(len(date_array)):
    
    temp_df = orders[orders.date_str == date_array[i]]
    temp_df.reset_index(drop=True, inplace=True)
    
    order_map = fm.Map(location=[35.6512, 139.7241],
                   tiles='Stamen Toner',
                   zoom_start = 13,
                   min_zoom = 13)
    
    fm.Marker(location=[35.6512, 139.7241],
              icon=fm.Icon(color='lightgreen',
                           icon='cart-plus',
                           prefix='fa')).add_to(order_map)
    
    fm.Circle(location=[35.6512, 139.7241],
              radius=2000.0,
              color='lightgreen').add_to(order_map)
    
    fm.Circle(location=[35.6512, 139.7241],
              radius=5000.0,
              color='lightgreen').add_to(order_map)
    
    
    for j in range(len(temp_df.drop_loc)):
        
        drop_coords = [float(temp_df.drop_loc[j].split(',')[0]),
                       float(temp_df.drop_loc[j].split(',')[1])]
        
        if temp_df.bee_group[j] == 'Adhoc':
            fm.Marker(location=drop_coords,
                      icon=fm.Icon(color='blue',
                                   icon='cart-arrow-down',
                                   prefix='fa')).add_to(order_map)
            
        else:
            fm.Marker(location=drop_coords,
                      icon=fm.Icon(color='red',
                                   icon='cart-arrow-down',
                                   prefix='fa')).add_to(order_map)
    
    order_map.save(r'C:/Users/reeves/Desktop/operational/d2d_adhoc_vs_others/html_files/{0}.html'.format(date_array[i]))
    
    driver.get(r'file:///C:/Users/reeves/Desktop/operational/d2d_adhoc_vs_others/html_files/{0}.html'.format(date_array[i]))
    driver.save_screenshot(r'C:/Users/reeves/Desktop/operational/d2d_adhoc_vs_others/png_files/{0}.png'.format(date_array[i]))
    
driver.quit()
