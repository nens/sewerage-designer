
import os

from osgeo import gdal, ogr
import networkx as nx
import json

from sewerage_designer.constants import *
from sewerage_designer.sewerage_designer_classes import Pipe, Weir, BGTInloopTabel, PipeNetwork, StormWaterPipeNetwork, SewerageDesigner

if __name__ == '__main__':

    # Generate a pipe network from a tracing
    # Tracing will be geopackage containing the following layers: pipes, outlets, weirs, pumpstations
    # Settings from QGIS gui will be :
        # Sewerage type (IT)
        # BGT Inlooptabel from a ogr datasource

    #TODO Check network for amount of outlets
    #TODO Check tracing for correct projection
    #TODO hoofdroutes kunnen aangeven in het trace/ of niet wenselijke routes duurder maken in trace voor netwerkanalyse
    #TODO opnkippen stelsel o.b.v stuwputten, optellen debieten
    #TODO checken diameters opeenvolgende buizen, ook bij stuwputten nooit kleiner
    #TODO Stuwputten bepalen voor stelsels met uitlaten, indicatie voor uitlaat stelsel zonder stuwputten
    #TODO NWRW model factors implementeren voor bgt inlooptabel,. vermenigvulden percentage verharding
    #TODO Niet dubbel oppervlak tellen bij aangesloten oppervlak
    #TODO DOwnload empty geopackge from GUI
    #TODO Dekking checken, diepteligging wordt bepaald door de drempelhoogte
    #TODO Colebrook-white beschikbare diameters variabel maken

    # Settings
    network_type = 'infiltratieriool'
    design_rain = 'Bui10'
    waking = 0
    dem = './tests/test_data/Zundert.tif'
    bgt_inlooptabel_file = './tests/test_data/bgt_inlooptabel_test.gpkg'
    dem_datasource = gdal.Open(dem)
    dem_rasterband = dem_datasource.GetRasterBand(1)
    dem_geotransform = dem_datasource.GetGeoTransform()

    sd = SewerageDesigner()

    # Load DEM rasterband and geotransform
    sd.set_dem(dem_fn)

    # Load BGT Inlooptabel
    bgt_inlooptabel = BGTInloopTabel(bgt_inlooptabel_file)
    bgt_inlooptabel.get_surface_area_for_pipe_id(pipe_code=8, pipe_type='infiltratievoorziening')
    sd.set_bgt_inlooptabel(bgt_inlooptabel_fn)

    # Define a new pipe network
    stormwater_network = StormWaterPipeNetwork()

    # Get pipes
    pipe_json = r'.\tests\test_data\pipes_simple_network.json'
    weir_json = r'.\tests\test_data\weir_simple_network.json'
    pipes = json.load(open(pipe_json, 'r'))
    weirs = json.load(open(weir_json, 'r'))

    # Add some pipes
    for i, feature in enumerate(pipes):
        pipe = Pipe(feature, i)
        pipe.connected_surface_area = 1
        pipe.sample_elevation_model(dem_rasterband=dem_rasterband, dem_geotransform=dem_geotransform)
        stormwater_network.add_pipe(pipe)

    stormwater_network.add_id_to_nodes()
    
    # Add an weir
    weir = Weir(weirs[0], 1)
    weir.freeboard = 0.1
    weir.weir_level = 6
    stormwater_network.add_weir(weir)
    #stormwater_network.network.nodes[weir.coordinate]
    
    # Determine connected surface areas and the max hydraulic gradient for the whole network
    stormwater_network.accumulate_connected_surface_area()
    stormwater_network.calculate_max_hydraulic_gradient(weir.coordinate, waking=waking)

    # Calculate the capacity for all the pipes
    for pipe_id, pipe in it_pipe_network.pipes.items():
        # Use Colebrook-White to estimate a diameter
        pipe.calculate_discharge(design_rain=design_rain)
        pipe.calculate_diameter()
        pipe.set_material()
        pipe.calculate_minimum_cover_depth(minimal_cover_depth=1)

    # Determine the depth for all pipes
    it_pipe_network.calculate_required_cover_depth()

    # # Save results to pipes layer
    for pipe in it_pipe_network.pipes.values():
        pipe.write_properties_to_feature()
        pipes.SetFeature(pipe.feature)
        pipe.feature = None

    #
    pipes = None
    test_tracing_ds = None
