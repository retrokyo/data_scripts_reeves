# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:12:37 2019

@author: froni
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
#%%

cap_bh = pd.read_csv(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/AeonOzeki/exportA.csv')
cap_ah = pd.read_csv(r'C:/Users/froni/Desktop/honestbee/Operational/Script Files/AeonOzeki/exportB.csv')

capacity = pd.concat([cap_bh, cap_ah])
capacity.sort_values(by='date', inplace=True)
capacity.reset_index(inplace=True, drop=True)

#%%

aeon = capacity.loc[capacity.store == 'Aeon']
ozeki = capacity.loc[capacity.store == 'Ozeki']
#%%
cap_hod = list(capacity)
for i in range(3):
    del cap_hod[0]

#%%
aeon_values = aeon.loc[:,cap_hod].apply(pd.value_counts)
ozeki_values = ozeki.loc[:, cap_hod].apply(pd.value_counts)

aeon_hod = list(aeon_values)
ozeki_hod = list(ozeki_values)

aeon_values_t = aeon_values.transpose()
ozeki_values_t = ozeki_values.transpose()

#%%
aeon_values_t.fillna(value=0, inplace=True)
ozeki_values_t.fillna(value=0, inplace=True)

#%%
aeon_store = ['Aeon'] * len(aeon_values_t)
ozeki_store = ['Ozeki'] * len(ozeki_values_t)

#%%

aeon_values_adj = aeon_values_t.assign(store = aeon_store, hod = aeon_hod)
ozeki_values_adj = ozeki_values_t.assign(store = ozeki_store, hod = aeon_hod)

#%%

aeon_ozeki = pd.concat([aeon_values_adj, ozeki_values_adj])
aeon_ozeki.reset_index(inplace=True, drop=True)

#%%

aeon_ozeki_t = aeon_ozeki.transpose()

#%%

sns.barplot()