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

from .colebrook_white import ColebrookWhite
from .utils import get_intermediates

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


class Weir:

    # Line geometry
    def __init__(self):
        self.height = None


class Outlet:
    def __init__(self, feature):
        property_json = json.loads(feature.ExportToJson())["properties"]
        self.ditch_level = property_json["ditch_level"]
        self.id = property_json["id"]
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



class GPKGDatabase:
    
    def __init__(self):
        pass
    
    def load_layer(self, layer):
        pass
    
    def set_field(self, layer, field, value):
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
        """sets the table if not exists"""
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

    def get_surface_area_for_pipe_id(self, pipe_id, pipe_type):
        """
        get the connected surface area for a pipe id
         determine all connected upstream pipes as well
        """

        pipe_type_codes = self._table["pipe_code_" + pipe_type]

        surface_areas = []
        for i, code in enumerate(pipe_type_codes):
            if code == pipe_id:
                bgt_identificatie = self._table["bgt_identificatie"][i]

                if bgt_identificatie not in self.connected_surfaces:
                    surface_area_bgt = self._table["surface_area"][i]
                    surface_fraction = self._table[pipe_type][i] / 100
                    connected_area = surface_area_bgt * surface_fraction

                    surface_areas.append(connected_area)
                    self.connected_surfaces.append(bgt_identificatie)

        surface_sum = sum(surface_areas)

        return surface_sum


class Pipe:

    def __init__(
            self,
            parent,
            wkb_geometry,
            diameter: float = None,
            start_level: float = None,
            end_level: float = None,
            material: str = None,
            connected_surface_area: float = None,
            sewerage_type: str = None,
            cover_depth: float = None,
            discharge: float = None,
            velocity: float = None
    ):
        if isinstance(parent, PipeNetwork):
            self.parent = parent
        else:
            raise TypeError('parent is not a PipeNetwork')
        self.geometry = ogr.CreateGeometryFromWkb(wkb_geometry)
        self.diameter = diameter
        self.start_level = start_level
        self.end_level = end_level
        self.material = material
        self.connected_surface_area = connected_surface_area
        self.sewerage_type = sewerage_type
        self.cover_depth = cover_depth
        self.discharge = discharge
        self.velocity = velocity

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

    @property
    def dem_datasource(self):
        return self.parent.dem_datasource

    @property
    def dem_rasterband(self):
        return self.parent.dem_rasterband

    @property
    def dem_geotransform(self):
        return self.parent.dem_geotransform

    def calculate_elevation(self):
        dem_no_data_value = self.dem_rasterband.GetNoDataValue()

        pipe_source_coordinates = self.start_coordinate
        pipe_target_coordinates = self.end_coordinate

        gt = self.dem_geotransform
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
            elevation = self.dem_rasterband.ReadAsArray(point[0], point[1], 1, 1)[0][0]
            if elevation == dem_no_data_value:
                elevation = None
            dem_elevation.append(elevation)

        # TODO @Emile wouldn't it make more sense to mek dem_elevation a hidden attribute (self._dem_elevation) and
        # start_elevation, end_elevation and lowest_elevation read-only properties (@property)?
        # this would also allow us to calculate _dem_elevation if it is None when start_elevation etc. are requested
        self.start_elevation = dem_elevation[0]
        self.end_elevation = dem_elevation[-1]
        self.lowest_elevation = min(dem_elevation)

    def calculate_discharge(self, design_rain):

        # TODO tijdstap omrekeken
        # TODO netwerkanalyse discharge

        if design_rain in AREA_WIDE_RAIN.keys():
            design_rain_pattern = AREA_WIDE_RAIN[design_rain]
        else:
            raise KeyError("Selected design rain not availabe")

        max_intensity = max(design_rain_pattern)
        pipe_discharge = self.connected_surface_area * (
            (max_intensity / 1000) / DESIGN_RAIN_TIMESTEP
        )
        
        self.discharge = pipe_discharge

    def calculate_diameter(self):

        """
        Use the Colebrook White method to esimate the diameters
        """

        colebrook_white = ColebrookWhite(
            q=self.discharge, Smax=self.max_hydraulic_gradient
        )

        estimated_diameter = colebrook_white.iterate_diameters()
        self.diameter = estimated_diameter

    def set_material(self):

        if self.diameter is not None:
            if self.diameter < 0.315:
                self.material = "PVC"
            else:
                self.material = "Concrete"

    def calculate_minimum_cover_depth(self, minimal_cover_depth):

        material_thickness = MATERIAL_THICKNESS[self.material]
        minimum_cover_depth = self.lowest_elevation - (
            minimal_cover_depth + self.diameter + material_thickness
        )
        self.minimum_cover_depth = minimum_cover_depth

    def validate(self):
        if len(self.points) != 2:
            raise InvalidGeometryException

    def write_properties_to_feature(self):        
        for key in self.properties.keys():
            value = getattr(self, key)
            self.feature.SetField(key, value)
    



