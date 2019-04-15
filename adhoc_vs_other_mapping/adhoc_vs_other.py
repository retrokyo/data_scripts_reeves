# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 15:23:42 2019

@author: reeves
"""

import pandas as pd
import folium as fm
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#%%
options = Options()
options.headless = True

orders = pd.read_excel(r'file:///C:/Users/reeves/Desktop/operational/adhoc_vs_other/adhoc_vs_other.xlsx',
                       sheet_name='nissin')

orders = orders.append(pd.read_excel(r'file:///C:/Users/reeves/Desktop/operational/adhoc_vs_other/adhoc_vs_other.xlsx',
                       sheet_name='lincos'), ignore_index=True, sort=False)

orders = orders.append(pd.read_excel(r'file:///C:/Users/reeves/Desktop/operational/adhoc_vs_other/adhoc_vs_other.xlsx',
                       sheet_name='daiei'), ignore_index=True, sort=False)

orders.columns = orders.columns.str.replace('.*?_ff_count', 'ff_count')

orders = orders.stack()
orders = orders.unstack()

orders.sort_values(by=['timeslot_woy', 'timeslot_date'],
                   axis=0,
                   ascending=[True, True],
                   inplace=True)
#%%

orders = orders.assign(date_str = '')

for i in range(len(orders.timeslot_date)):
    orders.date_str[i] = orders.timeslot_date[i].date()
    
#%%
    
date_array = orders.date_str.unique().tolist()
date_array.sort()
hod_array = orders.timeslot_hod.unique().tolist()
hod_array.sort()

recent_date_array = date_array[-7:]
recent_date_array.sort()
#%%
def daily_map():
    
    driver = webdriver.Firefox(options=options)
    driver.fullscreen_window()
    
    try:
        for i in range(len(date_array)):
    
            day_df = orders[orders.date_str == date_array[i]]
            day_df.reset_index(drop=True, inplace=True)
    
            order_map = fm.Map(location=[35.6512,139.7241],
                               tiles='Stamen Toner',
                               zoom_start=13,
                               min_zoom=13)

            fm.Marker(location=[35.6512,139.7241],
                      icon=fm.Icon(color='lightgreen',
                                   icon='cart-plus',
                                   prefix='fa')).add_to(order_map)
        
            fm.Circle(location=[35.6512, 139.7241],
                      radius=2000.0,
                      color='lightgreen').add_to(order_map)
    
            fm.Circle(location=[35.6512, 139.7241],
                      radius=5000.0,
                      color='lightgreen').add_to(order_map)
            
            print(date_array[i])
            
            for j in range(len(day_df.drop_loc)):
        
                drop_coords = [float(day_df.drop_loc[j].split(',')[0]),
                               float(day_df.drop_loc[j].split(',')[1])]
        
                if day_df.bee_group[j] == 'Adhoc':
                    fm.Marker(location=drop_coords,
                              icon=fm.Icon(color='blue',
                                           icon='cart-arrow-down',
                                           prefix='fa')).add_to(order_map)
            
                else:
                    fm.Marker(location=drop_coords,
                              icon=fm.Icon(color='red',
                                           icon='cart-arrow-down',
                                           prefix='fa')).add_to(order_map)
                    
                
            order_map.save(r'C:/Users/reeves/Desktop/operational/adhoc_vs_other/html_files/{0}.html'.format(date_array[i]))
    
            driver.get(r'file:///C:/Users/reeves/Desktop/operational/adhoc_vs_other/html_files/{0}.html'.format(date_array[i]))
            time.sleep(5)
            driver.save_screenshot(r'C:/Users/reeves/Desktop/operational/adhoc_vs_other/png_files/{0}.png'.format(date_array[i]))
        
    except:
        driver.quit()
        print('Welp...')
        
    driver.quit()
#%%
def hourly_map():
    
    driver = webdriver.Firefox(options=options)
    driver.fullscreen_window()
    
    try:
        for i in range(len(recent_date_array)):
        
            day_df = orders[(orders.date_str == recent_date_array[i])]
            day_df.reset_index(drop=True, inplace=True)
            print(recent_date_array[i])
            
            for j in range(len(hod_array)):
        
                hour_df = day_df[day_df.timeslot_hod == hod_array[j]]
                hour_df.reset_index(drop=True, inplace=True)
        
                hour_map = fm.Map(location=[35.6561, 139.7333],
                                  tiles='Stamen Toner',
                                  zoom_start=12,
                                  min_zoom=12)
            
                fm.Marker(location=[35.6561, 139.7333],
                          icon=fm.Icon(color='lightgreen',
                                       icon='cart-plus',
                                       prefix='fa')).add_to(hour_map)
            
                fm.Circle(location=[35.6561, 139.7333],
                          radius=2000.0,
                          color='lightgreen').add_to(hour_map)
            
                fm.Circle(location=[35.6561, 139.7333],
                          radius=5000.0,
                          color='lightgreen').add_to(hour_map)
                
                print(str(hod_array[j]) + ' ' + str(len(hour_df.drop_loc)))
                
                for k in range(len(hour_df.drop_loc)):
                    
                    drop_coords = [float(hour_df.drop_loc[k].split(',')[0]),
                                   float(hour_df.drop_loc[k].split(',')[1])]
                
                    if hour_df.bee_group[k] == 'Adhoc':
                        fm.Marker(location=drop_coords,
                                  icon=fm.Icon(color='blue',
                                               icon='cart-arrow-down',
                                               prefix='fa')).add_to(hour_map)
                    
                    else:
                        fm.Marker(location=drop_coords,
                                  icon=fm.Icon(color='red',
                                               icon='cart-arrow-down',
                                               prefix='fa')).add_to(hour_map)
                    
                hour_map.save(r'C:/Users/reeves/Desktop/operational/adhoc_vs_other/3_hourly_html/{0}-{1}.html'.format(recent_date_array[i], hod_array[j]))
            
                driver.get(r'file:///C:/Users/reeves/Desktop/operational/adhoc_vs_other/3_hourly_html/{0}-{1}.html'.format(recent_date_array[i], hod_array[j]))
                time.sleep(5)
                driver.save_screenshot(r'C:/Users/reeves/Desktop/operational/adhoc_vs_other/3_hourly_png/{0}-{1}.png'.format(recent_date_array[i], hod_array[j]))
                
    except:
        driver.quit()
        print('Welp...')
        
    driver.quit()