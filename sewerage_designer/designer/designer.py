# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 14:49:31 2021

@author: Emile.deBadts
@author: Chris.Kerklaan

"""
# @Leendert
# TODO seems too much code for one script
# TODO the hydraulic gradient computation seems rushed, chaotic and maybe even unfinished
# TODO make max_hydraulic_gradient an attribute of PipeNetwork instead of Pipe

# First-party imports
import os
import json
import numpy as np

# python > 3.8
#from functools import cached_property

# Third-party imports
from osgeo import gdal, ogr
import networkx as nx

# Local imports
# from . import constants as c
from .colebrook_white import ColebrookWhite
from .utils import get_intermediates

# Timestep of design rain is 5 minutes
# Timestep of design rain is 5 minutes
AREA_WIDE_RAIN = {
    "Bui01": [
        0.3,
        0.6,
        0.9,
        1.2,
        1.5,
        1.5,
        1.05,
        0.9,
        0.75,
        0.6,
        0.45,
        0.3,
        0.15,
        0.15,
        0.15,
    ],
    "Bui02": [
        0.15,
        0.15,
        0.15,
        0.3,
        0.45,
        0.6,
        0.75,
        0.9,
        1.05,
        1.5,
        1.5,
        1.2,
        0.9,
        0.6,
        0.3,
    ],
    "Bui03": [
        0.30,
        0.60,
        0.90,
        1.50,
        2.10,
        2.10,
        1.50,
        1.20,
        1.05,
        0.90,
        0.75,
        0.60,
        0.45,
        0.30,
        0.15,
    ],
    "Bui04": [
        0.15,
        0.30,
        0.45,
        0.60,
        0.75,
        0.90,
        1.05,
        1.20,
        1.50,
        2.10,
        2.10,
        1.50,
        0.90,
        0.60,
        0.30,
    ],
    "Bui05": [
        0.30,
        0.60,
        1.50,
        2.70,
        2.70,
        2.10,
        1.50,
        1.20,
        1.05,
        0.90,
        0.75,
        0.60,
        0.45,
        0.30,
        0.15,
    ],
    "Bui06": [
        0.15,
        0.30,
        0.45,
        0.60,
        0.75,
        0.90,
        1.05,
        1.20,
        1.50,
        2.10,
        2.70,
        2.70,
        1.50,
        0.60,
        0.30,
    ],
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
                "BGT Inlooptabel not found: {}".format(tabel_abspath)
            )
        tabel_ds = ogr.Open(tabel_abspath)
        if tabel_ds is None:
            raise ValueError("Could not open BGT Inlooptabel: {}".format(tabel_abspath))
        try:
            self.layer = tabel_ds.GetLayer(0)
        except Exception:
            raise ValueError("Not a valid file, {}".format(tabel_abspath))

        self.fields = list(self.get_layer_fields())
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
        ldefn = self.layer.GetLayerDefn()
        return (ldefn.GetFieldDefn(n).name for n in range(ldefn.GetFieldCount()))

    def set_table(self):
        """Sets the table if not exists"""
        if not hasattr(self, "_table"):
            self.table_fields = self.fields + ["fid", "surface_area"]
            self._table = {field: [] for field in self.table_fields}

            self.layer.ResetReading()
            for feature in self.layer:
                feature_items = feature.items()
                feature_geometry = feature.GetGeometryRef()
                for key, value in feature_items.items():
                    if key in self._table:
                        self._table[key].append(value)
                self._table["fid"].append(feature.GetFID())
                self._table["surface_area"].append(feature_geometry.GetArea())

    def get_surface_area_for_pipe_code(self, pipe_code, pipe_type):
        """Get the connected surface area for a pipe code and which type of sewerage system should be searched"""
        pipe_type_codes = self._table[f"pipe_code_{pipe_type}"]
        surface_areas = [
            self._table["surface_area"][i] * (self._table[pipe_type][i] / 100)
            for i, code in enumerate(pipe_type_codes)
            if str(code) == str(pipe_code)
        ]
        return sum(surface_areas)


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

    @property
    def flow_level(self):
        return self.weir_level + self.crest_flow_depth

    @property
    def node(self):
        if hasattr(self, "_node_coordinate"):
            return self._node_coordinate

    def __repr__(self):
        return f"Weir: {self.fid}"


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
        max_hydraulic_gradient: float = None,
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
    def length(self):
        return self.geometry.Length()

    @property
    def points(self):
        return self.geometry.GetPoints()

    @property
    def start_coordinate(self):
        return self.points[0]

    @property
    def end_coordinate(self):
        return self.points[1]

    @property
    def end_node(self):
        return int(round(self.end_coordinate[0])), int(round(self.end_coordinate[1]))

    @property
    def start_node(self):
        return int(round(self.start_coordinate[0])), int(
            round(self.start_coordinate[1])
        )

    @property
    def nodes(self):
        return [self.start_node, self.end_node]

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

    def calculate_diameter(self, vmax):
        """Use the Colebrook White method to esimate the diameters"""
        colebrook_white = ColebrookWhite(
            q=self.discharge,
            Smax=self.max_hydraulic_gradient,
            sewerage_type=self.sewerage_type,
            v_max=vmax,
        )

        estimated_diameter, velocity = colebrook_white.iterate_diameters()
        self.diameter = estimated_diameter
        self.velocity = velocity

        if self.velocity > vmax:
            self.velocity_to_high = True
        else:
            self.velocity_to_high = False

    def validate(self):
        if len(self.points) != 2:
            raise ValueError(f"Pipe with id {self.fid} has more than two points: {self.points}")

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

    def __repr__(self):
        return f"Pipe: {self.fid}"


class PipeSection:
    def __init__(self, list_of_pipes: [Pipe, Pipe, Pipe] = []):
        self.empty()
        self.pipes = list_of_pipes

        self.id = None
        self.drowned = None
        self.downstream_hydraulic_head = None
        self.downstream_weir = None
        self.downstream_weir_elevation = None
        self.upstream_hydraulic_head = None
        self.upstream_weir = None
        self.upstream_weir_elevation = None

        self.from_upstream_pipe = None
        self.from_upstream_weir = None
        self.to_downstream_pipe = None
        self.to_downstream_weir = None

        self.freeboard = None

    def __iter__(self):
        for pipe in self.pipes:
            yield pipe

    @property
    def hydraulic_gradient(self):
        """if downstream and upstream head are present, this is calculated
        automatically"""
        if not self.upstream_hydraulic_head or not self.downstream_hydraulic_head:
            return -9999
        else:
            return (
                self.upstream_hydraulic_head - self.downstream_hydraulic_head
            ) / self.length

    @property
    def above_freeboard(self):
        return (self.maximum_elevation - self.upstream_hydraulic_head) < 0

    @property
    def maximum_elevation(self):
        return self.upstream_elevation - self.freeboard

    @property
    def length(self):
        return sum([p.length for p in self])

    @property
    def nodes(self):
        return [p.nodes for p in self]

    @property
    def flat_nodes(self):
        return list(set([i for s in self.nodes for i in s]))

    @property
    def upstream_pipe(self):
        return self.pipes[-1]

    @property
    def downstream_pipe(self):
        return self.pipes[0]

    @property
    def downstream_node(self):
        return self.downstream_pipe.end_node

    @property
    def upstream_node(self):
        return self.upstream_pipe.start_node

    @property
    def upstream_elevation(self):
        return self.upstream_pipe.start_elevation

    @property
    def downstream_elevation(self):
        return self.downstream_pipe.end_elevation
    
    @property
    def between_weirs(self):
        return self.from_upstream_weir and self.to_downstream_weir

    def add(self, pipe: Pipe):
        self.pipes.append(pipe)

    def empty(self):
        self.pipes = []

    def weir_in_section(self, list_of_weirs: [Weir, Weir, Weir]):
        for weir in list_of_weirs:
            coordinate = weir.node
            if coordinate in self.nodes:
                return weir

    def __repr__(self):
        fids = " ".join([str(pipe.fid) for pipe in self.pipes])
        return f"Pipe Section ({self.id}) Gradient: {self.hydraulic_gradient}, Upstream head: {self.upstream_hydraulic_head}, Downstream head: {self.downstream_hydraulic_head}, Length: {self.length}, Fids: {fids}"

    def intersects_pipe(self, pipe: Pipe):
        """returns a node if the pipe intersects with this part"""
        flat_nodes = self.flat_nodes
        for node in pipe.nodes:
            if node in flat_nodes:
                return node

    def intersects_section(self, section):
        """Returns a node and the total length if this section intersects
        with another.
        """
        flat_nodes = self.flat_nodes
        total_length = 0
        for pipe in section:  # upstream direction
            total_length += pipe.length
            for node in pipe.nodes:
                if node in flat_nodes:
                    return node, total_length

    def find_connected_lengths(self, connected_section):
        """returns the location of connection between self.section and
        the param section in the form of a length of the self.section.

        params:
            section: PipeSection, must be connected.

        returns:
            connected length: int, 0 if not connected.
        """

        lengths = []
        used = []
        connected_length = 0
        for pipe in connected_section.pipes:
            connected_length += pipe.length
            for node in pipe.nodes:
                if node in used:  # we always use the end node
                    continue
                if node in self.flat_nodes:
                    lengths.append(connected_length)
                used.append(node)
        return lengths

    def find_connected_section(self, calc_sections: list):
        """finds a connected section in a list of sections.
        Downstream node only first looks in the downstream direction.
        If we cannot find it, we just take the first availabel connection after.

        params:
            calc_sections: list of PipeSection


        returns:
            The connected sections  in the form of a list.
        """
        connected = {"upstream": [], "downstream": [], "all": []}
        for calc_section in calc_sections:
            if self.downstream_node in calc_section.flat_nodes:
                connected["downstream"].append(calc_section)

            if self.upstream_node in calc_section.flat_nodes:
                connected["upstream"].append(calc_section)

            for node in calc_section.flat_nodes:
                if node in self.flat_nodes:
                    connected["all"].append(calc_section)

        return connected


class PipeNetwork:
    def __init__(self):
        self.network = nx.DiGraph()
        self.sewerage_type = None
        self.outlet_level = None
        self.pipes = {}
        self.weirs = {}
        self.gradients = {}
        self._cache = {}

    @property
    def reverse_network(self):
        """As we are using a DiGraph, this reverses the network direction"""
        return self.network.reverse()

    @property
    def distance_matrix(self):
        """Returns a dictionary for each node a dictionary with distances to every other node"""
        dm = self._cache.get("distance_matrix")
        if not dm:
            dm = dict(nx.all_pairs_dijkstra(self.network, weight="length"))
            self._cache["distance_matrix"] = dm
        return dm
    
    @property
    def distance_matrix_reversed(self):
        """Returns a dictionary for each node a dictionary with distances to every other node"""
        dmr = self._cache.get("distance_matrix_reversed")
        if not dmr:
            dmr = dict(nx.all_pairs_dijkstra(self.reverse_network, weight="length"))
            self._cache["distance_matrix_reversed"] = dmr
        return dmr

    @property
    def calculated_sections(self):
        return [u for u in self.upstream if u.hydraulic_gradient != -9999]

    def gradient(self, height1, height2, distance):
        """calculates a simple gradient"""
        return (height2 - height1) / distance

    def distance(self, node_a, node_b):
        """  calculates the distance in a directed graph
            If there is no directed connection we will return the global distance.
        """
        node_a_matrix = self.distance_matrix_reversed[node_a][0]
        if node_b in node_a_matrix:
            return node_a_matrix[node_b]
        else:
            line_wkt= f"LINESTRING ({node_a[0]} {node_a[1]}, {node_b[0]} {node_b[1]})"
            return ogr.CreateGeometryFromWkt(line_wkt).Length()
        
    def add_pipe(self, pipe: Pipe):
        """Add a pipe to the network as an object and as an edge to the graph"""
        self.pipes[pipe.fid] = pipe
        pipe_edge_start = (
            round(pipe.start_coordinate[0]),
            round(pipe.start_coordinate[1]),
        )
        pipe_edge_end = (round(pipe.end_coordinate[0]), round(pipe.end_coordinate[1]))

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

        # Add the node to the network, if the node is already present change it's type
        weir_coordinate = (round(weir.coordinate[0]), round(weir.coordinate[1]))
        weir._node_coordinate = weir_coordinate
        if weir_coordinate not in self.network.nodes:
            self.network.add_node(
                weir_coordinate, type="weir", connected_area=0, position=weir.coordinate
            )
        else:
            attr = {weir_coordinate: {"type": "weir", "connected_area": 0}}
            nx.set_node_attributes(self.network, attr)

        if len(self.find_downstream_pipes(weir_coordinate)) == 0:
            weir.external = True
        else:
            weir.external = False

        self.weirs[weir.fid] = weir

    def add_elevation_to_network(self, dem_filename: str):
        """Add elevation to all pipes in the network"""

        dem_datasource = gdal.Open(dem_filename)
        dem_rasterband = dem_datasource.GetRasterBand(1)
        dem_geotransform = dem_datasource.GetGeoTransform()

        for pipe in self.pipes.values():
            pipe.sample_elevation_model(
                dem_rasterband=dem_rasterband, dem_geotransform=dem_geotransform
            )

    # TODO not used -> can be removed?
    '''
    def calculate_max_hydraulic_gradient(self, waking: float):
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
            weir_node = weir._node_coordinate
            distance_dictionary = self.dmr[weir_node][0]
            furthest_node, distance = list(distance_dictionary.items())[-1]
            furthest_edge = list(self.network.edges(furthest_node))[0]
            furthest_pipe = self.get_pipe_with_edge(furthest_edge)

            hydraulic_gradient = (
                (furthest_pipe.start_elevation + waking)
                - (weir.weir_level + weir.crest_flow_depth)
            ) / distance

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
            setattr(
                self.pipes[pipe_fid], "max_hydraulic_gradient", max_hydraulic_gradient
            )

    '''
    def _gradient_internal_calc(
        self, section, calculated_sections, furthest_pipe_height, furthest_node
    ):

        section.downstream_recalc = False
        if section.id == 1:
            gradient = self.gradient(
                self.first_hydraulic_head,
                furthest_pipe_height,
                self.distance(section.downstream_node, furthest_node),
            )
            section.downstream_hydraulic_head = self.first_hydraulic_head
            section.upstream_hydraulic_head = section.downstream_hydraulic_head + (
                gradient * section.length
            )

        else:
            section.downstream_recalc = True
            connections = section.find_connected_section(calculated_sections)
            if len(connections["downstream"]) > 0:
                connected = connections["downstream"][0]
                section.downstream_section = connected
                section.downstream_hydraulic_head = connected.upstream_hydraulic_head

                if connected.drowned or connected.last:
                    hydraulic_gradient = connected.hydraulic_gradient
                else:

                    # if the last section was not drowned, we need change the gradient of
                    # all weir sections to that of the connected section.
                    weir_sections = self.find_downstream_sections_to_weir(
                        connected, calculated_sections
                    )
                    lowest_head = weir_sections[0].downstream_hydraulic_head
                    weir_sections_length = 0
                    for wsection in weir_sections:
                        weir_sections_length += wsection.length

                    gradient = self.gradient(
                        lowest_head,
                        connected.upstream_weir_elevation,
                        weir_sections_length,
                    )

                    current_head = lowest_head
                    for wsection in weir_sections:
                        wsection.upstream_hydraulic_head = current_head + (
                            wsection.length * gradient
                        )
                        wsection.downstream_hydraulic_head = current_head
                        current_head = wsection.upstream_hydraulic_head

                    # Also we need to compute the gradient for current section.
                    hydraulic_gradient = self.gradient(
                        connected.upstream_weir_elevation,
                        furthest_pipe_height,
                        self.distance(connected.upstream_weir.node, furthest_node),
                    )

                section.upstream_hydraulic_head = section.downstream_hydraulic_head + (
                    hydraulic_gradient * section.length
                )
                section.furthest_pipe_height = furthest_pipe_height

            else:
                return None, section

        if section.from_upstream_weir:
            drowned = section.upstream_hydraulic_head >= section.upstream_weir_elevation
        else: 
            drowned = True
        
        section.drowned = drowned
        if not drowned:
            section.upstream_hydraulic_head = section.upstream_weir_elevation

        return section, None

    def _gradient_internal(self, section, step=0.05):
        """
        Calculates the hydraulic gradient for an internal section.
        params:
            section: Section to be calculated.
            calculated_sections: Already have hydraulic gradients
            first_hydraulic_gradient: First gradient.
            first_hydraulic_head: First head.
            furthest_pipe_height: Furthest pipe height.
            furthest_node: Furthest node.
        """
        assert section.internal == True
        calculated_sections = self.calculated_sections
        section, spare = self._gradient_internal_calc(
            section, self.calculated_sections, self.furthest_pipe_height, self.furthest_node
        )
        if not section:
            return section, spare

        downstream_sections = []
        if section.above_freeboard:
            downstream = self.find_downstream_sections(section)
            for sid in downstream:
                dsection = [c for c in calculated_sections if c.id == sid]
                if len(dsection) > 0:
                    downstream_sections.append(dsection[0])

        # If the upstream hydraulic we will have to recalculate it all again.
        current_elevation = self.furthest_pipe_height
        if section.above_freeboard:        
            print(f"Recalculating section {section.id} because above current elevation")

        while section.above_freeboard and not section.between_weirs:
            current_elevation = current_elevation - step
            
            #TODO
            # A hard break. If elevation becomes lower than one meter
            # we do a hard break. We actually don't know what is happening.
            if abs(current_elevation - self.furthest_pipe_height) > 2:
                print("Doing the hard break")
                break
            
            # A similar break for this one.
            if current_elevation < -20:
                break 
            
            # First we recompute the downstream sections to the new elevation.
            for downstream_section in downstream_sections:
                downstream_section, _ = self._gradient_internal_calc(
                    downstream_section,
                    calculated_sections,
                    current_elevation,
                    self.furthest_node,
                )
            section, _ = self._gradient_internal_calc(
                section,
                calculated_sections,
                section.maximum_elevation,
                section.upstream_node,
            )

        if len(downstream_sections) > 0:
            # Then we do the rest with the altered downstream section
            # to the old height.
            for calc_section in calculated_sections:
                if calc_section.id not in downstream:
                    calc_section_renewed, _ = self._gradient_internal_calc(
                        calc_section,
                        calculated_sections,
                        self.furthest_pipe_height,
                        self.furthest_node,
                    )

        # TODO
        # Once the gradients of the 'weir sections' are recalculated.
        # Branches will change as well.
        # So, we have to recalculate these branches if not recalculated during
        # the 'above freeboard' procedure.
        # if len(downstream_sections) == 0 and section.downstream_recalc:
        # for calc_section in calculated_sections:
        #     if calc_section.id not in [w.id for w in weir_sections]:
        #         calc_section_renewed, _ = self._gradient_internal_calc(
        #             calc_section,
        #             calculated_sections,
        #             furthest_pipe_height,
        #             furthest_node,
        #         )

        # We expect that the sections

        return section, None

    def _gradient_last(self, section, freeboard):
        assert section.last == True
        
        section.upstream_hydraulic_head = section.upstream_elevation - freeboard
        
        if len(self.upstream) == 1:
            section.downstream_hydraulic_head = section.downstream_weir_elevation
            return section, None

        connections = section.find_connected_section(self.calculated_sections)
        if len(connections["downstream"]) > 0:
            connected = connections["downstream"][0]
        else:
            return None, section
        section.downstream_hydraulic_head = connected.upstream_hydraulic_head

        return section, None

    def calculate_max_hydraulic_gradient_weirs(self, freeboard: float):
        """
        Calculates the max hydraulic gradient with internal and external weirs.
        For each external weir, the max hydraulic gradient is calculated by looking at
        the difference between the start elevation of the furthest pipe with the level of the external weir
        [weir_level + crest_flow_level].

        We use the hydraulic gradient to calculate the hydraulic head above
        each weir. If a weir is drowned we keep the gradient and use the
        hydraulic head as a new starting elevation for the next section.
        If the weir is not drowned, we recalculate the gradient of this section.
        The new staring elevation is then the elevation of the weir.

        For each external weir, their upstream pipes are converted into sections.
        Section are from weir to weir or weir to end (no more upstream pipes).

        Each section has a downstream weir. First, we define hydraulic gradients and
        heads of internal sections (weir to weir). Then we define 'last' sections (weir to end).

        """

        external_weirs = [weir for weir in self.weirs.values() if weir.external]
        
        
        print("Amount of external weirs:", len(external_weirs))
        for i, weir in enumerate(external_weirs):

            # we set variables and the first hydraulic gradient.
            self.first_hydraulic_head = weir.flow_level
            
            # First we derive the furthest edge for computing the first
            # hydraulic head.            
            furthest_node, distance =  list(self.distance_matrix_reversed[weir.node][0].items())[-1]
            
            try:
                furthest_pipe = self.get_pipe_with_edge(list(self.network.edges(furthest_node))[0])
                print(f"calculating gradients of {weir}")
            except:
                print(f"skipping loose {weir} at {furthest_node}")
                continue
                #TODO what is the definition of a "loose weir" and why are there so many

            self.furthest_pipe_distance = distance
            self.furthest_pipe_height = furthest_pipe.start_elevation - freeboard
            self.furthest_node = furthest_node
            self.first_gradient = (
                self.furthest_pipe_height - self.first_hydraulic_head
            ) / self.furthest_pipe_distance

            # Upstream is shared. Once something is done in a section it will
            # come back in self.upstream.
            self.upstream = self.split_into_sections(weir, freeboard)

            # The variables in this loop are start_height and hydraulic_gradient.
            spared = []
            for i, section in enumerate(self.upstream):
                if not section.internal:
                    continue
                section, spare = self._gradient_internal(section)
                spared.append(spare)

            for section in self.upstream:
                if not section.last:
                    continue
                section, spare = self._gradient_last(section, freeboard)
                spared.append(spare)

            # Finally we solve all spare parts
            spared = [s for s in spared if s is not None]
            max_loops = len(spared) * 3
            i = 0
            while len(spared) > 0 and i != max_loops:
                section = spared.pop(0)
                if section.last:
                    section, spare = self._gradient_last(section, freeboard)
                if section.internal:
                    section, spare = self._gradient_internal(section)

                if spare:
                    spared.append(spare)

            self.gradients[weir.fid] = self.upstream
            
        self.section_gradients_to_pipe_gradients()

    def section_gradients_to_pipe_gradients(self):
        hydraulic_gradients = {pipe:[] for pipe in self.pipes}
        for sections in self.gradients.values():
            for section in sections:
                for pipe in section.pipes:
                    hydraulic_gradients[pipe.fid].append(section.hydraulic_gradient)
        
        for pipe_fid in self.pipes:
            pipe = self.pipes[pipe_fid]
            if len(hydraulic_gradients[pipe_fid]) > 0:
                self.pipes[pipe_fid].max_hydraulic_gradient =  min(hydraulic_gradients[pipe_fid])
            else:
                self.pipes[pipe_fid].max_hydraulic_gradient = -9999

    def accumulate_connected_surface_area(self):
        """For each pipe in the network, accumulate downstream connected area"""

        sink_nodes = [n for n, d in self.network.in_degree() if d == 0]
        tank_nodes = [n for n, d in self.network.out_degree() if d == 0]

        out_degree_nodes = self.network.out_degree()

        # We assume that pipe flow enters at the starting node of each pipe
        for edge in self.network.edges:
            pipe = self.get_pipe_with_edge(edge)
            end_node = edge[1]
            attrs = {
                end_node: {
                    "connected_area": pipe.connected_surface_area
                    + self.network.nodes[end_node]["connected_area"]
                }
            }
            nx.set_node_attributes(self.network, attrs)
            edge_attrs = {edge: {"connected_surface_area": pipe.connected_surface_area}}
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
                edge_flow = (
                    self.network.nodes[node]["connected_area"]
                    + self.network.edges[edge]["connected_surface_area"]
                )
                attrs = {edge: {"accumulated_connected_area": edge_flow}}
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
        """Find all connected upstream pipes in the network from a starting node
        This is a depth first search. https://www.programiz.com/dsa/graph-dfs#:~:text=Depth%20First%20Search%20Example&text=We%20use%20an%20undirected%20graph%20with%205%20vertices.&text=We%20start%20from%20vertex%200,adjacent%20vertices%20in%20the%20stack.&text=Next%2C%20we%20visit%20the%20element,go%20to%20its%20adjacent%20nodes.
        """
        upstream_edges = nx.edge_dfs(self.network, node, orientation="reverse")
        upstream_pipes = []
        for edge in upstream_edges:
            edge = (edge[0], edge[1])
            pipe = self.get_pipe_with_edge(edge)
            upstream_pipes.append(pipe)

        return upstream_pipes

    def find_downstream_sections(self, section):
        sections = []
        pipes = self.find_downstream_pipes(section.upstream_node)
        for pipe in pipes:
            if pipe.fid in self.pipe_sections_lookup:
                section_id = self.pipe_sections_lookup[pipe.fid]
                if section_id not in sections and not section_id == section.id:
                    sections.append(section_id)

        return list(set(sections))

    def find_downstream_sections_to_weir(self, section, sections):
        section_ids = self.find_downstream_sections(section)
        section_ids.sort(reverse=True)  # upstream to downstream
        weir_sections = []
        for sid in section_ids:
            match = [s for s in sections if s.id == sid]
            if len(match) > 0:
                weir_sections.append(match[0])
                if match[0].to_downstream_weir:
                    break

        weir_sections.reverse()  # downstream to upstream
        weir_sections.append(section)
        return weir_sections

    def find_pipes_with_node(self, node, in_edge=True, out_edge=True):
        edges = []
        if in_edge:
            edges.extend(list(self.network.in_edges(node)))

        if out_edge:
            edges.extend(list(self.network.out_edges(node)))
        return [self.get_pipe_with_edge(e) for e in edges]

    def find_closest_weir(self, node):
        """Get the distance to the closest weir from a node in the network"""

        distance = np.inf
        closest_weir = None
        for weir in self.weirs.values():
            weir_node = weir._node_coordinate
            try:
                distance_to_weir = nx.shortest_path_length(
                    G=self.network, source=node, target=weir_node, weight="length"
                )
                if distance_to_weir < distance:
                    distance = distance_to_weir
                    closest_weir = weir
            except nx.NetworkXNoPath:
                continue

        return distance, closest_weir

    def find_weir_on_pipe(self, pipe: Pipe):
        """returns weirs if found on a pipe
        Chris, 28-04-2022: This most likely can be done with NetworkX,
        But due to time constraints we solve it with python.
        """
        return [w for w in self.weirs.values() if w.node in pipe.nodes]

    def split_into_sections(self, external_weir, freeboard=0.2):
        """Splits the list of pipes in sections:
            - Interweirs.
            - Intersections.
            - Endpoints.

        The idea is that all the pipes in the section have an equal gradient.

        Also adds a lot data which is used in gradient estimation.


        """
        upstream = PipeSection(self.find_upstream_pipes(external_weir.node))

        sections = []
        used_weirs = [external_weir]
        pipes = []
        list_of_branches = []
        for pipe in upstream:

            weirs = self.find_weir_on_pipe(pipe)

            # It is internal if the section has a beginning and an
            # end in the same system.
            # Internal can be:
            #                   - weir to weir
            #                   convered by looking at a new weir.
            #                   - pipe to weir
            #                   This is actually a branch
            #                   - weir to pipe
            #                   This is covered by looking at a new part.
            #                   - pipe intersection to pipe intersection.

            internal = False
            to_weir = False
            to_pipe = False
            from_pipe = False
            from_weir = False
            pipe_node = None
            last = False

            # Internal - weir to weir when only one pipe.
            # We expect one weir to be used already.
            multiple_weirs = len(weirs) == 2
            if multiple_weirs:
                for internal_weir in weirs:
                    if internal_weir.fid in [w.fid for w in used_weirs]:
                        start_weir = internal_weir  # first pipe of a new section.
                    else:
                        end_weir = internal_weir

                internal = True
                to_weir = True
                from_weir = True
                used_weirs.append(end_weir)

            # Internal - weir to pipe when only one pipe.
            # This should base defined as
            # Normally weir should be on the crossing, so skipped for now.
            # if len(weirs) == 1:
            #     used_weir = weirs[0].fid in [w.fid for w in used_weirs]

            # Internal - pipe to weir when only one pipe.
            # Unlikely, so skipped for now.

            # Internal - weir to weir and pipe to weir for multiple pipes.
            # By going upstream, the first weir should be already used.
            # The a few pipes pass which have no weirs.
            # Eventally we'll come across a weir which is the eind weir.
            # So therefore, it covers both weir to weir and pipe to weir section.
            if not internal:
                for internal_weir in weirs:
                    if internal_weir.fid in [w.fid for w in used_weirs]:
                        start_weir = internal_weir  # first pipe of a new section.
                    else:
                        internal = True
                        end_weir = internal_weir
                        to_weir = True
                        used_weirs.append(internal_weir)

            # Internal - weir to pipe for multiple pipes.
            # The pipe starts at the end of another internal section,
            # which is always a weir.
            # If the following pipes intersect with a pipe, we call it a section.
            if not internal and len(pipes) > 0:
                for section in sections:
                    pipe_node = section.intersects_pipe(pipe)
                    if pipe_node:
                        internal = True
                        to_pipe = True
                        end_weir = None
                        break

            # Internal - Pipe intersection
            # This is notable different than 'Internal weir to pipe'.
            # This is not happening halfway.
            if not internal:
                intersects = self.find_pipes_with_node(pipe.start_node)
                if len(intersects) > 2:
                    internal = True
                    to_pipe = True
                    end_weir= None

            # Find out if last.
            # Something is last if there are no upstream things.
            if len(self.distance_matrix_reversed[pipe.start_node][0]) == 1:
                last = True
            elif len(self.distance_matrix_reversed[pipe.end_node][0]) == 1:
                last = True

            # Note that last is absolute, if something starts off as internal
            # But is then found to be last by this function, it will be last.
            if last:
                internal = False

            pipes.append(pipe)

            # Some administration to find out where the section comes from.
            if (internal or last) and not multiple_weirs:
                from_pipe = False
                from_weir = True
                used_nodes = [w.node for w in used_weirs]
                for section in sections:
                    pipe_node = section.intersects_pipe(pipes[0])
                    if pipe_node and pipe_node not in used_nodes:
                        from_pipe = True
                        from_weir = False

            if internal:
                section = PipeSection(pipes)
                section.internal = True
                section.last = False
                section.from_upstream_weir = to_weir
                section.from_upstream_pipe = to_pipe
                section.to_downstream_pipe = from_pipe
                section.to_downstream_weir = from_weir
                section.downstream_weir = start_weir
                section.upstream_weir = end_weir
                section.pipe_node = pipe_node
                if end_weir:
                    section.upstream_weir_elevation = (
                        end_weir.weir_level + end_weir.crest_flow_depth
                    )
                if start_weir:
                    section.downstream_weir_elevation = (
                        start_weir.weir_level + start_weir.crest_flow_depth
                    )

                pipes = []
                list_of_branches.append("internal")

            if last:
                section = PipeSection(pipes)
                section.internal = False
                section.last = True
                section.upstream_weir = None
                section.from_upstream_weir = to_weir  # Is always false, because we end.
                section.from_upstream_pipe = to_pipe  # always false due to one section.
                section.to_downstream_pipe = from_pipe
                section.to_downstream_weir = from_weir
                section.downstream_weir = start_weir
                if start_weir:
                    section.downstream_weir_elevation = (
                        start_weir.weir_level + start_weir.crest_flow_depth
                    )
                list_of_branches.append("last")
                pipes = []

            # A branch tells us that a new non-consecutive section is present.
            # Branching happens because of the nature of
            # reverse first-depth searching in NetworkX (search it).
            # This is usefull, because we want to know when to recalculate the
            # hydraulic head.
            if last or internal:
                section.drowned = False

                section.branch = False
                if len(sections) >= 1:
                    section.branch = (
                        sections[-1].upstream_node != section.downstream_node
                    )

                section.freeboard = freeboard

                sections.append(section)

        for i, section in enumerate(sections):
            section.id = i + 1  # from one

        self.pipe_sections_lookup = {}
        for section in sections:
            for pipe in section.pipes:
                self.pipe_sections_lookup[pipe.fid] = section.id

        return self.reorder_sections_upstream(sections, external_weir)

    def reorder_sections_upstream(self, sections, external_weir):
        """The current sections have depth-first searching order.
        Which is fine for creating sections. But is not a perferct
        downstream upstream order.
        Here we find all internal sections and put them in order by
        looking at the distance to the first section.
        Assumption is that a longer length == more upstream.


        """

        # retrieve the end_pipe of each section and calculate the distance
        # towards the begin
        upstream = []
        for section in sections:
            section.external_weir_distance_downstream = self.distance(
                external_weir.node, section.downstream_node
            )
            section.external_weir_distance_upstream = self.distance(
                external_weir.node, section.upstream_node
            )

            section.external_weir_gradient = (
                section.maximum_elevation - external_weir.flow_level
            ) / section.external_weir_distance_upstream
            upstream.append(section)
        upstream.sort(key=lambda sec: sec.external_weir_distance_upstream)

        # reset ids
        new = []
        i = 0
        for section in upstream:
            if section.internal:
                i += 1
                section.id = i
                new.append(section)

        for section in upstream:
            if section.last:
                i += 1
                section.id = i
                new.append(section)

        self.pipe_sections_lookup = {}
        for section in new:
            for pipe in section.pipes:
                self.pipe_sections_lookup[pipe.fid] = section.id

        return new

    def draw_network(self, node_label_attr, edge_label_attr):

        G = self.network.copy()
        for edge in G.edges:
            pipe = self.get_pipe_with_edge(edge)
            attr = getattr(pipe, edge_label_attr)
            if isinstance(attr, float):
                attr = round(attr, 2)
            attrs = {edge: {edge_label_attr: attr}}
            nx.set_edge_attributes(G, attrs)

        node_labels = nx.get_node_attributes(G, node_label_attr)
        pos = nx.get_node_attributes(G, "position")
        nx.draw(
            G,
            pos,
            edge_color="black",
            width=1,
            linewidths=1,
            node_size=100,
            node_color="pink",
            alpha=0.9,
            labels=node_labels,
        )

        edge_labels = nx.get_edge_attributes(G, edge_label_attr)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    def validate_network_diameters(self):
        # TODO Walk the network and determine that there are no decreases in diameter
        pass


class StormWaterPipeNetwork(PipeNetwork):

    def __init__(self):
        super().__init__()
        self.network_type = "infiltratieriool"

    def calculate_cover_depth(self):
        """Determine the depth"""

        undirected_network = self.network.to_undirected()
        #TODO undirected_network unused, in fact does not work for retrieving subgraphs, what to do with it?
        subgraphs = (self.network.subgraph(c) for c in nx.weakly_connected_components(self.network))

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

            if network_pipes:
                max_diameter = max([pipe.diameter for pipe in network_pipes])
            else:
                print(f"DiGraph is invalid, we cannot validate depth. "
                      f"subgraph_edges = {subgraph.edges}, "
                      f"subgraph_nodes = {subgraph.nodes}")
                # TODO how is this possible? is this user input that should be improved? if so improve checkers

            for pipe in network_pipes:
                material_thickness = MATERIAL_THICKNESS[pipe.material]
                pipe.start_level = lowest_weir_height - max_diameter
                pipe.end_level = lowest_weir_height - max_diameter
                invert_level = max(pipe.start_level, pipe.end_level)
                cover_depth = pipe.lowest_elevation - (
                    invert_level + pipe.diameter + material_thickness * 2
                )
                pipe.cover_depth = cover_depth

    def check_invert_levels(self):
        for pipe in self.pipes.values():
            if pipe.invert_level_start > pipe.minimum_cover_depth:
                raise ValueError(
                    "Pipe invert level is too high, invert level: {}, minimum invert level: {}".format(
                        pipe.invert_level_start, pipe.minimum_cover_depth
                    )
                )

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