class PipeNetwork:
    def __init__(self, parent):
        self.parent = parent
        self.network = nx.DiGraph()
        self.sewerage_type = None
        self.outlet_level = None
        self.pipes = {}

    @property
    def dem_datasource(self):
        return self.parent.dem_datasource

    @property
    def dem_rasterband(self):
        return self.parent.dem_rasterband

    @property
    def dem_geotransform(self):
        return self.parent.dem_geotransform

    def add_pipe(self, pipe: Pipe):

        # Add pipe to the networkx DiGraph
        # Also save pipes to dictionary
        self.pipes[pipe.id] = pipe

        if pipe.start_coordinate not in self.network.nodes:
            self.network.add_node(pipe.start_coordinate, type="manhole")

        if pipe.end_coordinate not in self.network.nodes:
            self.network.add_node(pipe.end_coordinate, type="manhole")

        self.network.add_edge(
            pipe.start_coordinate,
            pipe.end_coordinate,
            id=pipe.id,
            length=pipe.geometry.Length(),
        )

    def calculate_max_hydraulic_gradient(self, outlet_node, waking):

        """ "
        Calculates the max hydraulic gradient based on the network end point and start/end elevation
        The max hydraulic gradient is defined as the maximum difference in elevation between the endpoint of the network
        and the furthest node divided by the distance between the two
        Assign this back to all the pipes in the network
        """

        # TODO waking over gehele trace berekenen
        # TODO aanpassen hydraulische gradient op basis van evaluatie

        distance_matrix = dict(
            nx.all_pairs_dijkstra(self.reverse_network, weight="length")
        )

        # Get the distance dictionary for the end node
        distance_dictionary = distance_matrix[outlet_node][0]
        furthest_node, distance = list(distance_dictionary.items())[-1]
        furthest_edge = self.network.edges(furthest_node, data=True)
        furthest_pipe = self.get_pipe_with_edge(furthest_edge)

        max_hydraulic_gradient = (
            (furthest_pipe.start_elevation + waking) - self.outlet_level
        ) / distance

        for pipe in self.pipes:
            setattr(self.pipes[pipe], "max_hydraulic_gradient", max_hydraulic_gradient)

    def determine_connected_surface_area_totals(self, bgt_inlooptabel: BGTInloopTabel):

        pipe_connected_surface = {}
        for pipe_id, pipe in self.pipes.items():
            connected_surface_area = bgt_inlooptabel.get_surface_area_for_pipe_id(
                pipe_id=str(pipe.id), pipe_type=pipe.sewerage_type
            )
            pipe_connected_surface[pipe.id] = connected_surface_area

        for edge in self.network.edges:
            pipe = self.get_pipe_with_edge(edge)
            if getattr(pipe, "connected_surface_area") is None:
                start_node = edge[0]
                upstream_pipes = self.find_upstream_pipes(start_node)
                upstream_pipes.append(pipe)
                pipe_total_connected_surface = sum(
                    [pipe_connected_surface[pipe.id] for pipe in upstream_pipes]
                )
                setattr(pipe, "connected_surface_area", pipe_total_connected_surface)

    def add_id_to_nodes(self):
        for i, node in enumerate(self.network.nodes):
            self.network.nodes[node]["id"] = i

    def get_pipe_with_edge(self, edge):

        if not isinstance(edge, nx.classes.reportviews.OutEdgeDataView):
            edge = self.network.edges(edge, data=True)

        edge_data = list(edge)[0][2]
        edge_id = edge_data["id"]
        pipe = self.pipes[edge_id]
        return pipe

    def find_upstream_pipes(self, node):

        """
        Find all connected upstream pipes in the network from a starting node
        """

        upstream_edges = nx.edge_dfs(self.network, node, orientation="reverse")
        upstream_pipes = []
        for edge in upstream_edges:
            pipe = self.get_pipe_with_edge(edge)
            upstream_pipes.append(pipe)

        return upstream_pipes

    def validate_network_diameters(self):
        # TODO Walk the network and determine that there are no decreases in diameter
        pass

    def create_result_layer(self):
        pass

    @property
    def reverse_network(self):
        return self.network.reverse()


class StormWaterPipeNetwork(PipeNetwork):
    # TODO maybe rename to StormWaterPipeNetwork
    def __init__(self, parent):
        super().__init__(parent)
        self.network_type = "infiltratieriool"

    def calculate_required_cover_depth(self):
        # For IT network the gradient of the pipes is 0, find the highest possible solution
        lowest_cover_depth_network = min(
            pipe.minimum_cover_depth for pipe in self.pipes.values()
        )

        for pipe in self.pipes.values():            
            if pipe.invert_level_start is None:            
                pipe.invert_level_start = lowest_cover_depth_network
            if pipe.invert_level_end is None:
                pipe.invert_level_end = lowest_cover_depth_network

    def add_weir(weir: Weir):
        pass

    def estimate_internal_weir_locations(self):
        #TODO  For a given network and elevation model, determine the best locations to install weirs
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
