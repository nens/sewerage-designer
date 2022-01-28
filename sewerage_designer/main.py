
import os

from osgeo import gdal, ogr
import networkx as nx
import json

from sewerage_designer_core.constants import *
from sewerage_designer_core.sewerage_designer_classes import Pipe, Weir, BGTInloopTabel, PipeNetwork, StormWaterPipeNetwork, SewerageDesigner


if __name__ == '__main__':
    
    pipe_ds = ogr.Open('./tests/test_data/test_pipes_mesh_design_2.gpkg')
    pipe_layer = pipe_ds.GetLayer(0)

    # Settings
    network_type = 'infiltratieriool'
    design_rain = 'Bui10'
    waking = 0
    dem = './tests/test_data/Zundert.tif'
    bgt_inlooptabel_file = './tests/test_data/bgt_inlooptabel_test_mesh_design_2.gpkg'
    dem_datasource = gdal.Open(dem)
    dem_rasterband = dem_datasource.GetRasterBand(1)
    dem_geotransform = dem_datasource.GetGeoTransform()

    # Define a new pipe network
    stormwater_network = StormWaterPipeNetwork()

    # Add some pipes
    for i,feature in enumerate(pipe_layer):
        props = json.loads(feature.ExportToJson())['properties']
        geom = feature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        pipe = Pipe(wkt_geometry=wkt, 
                    fid=props['id'],
                    sewerage_type=props['sewerage_type'])
        pipe.connected_surface_area = 1
        pipe.sample_elevation_model(dem_rasterband=dem_rasterband, dem_geotransform=dem_geotransform)
        stormwater_network.add_pipe(pipe)
        
    stormwater_network.add_id_to_nodes()
    
    # Add an weir
    # We can use the final pipe's coordinate
    wkt = 'POINT (105113.27273163 386797.394822074)'
    weir = Weir(wkt, 1)
    weir.freeboard = 0.1
    weir.weir_level = 6
    stormwater_network.add_weir(weir)
    #stormwater_network.network.nodes[weir.coordinate]
    
    # Determine connected surface areas and the max hydraulic gradient for the whole network
    bgt_inlooptabel = BGTInloopTabel(bgt_inlooptabel_file)
    for pipe in stormwater_network.pipes.values():
        pipe.determine_connected_surface_area(bgt_inlooptabel)

    # Network connected surface area    
    stormwater_network.accumulate_connected_surface_area()
    stormwater_network.calculate_max_hydraulic_gradient(weir.coordinate, waking=waking)
    stormwater_network.evaluate_hydraulic_gradient_upstream(waking=waking)

    # Calculate the capacity for all the pipes
    for pipe_id, pipe in stormwater_network.pipes.items():
        pipe.calculate_discharge(intensity=0.01, timestep = 300)
        pipe.calculate_diameter()
        pipe.set_material()
        
    # Determine the depth for all pipes
    stormwater_network.set_invert_levels()
    stormwater_network.check_invert_levels()
    
    # Draw network with a property
    stormwater_network.draw_network(node_label_attr='id', edge_label_attr='diameter')
    
    # Discharge check

    
    
    
    
    

