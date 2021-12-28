# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 14:49:31 2021

@author: Emile.deBadts
"""

import os

from osgeo import gdal, ogr
import networkx as nx
import json
import logging

from constants import *
from colebrook_white import ColebrookWhite


BGT_INLOOPTABEL_REQUIRED_FIELDS = ['bgt_identificatie', 'gemengd_riool', 'pipe_code_gemengd_riool', 'hemelwaterriool', 'pipe_code_hemelwaterriool', 'vgs_hemelwaterriool', 'pipe_code_vgs_hemelwaterriool', 'infiltratievoorziening', 'pipe_code_infiltratievoorziening']

class InvalidGeometryException:
    pass

class Weir:
    
    # Line geometry
    def __init__(self):
        self.height = None
    
class Outlet:

    def __init__(self, feature):
        property_json = json.loads(feature.ExportToJson())['properties']
        self.ditch_level = property_json['ditch_level']
        self.id = property_json['id']
        self.feature = feature

    @property
    def wkt_geometry(self):
        return self.geometry.ExportToWkt()

    @property
    def geometry(self):
        return self.feature.GetGeometryRef()

    @property
    def coordinate(self):
        return self.geometry.GetPoints()[0]        
        
        
class PumpingStation(ogr.Feature):

    # Outlets are also line geometry
    def __init__(self):
        self.end_level = None
        
class BGTInloopTabel:
    
    def __init__(self, bgt_inlooptabel_fn):
    
        tabel_abspath = os.path.abspath(bgt_inlooptabel_fn)
        if not os.path.isfile(tabel_abspath):
            raise FileNotFoundError(
                "BGT Inloop tabel niet gevonden: {}".format(tabel_abspath)
            )
        tabel_ds = ogr.Open(tabel_abspath)
        # TODO more thorough checks of validity of input geopackage
        try:
            self.layer = tabel_ds.GetLayer(0)
        except Exception:
            raise ValueError(
                "Geen geldig bestand, {}".format(
                    tabel_abspath
                )
            )
            
        self.fields = self.get_layer_fields() 
        for field in BGT_INLOOPTABEL_REQUIRED_FIELDS:
            if field not in self.fields:
                raise ValueError("Required field '{}' not in BGT inlooptabel".format(field))
            
        self.set_table()
            
    def get_layer_fields(self):
        """Sets the layers fields"""
        fields = []
        ldefn = self.layer.GetLayerDefn()
        for n in range(ldefn.GetFieldCount()):
            fdefn = ldefn.GetFieldDefn(n)
            fields.append(fdefn.name)
            
        return fields
    
    def set_table(self):
        """sets the table if not exists"""
        if not hasattr(self, "_table"):
            self.table_fields = self.fields + ["fid", 'surface_area']
            self._table = {field: [] for field in self.table_fields}

            for feature in self.layer:
                feature_items = json.loads(feature.ExportToJson())['properties']
                feature_geometry = feature.GetGeometryRef()
                for key, value in feature_items.items():
                    self._table[key].append(value)
                    self._table["fid"].append(feature.GetFID())
                    self._table['surface_area'].append(feature_geometry.GetArea())

    def get_surface_area_for_pipe_id(self, pipe_id, pipe_type):
        """get the connected surface area for a pipe id"""

        pipe_type_codes = self._table['pipe_code_' + pipe_type]
        
        surface_areas = []
        for i, code in enumerate(pipe_type_codes):
            if code == pipe_id:
                surface_area_bgt = self._table['surface_area'][i]
                surface_fraction = self._table[pipe_type][i] / 100
                connected_area = surface_area_bgt * surface_fraction
                surface_areas.append(connected_area)
        
        surface_sum = sum(surface_areas)
        
        return surface_sum
                    

class Pipe:

    def __init__(self, feature):
        
        #TODO If feature is not a linestring with two points raise error
        
        # Export properties to json and add to class properties
        property_json = json.loads(feature.ExportToJson())['properties']
        
        self.feature = feature
        self.id = property_json['id']
        self.diameter = None
        self.start_level = None
        self.end_level = None
        self.start_elevation = None
        self.end_elevation = None 
        self.material = None
        self.sewerage_type = None
        self.connected_surface_area = None
        self.surface_area_discharge = None
        self.max_hydraulic_gradient = None
        self.distance_to_outlet = None

        self.validate_feature(feature)
    
    def calculate_elevation(self, elevation_rasterband, gt):
        dem_no_data_value =  elevation_rasterband.GetNoDataValue()
                
        pipe_source_coordinates = self.start_coordinate
        pipe_target_coordinates = self.end_coordinate 
           
        p_source_x = int((pipe_source_coordinates[0] - gt[0]) / gt[1]) #x pixel
        p_source_y = int((pipe_source_coordinates[1] - gt[3]) / gt[5]) #y pixel
        p_target_x = int((pipe_target_coordinates[0] - gt[0]) / gt[1]) #x pixel
        p_target_y = int((pipe_target_coordinates[1] - gt[3]) / gt[5]) #y pixel
                    
        p_source_dem = elevation_rasterband.ReadAsArray(p_source_x,p_source_y,1,1).flat[0]
        p_target_dem = elevation_rasterband.ReadAsArray(p_target_x,p_target_y,1,1).flat[0]
        
        if p_source_dem == dem_no_data_value:
            p_source_dem = None

        if p_target_dem == dem_no_data_value:
            p_target_dem = None
        
        self.start_elevation = p_source_dem
        self.end_elevation = p_target_dem
        
    def calculate_discharge(self, design_rain):   
        
        if design_rain in AREA_WIDE_RAIN.keys():
            design_rain_pattern = AREA_WIDE_RAIN[design_rain]
        else:
            raise KeyError('Selected design rain not availabe')
            
        max_intensity = max(design_rain_pattern)
        pipe_discharge = self.connected_surface_area * (max_intensity / 1000)
        self.discharge = pipe_discharge
        
    def calculate_diameter(self):
        
        """
        Use the Colebrook White method to esimate the diameters
        """
        
        colebrook_white = ColebrookWhite(q = self.discharge, 
                                         Smax = self.max_hydraulic_gradient)
        
        estimated_diameter = colebrook_white.iterate_diameters()
        self.diameter = estimated_diameter        
    
    
    def calculate_cover_depth(self):
        pass
        
    
    def validate_feature(self, feature):        
        if len(self.points) != 2:
            raise InvalidGeometryException
        
    @property
    def geometry(self):
        return self.feature.GetGeometryRef()
    
    @property
    def wkt_geometry(self):
        return self.geometry.ExportToWkt()
    
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
        self.pipes = {}
    
    def add_pipe(self, pipe : Pipe):

        # Add pipe to the networkx DiGraph
        # Also save pipes to dictionary
        self.pipes[pipe.id] = pipe
        self.network.add_node(pipe.start_coordinate, type='manhole')
        self.network.add_node(pipe.end_coordinate, type='manhole')
        self.network.add_edge(pipe.start_coordinate, 
                              pipe.end_coordinate, 
                              id = pipe.id,
                              length = pipe.geometry.Length())

    
    def calculate_max_hydraulic_gradient(self, outlet_node):
            
        """"
         Calculates the max hydraulic gradient based on the network end point and start/end elevation
         The max hydraulic gradient is defined as the maximum difference in elevation between the endpoint of the network 
         and the furthest node divided by the distance between the two
         Assign this back to all the pipes in the network
        """

        self.reverse_network = self.network.reverse()
        distance_matrix = dict(nx.all_pairs_dijkstra(self.reverse_network, weight='length'))
                
        # Get the distance dictionary for the end node 
        distance_dictionary = distance_matrix[outlet_node][0]
        furthest_node, distance = list(distance_dictionary.items())[-1]
        furthest_edge = it_sewerage.network.edges(furthest_node, data=True)        
        furthest_pipe = self.get_pipe_with_edge(furthest_edge)
        
        max_hydraulic_gradient = furthest_pipe.start_elevation / distance
            
        for pipe in self.pipes:
            setattr(self.pipes[pipe], 'max_hydraulic_gradient',  max_hydraulic_gradient)

    def add_id_to_nodes(self):
        for i, node in enumerate(self.network.nodes):
            self.network.nodes[node]['id'] = i
                    
    def get_pipe_with_edge(self, edge):        
        edge_data = list(edge)[0][2]
        edge_id = edge_data['id']    
        pipe = self.pipes[edge_id]
        return pipe

    
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
    
class SewerageDesigner:
    
    def __init__(self):
        pass
        
    
if __name__ == '__main__':
    
    # Generate a pipe network from a tracing
    # Tracing will be geopackage containing the following layers: pipes, outlets, weirs, pumpstations
    # Settings from QGIS gui will be :
        # Sewerage type (IT)
        # BGT Inlooptabel from a ogr datasource
        
    #TODO Check network for amount of outlets
    #TODO Check tracing for correct projection
        
    test_tracing = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\zundert_test_28992.gpkg'
    dem_fn = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\Zundert.tif'
    bgt_inlooptabel = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\bgt_inlooptabel.gpkg'
    network_type = 'gemengd_riool'
    design_rain = '9'
    test_tracing_ds = ogr.Open(test_tracing)
    
    # Load BGT Inlooptabel
    bgt_inlooptabel = BGTInloopTabel(bgt_inlooptabel)
    
    # Load DEM rasterband and geotransform
    dem_ds = gdal.Open(dem_fn)
    dem_rb = dem_ds.GetRasterBand(1)
    gt = dem_ds.GetGeoTransform()

    # Get pipes 
    pipes = test_tracing_ds.GetLayer('pipe')
    outlets = test_tracing_ds.GetLayer('outlet')
    
    # Define a new pipe network
    it_sewerage = PipeNetwork()
    
    # Add some pipes
    for feature in pipes:
        pipe = Pipe(feature)
        # Determine the connected surface area using the BGT inlooptabel
        pipe.connected_surface_area = bgt_inlooptabel.get_surface_area_for_pipe_id(pipe_id = str(pipe.id), pipe_type = network_type)
        pipe.calculate_elevation(elevation_rasterband=dem_rb, gt=gt)            

        # Add the pipe to the network        
        it_sewerage.add_pipe(pipe)        


    it_sewerage.add_id_to_nodes()

    # Add some outlets
    for feature in outlets:
        outlet = Outlet(feature)
        if outlet.coordinate in it_sewerage.network.nodes(data=True):
            attr = {outlet.coordinate : {'type': 'outlet'}}
            nx.set_node_attributes(it_sewerage.network, attr)
        else:
            raise KeyError('Outlet coordinate is not a node in the network')
    
    # Get the surface area 
    
    # Calculate max hydraulic gradient possible for the network
    it_sewerage.calculate_max_hydraulic_gradient(outlet.coordinate)
    
    # Calculate the capacity for all the pipes 
    for pipe_id, pipe in it_sewerage.pipes.items():
        # Use Colebrook-White to estimate a diameter
        pipe.calculate_discharge(design_rain=design_rain)
        pipe.calculate_diameter()


    
     
    