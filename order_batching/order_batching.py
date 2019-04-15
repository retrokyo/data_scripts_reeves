# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:28:07 2019

@author: reeves
"""

import pandas as pd

#%%

df = pd.read_csv(r'file:///C:/Users/reeves/Desktop/operational/grocery_adhoc/deep_dive/grocery_adhoc_time.csv')

df.rename(columns={'Deliverers Name' : 'bee_name',
                   'Fulfillments Operation Local Delivery Timeslot Starts Week of Year' : 'timeslot_woy',
                   'Fulfillments Operation Local Delivery Timeslot Starts Date' : 'timeslot_date',
                   'Fulfillments Operation Local Delivery Timeslot Starts Hour of Day' : 'timeslot_hod',
                   'Fulfillments Operation Local Deliverer Completes Pick Up Time' : 'pickup_time',
                   'Fulfillments Operation Local Deliverer Ends Time' : 'ends_time'},
            inplace=True)

df.dropna(inplace=True)

df.pickup_time = pd.to_datetime(df.pickup_time)
df.ends_time = pd.to_datetime(df.ends_time)

df.sort_values(['bee_name', 'pickup_time'],
               ascending=[True, True],
               inplace=True)

df.reset_index(drop=True, inplace=True)

#%%

grouping = 1

df = df.assign(group='')

for i in range(len(df.pickup_time)-1):
    
    if df.group[i] == grouping:
        pass

    else:
        df.group[i] = grouping

    if df.bee_name[i] == df.bee_name[i+1]:
        if abs((df.pickup_time[i+1]-df.pickup_time[i]).total_seconds())/60 < 15:
            df.group[i+1] = grouping
            
        else:
            df.group[i] = grouping
            grouping +=1
            
    else:
        grouping += 1
        
        
#%%
        
grouped_df = pd.DataFrame()
for i in range(1,grouping+1):
    subset = df.loc[df.group == i]
    subset.reset_index(drop=True, inplace=True)
    min_time = min(subset.pickup_time)
    max_time = max(subset.ends_time)
    
    d = {'bee_name' : subset.bee_name[0],
         'timeslot_woy' : subset.timeslot_woy[0],
         'timeslot_date' : subset.timeslot_date[0],
         'timeslot_hod' : subset.timeslot_hod[0],
         'pickup_time' : min_time,
         'ends_time' : max_time}
    
    transfer_df = pd.DataFrame(index=[0], data=d)
    grouped_df = grouped_df.append(transfer_df, ignore_index=True)
    
#%%
    
grouped_df = grouped_df.assign(work_time = [(((time[5]-time[4]).total_seconds())/60)/60
                                            for time in
                                            grouped_df.itertuples(index=False, name=None)])
    
#%%
    
grouped_df.to_excel(r'C:/Users/reeves/Desktop/operational/grocery_adhoc/deep_dive/adhoc_work_time.xlsx',
                    index=False)
