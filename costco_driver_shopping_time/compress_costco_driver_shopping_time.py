# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:23:56 2019

@author: froni
"""

import pandas as pd
import numpy as np

#%%
'''
Create and set up data frame for usage
'''
df = pd.read_csv(r'file:///C:/Users/froni/Desktop/honestbee/operational/script_files/costco_driver_shopping_time/driver_shopping_time_wk_02_11.csv')

df.rename(columns={'Stores Name' : 'store_name',
                   'Bees Name' : 'bee_name',
                   'Jobs Job Type' : 'job_type',
                   'Jobs Local Shopper Starts Gathering Time' : 's_time',
                   'Jobs Local Shopper Completes Time' : 'e_time'},
                    inplace=True)

df.dropna(inplace=True)

df.s_time = pd.to_datetime(df.s_time)
df.e_time = pd.to_datetime(df.e_time)

df.sort_values(['bee_name', 's_time'], ascending=[True, True], inplace=True)
df.reset_index(drop=True, inplace=True)

#%%
'''
Group orders based on start time of shopping job, and the bee that preformed the job
'''
grouping = 1
df = df.assign(grouping = '')
for i in range(len(df.s_time) - 1):
    
    if df.grouping[i] == grouping:
        pass
    else:
        df.grouping[i] = grouping
        
    if df.bee_name[i] == df.bee_name[i+1]:
        if (abs((df.s_time[i+1]-df.s_time[i]).total_seconds()) / 60) < 15:
            df.grouping[i+1] = grouping
        else:
            df.grouping[i] = grouping
            grouping += 1
    else:
        grouping += 1
        
#%%
'''
Get the maximum and minimum times of each bucketed group. Thanks! @Nino
'''
compressed_df = pd.DataFrame()
for i in range(1,grouping+1):
    subset = df.loc[df.grouping == i]
    subset.reset_index(drop=True, inplace=True)
    min_time = min(subset.s_time)
    max_time = max(subset.e_time)
    
    d = {'bee_name' : subset.bee_name[0],
         's_time' : min_time,
         'e_time' : max_time}
    
    temp_df = pd.DataFrame(index=[0], data=d)
    compressed_df = compressed_df.append(temp_df, ignore_index=True)
    
#%%
'''
Calculate the time difference in hours of shopping time, and give each row a date
'''
compressed_df = compressed_df.assign(s_date = [d.date() for d in compressed_df.s_time])
compressed_df = compressed_df.assign(shopping_hours = [(((row[2] - row[1]).total_seconds())/60)/60 
                                                       for row in 
                                                       compressed_df.itertuples(index=False, name=None)])

#%%
'''
Pivot the data
'''
pivot = compressed_df.pivot_table(index='s_date',
                                  columns='bee_name',
                                  values='shopping_hours',
                                  aggfunc = np.sum,
                                  fill_value = 0)

#%%
'''
Export to excel
'''
pivot.to_excel(r'C:/Users/froni/Desktop/honestbee/operational/script_files/costco_driver_shopping_time/driver_shopping_time_compressed.xlsx')