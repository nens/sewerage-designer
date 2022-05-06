import inspect
from osgeo import ogr, gdal
import networkx as nx
from qgis.core import QgsFeature, QgsVectorLayer, QgsWkbTypes
from PyQt5.QtCore import QVariant
from qgis.core.additions.edit import edit

from sewerage_designer_core.sewerage_designer_classes import (
    Pipe,
    Outlet,
    Weir,
    PumpingStation,
    StormWaterPipeNetwork,
    WasteWaterPipeNetwork,
)
from sewerage_designer_core.constants import *

ogr.UseExceptions()


class SewerageDesignerQgsConnector:
    def __init__(self):
        pass


def pipe_from_feature(feature: QgsFeature):
    fid = feature.id()
    geom = feature.geometry()
    wkb_type = geom.wkbType()
    types_in_text = dict(
        [(v, k) for k, v in QgsWkbTypes.__dict__.items() if isinstance(v, int)]
    )
    wkb_type_text = types_in_text.get(wkb_type)

    if (not geom.type() == QgsWkbTypes.LineGeometry) or geom.isMultipart():
        raise ValueError(
            f"Invalid geometry type: {wkb_type_text} for pipe with id {fid}. Pipes should be singlepart line geometries."
        )

    wkt_geometry = feature.geometry().asWkt()
    pipe_signature = inspect.signature(Pipe).parameters
    pipe = Pipe(wkt_geometry=wkt_geometry, fid=fid)
    for variable, parameter in pipe_signature.items():
        if variable != "wkt_geometry":
            qgis_feature = feature[variable]
            if isinstance(qgis_feature, QVariant):
                value = None
            else:
                value = qgis_feature
            setattr(pipe, variable, value)

    return pipe


def outlet_from_feature(feature: QgsFeature):
    wkt_geometry = feature.geometry().asWkt()
    outlet_signature = inspect.signature(Outlet).parameters
    outlet = Outlet(wkt_geometry=wkt_geometry)

    for variable, parameter in outlet_signature.items():
        if variable != "wkt_geometry":
            qgis_feature = feature[variable]
            if isinstance(qgis_feature, QVariant):
                value = None
            else:
                value = qgis_feature
            setattr(outlet, variable, value)

    return outlet


def weir_from_feature(feature: QgsFeature):

    wkt_geometry = feature.geometry().asWkt()
    weir_signature = inspect.signature(Weir).parameters
    weir = Weir(wkt_geometry=wkt_geometry)

    for variable, parameter in weir_signature.items():
        if variable != "wkt_geometry":
            qgis_feature = feature[variable]
            if isinstance(qgis_feature, QVariant):
                value = None
            else:
                value = qgis_feature
            setattr(weir, variable, value)

    return weir


def pumping_station_from_feature(feature: QgsFeature):
    wkt_geometry = feature.geometry().asWkt()
    pumping_station_signature = inspect.signature(Pipe).parameters
    pumping_station = PumpingStation(wkt_geometry=wkt_geometry)

    for variable, parameter in pumping_station_signature.items():
        if variable != "wkt_geometry":
            qgis_feature = feature[variable]
            if isinstance(qgis_feature, QVariant):
                value = None
            else:
                value = qgis_feature
            setattr(pumping_station, variable, value)

    return pumping_station


"""
def update_qgs_feature(layer, feature_id, attribute, attribute_value):
    provider = layer.dataProvider()
    updateMap = {}
    fieldIdx = provider.fields().indexFromName( 'attr' )
    features = provider.getFeatures()
    for feature in features:
        updateMap[feature.id()] = { fieldIdx: 'a' }

    provider.changeAttributeValues( updateMap )
"""


def get_feature_count(layer):
    count = layer.featureCount()
    if count > 0:
        not_zero = True
    else:
        not_zero = False
    return count, not_zero


def get_features(layer):
    features = layer.getFeatures()
    return features


def check_sewer_type(pipe_features):
    sewerage_types = {feature["sewerage_type"] for feature in pipe_features}
    if len(sewerage_types) > 1:
        raise ValueError("Multiple sewerage types in layer")
    sewerage_type = sewerage_types.pop()
    return sewerage_type


def validate_network(network):
    # Check for loops in the network
    pipes_in_loop = []
    cycles = nx.simple_cycles(network.network)
    if sum(1 for _ in cycles) > 0:
        cycles = nx.simple_cycles(network.network)
        for cycle in cycles:
            for i in range(0, len(cycle) - 1):
                edge = (cycle[i], cycle[i + 1])
                pipe = network.get_pipe_with_edge(edge)
                pipes_in_loop += [pipe.fid]

    # Check if all pipes in the network are connected to a weir
    # If not, this will break the hydraulic gradient calculation
    pipes_without_weir = []
    for edge in network.network.edges():
        end_node = edge[1]
        distance, weir = network.find_closest_weir(end_node)
        if weir is None:
            pipe = network.get_pipe_with_edge(edge)
            pipes_without_weir += [pipe.fid]

    return pipes_in_loop, pipes_without_weir


