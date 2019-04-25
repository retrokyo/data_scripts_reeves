import numpy as np

class node:

    __distance_to = 0.0
    __time_to = 0.0

    def __init__(self, lat, long, distance_scalar):
        self.lat = float(lat)
        self.long = float(long)
        self.distance_scalar = float(distance_scalar)

    def euclidian_distance(self, from_node):
        '''
        Calculate the Euclidean Distance to the node from another node\n
        Parameters:\n
            from_node: node object
        Return\n
        Euclidean Distance - type: Float\n
        '''
        world_km = 6371.0

        node_lat_radians = np.radians(self.lat)
        node_long_radians = np.radians(self.long)

        from_node_lat_radians = np.radians(from_node.lat)
        from_node_long_radians = np.radians(from_node.long)

        node_point = [world_km * np.cos(node_lat_radians) * np.cos(node_long_radians),
            world_km * np.cos(node_lat_radians) * np.sin(node_long_radians),
            world_km * np.sin(node_lat_radians)]

        from_node_point = [world_km * np.cos(from_node_lat_radians) * np.cos(from_node_long_radians),
                        world_km * np.cos(from_node_lat_radians) * np.sin(from_node_long_radians),
                        world_km * np.sin(from_node_lat_radians)]

        distance_sq = (((node_point[0] - from_node_point[0]) ** 2) + 
                        ((node_point[1] - from_node_point[1]) ** 2) +
                        ((node_point[2] - from_node_point[2]) ** 2))

        distance = np.sqrt(distance_sq)

        return distance

    def _set_time_to(self, distance, distance_scalar):
        '''
        Sets the time_to variable of the object to ('distance' * 'distance_scalar')\n

        Parameters:\n
            distance - type: float\n
            distance_scalar - type: float\n
        '''
        self.__time_to = distance * distance_scalar

    def _set_distance_to(self, from_node):
        '''
        Sets the distance_to variable of the object by calling on the '__euclidean_distance' function\n
        MUST BE SET BEFORE '__time_to' VARIABLE\n
        Parameters:\n
            from_node: Node object\n
        '''
        self.__distance_to = self.euclidian_distance(from_node)

    def calculate_node_info(self, from_node):
        self._set_distance_to(from_node)
        self._set_time_to(self.__distance_to, self.distance_scalar)

    def _get_time_to(self):
        '''
        Retrieve '__time_to' variable
        '''
        return self.__time_to

    def _get_distance_to(self):
        '''
        Retrieve '__distance_to' variable
        '''
        return self.__distance_to

    def retrieve_node_info(self):
        '''
        Gives the infromation of the node in a string formated for HTML use 
        '''
        node_info = '''
        Node Location: {:00.4f}, {:00.4f}<br>
        Node Distance To: {:00.2f}<br>
        Node Time To: {:00.2f}<br>
        Node Distance Scalar: {:00.0f}<br>
        '''.format(self.lat, self.long,
                    self._get_distance_to(), self._get_time_to(),
                    self.distance_scalar)

        return node_info

class drop_node(node):

    def __init__(self, lat, long, item_count, distance_scalar):
        self.lat = float(lat)
        self.long = float(long)
        self.item_count = float(item_count)
        self.distance_scalar = float(distance_scalar)

        super(drop_node, self).__init__(lat, long, distance_scalar)

    def retrieve_node_info(self):
        '''
        Gives the infromation of the node in a string formated for HTML use 
        '''
        node_info = '''
        Node Location: {:00.4f}, {:00.4f}<br>
        Node Item Count: {:00.0f}<br>
        Node Distance To: {:00.2f}<br>
        Node Time To: {:00.2f}<br>
        Node Distance Scalar: {:00.0f}<br>
        '''.format(self.lat, self.long, self.item_count,
                    super(drop_node, self)._get_distance_to(),
                    super(drop_node, self)._get_time_to(),
                    self.distance_scalar)

        return node_info