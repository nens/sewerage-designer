# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 14:49:31 2021

@author: Emile.deBadts
"""
# TODO make max_hydraulic_gradient an attribute of PipeNetwork instead of Pipe
import os

from osgeo import gdal, ogr
import networkx as nx
import json
import numpy as np

from .constants import *
from .colebrook_white import ColebrookWhite
from .utils import get_intermediates


# Timestep of design rain is 5 minutes
# Timestep of design rain is 5 minutes
AREA_WIDE_RAIN = {
    "Bui01": [0.3, 0.6, 0.9, 1.2, 1.5, 1.5, 1.05, 0.9, 0.75, 0.6, 0.45, 0.3, 0.15, 0.15, 0.15],
    "Bui02": [0.15, 0.15, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.5, 1.5, 1.2, 0.9, 0.6, 0.3],
    "Bui03": [0.30, 0.60, 0.90, 1.50, 2.10, 2.10, 1.50, 1.20, 1.05, 0.90, 0.75, 0.60, 0.45, 0.30, 0.15],
    "Bui04": [0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05, 1.20, 1.50, 2.10, 2.10, 1.50, 0.90, 0.60, 0.30],
    "Bui05": [0.30, 0.60, 1.50, 2.70, 2.70, 2.10, 1.50, 1.20, 1.05, 0.90, 0.75, 0.60, 0.45, 0.30, 0.15],
    "Bui06": [0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05, 1.20, 1.50, 2.10, 2.70, 2.70, 1.50, 0.60, 0.30],
    "Bui07": [0.6, 1.2, 2.1, 3.3, 3.3, 2.7, 2.1, 1.5, 1.2, 0.9, 0.6, 0.3],
    "Bui08": [0.3, 0.6, 0.9, 1.2, 1.5, 2.1, 2.7, 3.3, 3.3, 2.1, 1.2, 0.6],
    "Bui09": [1.5, 2.7, 4.8, 4.8, 4.2, 3.3, 2.7, 2.1, 1.5, 0.9, 0.6, 0.3],
    "Bui10": [1.8, 3.6, 6.3, 6.3, 5.7, 4.8, 3.6, 2.4, 1.2],
    "T100": [5.833333333] * 12,
    "T250": [7.5] * 12,
    "T1000": [6.666666667] * 24,
    # # Last 3 designs should use 1 hour timestep.
    # "14": [0.208333333] * 48,
    # "15": [0.225694444] * 48,
    # "16": [0.277777778] * 48,
}


DESIGN_RAIN_TIMESTEP = 300
BGT_INLOOPTABEL_REQUIRED_FIELDS = [
    "bgt_identificatie",
    "gemengd_riool",
    "pipe_code_gemengd_riool",
    "hemelwaterriool",
    "pipe_code_hemelwaterriool",
    "vgs_hemelwaterriool",
    "pipe_code_vgs_hemelwaterriool",
    "infiltratievoorziening",
    "pipe_code_infiltratievoorziening",
]
LINE_SAMPLE_POINTS = 100

MATERIAL_THICKNESS = {"PVC": 0.1, "Concrete": 0.2}


class InvalidGeometryException(Exception):
    pass


class BGTInloopTabel:
    def __init__(self, bgt_inlooptabel_fn):

        tabel_abspath = os.path.abspath(bgt_inlooptabel_fn)
        if not os.path.isfile(tabel_abspath):
            raise FileNotFoundError(
                "BGT Inlooptabel niet gevonden: {}".format(tabel_abspath)
            )
        tabel_ds = ogr.Open(tabel_abspath)
        # TODO more thorough checks of validity of input geopackage
        try:
            self.layer = tabel_ds.GetLayer(0)
        except Exception:
            raise ValueError("Geen geldig bestand, {}".format(tabel_abspath))

        self.fields = self.get_layer_fields()
        for field in BGT_INLOOPTABEL_REQUIRED_FIELDS:
            if field not in self.fields:
                raise ValueError(
                    "Required field '{}' not in BGT inlooptabel".format(field)
                )

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
        """Sets the table if not exists"""
        if not hasattr(self, "_table"):
            self.table_fields = self.fields + ["fid", "surface_area"]
            self._table = {field: [] for field in self.table_fields}

            for feature in self.layer:
                feature_items = json.loads(feature.ExportToJson())["properties"]
                feature_geometry = feature.GetGeometryRef()
                for key, value in feature_items.items():
                    self._table[key].append(value)
                self._table["fid"].append(feature.GetFID())
                self._table["surface_area"].append(feature_geometry.GetArea())

    def get_surface_area_for_pipe_code(self, pipe_code, pipe_type):
        """Get the connected surface area for a pipe code and which type of sewerage system should be searched"""
        pipe_type_codes = self._table["pipe_code_" + pipe_type]
        surface_areas = []
        for i, code in enumerate(pipe_type_codes):
            if str(code) == str(pipe_code):
                surface_area_bgt = self._table["surface_area"][i]
                surface_fraction = self._table[pipe_type][i] / 100
                connected_area = surface_area_bgt * surface_fraction

                surface_areas.append(connected_area)

        surface_sum = sum(surface_areas)
        return surface_sum


class Weir:

    """Class representing external weir"""

    def __init__(
        self,
        wkt_geometry,
        fid: int = None,
        weir_level: float = None,
        crest_flow_depth: float = None,
        pipe_in_id: int = None,
        pipe_out_id: int = None,
    ):
        self.geometry = ogr.CreateGeometryFromWkt(wkt_geometry)
        self.weir_level = weir_level
        self.fid = fid
        self.crest_flow_depth = crest_flow_depth
        self.pipe_in_id = pipe_in_id
        self.pipe_out_id = pipe_out_id

    @property
    def wkt_geometry(self):
        return self.geometry.ExportToWkt()

    @property
    def coordinate(self):
        return self.geometry.GetPoints()[0]


class Outlet:
    def __init__(
        self,
        wkb_geometry,
        ditch_level: float = None,
        outlet_id: int = None,
        surface_elevation: float = None,
        crest_flow_depth: float = None,
        pipe_in_id: int = None,
        pipe_out_id: int = None,
        hydraulic_head: float = None,
    ):
        self.geometry = ogr.CreateGeometryFromWkb(wkb_geometry)
        self.ditch_level = ditch_level
        self.outlet_id = outlet_id
        self.surface_elevation = surface_elevation
        self.crest_flow_depth = crest_flow_depth
        self.pipe_in_id = pipe_in_id
        self.pipe_out_id = pipe_out_id
        self.hydraulic_head = hydraulic_head

    @property
    def wkt_geometry(self):
        return self.geometry.ExportToWkt()

    @property
    def coordinate(self):
        return self.geometry.GetPoints()[0]


class PumpingStation(ogr.Feature):

    # Outlets are also line geometry
    def __init__(self):
        self.end_level = None


class Pipe:
    def __init__(
        self,
        wkt_geometry,
        fid,
        diameter: float = None,
        start_level: float = None,
        end_level: float = None,
        material: str = None,
        connected_surface_area: float = 0.0,
        accumulated_connected_surface_area: float = None,
        max_hydraulic_gradient : float = None,
        sewerage_type: str = None,
        cover_depth: float = None,
        discharge: float = None,
        velocity: float = None,
    ):
        self.geometry = ogr.CreateGeometryFromWkt(wkt_geometry) 
        self.fid = fid
        self.diameter = diameter
        self.start_level = start_level
        self.end_level = end_level
        self.material = material
        self.connected_surface_area = connected_surface_area
        self.accumulated_connected_surface_area = accumulated_connected_surface_area
        self.sewerage_type = sewerage_type
        self.cover_depth = cover_depth
        self.discharge = discharge
        self.velocity = velocity
        self.max_hydraulic_gradient = max_hydraulic_gradient

        self.start_elevation = None
        self.end_elevation = None
        self.lowest_elevation = None

        self.validate()

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

    def set_material(self):
        """Sets the material type based on the diameter"""
        if self.diameter is None:
            self.material = None
        elif self.diameter < 0.315:
            self.material = "PVC"
        else:
            self.material = "Concrete"

    def sample_elevation_model(self, dem_rasterband, dem_geotransform):
        """Sample an elevation model on points along the pipe"""
        dem_no_data_value = dem_rasterband.GetNoDataValue()
        pipe_source_coordinates = self.start_coordinate
        pipe_target_coordinates = self.end_coordinate
        gt = dem_geotransform

        p_source_x = int((pipe_source_coordinates[0] - gt[0]) / gt[1])  # x pixel
        p_source_y = int((pipe_source_coordinates[1] - gt[3]) / gt[5])  # y pixel
        p_target_x = int((pipe_target_coordinates[0] - gt[0]) / gt[1])  # x pixel
        p_target_y = int((pipe_target_coordinates[1] - gt[3]) / gt[5])  # y pixel

        # sample dem for intermediate points
        points = [[p_source_x, p_source_y]]

        for point in get_intermediates(
            [p_source_x, p_source_y], [p_target_x, p_target_y], LINE_SAMPLE_POINTS
        ):
            points.append(point)
        points.append([p_target_x, p_target_y])

        dem_elevation = []
        for point in points:
            elevation = dem_rasterband.ReadAsArray(point[0], point[1], 1, 1)[0][0]
            if elevation == dem_no_data_value:
                elevation = None
            dem_elevation.append(elevation)

        self.dem_elevation = dem_elevation
        self.start_elevation = dem_elevation[0]
        self.end_elevation = dem_elevation[-1]
        self.lowest_elevation = min(dem_elevation)

    def determine_connected_surface_area(self, bgt_inlooptabel: BGTInloopTabel):
        """Find the connected surface area from the BGT Inlooptabel, sewerage type is needed to filter"""
        connected_surface_area = bgt_inlooptabel.get_surface_area_for_pipe_code(
            pipe_code=str(self.fid), pipe_type=self.sewerage_type
        )
        self.connected_surface_area = connected_surface_area

    def calculate_discharge(self, intensity):
        """Calculate the inflow from connected surfaces given an intensity in mm/h"""

        # intensity is in mm/h, timestep is in seconds, output discharge is m3/s
        pipe_discharge = self.accumulated_connected_surface_area * (
            (intensity / 1000) / 3600
        )
        self.discharge = pipe_discharge

    def calculate_diameter(self,vmax):
        """Use the Colebrook White method to esimate the diameters"""
        colebrook_white = ColebrookWhite(
            q=self.discharge, Smax=self.max_hydraulic_gradient, sewerage_type=self.sewerage_type, v_max=vmax
        )

        estimated_diameter,velocity = colebrook_white.iterate_diameters()
        self.diameter = estimated_diameter
        self.velocity=velocity
        
        if self.velocity > vmax:
            self.velocity_to_high=True
        else:
            self.velocity_to_high=False
            
    def validate(self):
        if len(self.points) != 2:
            raise InvalidGeometryException

    def write_properties_to_feature(self):
        for key in self.properties.keys():
            value = getattr(self, key)
            self.feature.SetField(key, value)

    def __str__(self):
        output = ""
        for _, var in vars(self).items():
            output += str(_) + ": "
            output += str(var)
            output += "\n"

        return output


class PipeNetwork:
    def __init__(self):
        self.network = nx.DiGraph()
        self.sewerage_type = None
        self.outlet_level = None
        self.pipes = {}
        self.weirs = {}

    @property
    def reverse_network(self):
        """As we are using a DiGraph, this reverses the network direction"""
        return self.network.reverse()

    @property
    def distance_matrix(self):
        """Returns a dictionary for each node a dictionary with distances to every other node"""
        return dict(nx.all_pairs_dijkstra(self.network, weight="length"))

    @property
    def distance_matrix_reversed(self):
        """Returns a dictionary for each node a dictionary with distances to every other node"""
        return dict(nx.all_pairs_dijkstra(self.reverse_network, weight="length"))

    @property
    def network_upstream_hydraulic_head(self):
        """Used to estimate the max hydraulic gradient"""
        if self.weir is not None:
            return self.weir.crest_flow_depth + self.weir.weir_level

    def add_pipe(self, pipe: Pipe):
        """Add a pipe to the network as an object and as an edge to the graph"""
        self.pipes[pipe.fid] = pipe
        pipe_edge_start = (round(pipe.start_coordinate[0]),round(pipe.start_coordinate[1]))
        pipe_edge_end = (round(pipe.end_coordinate[0]),round(pipe.end_coordinate[1]))
        
        if pipe.start_coordinate not in self.network.nodes:
            self.network.add_node(
                (pipe_edge_start[0], pipe_edge_start[1]),
                type="manhole",
                position=pipe.start_coordinate,
                connected_area=0,
            )

        if pipe.end_coordinate not in self.network.nodes:
            self.network.add_node(
                (pipe_edge_end[0], pipe_edge_end[1]),
                type="manhole",
                position=pipe.end_coordinate,
                connected_area=0,
            )

        self.network.add_edge(
            (pipe_edge_start[0], pipe_edge_start[1]),
            (pipe_edge_end[0], pipe_edge_end[1]),
            fid=pipe.fid,
            length=pipe.geometry.Length(),
        )

    def add_weir(self, weir: Weir):
        """Add a weir to the network, as an object and as an edge to the graph"""
        self.weirs[weir.fid] = weir
        
        # Add the node to the network, if the node is already present change it's type
        weir_coordinate = (round(weir.coordinate[0]),round(weir.coordinate[1]))
        weir._node_coordinate = weir_coordinate
        if weir_coordinate not in self.network.nodes:
            self.network.add_node(weir_coordinate, 
                                  type="weir",
                                 connected_area=0,
                                 position=weir.coordinate)
        else:
            attr = {weir_coordinate: {"type": "weir", "connected_area":0}}
            nx.set_node_attributes(self.network, attr)

    def add_elevation_to_network(self, dem_filename : str):
        """Add elevation to all pipes in the network"""
        
        dem_datasource = gdal.Open(dem_filename)
        dem_rasterband = dem_datasource.GetRasterBand(1)
        dem_geotransform = dem_datasource.GetGeoTransform()
        
        for pipe in self.pipes.values():
            pipe.sample_elevation_model(dem_rasterband=dem_rasterband, 
                                        dem_geotransform=dem_geotransform)
        
        
    def calculate_max_hydraulic_gradient(self, waking : float):
        """
        Calculates the max hydraulic gradient based on the network end point and start/end elevation
        The max hydraulic gradient is defined as the maximum difference in elevation between the endpoint of the network
        and the furthest node divided by the distance between the two
        Assign this back to all the pipes in the network
        """
        
        # Get all weirs (out-degree=0) nodes in the network
        # Calculate the hydraulic gradient to the furthest upstream point
        # Walk the network upstream from each of these nodes
        # At each pipe, calculate if the estmated hydraulic gradient is sufficient for it's lowest elevation
        # If not, lower the gradient for all downstream pipes
        # Calculate what the new hydraulic head will be at the start of the pipe
        # Calculate the new hydraulic gradient for upstream pipes using the new hydraulic head

        # Get the distance dictionary for the end node
        hydraulic_gradients = {}
        for weir in self.weirs.values():
            print(weir)
            weir_node = weir._node_coordinate
            distance_dictionary = self.distance_matrix_reversed[weir_node][0]
            furthest_node, distance = list(distance_dictionary.items())[-1]
            furthest_edge = list(self.network.edges(furthest_node))[0]
            furthest_pipe = self.get_pipe_with_edge(furthest_edge)

            hydraulic_gradient = (
                (furthest_pipe.start_elevation + waking)
                - (weir.weir_level + weir.crest_flow_depth)
            ) / distance
            
            print(hydraulic_gradient)
            
            # for each upstream pipe, assign hydraulic gradient
            upstream_pipes = self.find_upstream_pipes(weir_node)
            
            for pipe in upstream_pipes:
                print(pipe.fid)
                if pipe.fid not in hydraulic_gradients:
                    hydraulic_gradients[pipe.fid] = []
                    hydraulic_gradients[pipe.fid] += [hydraulic_gradient]
                else:
                    hydraulic_gradients[pipe.fid] += [hydraulic_gradient]                    
            
        for pipe_fid in self.pipes:
            pipe = self.pipes[pipe_fid]
            max_hydraulic_gradient = min(hydraulic_gradients[pipe_fid])
            setattr(self.pipes[pipe_fid], "max_hydraulic_gradient", max_hydraulic_gradient)

    def evaluate_hydraulic_gradient_upstream(self, waking):
        """Evaluate the maximum hydraulic gradient for each pipe in the network based on it's elevation"""

        for edge in self.network.edges:
            pipe = self.get_pipe_with_edge(edge)
            start_node = edge[0]
            distance_to_weir, closest_weir = self.find_closest_weir(start_node)
            print('start_node='f"{start_node}")
            print('distance_to_weir='f"{distance_to_weir}")
            hydraulic_head = (
                (closest_weir.weir_level + closest_weir.crest_flow_depth)
                + pipe.max_hydraulic_gradient * distance_to_weir
            )
            print('hydraulic_head='f"{hydraulic_head}")
            print('pipe.lowest_elevation='f"{pipe.lowest_elevation}")
            head_difference = (pipe.lowest_elevation - waking) - hydraulic_head
            print('head_difference='f"{head_difference}")
            if head_difference < 0:
                new_hydraulic_gradient = pipe.max_hydraulic_gradient - (
                    head_difference / distance_to_weir
                )
                print('new_hydraulic_gradient='f"{new_hydraulic_gradient}")
                if new_hydraulic_gradient < self.max_hydraulic_gradient:
                    self.max_hydraulic_gradient = new_hydraulic_gradient
                    print('smaller,so:self.max_hydraulic_gradient='f"{self.max_hydraulic_gradient}")

        for pipe in self.pipes:
            setattr(
                self.pipes[pipe], "max_hydraulic_gradient", self.max_hydraulic_gradient
            )

    def accumulate_connected_surface_area(self):
        """For each pipe in the network, accumulate downstream connected area"""

        sink_nodes = [n for n, d in self.network.in_degree() if d == 0]
        tank_nodes = [n for n, d in self.network.out_degree() if d == 0]

        out_degree_nodes = self.network.out_degree()

        # We assume that pipe flow enters at the starting node of each pipe
        for edge in self.network.edges:
            pipe = self.get_pipe_with_edge(edge)
            end_node = edge[1]
            attrs = {end_node: {"connected_area": pipe.connected_surface_area + self.network.nodes[end_node]['connected_area']}}
            nx.set_node_attributes(self.network, attrs)  
            edge_attrs = {edge:{'connected_surface_area':pipe.connected_surface_area}}
            nx.set_edge_attributes(self.network, edge_attrs)


        # Define recursive function used to accumulate the connected surface area
        def get_node_output(node, completed_nodes):
            if node in completed_nodes:
                return completed_nodes[node]
            else:
                stack = self.network.predecessors(node)
                upstream_nodes = []
                while stack:
                    try:
                        in_node = next(stack)
                        upstream_nodes += [in_node]
                    except StopIteration:
                        break

                node_output = self.network.nodes[node]["connected_area"]
                for in_node in upstream_nodes:
                    node_output += get_node_output(in_node, completed_nodes)

                if out_degree_nodes[node] > 0:
                    node_output /= out_degree_nodes[node]

                attrs = {node: {"connected_area": node_output}}
                nx.set_node_attributes(self.network, attrs)

                completed_nodes[node] = node_output
                return node_output

        completed_nodes = {
            sink: self.network.nodes[sink]["connected_area"] for sink in sink_nodes
        }
        for tank in tank_nodes:
            score = get_node_output(tank, completed_nodes)

        for node, area in completed_nodes.items():
            node_successors = []
            for i in self.network.successors(node):
                node_successors += [i]

            for successor in node_successors:
                edge = (node, successor)
                edge_flow = self.network.nodes[node]["connected_area"] + self.network.edges[edge]['connected_surface_area']
                attrs = {edge:{'accumulated_connected_area':edge_flow}}
                nx.set_edge_attributes(self.network, attrs)
                pipe = self.get_pipe_with_edge(edge)
                pipe.accumulated_connected_surface_area = edge_flow

    def add_id_to_nodes(self):
        """Add an incremental id to all nodes in the network"""
        for i, node in enumerate(self.network.nodes):
            self.network.nodes[node]["id"] = i

    def get_pipe_with_edge(self, edge):
        """Use network edge to get correspondent Pipe instance"""
        edge_fid = nx.get_edge_attributes(self.network, "fid")[edge]
        pipe = self.pipes[edge_fid]

        return pipe

    def find_downstream_pipes(self, node):
        """Find all connected downstream pipes in the network from a starting node"""
        downstream_edges = nx.edge_dfs(self.network, node)
        downstream_pipes = []
        for edge in downstream_edges:
            pipe = self.get_pipe_with_edge(edge)
            downstream_pipes.append(pipe)

        return downstream_pipes

    def find_upstream_pipes(self, node):
        """Find all connected upstream pipes in the network from a starting node"""
        upstream_edges = nx.edge_dfs(self.network, node, orientation="reverse")
        upstream_pipes = []
        for edge in upstream_edges:
            edge = (edge[0], edge[1])
            pipe = self.get_pipe_with_edge(edge)
            upstream_pipes.append(pipe)

        return upstream_pipes

    def find_closest_weir(self,node):
        """Get the distance to the closest weir from a node in the network"""
        
        distance = np.inf
        closest_weir = None
        for weir in self.weirs.values():
            weir_node = weir._node_coordinate
            try:
                distance_to_weir=nx.shortest_path_length(G=self.network,source=node,target=weir_node,weight='length')
                if distance_to_weir < distance:
                    distance = distance_to_weir
                    closest_weir = weir
            except nx.NetworkXNoPath:
                continue
            
        return distance, closest_weir

    def draw_network(self, node_label_attr, edge_label_attr):
        
        G = self.network.copy()
        for edge in G.edges:
            pipe = self.get_pipe_with_edge(edge)
            attr = getattr(pipe, edge_label_attr)
            if isinstance(attr, float):
                attr= round(attr,2)
            attrs = {edge: {edge_label_attr: attr}}
            nx.set_edge_attributes(G, attrs)
            
        node_labels = nx.get_node_attributes(G, node_label_attr)
        pos = nx.get_node_attributes(G, "position")        
        nx.draw(
            G, pos, edge_color='black', width=1, linewidths=1,
            node_size=100, node_color='pink', alpha=0.9,
            labels=node_labels)

        edge_labels = nx.get_edge_attributes(G, edge_label_attr)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
    def validate_network_diameters(self):
        # TODO Walk the network and determine that there are no decreases in diameter
        pass