def create_sewerage_network(
    pipe_layer, weir_layer, pumping_station_layer, outlet_layer
):
    """
    Assumptions:
    Pipes in the layer form a single network with one type
    StormWaterNetwork should have atleast one weir and one pipe
    WasteWaterNetwork should have atleast one weir or outlet and one pipe

    Funtion:
    count number of features per layer
    check if n features is 0
    check type of sewer system
    check if necessary layers have features (n feature is not 0)
    get pipe network
    add layers to pipe network if count of features is not 0
    """

    n_pipes, n_pipes_not_zero = get_feature_count(pipe_layer)
    n_weirs, n_weirs_not_zero = get_feature_count(weir_layer)
    n_pumping_stations, n_pumping_stations_not_zero = get_feature_count(
        pumping_station_layer
    )
    n_outlets, n_outlets_not_zero = get_feature_count(outlet_layer)

    if n_pipes_not_zero:
        pipe_features = get_features(pipe_layer)
        sewerage_type = check_sewer_type(pipe_features)
    else:
        raise ValueError("Sewerage should have pipe features.")

    if sewerage_type in [HEMELWATERRIOOL, INFILTRATIEVOORZIENING, VGS_HEMELWATERRIOOL]:
        if n_weirs_not_zero:
            network = StormWaterPipeNetwork()
        else:
            raise ValueError("Sewerage should have weir features.")
    elif sewerage_type in [GEMENGD_RIOOL, VUILWATERRIOOL]:
        if n_weirs_not_zero or n_outlets_not_zero:
            network = WasteWaterPipeNetwork()
        else:
            raise ValueError(
                "Sewerage should have weir or outlet features."
            )  # TODO: is this true?
    else:
        raise ValueError("Invalid sewerage type")

    pipe_features = get_features(pipe_layer)
    for feature in pipe_features:
        pipe = pipe_from_feature(feature)
        network.add_pipe(pipe)
    if n_outlets_not_zero:
        outlet_features = get_features(outlet_layer)
        for feature in outlet_features:
            outlet = outlet_from_feature(feature)
            network.add_outlet(outlet)
    if n_weirs_not_zero:
        weir_features = get_features(weir_layer)
        for feature in weir_features:
            weir = weir_from_feature(feature)
            network.add_weir(weir)
    if n_pumping_stations_not_zero:
        pumping_station_features = get_features(pumping_station_layer)
        for feature in pumping_station_features:
            pumping_station = pumping_station_from_feature(feature)
            network.add_pumping_station(pumping_station)

    network.add_id_to_nodes()
    pipes_in_loop, pipes_without_weir = validate_network(network)

    if len(pipes_in_loop) > 0 or len(pipes_without_weir) > 0:
        fault_network = True
    else:
        fault_network = False

    return network, pipes_in_loop, pipes_without_weir, fault_network


def update_field(layer, feature, field, value):
    feature[field] = value
    layer.updateFeature(feature)


def core_to_layer(network, layer):
    """writes all changed fields of network python object back to QGIS sewerage layer"""
    empty_accumulated_fields = []
    fields = layer.fields().names()
    with edit(layer):
        for field in fields:
            if field == "connected_surface_area":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.connected_surface_area is not None and feature_update:
                        update_field(
                            layer,
                            feature,
                            field,
                            round(float(pipe.connected_surface_area), 2),
                        )
            elif field == "accumulated_connected_surface_area":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    val = [None, 0]
                    if (
                        pipe.accumulated_connected_surface_area not in val
                        and feature_update
                    ):
                        update_field(
                            layer,
                            feature,
                            field,
                            round(float(pipe.accumulated_connected_surface_area), 2),
                        )
                    else:
                        empty_accumulated_fields.append(feature_fid)
            elif field == "max_hydraulic_gradient":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.max_hydraulic_gradient is not None and feature_update:
                        update_field(
                            layer,
                            feature,
                            field,
                            round(float(pipe.max_hydraulic_gradient), 5),
                        )
            elif field == "diameter":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.diameter is not None and feature_update:
                        update_field(layer, feature, field, float(pipe.diameter))
            elif field == "discharge":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.discharge is not None and feature_update:
                        update_field(
                            layer, feature, field, round(float(pipe.discharge), 5)
                        )
            elif field == "material":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.material is not None and feature_update:
                        update_field(layer, feature, field, pipe.material)
            elif field == "velocity":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.velocity is not None and feature_update:
                        update_field(
                            layer, feature, field, round(float(pipe.velocity), 3)
                        )
            elif field == "cover_depth":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.cover_depth is not None and feature_update:
                        update_field(
                            layer, feature, field, round(float(pipe.cover_depth), 2)
                        )
            elif field == "end_level":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.end_level is not None and feature_update:
                        update_field(
                            layer, feature, field, round(float(pipe.end_level), 2)
                        )
            elif field == "start_level":
                features = get_features(layer)
                for feature in features:
                    feature_fid = feature["fid"]
                    feature_update = feature["update"]
                    pipe = network.pipes[feature_fid]
                    if pipe.start_level is not None and feature_update:
                        update_field(
                            layer, feature, field, round(float(pipe.start_level), 2)
                        )
    return empty_accumulated_fields
