
import pytest
from osgeo import gdal, ogr, osr
import pathlib
import json
import sys

from sewerage_designer.sewerage_designer.sewerage_designer_classes import Pipe, Weir, BGTInloopTabel, PipeNetwork, StormWaterPipeNetwork

TEST_DIRECTORY = pathlib.Path(__file__).parent.absolute() / "test_data"

def test_add_pipe():
    """Adds pipes from the simple testcase to a network"""
    simple_network_pipe_json = TEST_DIRECTORY / 'pipes_simple_network.json'
    pipes = json.load(open(simple_network_pipe_json, 'r'))
    
    stormwaternetwork = StormWaterPipeNetwork()
    for i, feature in enumerate(pipes):
        pipe = Pipe(feature, i)
        stormwaternetwork.add_pipe(pipe)        
       
    assert len(stormwaternetwork.pipes) == 8
    assert len(stormwaternetwork.network.edges) == 8

def test_sample_elevation():
    """Test sampling an elevation model for a pipe"""
    dem = str(TEST_DIRECTORY / 'Zundert.tif')
    dem_datasource = gdal.Open(dem)
    dem_rasterband = dem_datasource.GetRasterBand(1)
    dem_geotransform = dem_datasource.GetGeoTransform()
    
    simple_network_pipe_json = TEST_DIRECTORY / 'pipes_simple_network.json'
    pipes = json.load(open(simple_network_pipe_json, 'r'))

    pipe = Pipe(pipes[0], 1)
    pipe.sample_elevation_model(dem_rasterband=dem_rasterband, dem_geotransform=dem_geotransform)
    
    assert 11.19 == pytest.approx(pipe.start_elevation)
    assert 11.2 == pytest.approx(pipe.end_elevation)
    assert 11.02 == pytest.approx(pipe.lowest_elevation)    
    
def test_add_weir():
    """Test adding a weir to the network"""
    simple_network_weir_json = TEST_DIRECTORY / 'weir_simple_network.json'
    weirs = json.load(open(simple_network_weir_json , 'r'))
    
    stormwaternetwork = StormWaterPipeNetwork()
    weir = Weir(weirs[0], 1)
    stormwaternetwork.add_weir(weir)
    
    assert stormwaternetwork.weir is not None
    assert len(stormwaternetwork.network.nodes) == 1
    
def test_bgt_inlooptabel():
    """Get surface area for pipe id's"""
    bgt_inlooptabel_file = TEST_DIRECTORY  / 'bgt_inlooptabel_test.gpkg'
    bgt_inlooptabel = BGTInloopTabel(bgt_inlooptabel_file)
    surface_area_6 = bgt_inlooptabel.get_surface_area_for_pipe_id(pipe_code = 6, pipe_type='infiltratievoorziening')
    surface_area_7 = bgt_inlooptabel.get_surface_area_for_pipe_id(pipe_code = 7, pipe_type='infiltratievoorziening')
    surface_area_8 = bgt_inlooptabel.get_surface_area_for_pipe_id(pipe_code = 8, pipe_type='infiltratievoorziening')

    assert pytest.approx(surface_area_6) == 65.6751
    assert pytest.approx(surface_area_7) == 53.90597
    assert pytest.approx(surface_area_8) == 114.7000
    
def test_network_connected_surface_area_simple_network():
    """Test aggregated surface areas along the network"""
    
    pipes = ['LINESTRING (0 0, 1 0)',
             'LINESTRING (1 0, 2 0)',
             'LINESTRING (2 0, 3 0)']    
    
    stormwaternetwork = StormWaterPipeNetwork()
    for i, feature in enumerate(pipes):
        pipe = Pipe(feature, i)
        pipe.connected_surface_area = 1
        stormwaternetwork.add_pipe(pipe)        
    stormwaternetwork.accumulate_connected_surface_area()
    
    assert stormwaternetwork.pipes[0].accumulated_connected_surface_area == 1
    assert stormwaternetwork.pipes[1].accumulated_connected_surface_area == 2
    assert stormwaternetwork.pipes[2].accumulated_connected_surface_area == 3    

    
def test_network_connected_surface_area_mesh_network():
    """Test aggregated surface areas along the network, for a meshed network"""

    pipe_fn = TEST_DIRECTORY / 'test_pipes_simple_mesh_design.gpkg'
    pipe_ds = ogr.Open(str(pipe_fn))
    pipe_layer = pipe_ds.GetLayer(0)
    stormwaternetwork = StormWaterPipeNetwork()

    for i, feature in enumerate(pipe_layer):
        geom = feature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        pipe = Pipe(wkt_geometry=wkt, fid=i)
        pipe.connected_surface_area = 1
        stormwaternetwork.add_pipe(pipe)

    stormwaternetwork.accumulate_connected_surface_area()
    
    assert stormwaternetwork.pipes[0].accumulated_connected_surface_area == 1
    assert stormwaternetwork.pipes[1].accumulated_connected_surface_area == 1.5
    assert stormwaternetwork.pipes[2].accumulated_connected_surface_area == 1.5 
    assert stormwaternetwork.pipes[3].accumulated_connected_surface_area == 2.5    
    assert stormwaternetwork.pipes[4].accumulated_connected_surface_area == 2.5    
    assert stormwaternetwork.pipes[5].accumulated_connected_surface_area == 6    


def test_calculate_max_hydraulic_gradient():

    pipes = ['LINESTRING (0 0, 1 0)',
             'LINESTRING (1 0, 2 0)',
             'LINESTRING (2 0, 3 0)']    
        
    stormwaternetwork = StormWaterPipeNetwork()
    for i, feature in enumerate(pipes):
        pipe = Pipe(feature, i)
        pipe.start_elevation = 8
        pipe.end_elevation = 8
        stormwaternetwork.add_pipe(pipe)        

    weir = 'POINT (3 0)'
    weir = Weir(weir, 1)
    weir.weir_level = 6
    weir.freeboard = 0.5
    stormwaternetwork.add_weir(weir)
    
    stormwaternetwork.calculate_max_hydraulic_gradient(outlet_node=weir.coordinate, waking=0)

    theoretical_max_hydraulic_gradient = (8-6.5)/3
    assert stormwaternetwork.pipes[0].max_hydraulic_gradient == theoretical_max_hydraulic_gradient

def test_calculate_discharge():
    pass







