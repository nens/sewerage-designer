# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 14:49:31 2021

@author: Emile.deBadts
"""

import ogr
import networkx as nx
import json

class InvalidGeometryException:
    pass

class Weir(ogr.Feature):
    
    # Line geometry
    def __init__(self):
        self.height = None
    
class Outlet(ogr.Feature):

    # Line geometry
    def __init__(self, ditch_level):
        super().__init__(feature_def = feature.GetDefnRef())
        self.ditch_level = ditch_level
    
class PumpingStation(ogr.Feature):

    # Outlets are also line geometry
    def __init__(self):
        self.end_level = None

class Pipe:

    def __init__(self, feature):
        
        #TODO If feature is not a linestring with two points raise error
        
        # Export properties to json
        property_json = json.loads(feature.ExportToJson())['properties']
        self.feature = feature
        self.id = property_json['id']
        self.diameter = None
        self.start_level = None
        self.end_level = None
        self.start_elevation = None
        self.end_elevation = None 
        self.material = None
        self.uuid = None
        self.sewerage_type = None
        self.max_hydraulic_gradient = None
        
    def calculate_diameter():
        # Colebrook white function
        pass
    
    def calculate_elevation(self, dem_path):
        pass
    
    def calculate_capacity(self):        
        pass
    
    def calculate_cover_depth(self):
        pass
        
    @property
    def geometry(self):
        return self.feature.GetGeometryRef()
    
    @property
    def points(self):
        return self.geometry.GetPoints()
    
    @property
    def start_coordinate(self):
        return self.points[0]
        
    @property
    def end_coordinate(self):
        return self.points[1]
    
class PipeNetwork:
    
    def __init__(self):
        self.network = nx.DiGraph()
        self.pipes = []
    
    def add_pipe(self, pipe : Pipe):

        # Add pipe to network
        self.pipes += pipe
        self.network.add_node(pipe.start_coordinate)
        self.network.add_node(pipe.end_coordinate)
        self.network.add_edge(pipe.start_coordinate, 
                              pipe.end_coordinate, 
                              id = pipe.id,
                              length = pipe.geometry.Length())


    def add_outlet(self, outlet : Outlet):
        
        # As the outlets are defined as point geometries, assign the property of the outlet to the already existing node
        # Outlet is defined as a point geometry
        self.add_edge()
        self.add_node()

    def add_weir(self, weir : Weir):
        
        
        # Add an edge using start and end coordinate 
        self.add_edge()
        self.add_node()        
    
    def calculate_max_hydraulic_gradient(self):
            
        """"
         Calculates the max hydraulic gradient based on the network end point and start/end elevation
         The max hydraulic gradient is defined as the maximum difference in elevation between the endpoint of the network 
         and the furthest node divided by the distance between the two
         Assign this back to all the pipes in the network
        """

        self.reverse_network = self.network.reverse()
        distance_matrix = dict(nx.all_pairs_dijkstra(self.reverse_network, weight='length'))
        
        for node in self.network.nodes:
            node_id = self.network.nodes[node]['id']
            distance_dictionary = distance_matrix[node][0]
            max_distance = list(distance_dictionary.items())[-1][1]   
         
        # Calculate 
        max_hydraulic_gradient = 
            
        for pipe in self.pipes:
            setattr(pipe, 'max_hydraulic_gradient',  max_hydraulic_gradient)
            
        
    
    def validate_network(self):
        # Check for outlets connection, all pipes connected, at least one outlet
        pass
    
    def generate_output_layer(self):
        pass
    
        
class ITPipeNetwork(PipeNetwork):
    
    def __init__(self):
        pass

    def add_weir(weir: Weir):
        pass
    
    def calculate_required_cover_depth(self, minimum_cover_depth):
        # For IT network the gradient of the pipes is 0, find the highest possible solution
        pass
    
    def estimate_stuwput_locations(self, dem_path):
        # For a given network and elevation model, determine the best locations to install weirs
        # If there are already weirs in the network, raise error
        pass
        

class MixedPipeNetwork(PipeNetwork):
    
    def __init__(self):
        pass    
    
    def calculate_required_cover_depth(self):
        pass
    
class SewerageDesignSettings:
    
    def __init__(self):
        pass
    
    def to_file(self):
        pass
    
    def from_file(self):
        pass
    
if __name__ == '__main__':
    
    # Generate a pipe network from a tracing
    # Tracing will be geopackage containing the following layers: pipes, outlets, weirs, pumpstations
    # Settings from QGIS gui will be :
        # Sewerage type (IT)
        # BGT Inlooptabel from a ogr datasource
        
        
    test_tracing = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\zundert_test_tracing.gpkg'
    test_tracing_ds = ogr.Open(test_tracing)
    
    # Get pipes 
    test_tracing_layer = test_tracing_ds[0]

    # Get outlets
    
    # Get weirs
    
    # Get pumping stations

    # Define a new pipe network
    it_sewerage = PipeNetwork()
    
    for feature in test_tracing_layer:
        # New pipe class
        #TODO Check for valid geometries?
        pipe = Pipe(feature)
        
        # Add pipe to network
        it_sewerage.add_pipe(pipe)        
        it_sewerage.calculate_max_hydraulic_gradient()
        
    reverse = it_sewerage.network.reverse()
    distance_matrix = dict(nx.all_pairs_dijkstra(reverse, weight='length'))

    for node in it_sewerage.network.nodes:
        node_id = it_sewerage.network.nodes[node]['id']
        distance_dictionary = distance_matrix[node][0]
        max_distance = list(distance_dictionary.items())[-1][1]   


     
    