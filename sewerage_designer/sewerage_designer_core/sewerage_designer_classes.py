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


class InvalidGeometryException:
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
                bgt_identificatie = self._table["bgt_identificatie"][i]

                if bgt_identificatie not in self.connected_surfaces:
                    surface_area_bgt = self._table["surface_area"][i]
                    surface_fraction = self._table[pipe_type][i] / 100
                    connected_area = surface_area_bgt * surface_fraction

                    surface_areas.append(connected_area)
                    self.connected_surfaces.append(bgt_identificatie)

        surface_sum = sum(surface_areas)
        return surface_sum


class Weir:

    """Class representing external weir"""

    def __init__(
        self,
        wkt_geometry,
        fid: int = None,
        weir_level: float = None,
        freeboard: float = None,
        pipe_in_id: int = None,
        pipe_out_id: int = None,
    ):
        self.geometry = ogr.CreateGeometryFromWkt(wkt_geometry)
        self.weir_level = weir_level
        self.fid = fid
        self.freeboard = freeboard
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
        freeboard: float = None,
        pipe_in_id: int = None,
        pipe_out_id: int = None,
        hydraulic_head: float = None,
    ):
        self.geometry = ogr.CreateGeometryFromWkb(wkb_geometry)
        self.ditch_level = ditch_level
        self.outlet_id = outlet_id
        self.surface_elevation = surface_elevation
        self.freeboard = freeboard
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
        fid: int = None,
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

    def calculate_discharge(self, intensity, timestep):
        """Calculate the inflow from connected surfaces given an intensity in mm/h"""

        # intensity is in mm/hr, timestep is in seconds, output discharge is m3/s
        pipe_discharge = self.accumulated_connected_surface_area * (
            (intensity / 1000) / timestep
        )
        self.discharge = pipe_discharge

    def calculate_diameter(self):
        """Use the Colebrook White method to esimate the diameters"""
        colebrook_white = ColebrookWhite(
            q=self.discharge, Smax=self.max_hydraulic_gradient, sewerage_type=self.sewerage_type
        )

        estimated_diameter = colebrook_white.iterate_diameters()
        self.diameter = estimated_diameter

    def calculate_minimum_cover_depth(self, minimal_cover_depth):
        """Determine the depth """

        material_thickness = MATERIAL_THICKNESS[self.material]
        minimum_cover_depth = self.lowest_elevation - (
            minimal_cover_depth + self.diameter + material_thickness *2
        )
        self.minimum_cover_depth = minimum_cover_depth

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
        self.weir = None

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
            return self.weir.freeboard + self.weir.weir_level

    def add_pipe(self, pipe: Pipe):
        """Add a pipe to the network as an object and as an edge to the graph"""
        self.pipes[pipe.fid] = pipe

        if pipe.start_coordinate not in self.network.nodes:
            self.network.add_node(
                (round(pipe.start_coordinate[0]), round(pipe.start_coordinate[1])),
                type="manhole",
                position=pipe.start_coordinate,
                connected_area=0,
            )

        if pipe.end_coordinate not in self.network.nodes:
            self.network.add_node(
                (round(pipe.end_coordinate[0]), round(pipe.end_coordinate[1])),
                type="manhole",
                position=pipe.end_coordinate,
                connected_area=0,
            )

        self.network.add_edge(
            (round(pipe.start_coordinate[0]), round(pipe.start_coordinate[1])),
            (round(pipe.end_coordinate[0]), round(pipe.end_coordinate[1])),
            fid=pipe.fid,
            length=pipe.geometry.Length(),
        )

    def add_weir(self, weir: Weir):
        """Add a weir to the network, as an object and as an edge to the graph"""
        self.weir = weir

        # Add the node to the network, if the node is already present change it's type
        weir_coordinate = (round(weir.coordinate[0]),round(weir.coordinate[1]))
        self.weir_coordinate = weir_coordinate
        if weir_coordinate not in self.network.nodes:
            self.network.add_node(weir_coordinate, 
                                  type="weir",
                                 connected_area=0)
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

        # Get the distance dictionary for the end node
        weir_coordinate = (round(self.weir.coordinate[0]), round(self.weir.coordinate[1]))
        distance_dictionary = self.distance_matrix_reversed[weir_coordinate][0]
        furthest_node, distance = list(distance_dictionary.items())[-1]
        furthest_edge = list(self.network.edges(furthest_node))[0]
        furthest_pipe = self.get_pipe_with_edge(furthest_edge)
        print('weir_coodinate='f"{weir_coordinate}")
        print('distance_dictionary='f"{distance_dictionary}")
        print('distance='f"{distance}")
        print('furthest_node='f"{furthest_node}")
        print('furthest_edge='f"{furthest_edge}")
        print('furthest_pipe='f"{furthest_pipe}")

        max_hydraulic_gradient = (
            (furthest_pipe.start_elevation + waking)
            - self.network_upstream_hydraulic_head
        ) / distance

        print('self.network_upstream_hydraulic_head='f"{self.network_upstream_hydraulic_head}")
        print('waking='f"{waking}")
        print('furthest_pipe.start_elevation='f"{furthest_pipe.start_elevation}")
        print('max_hydraulic_gradient='f"{max_hydraulic_gradient}")
        
        self.max_hydraulic_gradient = max_hydraulic_gradient
        for pipe in self.pipes:
            setattr(self.pipes[pipe], "max_hydraulic_gradient", max_hydraulic_gradient)

    def evaluate_hydraulic_gradient_upstream(self, waking):
        """Evaluate the maximum hydraulic gradient for each pipe in the network based on it's elevation"""

        for edge in self.network.edges:
            pipe = self.get_pipe_with_edge(edge)
            start_node = edge[0]
            distance_to_weir = self.distance_to_weir(start_node)

            hydraulic_head = (
                self.network_downstream_hydraulic_head
                + pipe.max_hydraulic_gradient * distance_to_weir
            )
            head_difference = hydraulic_head - (pipe.lowest_elevation + waking)
            if head_difference > 0:
                new_hydraulic_gradient = pipe.max_hydraulic_gradient - (
                    head_difference / distance_to_weir
                )
                if new_hydraulic_gradient < self.max_hydraulic_gradient:
                    self.max_hydraulic_gradient = new_hydraulic_gradient

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

    def find_upstream_pipes(self, node):
        """Find all connected upstream pipes in the network from a starting node"""
        upstream_edges = nx.edge_dfs(self.network, node, orientation="reverse")
        upstream_pipes = []
        for edge in upstream_edges:
            pipe = self.get_pipe_with_edge(edge)
            upstream_pipes.append(pipe)

        return upstream_pipes

    def distance_to_weir(self, node):
        """Get the distance to the outlet from a node in the network"""

        spl = dict(nx.all_pairs_shortest_path_length(self.network))
        distance_to_weir = spl[node][self.weir_coordinate]

        return distance_to_weir

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

    @property
    def network_downstream_hydraulic_head(self):
        """Used to estimate the max hydraulic gradient"""
        if self.weir is not None:
            return self.weir.freeboard + self.weir.weir_level

    def set_invert_levels(self):
        # For IT network the gradient of the pipes is 0, find the highest possible solution
        max_diameter = max([pipe.diameter for pipe in self.pipes.values()])
        self.network_level = self.weir.weir_level - max_diameter
        for pipe in self.pipes.values():
            pipe.invert_level_start = self.network_level
            pipe.invert_level_end = self.network_level
                        
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
