import folium as fm

from node_class import *


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
    
    travel_path = [node_list[0]]
    node_list.pop(0)
    
    for node in node_list:
        
        node.calculate_node_info(travel_path[0])

        fm.Marker(location=[node.lat, node.long],
                    tooltip=fm.Tooltip(text=node.retrieve_node_info()),
                    icon=fm.Icon(color='blue', icon='angle-down', prefix='fa')).add_to(node_map)
        


    if save == True:
        node_map.save(r'C:/Users/reeves/Desktop/route_test.html')

    return node_map

def node_path_calc(node_list):
    node_path = []

    for node in node_list:
        node.calculate_node_info[node_list[0]]

    node_path.append(node_list[0])
    node_list.pop[0]
    
    for node in node_list:
        pass

def sort_nodes(node_list):
    pass