# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:27:47 2019

@author: reeves
"""

import pandas as pd
#%%
'''
Reads the input data, and prepares it for he following operation
'''
df = pd.read_csv(r'file:///C:/Users/reeves/Desktop/operational/order_waterfall/input.csv')

df.rename(columns={'Fulfillments Operation Local Delivery Timeslot Starts Week of Year': 'week_num',
                   'Fulfillments Operation Local Delivery Timeslot Starts Date': 'timeslot_date',
                   'Fulfillments Operation Local Delivery Timeslot Starts Day of Week': 'timeslot_dow',
                   'Fulfillments Local Created Time': 'created_at',
                   'Fulfillments Operation Local Delivery Timeslot Starts Hour of Day': 'timeslot_hod',
                   'Stores Name': 'store_name',
                   'Fulfillments Net Fulfillments': 'net_ff'},
            inplace=True)

df.sort_values(by=['timeslot_date', 'created_at'], ascending=[True, True], inplace=True)
df.reset_index(drop=True, inplace=True)
#%%
'''
Change the type of the data stored in the columns to pandas datetime
'''
df.timeslot_date = pd.to_datetime(df.timeslot_date)
df.created_at = pd.to_datetime(df.created_at)

#%%
'''
First creates a list of the timeslot hours available, and an empty list. The nested
for loops iterate through each created datetime in the data, and compares it against
each timeslot. When it finds the correct timeslot, the value is appended to the blank list.
When complete the new list is added to the DataFrame. 
'''
timeslot_hours = range(9,22)
count_bucket = []

for i in range(len(df.created_at)):
    for hour in timeslot_hours:
        if df.created_at[i] < (df.timeslot_date[i] + pd.Timedelta('{0} hours'.format(hour))):
            count_bucket.append(hour)
            break

df = df.assign(entered_at = count_bucket)

#%%
'''
Export the Dataframe to an excel sheet for further manipulation, and graphing purposes
'''
df.to_excel(r'C:/Users/reeves/Desktop/operational/order_waterfall/waterfall_output.xlsx', index=False)
