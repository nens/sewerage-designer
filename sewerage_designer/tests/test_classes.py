
from osgeo import gdal, ogr, osr
import pathlib

from sewerage_designer.sewerage_designer_classes import Pipe, Outlet, BGTInloopTabel, PipeNetwork, ITPipeNetwork

TEST_DIRECTORY = pathlib.Path(__file__).parent.absolute() / "test_data"

def test_add_pipe():
    
    test_geopackage = TEST_DIRECTORY / 'zundert_test_simple_design.gpkg'
    test_tracing_ds = ogr.Open(str(test_geopackage), 1)
    pipes = test_tracing_ds.GetLayer('pipe')
    it_sewerage = ITPipeNetwork()

    for feature in pipes:
        pipe = Pipe(feature)
        it_sewerage.add_pipe(pipe)        
    
    assert(len(it_sewerage.pipes) == 8)

def test_add_outlet():

    test_geopackage = TEST_DIRECTORY / 'zundert_test_simple_design.gpkg'
    test_tracing_ds = ogr.Open(str(test_geopackage), 1)
    outlets = test_tracing_ds.GetLayer('outlet')
    pipes = test_tracing_ds.GetLayer('pipe')
    it_sewerage = ITPipeNetwork()

    for feature in pipes:
        pipe = Pipe(feature)
        it_sewerage.add_pipe(pipe)        
    
    
    
    assert(len(it_sewerage.pipes) == 8)
    

    
def test_calculate_elevation():
    pass

def test_calculate_discharge():
    pass







