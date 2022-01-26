from osgeo import ogr
from qgis.core import QgsFeature, QgsVectorLayer

from sewerage_designer_core.sewerage_designer_classes import Pipe, Weir,StormWaterPipeNetwork, WasteWaterPipeNetwork
from sewerage_designer_core.constants import *

ogr.UseExceptions()

class SewerageDesignerQgsConnector:
    def __init__(self):
        pass


def pipe_from_feature(feature: QgsFeature):
    wkt_geometry = feature.geometry().asWkt()

    return Pipe(
        wkt_geometry,
        feature['fid'],
        feature['diameter'],
        feature['start_level'],
        feature['end_level'],
        feature['material'],
        feature['connected_surface_area'],
        feature['sewerage_type'],
        feature['cover_depth'],
        feature['discharge'],
        feature['velocity']
    )

def weir_from_feature(feature: QgsFeature):
    wkt_geometry = feature.geometry().asWkt()

    return Weir(
        wkt_geometry,
        feature['fid'],
        feature['weir_level'],
        feature['surface_elevation'],
        feature['freeboard'],
        feature['pipe_in_id'],
        feature['pipe_out_id'],
        feature['hydraulic_head']
    ) 

    
def update_qgs_feature(layer, feature_id, attribute, attribute_value):
    provider = layer.dataProvider()
    updateMap = {}
    fieldIdx = provider.fields().indexFromName( 'attr' )
    features = provider.getFeatures()
    for feature in features:
        updateMap[feature.id()] = { fieldIdx: 'a' }

    provider.changeAttributeValues( updateMap )    

def pipe_network_from_layer(pipe_layer, weir_layer):
    # Assumptions: pipes in the layer form a single network with one type
    pipe_features = pipe_layer.getFeatures()
    weir_features = weir_layer.getFeatures()
    sewerage_types = {feature['sewerage_type'] for feature in pipe_features}
    if len(sewerage_types) > 1:
        raise ValueError('Multiple sewerage types in layer')
    sewerage_type = sewerage_types.pop()
    if sewerage_type in [HEMELWATERRIOOL, INFILTRATIEVOORZIENING, VGS_HEMELWATERRIOOL]:
        network = StormWaterPipeNetwork()
        for feature in pipe_features:
            pipe = pipe_from_feature(feature)
            network.add_pipe(pipe)
            
        for feature in weir_features:
            weir = weir_from_feature(feature)
            network.add_weir(weir)
            
        network.add_id_to_nodes()
        return network

    elif sewerage_type in [GEMENGD_RIOOL, VUILWATERRIOOL]:
        network = WasteWaterPipeNetwork()
        
        return network
    else:
        raise ValueError('Invalid sewerage type')
            
