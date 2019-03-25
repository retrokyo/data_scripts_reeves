# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 10:45:17 2019

@author: froni
"""

import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt

#%%

def orders_plot(ax, start_index, end_index, x_values, step=1):
    for day in range(start_index, end_index, step):
        y_values = df_order.iloc[day].tolist()
        ax.plot(x_values[1:], y_values[1:], label=df_order.date[day].strftime('%m-%d'))
        ax.set_xticks(range(6,24))
        ax.grid()
        ax.legend(ncol=7, framealpha=0, loc='upper left', bbox_to_anchor=[0,1.4])
        
def shifts_plot(ax, start_index, end_index, x_values, step=1):
    for day in range(start_index, end_index, step):
        y_values = df_shift.iloc[day].tolist()
        ax.plot(x_values[1:], y_values[1:], label = df_shift.date[day].strftime('%m-%d'))
        ax.set_xticks(range(6, 24))
        ax.grid()
        ax.legend(ncol=7, framealpha=0, loc='upper left', bbox_to_anchor=[0,1.4])
        

#%%

shift = pd.read_csv(r'file:///C:/Users/froni/Desktop/honestbee/Operational/Script Files/Visualizations/v3_shifts_shopper.csv')

shift.rename(columns={'Bees Name':'shopper',
                      'Shift Hub Name': 'shift_hub',
                      'Shifts Local Start Date':'date',
                      'Shifts Local Start Hour of Day':'hod',
                      'Shifts Total Paid Hours Sum':'hours',
                      'Shifts Count':'count'},
                        inplace=True)


#%%
hod_unique_shift = shift.hod.unique()
hod_unique_shift = np.append(hod_unique_shift, [21, 22, 23])
hod_unique_shift.sort()


shift['date'] = shift['date'].astype('datetime64')
date_unique_shift = shift.date.unique()
date_unique_shift.sort()

#%%

df_shift = pd.DataFrame(index=date_unique_shift, columns=hod_unique_shift)
df_shift = df_shift.fillna(0)

#%%

for shifts in shift.itertuples(index=False):
    date_index = shifts[2]
    start_hour = shifts[3]
    shift_hours = math.floor(shifts[5])
    
    for i in range(shift_hours):
        df_shift.at[date_index, start_hour] += 1
        start_hour += 1

#%%
df_shift.reset_index(inplace=True)
df_shift.rename(columns={'index':'date'}, inplace=True)

#%%

orders = pd.read_csv(r'file:///C:/Users/froni/Desktop/honestbee/Operational/Script Files/Visualizations/v3_fulfillments_grocery.csv')

orders.rename(columns={'Fulfillments Local Delivery Timeslot Starts Date':'date',
                       'Fulfillments Local Delivery Timeslot Starts Hour of Day':'hour',
                       'Fulfillments Net Fulfillments':'fulfillments'},
                        inplace=True)

#%%
hod_unique_order = orders.hour.unique()
hod_unique_order = np.append(hod_unique_order, [22, 23])
hod_unique_order.sort()

orders.date = orders.date.astype('datetime64')
date_unique_order = orders.date.unique()
date_unique_order.sort()

#%%

df_order = pd.DataFrame(index=date_unique_order, columns=hod_unique_order)
df_order = df_order.fillna(0)

#%%


for hour in orders.itertuples(index=False):
    date_index = hour[0]
    hour_index = hour[1]
    fulfillment_count = hour[2]
    df_order.at[date_index, hour_index] = fulfillment_count
    
#%%
    
df_order.reset_index(inplace=True)
df_order.rename(columns={'index':'date'}, inplace=True)

#%%
      
fig1 = plt.figure(1, figsize=(30,20))
ax2 = fig1.add_subplot(7,2,2)
ax4 = fig1.add_subplot(7,2,4)
ax6 = fig1.add_subplot(7,2,6)
ax8 = fig1.add_subplot(7,2,8)
ax10 = fig1.add_subplot(7,2,10)
ax12 = fig1.add_subplot(7,2,12)
ax14 = fig1.add_subplot(7,2,14)

x_order = list(df_order)
orders_plot(ax2, 0, 7, x_order)
orders_plot(ax4, 7, 14, x_order)
orders_plot(ax6, 14, 21, x_order)
orders_plot(ax8, 21, 28, x_order)
orders_plot(ax10, 28, 35, x_order)
orders_plot(ax12, 35, 42, x_order)
orders_plot(ax14, 42, 49, x_order)

ax1 = fig1.add_subplot(7,2,1)
ax3 = fig1.add_subplot(7,2,3)
ax5 = fig1.add_subplot(7,2,5)
ax7 = fig1.add_subplot(7,2,7)
ax9 = fig1.add_subplot(7,2,9)
ax11 = fig1.add_subplot(7,2,11)
ax13 = fig1.add_subplot(7,2,13)

x_shift = list(df_shift)
shifts_plot(ax1, 0, 7, x_shift)
shifts_plot(ax3, 7, 14, x_shift)
shifts_plot(ax5, 14, 21, x_shift)
shifts_plot(ax7, 21, 28, x_shift)
shifts_plot(ax9, 28, 35, x_shift)
shifts_plot(ax11, 35, 42, x_shift)
shifts_plot(ax13, 42, 49, x_shift)

ax1.set_title('Shoppers', pad=10.0)
ax2.set_title('Orders',  pad=10.0)
ax7.set_ylabel('People on Shift')
ax13.set_xlabel('Hour of Day')
ax14.set_ylabel('Hour of Day')

plt.subplots_adjust(top=0.964,
                    bottom=0.061,
                    left=0.032,
                    right=0.96,
                    hspace=1.0,
                    wspace=0.149)
plt.show()

#%%

fig2 = plt.figure(2, figsize=(30,20))

monday_shift_ax = fig2.add_subplot(7,2,1)
tuesday_shift_ax = fig2.add_subplot(7,2,3)
wednesday_shift_ax = fig2.add_subplot(7,2,5)
thursday_shift_ax = fig2.add_subplot(7,2,7)
friday_shift_ax = fig2.add_subplot(7,2,9)
saturday_shift_ax = fig2.add_subplot(7,2,11)
sunday_shift_ax = fig2.add_subplot(7,2,13)

shifts_plot(monday_shift_ax, 0, 49, x_shift, 7)
shifts_plot(tuesday_shift_ax, 1, 49, x_shift, 7)
shifts_plot(wednesday_shift_ax, 2, 49, x_shift, 7)
shifts_plot(thursday_shift_ax, 3, 49, x_shift, 7)
shifts_plot(friday_shift_ax, 4, 49, x_shift, 7)
shifts_plot(saturday_shift_ax, 5, 49, x_shift, 7)
shifts_plot(sunday_shift_ax, 6, 49, x_shift, 7)

monday_order_ax = fig2.add_subplot(7,2,2)
tuesday_order_ax = fig2.add_subplot(7,2,4)
wednesday_order_ax = fig2.add_subplot(7,2,6)
thursday_order_ax = fig2.add_subplot(7,2,8)
friday_order_ax = fig2.add_subplot(7,2,10)
saturday_order_ax = fig2.add_subplot(7,2,12)
sunday_order_ax = fig2.add_subplot(7,2,14)

orders_plot(monday_order_ax, 0, 49, x_order, 7)
orders_plot(tuesday_order_ax, 1, 49, x_order, 7)
orders_plot(wednesday_order_ax, 2, 49, x_order, 7)
orders_plot(thursday_order_ax, 3, 49, x_order, 7)
orders_plot(friday_order_ax, 4, 49, x_order, 7)
orders_plot(saturday_order_ax, 5, 49, x_order, 7)
orders_plot(sunday_order_ax, 6, 49, x_order, 7)

plt.subplots_adjust(top=0.964,
                    bottom=0.061,
                    left=0.032,
                    right=0.99,
                    hspace=0.802,
                    wspace=0.051)

sunday_order_ax.set_xlabel('Hour of Day')
sunday_shift_ax.set_xlabel('Hour of Day')
monday_order_ax.set_title('Order', pad=10.0)
monday_shift_ax.set_title('Shift', pad=10.0)

monday_shift_ax.set_ylabel('Monday')
tuesday_shift_ax.set_ylabel('Tuesday')
wednesday_shift_ax.set_ylabel('Wednesday')
thursday_shift_ax.set_ylabel('Thursday')
friday_shift_ax.set_ylabel('Friday')
saturday_shift_ax.set_ylabel('Saturday')
sunday_shift_ax.set_ylabel('Sunday')


plt.show()
#%%

df_order.to_csv(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Visualizations/df_order.csv',
                header=True,
                index=False)
df_shift.to_csv(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/Visualizations/df_shift.csv',
                header=True,
                index=False)

#%%

x_values = list(df_order.iloc[:,1:15])
order_avg = df_order.mean(axis=0)

fig3 = plt.figure(3, figsize=(30,20))
plt.plot(x_values,
         order_avg,
         linewidth=5,
         marker='x',
         markersize=5,
         color='k')
plt.xticks(range(8,23))
plt.grid()
plt.show()