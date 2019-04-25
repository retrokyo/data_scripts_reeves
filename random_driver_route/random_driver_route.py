import pandas as pd
import random
import folium as fm
import folium.plugins
import numpy as np
from collections import namedtuple

def set_points(bee_df):
    '''
    Create the path that the driver is assumed to take based on drop off time
    
    Parameters
    bee_df: DataFrame object
    
    Return 
    list of lists containg the start and end points
    '''
    
    store_start = bee_df.iloc[0, 4]
    point_array = [
            [bee_df.store_address[0], bee_df.drop_address[0]]
            ] 
    
    for i in range(1, len(bee_df.store_address)):
        if bee_df.group[i] != bee_df.group[i-1]:
            store_start = bee_df.store_name[i]

        if (bee_df.store_name[i] == (store_start) == True) & (bee_df.group[i] == bee_df.group[i-1]):
            point_array.append([bee_df.drop_address[i-1], bee_df.drop_address[i]])

        elif (bee_df.store_name[i] == (store_start) == False) & (bee_df.group[i] == bee_df.group[i-1]):
            point_array.append([bee_df.drop_address[i-1], bee_df.store_address[i]])
            point_array.append([bee_df.store_address[i], bee_df.drop_address[i]])

        else:
            point_array.append([bee_df.drop_address[i-1], bee_df.store_address[i]])
            point_array.append([bee_df.store_address[i], bee_df.drop_address[i]])

    return point_array

def get_arrow(locations, color='black', size=6, n_arrows=5):
    '''
    Get a list of correctly places and rotated arrows/markers to be plotted
    
    Parameters
    locations: list of ists of lat longs that represent the start and end of
                the line. eg [[35.61, 139.62], [35.63, 139.63]]
                
    arrow_color: default is 'black'
    size: default is 6
    n_arrows: number of arrows to create default is 5
    
    Return
    list of arrows/markers
    
    Reference/Credit: https://medium.com/@bobhaffner/folium-lines-with-arrows-25a0fe88e4e
    '''
    arrow_map= fm.Map(location=[35.6895, 139.6917])
    Point = namedtuple('Point', field_names=['lat', 'long'])

    p1 = Point(locations[0][0], locations[0][1])
    p2 = Point(locations[1][0], locations[1][1])

    rotation = get_bearing(p1, p2) - 90.0
    arrow_lats = np.linspace(p1.lat, p2.lat, n_arrows + 2)
    arrow_longs = np.linspace(p1.long, p2.long, n_arrows + 2)

    arrows = []
    for point in zip(arrow_lats, arrow_longs):
        arrows.append(fm.RegularPolygonMarker(location=point,
                                            fill_color=color,
                                            number_of_sides=3,
                                            radius=size,
                                            rotation=rotation).add_to(arrow_map))
    return arrows

def get_bearing(p1, p2):
    '''
    Returns compass bearing from p1 to p2
    
    Parameters
    p1: namestuple with lat long
    p2: namestuple with lat long
    
    Return
    Compass bearing of type float
    
    Reference/Credit: https://medium.com/@bobhaffner/folium-lines-with-arrows-25a0fe88e4e
    Reference Based on https://gist.github.com/jeromer/2005586
    '''
    long_diff = np.radians(p2.long - p1.long)

    lat1= np.radians(p1.lat)
    lat2 = np.radians(p2.lat)

    x = np.sin(long_diff) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) *
                                        np.cos(long_diff))

    bearing = np.degrees(np.arctan2(x, y))

    if bearing < 0:
        return bearing + 360

    else:
        return bearing

def organize_df(bee_df):
    '''
    Organize the DataFrame in the required manor
    
    Parameters
    bee_df: Pandas DateFrame object
    
    Return
    Pandas DataFrame object that is correctly adjusted
    '''
    bee_df.rename(columns={'Deliverers Name': 'bee_name',
                            'Fulfillments Operation Local Deliverer Ends Date': 'ends_date',
                            'Fulfillments Operation Local Deliverer Completes Pick Up Time of Day': 'pickup_tod',
                            'Fulfillments Operation Local Deliverer Ends Time of Day': 'ends_tod',
                            'Stores Name': 'store_name',
                            'Store Addresses Address Location': 'store_address',
                            'Shipping Address Address Location': 'drop_address'},
                            inplace=True)

    bee_df.dropna(inplace=True)

    bee_df.pickup_tod = pd.to_datetime(bee_df.pickup_tod)
    bee_df.ends_tod = pd.to_datetime(bee_df.ends_tod)

    bee_df.sort_values(['bee_name', 'pickup_tod'],
                        ascending=[True, True],
                        inplace=True)

    bee_df.reset_index(drop=True, inplace=True)
    return bee_df

