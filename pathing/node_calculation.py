import folium as fm
from random import randrange

from node_class import *

'''
Collection of functions to calculate the node pathing

TO-DO: Figure out how I want to remove nodes that have been pathed from the node_list
'''
def node_map(node_list, city='tokyo', save=False):
    '''
    Create a map from a collection of node, and drop_node objects.\n

    Parameters:\n
        node_list: List of node / drop_node objects\n
        city: String code for the city where the map starts (Current options below)\n
            city-options: {'tokyo': tokyo}\n
        save: Boolean value that determines whether the map is saved to an html file - Default is False\n

    Return\n
        Folium map object
    '''
    
    city_coord_dict = {'tokyo': [35.6762, 139.6503],}
    node_map = fm.Map(location=city_coord_dict[city],
                                tiles='CartoDB Positron')

    fm.Marker(location=[node_list[0].lat, node_list[0].long],
                        tooltip=fm.Tooltip(text=node_list[0].retrieve_node_info()),
                        icon=fm.Icon(color='green', icon='angle-up', prefix='fa')).add_to(node_map)
    
    
    for node in node_list[1:]:
        
        node.calculate_node_info(travel_path[0])

        fm.Marker(location=[node.lat, node.long],
                    tooltip=fm.Tooltip(text=node.retrieve_node_info()),
                    icon=fm.Icon(color='blue', icon='angle-down', prefix='fa')).add_to(node_map)
        


    if save == True:
        node_map.save(r'C:/Users/reeves/Desktop/route_test.html')

    return node_map

def node_path_calc(node_list, item_limit=100, time_limit=60):
    '''
    Calculates a node path based on first best option\n

    Parameters:\n
    node_list: List containing node type objects. First object in list should be of object node

    Return:

    '''
    node_list_copy = node_list[:]
    node_path = [node_list_copy[0]]

    while (node_path_item_sum(node_path) < item_limit & node_path_time_sum(node_path) < time_limit & node_list_copy):
        node_path.append(next_best_node(node_list_copy))
        node_list_copy.pop(0)

    return node_path

def next_best_node(node_list):
    for node in node_list[1:]:
        node.calculate_node_info(node_list[0])

    sort_nodes(node_list, 1)

    return node_list[1]


def sort_nodes(node_list, start=0, end=len(node_list)-1):
    '''
    Sort node objects using quicksort method, inplace\n

    Parameters:\n
    node_list: list containing node objects\n
    start: start index\n
    end: end index\n

    Return\n
    List of node objects sorted on the '__distance_to' property
    '''
    if start >= end:
        return
    
    pivot_idx = randrange(start, end, 1)
    pivot_node = node_list[pivot_idx]._get_distance_to

    node_list[end], node_list[pivot_idx] = node_list[pivot_idx], node_list[end]

    lt_pointer = start

    for i in range(start, end):

        if node_list[i]._get_distance_to < pivot_node:
            node_list[i], node_list[lt_pointer] = node_list[lt_pointer], node_list[i]
            lt_pointer += 1

    node_list[end], node_list[lt_pointer] = node_list[lt_pointer], node_list[end]

    sort_nodes(node_list, start, lt_pointer-1)
    sort_nodes(node_list, lt_pointer+1, end)

def node_path_item_sum(node_path):
    '''
    Calculates the node path's item count sum\n

    Parameters:\n
    node_path: list of node object\n

    Return:\n
    The sum of the nodes' item count in the current path
    '''
    item_count_sum = 0
    for node in node_path:
        item_count_sum += node.item_count

    return item_count_sum

def node_path_time_sum(node_path):
    '''
    Calculates the node path's time sum\n

    Parameters:\n
    node_path: list of node objects\n

    Return:\n
        The sum of the nodes' time in the current path
    '''
    time_sum = 0.0
    for node in node_path:
        time_sum += node._get_time_to

    return time_sum