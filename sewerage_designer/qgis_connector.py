from osgeo import ogr
from qgis.core import QgsFeature, QgsLayer

from sewerage_designer_classes import Pipe, StormWaterPipeNetwork, WasteWaterPipeNetwork
from constants import *

ogr.UseExceptions()


class SewerageDesignerQgsConnector:
    def __init__(self):
        pass


def pipe_from_feature(feature: QgsFeature):
    wkb_geometry = feature.geometry().asWkb()

    return Pipe(
        wkb_geometry,
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

def pipe_network_from_layer(layer: QgsLayer):
    # Assumptions: pipes in the layer form a single network with one type
    sewerage_types = {feature['sewerage_type'] for feature in layer}
    if len(sewerage_types) > 1:
        raise ValueError('Multiple sewerage types in layer')
    sewerage_type = sewerage_types.pop()
    if sewerage_type in [HEMELWATERRIOOL, INFILTRATIEVOORZIENING, VGS_HEMELWATERRIOOL]:
        network = StormWaterPipeNetwork()
    elif sewerage_type in [GEMENGD_RIOOL, VUILWATERRIOOL]:
        network = WasteWaterPipeNetwork()
    else:
        raise ValueError('Invalid sewerage type')
    for feature in layer:
        pipe = pipe_from_feature(feature)
        pipe.calculate_elevation()
        it_pipe_network.add_pipe(pipe)

    it_pipe_network.add_id_to_nodes()
