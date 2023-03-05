import pytest
from osgeo import gdal, ogr
import pathlib
import json

from sewerage_designer.designer.sewerage_designer_classes import (
    BGTInloopTabel,
    Weir,
    Outlet,
    Pipe,
    PipeNetwork,
    StormWaterPipeNetwork,
    SewerageDesigner
)

TEST_DIRECTORY = pathlib.Path(__file__).parent.absolute()

@pytest.fixture(scope="module")
def bgt_inlooptabel():
    bgt_inlooptabel_fn = TEST_DIRECTORY / "bgt_inloop/bgt_inlooptabel_test_mesh_design_2.gpkg"
    return BGTInloopTabel(bgt_inlooptabel_fn)

def test_get_layer_fields(bgt_inlooptabel):
    fields = bgt_inlooptabel.get_layer_fields()
    assert len(fields) == 4
    assert "code" in fields
    assert "surface_area" in fields

def test_set_table(bgt_inlooptabel):
    bgt_inlooptabel.set_table()
    assert hasattr(bgt_inlooptabel, "_table")
    assert len(bgt_inlooptabel._table) == 6
    assert "fid" in bgt_inlooptabel._table
    assert "surface_area" in bgt_inlooptabel._table

def test_get_surface_area_for_pipe_code(bgt_inlooptabel):

    surface_area = bgt_inlooptabel.get_surface_area_for_pipe_code(
        pipe_code=6, pipe_type="infiltratievoorziening"
    )
    assert pytest.approx(surface_area) == 65.6751


@pytest.fixture(scope="module")
def weir():
    # Example WKT geometry for a weir
    wkt_geometry = "POINT(1 1)"
    return Weir(wkt_geometry, fid=1, weir_level=2.0, crest_flow_depth=1.0, pipe_in_id=2, pipe_out_id=3)

def test_init(weir):
    assert isinstance(weir.geometry, ogr.Geometry)
    assert weir.geometry.GetGeometryName() == "POINT"
    assert weir.fid == 1
    assert weir.weir_level == 2.0
    assert weir.crest_flow_depth == 1.0
    assert weir.pipe_in_id == 2
    assert weir.pipe_out_id == 3

def test_wkt_geometry(weir):
    assert weir.wkt_geometry == "POINT (1 1)"

def test_coordinate(weir):
    assert weir.coordinate == (1.0, 1.0)

def test_node(weir):
    weir._node_coordinate = (1.0, 1.0)
    assert weir.node == (1.0, 1.0)



def test_add_pipe():
    """Adds pipes from the simple testcase to a network"""
    simple_network_pipe_json = TEST_DIRECTORY / "unit/pipes_simple_network.json"
    pipes = json.load(open(simple_network_pipe_json, "r"))

    stormwaternetwork = StormWaterPipeNetwork()
    for i, feature in enumerate(pipes):
        pipe = Pipe(feature, i)
        stormwaternetwork.add_pipe(pipe)

    assert len(stormwaternetwork.pipes) == 8
    assert len(stormwaternetwork.network.edges) == 8


def test_sample_elevation():
    """Test sampling an elevation model for a pipe"""
    dem = str(TEST_DIRECTORY / "Zundert.tif")
    dem_datasource = gdal.Open(dem)
    dem_rasterband = dem_datasource.GetRasterBand(1)
    dem_geotransform = dem_datasource.GetGeoTransform()

    simple_network_pipe_json = TEST_DIRECTORY / "unit/pipes_simple_network.json"
    pipes = json.load(open(simple_network_pipe_json, "r"))

    pipe = Pipe(pipes[0], 1)
    pipe.sample_elevation_model(
        dem_rasterband=dem_rasterband, dem_geotransform=dem_geotransform
    )

    assert 11.19 == pytest.approx(pipe.start_elevation)
    assert 11.2 == pytest.approx(pipe.end_elevation)
    assert 11.02 == pytest.approx(pipe.lowest_elevation)


def test_add_weir():
    """Test adding a weir to the network"""
    simple_network_weir_json = TEST_DIRECTORY / "unit/weir_simple_network.json"
    weirs = json.load(open(simple_network_weir_json, "r"))

    stormwaternetwork = StormWaterPipeNetwork()
    weir = Weir(weirs[0], 1)
    stormwaternetwork.add_weir(weir)

    assert stormwaternetwork.weir is not None
    assert len(stormwaternetwork.network.nodes) == 1

def test_network_connected_surface_area_simple_network():
    """Test aggregated surface areas along the network"""

    pipes = ["LINESTRING (0 0, 1 0)", "LINESTRING (1 0, 2 0)", "LINESTRING (2 0, 3 0)"]

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

    pipe_fn = TEST_DIRECTORY / "unit/test_pipes_simple_mesh_design.gpkg"
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


