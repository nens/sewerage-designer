
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
    
    assert len(stormwaternetwork.weirs) == 1
    assert len(stormwaternetwork.network.nodes) == 1
    
    
def test_calculate_elevation():
    pass

def test_calculate_discharge():
    pass