def group_orders(bee_df):
    '''
    Group order based on 15 min buckets determined by pickup time
    
    Parameters
    Pandas DataFrame object
    
    Return
    Pandas DataFrame object
    '''
    grouping = 1

    grouping_array = [grouping]
    for i in range(1, len(bee_df.pickup_tod)):

        if bee_df.bee_name[i] == bee_df.bee_name[i-1]:
            if abs((bee_df.pickup_tod[i]-bee_df.pickup_tod[i-1]).total_seconds())/60 < 15:
                grouping_array.append(grouping)

            else:
                grouping += 1
                grouping_array.append(grouping)

        else:
            grouping += 1
            grouping_array.append(grouping)
    
    print(len(grouping_array))
    bee_df = bee_df.assign(group = grouping_array)
    return bee_df

def group_store_names(bee_df, store_name_df):
    '''
    Change the store name to a standarized version of what the store is grouped under
    
    Parameters
    bee_df: DataFrame object
    store_name_df: DataFrame object for mapping store names
    
    Return
    Pandas DataFrame object
    '''
    
    store_name_df.grouped_name = store_name_df.grouped_name.str.strip()
    store_index_dict = store_name_df.set_index('store_name')
    store_name_dict = store_index_dict.grouped_name.to_dict()
    
    bee_df.store_name.str.strip()
    store_name_df.grouped_name.str.strip()
    
    #bee_df = bee_df.assign(grouped_name = bee_df.store_name.map(store_name_dict))
    bee_df = bee_df.replace(store_name_dict)
    #bee_df.loc[bee_df.grouped_name.isnull(), 'grouped_name'] = bee_df.store_name
    
    return bee_df
    
def draw_random_map(bee_df, store_name_df):
    '''
    Draws the pathing a a random person within the dataset
    
    Parameters
    bee_df: Pandas DataFrame objects
    '''
    
    df_organized = organize_df(bee_df)
    df_organized = group_store_names(bee_df, store_name_df)
    random_bee = bee_df.loc[random.randint(0, len(df_organized)),
                            ['bee_name', 'ends_date']].tolist()
    
    bee_jobs = bee_df.loc[(bee_df.bee_name == random_bee[0]) & 
                          (bee_df.ends_date == random_bee[1])]
    
    bee_jobs_organized = organize_df(bee_jobs)
    bee_jobs_organized_grouped = group_orders(bee_jobs_organized)
    
    bee_jobs_organized_grouped.sort_values(by=['ends_tod'], inplace=True)
    bee_jobs_organized_grouped.reset_index(drop=True, inplace=True)
    
    
    bee_points = set_points(bee_jobs_organized_grouped)

    tokyo_coords = [35.6895, 139.6917]
    bee_map = fm.Map(location=tokyo_coords, zoom_start=10, tiles='CartoDB Positron')

    arrow_array = []
    arrow_between = []
    
    clusters = fm.plugins.MarkerCluster()

    i = 0
    end = 0.0
    for path in bee_points:
        
        start = list(map(float, path[0].split(',')))
        
        if (i > 0) & (start == end):
            end = list(map(float, path[1].split(',')))
            
            fm.Marker(location=end,
                      popup=str(i),
                      icon=fm.Icon(icon='android',
                                   color='yellow',
                                   prefix='fa')).add_to(clusters)
            
            fm.PolyLine(locations=[start, end]).add_to(bee_map)
            
            arrow_array.append(get_arrow([start, end], color='green', n_arrows = 4))
            
        else:
            end = list(map(float, path[1].split(',')))
            
            fm.Marker(location=start, popup=str(i),
                      icon=fm.Icon(icon='android',
                                   color='green',
                                   prefix='fa')).add_to(clusters)
            
            fm.Marker(location=end, popup=str(i),
                      icon=fm.Icon(icon='android',
                                   color='green',
                                   prefix='fa')).add_to(clusters)
            
            fm.PolyLine(locations=[start, end]).add_to(bee_map)
            arrow_array.append(get_arrow([start, end], color='green', n_arrows = 4))
            
        i += 1

    for i in range(len(arrow_array)):
        for arrow in arrow_array[i]:
            arrow.add_to(bee_map)

    for i in range(len(arrow_between)):
        for arrow in arrow_between[i]:
            arrow.add_to(bee_map)
            
    bee_map.add_child(clusters)
    fm.LayerControl().add_to(bee_map)
    bee_jobs_organized_grouped.to_excel(r'C:/Users/reeves/Downloads/test_run_output.xlsx')
    bee_map.save(r'C:/Users/reeves/Downloads/test_run.html')


