# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 14:49:31 2021

@author: Emile.deBadts
"""

import os

from osgeo import gdal, ogr
import networkx as nx
import json

from constants import *
from colebrook_white import ColebrookWhite

# Timestep of design rain is 5 minutes
DESIGN_RAIN_TIMESTEP = 300
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
        # Log in the table instance which surfaces have already been coupled to a pipe
        self.connected_surfaces = []

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
        """
        get the connected surface area for a pipe id
         determine all connected upstream pipes as well
        """

        pipe_type_codes = self._table['pipe_code_' + pipe_type]

        surface_areas = []
        for i, code in enumerate(pipe_type_codes):
            if code == pipe_id:
                bgt_identificatie = self._table['bgt_identificatie'][i]

                if bgt_identificatie not in self.connected_surfaces:
                    surface_area_bgt = self._table['surface_area'][i]
                    surface_fraction = self._table[pipe_type][i] / 100
                    connected_area = surface_area_bgt * surface_fraction

                    surface_areas.append(connected_area)
                    self.connected_surfaces.append(bgt_identificatie)

        surface_sum = sum(surface_areas)

        return surface_sum


class Pipe:

    def __init__(self, feature):

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

    def get_intermediates(p1,p2,nb_points):
        x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
        y_spacing = (p2[1] - p1[1]) / (nb_points + 1)

        return [[p1[0] + i * x_spacing, p1[1] +  i * y_spacing]
                for i in range(1, nb_points+1)]

    def calculate_elevation(self, elevation_rasterband, gt):
        dem_no_data_value =  elevation_rasterband.GetNoDataValue()

        pipe_source_coordinates = self.start_coordinate
        pipe_target_coordinates = self.end_coordinate

        p_source_x = int((pipe_source_coordinates[0] - gt[0]) / gt[1]) #x pixel
        p_source_y = int((pipe_source_coordinates[1] - gt[3]) / gt[5]) #y pixel
        p_target_x = int((pipe_target_coordinates[0] - gt[0]) / gt[1]) #x pixel
        p_target_y = int((pipe_target_coordinates[1] - gt[3]) / gt[5]) #y pixel

        # sample dem for intermediate points
        self.points=[];self.nb_points=100
        self.points.append([p_source_x,p_source_y])
        for point in get_intermediates([p_source_x,p_source_y],[p_target_x,p_target_y],self.nb_points):
            self.points.append(point)
        self.points.append([p_target_x,p_target_y])

        self.dem_elevation=[]
        for point in self.points:
            elevation=dem_rb.ReadAsArray(point[0],point[1],1,1)[0][0]
            if elevation == dem_no_data_value:
                elevation = None
            self.dem_elevation.append(elevation)

    def calculate_discharge(self, design_rain):

        #TODO tijdstap omrekeken
        #TODO netwerkanalyse discharge

        if design_rain in AREA_WIDE_RAIN.keys():
            design_rain_pattern = AREA_WIDE_RAIN[design_rain]
        else:
            raise KeyError('Selected design rain not availabe')

        max_intensity = max(design_rain_pattern)
        pipe_discharge = self.connected_surface_area * ((max_intensity / 1000) / DESIGN_RAIN_TIMESTEP)
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

        thickness = 0.1 #voorbeeld wanddikte (should be based on material, which should be based on diameter)

        pipe_elevation=[]
        pipe_elevation.append(self.start_level)
        for elevation in get_intermediates([self.start_level,self.start_level],[self.end_level,self.end_level],self.nb_points):
            pipe_elevation.append(elevation[0])
        pipe_elevation.append(self.end_level)

        cover_depths=[]
        for i in range(len(self.points)):
            cover_depths.append(self.dem_elevation[i]-(self.pipe_elevation[i]+self.diameter+thickness))

        # minimale cover depth
        self.cover_depth=min(cover_depths)


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
        self.sewerage_type = None
        self.pipes = {}

    def add_pipe(self, pipe : Pipe):

        # Add pipe to the networkx DiGraph
        # Also save pipes to dictionary
        self.pipes[pipe.id] = pipe

        if pipe.start_coordinate not in self.network.nodes:
            self.network.add_node(pipe.start_coordinate, type='manhole')

        if pipe.end_coordinate not in self.network.nodes:
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

        #TODO opgeven minimale waking
        #TODO waking over gehele trace berekenen
        #TODO aanpassen hydraulische gradient op basis van evaluatie
        distance_matrix = dict(nx.all_pairs_dijkstra(self.reverse_network, weight='length'))

        # Get the distance dictionary for the end node
        distance_dictionary = distance_matrix[outlet_node][0]
        furthest_node, distance = list(distance_dictionary.items())[-1]
        furthest_edge = self.network.edges(furthest_node, data=True)
        furthest_pipe = self.get_pipe_with_edge(furthest_edge)

        max_hydraulic_gradient = furthest_pipe.start_elevation / distance

        for pipe in self.pipes:
            setattr(self.pipes[pipe], 'max_hydraulic_gradient',  max_hydraulic_gradient)

    def determine_connected_surface_area_totals(self, bgt_inlooptabel : BGTInloopTabel):

        pipe_connected_surface = {}
        for pipe_id, pipe in self.pipes.items():
            connected_surface_area = bgt_inlooptabel.get_surface_area_for_pipe_id(pipe_id = str(pipe.id), pipe_type = self.sewerage_type)
            pipe_connected_surface[pipe.id] = connected_surface_area

        for edge in self.network.edges(data=True):
            pipe = self.get_pipe_with_edge(edge)

            if getattr(pipe, 'connected_surface_area') is None:
                start_node = edge[0]
                upstream_nodes = [n for n in nx.traversal.bfs_tree(self.network, start_node , reverse=True) if n != start_node]
                upstream_pipes = set()
                upstream_pipes.add(pipe.id)
                for i, node in enumerate(upstream_nodes):
                    if i == len(upstream_nodes) - 1:
                        break
                    upstream_edge = (node, upstream_nodes[i+1])
                    upstream_pipe = self.get_pipe_with_edge(upstream_edge)
                    upstream_pipes.add(upstream_pipe.id)

                pipe_total_connected_surface = sum([pipe_connected_surface[pipe_id] for pipe_id in upstream_pipes])
                setattr(pipe, 'connected_surface_area', pipe_total_connected_surface)

    def add_id_to_nodes(self):
        for i, node in enumerate(self.network.nodes):
            self.network.nodes[node]['id'] = i

    def get_pipe_with_edge(self, edge):
        edge_data = list(edge)[0][2]
        edge_id = edge_data['id']
        pipe = self.pipes[edge_id]
        return pipe

    def validate_network(self):
        #TODO Check for outlets connection, all pipes connected, at least one outlet
        pass

    def generate_output_layer(self):
        pass

    @property
    def reverse_network(self):
        return self.network.reverse()


class ITPipeNetwork(PipeNetwork):

    def __init__(self):
        self.network_type = 'infiltratieriool'

    def add_weir(weir: Weir):
        pass

    def calculate_required_cover_depth(self, minimum_cover_depth):
        # For IT network the gradient of the pipes is 0, find the highest possible solution
        pass

    def estimate_internal_weir_locations(self):
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