def test_network_connected_surface_area_mesh_network_2():
    """Test aggregated surface areas along the network, for a meshed network"""

    pipe_fn = TEST_DIRECTORY / "unit/test_pipes_mesh_design_2.gpkg"
    pipe_ds = ogr.Open(str(pipe_fn))
    pipe_layer = pipe_ds.GetLayer(0)
    stormwaternetwork = StormWaterPipeNetwork()

    for i, feature in enumerate(pipe_layer):
        props = json.loads(feature.ExportToJson())["properties"]
        geom = feature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        pipe = Pipe(wkt_geometry=wkt, fid=props["id"])
        pipe.connected_surface_area = 1
        stormwaternetwork.add_pipe(pipe)

    stormwaternetwork.accumulate_connected_surface_area()

    assert stormwaternetwork.pipes[31].accumulated_connected_surface_area == 12
    assert stormwaternetwork.pipes[6].accumulated_connected_surface_area == 1.5
    assert stormwaternetwork.pipes[4].accumulated_connected_surface_area == 2.5
    assert stormwaternetwork.pipes[3].accumulated_connected_surface_area == 1.5
    assert stormwaternetwork.pipes[5].accumulated_connected_surface_area == 5


def test_network_connected_surface_area_mesh_network_2_variable_connected_area():
    """Test aggregated surface areas along the network, for a meshed network"""

    pipe_fn = TEST_DIRECTORY / "unit/test_pipes_mesh_design_2.gpkg"
    pipe_ds = ogr.Open(str(pipe_fn))
    pipe_layer = pipe_ds.GetLayer(0)
    stormwaternetwork = StormWaterPipeNetwork()

    for i, feature in enumerate(pipe_layer):
        props = json.loads(feature.ExportToJson())["properties"]
        geom = feature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        pipe = Pipe(wkt_geometry=wkt, fid=props["id"])
        pipe.connected_surface_area = 1
        stormwaternetwork.add_pipe(pipe)

    stormwaternetwork.pipes[6].connected_surface_area = 2
    stormwaternetwork.pipes[7].connected_surface_area = 4

    stormwaternetwork.accumulate_connected_surface_area()

    assert stormwaternetwork.pipes[31].accumulated_connected_surface_area == 16
    assert stormwaternetwork.pipes[6].accumulated_connected_surface_area == 2.5
    assert stormwaternetwork.pipes[7].accumulated_connected_surface_area == 4.5


def test_calculate_max_hydraulic_gradient():

    pipes = ["LINESTRING (0 0, 1 0)", "LINESTRING (1 0, 2 0)", "LINESTRING (2 0, 3 0)"]

    stormwaternetwork = StormWaterPipeNetwork()
    for i, feature in enumerate(pipes):
        pipe = Pipe(feature, i)
        pipe.start_elevation = 8
        pipe.end_elevation = 8
        stormwaternetwork.add_pipe(pipe)

    weir = "POINT (3 0)"
    weir = Weir(weir, 1)
    weir.weir_level = 6
    weir.freeboard = 0.5
    stormwaternetwork.add_weir(weir)

    stormwaternetwork.calculate_max_hydraulic_gradient(waking=0)

    theoretical_max_hydraulic_gradient = (8 - 6.5) / 3
    assert (
        stormwaternetwork.pipes[0].max_hydraulic_gradient
        == theoretical_max_hydraulic_gradient
    )


def test_evalute_max_hydraulic_gradient():

    pipes = ["LINESTRING (0 0, 1 0)", "LINESTRING (1 0, 2 0)", "LINESTRING (2 0, 3 0)"]

    stormwaternetwork = StormWaterPipeNetwork()
    for i, feature in enumerate(pipes):
        pipe = Pipe(feature, i)
        pipe.start_elevation = 8
        pipe.end_elevation = 8
        pipe.lowest_elevation = 8
        stormwaternetwork.add_pipe(pipe)

    stormwaternetwork.pipes[1].lowest_elevation = 7

    weir = "POINT (3 0)"
    weir = Weir(weir, 1)
    weir.weir_level = 6
    weir.freeboard = 0.5
    stormwaternetwork.add_weir(weir)

    stormwaternetwork.calculate_max_hydraulic_gradient(waking=0)
    stormwaternetwork.evaluate_hydraulic_gradient_upstream(waking=0)

    assert stormwaternetwork.pipes[0].max_hydraulic_gradient == 0.25


def test_calculate_discharge():

    pipes = ["LINESTRING (0 0, 1 0)"]
    pipe = Pipe(
        wkt_geometry=pipes[0],
        fid=1,
        accumulated_connected_surface_area=1000,
        max_hydraulic_gradient=0.05,
    )

    pipe.calculate_discharge(intensity=5)
    assert pipe.discharge == (5 / 1000) * 1000


def test_calculate_diameter():

    pipes = ["LINESTRING (0 0, 1 0)"]
    pipe = Pipe(
        wkt_geometry=pipes[0], fid=1, discharge=0.01, max_hydraulic_gradient=0.05
    )

    # Diameter is based on colebrook white
    pipe.calculate_diameter(vmax=1.5)
    assert pipe.diameter == 0.315