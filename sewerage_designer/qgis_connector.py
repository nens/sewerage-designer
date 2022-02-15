import inspect
from osgeo import ogr,gdal
from qgis.core import QgsFeature, QgsVectorLayer
from PyQt5.QtCore import QVariant
from qgis.core.additions.edit import edit

from sewerage_designer_core.sewerage_designer_classes import Pipe,Outlet,Weir,PumpingStation,StormWaterPipeNetwork,WasteWaterPipeNetwork
from sewerage_designer_core.constants import *

ogr.UseExceptions()

class SewerageDesignerQgsConnector:
    def __init__(self):
        pass

def pipe_from_feature(feature: QgsFeature):
    wkt_geometry = feature.geometry().asWkt()
    pipe_signature = inspect.signature(Pipe).parameters
    pipe = Pipe(wkt_geometry=wkt_geometry)
    
    for variable, parameter in pipe_signature.items():
        if variable != 'wkt_geometry':
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
        if variable != 'wkt_geometry':
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
        if variable != 'wkt_geometry':
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
        if variable != 'wkt_geometry':
            qgis_feature = feature[variable]
            if isinstance(qgis_feature, QVariant):
                value = None
            else:
                value = qgis_feature
            setattr(pumping_station, variable, value)
    
    return pumping_station

'''
def update_qgs_feature(layer, feature_id, attribute, attribute_value):
    provider = layer.dataProvider()
    updateMap = {}
    fieldIdx = provider.fields().indexFromName( 'attr' )
    features = provider.getFeatures()
    for feature in features:
        updateMap[feature.id()] = { fieldIdx: 'a' }

    provider.changeAttributeValues( updateMap )    
'''
def get_feature_count(layer):
    count=layer.featureCount()
    if count>0:
        not_zero=True
    else:
        not_zero=False
    return count,not_zero

def get_features(layer):
    features=layer.getFeatures()
    return features

def check_sewer_type(pipe_features):
    sewerage_types = {feature['sewerage_type'] for feature in pipe_features}
    if len(sewerage_types) > 1:
        raise ValueError('Multiple sewerage types in layer')
    sewerage_type = sewerage_types.pop()        
    return sewerage_type

def create_sewerage_network(pipe_layer,weir_layer,pumping_station_layer,outlet_layer):
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
    
    n_pipes,n_pipes_not_zero=get_feature_count(pipe_layer)
    n_weirs,n_weirs_not_zero=get_feature_count(weir_layer)
    n_pumping_stations,n_pumping_stations_not_zero=get_feature_count(pumping_station_layer)
    n_outlets,n_outlets_not_zero=get_feature_count(outlet_layer)
    
    if n_pipes_not_zero:
        pipe_features=get_features(pipe_layer)
        sewerage_type=check_sewer_type(pipe_features)
    else:
        raise ValueError('Sewerage should have pipe features.')
        
    if sewerage_type in [HEMELWATERRIOOL, INFILTRATIEVOORZIENING, VGS_HEMELWATERRIOOL]:
        if n_weirs_not_zero:
            network = StormWaterPipeNetwork()
        else:
            raise ValueError('Sewerage should have weir features.')
    elif sewerage_type in [GEMENGD_RIOOL, VUILWATERRIOOL]:
        if n_weirs_not_zero or n_outlets_not_zero:
            network = WasteWaterPipeNetwork()
        else:
            raise ValueError('Sewerage should have weir or outlet features.')      #TODO: is this true?       
    else:
        raise ValueError('Invalid sewerage type')
    
    pipe_features=get_features(pipe_layer)
    for feature in pipe_features:
        pipe = pipe_from_feature(feature)
        network.add_pipe(pipe)
    if n_outlets_not_zero:
        outlet_features=get_features(outlet_layer)
        for feature in outlet_features:
            outlet = outlet_from_feature(feature)
            network.add_outlet(outlet)
    if n_weirs_not_zero:
        weir_features=get_features(weir_layer)
        for feature in weir_features:
            weir = weir_from_feature(feature)
            network.add_weir(weir)
    if n_pumping_stations_not_zero:
        pumping_station_features=get_features(pumping_station_layer)
        for feature in pumping_station_features:
            pumping_station = pumping_station_from_feature(feature)
            network.add_pumping_station(pumping_station)
    
    network.add_id_to_nodes()
    return network

def update_field(layer,feature,field,value):
    feature[field]=value
    layer.updateFeature(feature)

def core_to_layer(network,layer):
    """writes all changed fields of network python object back to QGIS sewerage layer
    """
    fields=layer.fields().names()
    with edit(layer):
        for field in fields:
            if field=='connected_surface_area':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,round(float(pipe.connected_surface_area),2))
                    print(float(pipe.connected_surface_area))
            elif field=='accumulated_connected_surface_area':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,round(float(pipe.accumulated_connected_surface_area),2))
                    print(float(pipe.accumulated_connected_surface_area))
            elif field=='max_hydraulic_gradient':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,round(float(pipe.max_hydraulic_gradient),5))
                    print(float(pipe.max_hydraulic_gradient))
            elif field=='diameter':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,float(pipe.diameter))
                    print(float(pipe.diameter))
            elif field=='discharge':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,round(float(pipe.discharge),5))
                    print(float(pipe.discharge))
            elif field=='material':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,pipe.material)
                    print(pipe.material)
            elif field=='velocity':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,round(float(pipe.velocity),3))
                    print(float(pipe.velocity))
            elif field=='cover_depth':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,round(float(pipe.cover_depth),2))
                    print(float(pipe.cover_depth))
            elif field=='end_level':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,round(float(pipe.end_level),2))
                    print(float(pipe.end_level))
            elif field=='start_level':
                print(field)
                features=get_features(layer)
                for feature in features:
                    feature_fid = feature['fid']
                    pipe = network.pipes[feature_fid]
                    update_field(layer,feature,field,round(float(pipe.start_level),2))
                    print(float(pipe.start_level))