class StormWaterPipeNetwork(PipeNetwork):
    # TODO maybe rename to StormWaterPipeNetwork
    def __init__(self):
        super().__init__()
        self.network_type = "infiltratieriool"

    def calculate_cover_depth(self):
        """Determine the depth """
        
        undirected_network = self.network.to_undirected()
        subgraphs = nx.weakly_connected_component_subgraphs(self.network)
        
        for subgraph in subgraphs:
            subgraph_edges = subgraph.edges
            network_pipes = []
            lowest_weir_height = np.inf
            for edge in subgraph_edges:
                _, closest_weir = self.find_closest_weir(edge[1])
                pipe = self.get_pipe_with_edge(edge)
                network_pipes += [pipe]
                
                if closest_weir.weir_level < lowest_weir_height:
                    lowest_weir_height = closest_weir.weir_level

            max_diameter = max([pipe.diameter for pipe in network_pipes])
            
            for pipe in network_pipes:                
                material_thickness = MATERIAL_THICKNESS[pipe.material]        
                pipe.start_level=lowest_weir_height - max_diameter
                pipe.end_level=lowest_weir_height - max_diameter
                invert_level=max(pipe.start_level,pipe.end_level) 
                cover_depth = pipe.lowest_elevation - (
                    invert_level + pipe.diameter + material_thickness *2
                )
                pipe.cover_depth=cover_depth
            
    def check_invert_levels(self):
        for pipe in self.pipes.values():
            if pipe.invert_level_start > pipe.minimum_cover_depth:
                raise ValueError('Pipe invert level is too high, invert level: {}, minimum invert level: {}'.format(pipe.invert_level_start, pipe.minimum_cover_depth))
            
    def estimate_internal_weir_locations(self):
        # TODO  For a given network and elevation model, determine the best locations to install weirs
        # If there are already weirs in the network, raise error
        pass


class WasteWaterPipeNetwork(PipeNetwork):
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
        self.dem_datasource = None
        self.dem_rasterband = None
        self.dem_geotransform = None
        self.bgt_inlooptabel = None
        self.pipe_networks = []

    def set_dem(self, filename):
        self.dem_datasource = gdal.Open(filename)
        self.dem_rasterband = self.dem_datasource.GetRasterBand(1)
        self.dem_geotransform = self.dem_datasource.GetGeoTransform()

    def set_bgt_inlooptabel(self, filename):
        self.bgt_inlooptabel = BGTInloopTabel(filename)

    def set_design_rain(self, design_rain):
        if design_rain in AREA_WIDE_RAIN.keys():
            design_rain_pattern = AREA_WIDE_RAIN[design_rain]
        else:
            raise KeyError("Selected design rain not availabe")
        self.design_rain = design_rain_pattern
