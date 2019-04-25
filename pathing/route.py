import numpy as np
import pandas as pd
import csv
import folium as fm
import node_calculation as nc

from node_class import node
from node_class import drop_node


# test_set_path = input('Data File Path: ')
# df = pd.read_csv(r'{0}'.format(test_set_path))
df = pd.read_csv(r'C:\Users\reeves\Downloads\test_set_route.csv')

df.rename(columns={'Shipping Address Address Location': 'destination',
                    'Fulfillments Operation Local Deliverer Ends Time of Day': 'end_tod',
                    'Line Items Fulfilled Quantity Sum': 'item_count'},
                    inplace=True)

with open(r'C:\Users\reeves\Downloads\test_store_route.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader)
    for row in csvreader:
        store_node = node(float(row[0].split(',')[0]),
                        float(row[0].split(',')[1]),
                        4)
csvfile.close()

node_obj_list = [store_node]

for row in df.itertuples(index=False, name=None):
    lat, long = row[0].split(',')
    node_obj = drop_node(lat, long, row[2], 4)
    node_obj_list.append(node_obj)

nc.node_map(node_obj_list, save=True)
# for node in node_obj_list:
#     print(node.retrieve_node_info())
# print(df.head())
# print(node_obj_list)

############ IMPORT TESTING #################
# na_01 = node(35.6342826, 139.7046757, 5, 4)
# na_02 = node(35.6491323, 139.7394593, 16, 4)

# na_02.calculate_node_info(na_01)
# na_02.retrieve_node_info()
#############################################