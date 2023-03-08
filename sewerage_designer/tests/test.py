'''
Use:
Test totality of SewerageDesigner without having to use the QGIS plug-in.
Optimal for debugging and code improvements.

Approach:
You can look at it as a simplified version of the sewerage_designer_dockwidget.py and qgis_connector.py
Changes made to the core will be tested here and later implemented in the actual code

Three input files
    - SewerageDesigner database (.gpkg)
    - BGT inlooptabel (.gpkg)
    - DEM (.tif)

Required settings
    - Peak intensity [mm/hour]
    - Minimum freeboard [m]
    - Minimum cover depth [m]
    - Maximum velocity [m/s]

Three steps:
    - Compute connected surfaces
    - Compute diameters
    - Validate depths
'''
import inspect
import networkx as nx
import pickle
import time

from osgeo import ogr

from sewerage_designer.designer.designer import (
BGTInloopTabel,
StormWaterPipeNetwork,
Pipe,
Weir
)

def test_compute_cs(SD_db_path, BGT_inlooptabel_path):

    driver = ogr.GetDriverByName('GPKG')
    gpkg = driver.Open(SD_db_path, 0)

    for i in range(gpkg.GetLayerCount()):
        layer = gpkg.GetLayerByIndex(i)
        layername = layer.GetName()
        if layername == 'sewerage':
            sewerage_layer = layer
        elif layername == 'weir':
            weir_layer = layer

    print("sewerage designer gpkg loaded...")

    # I create a sewerage network from the layers, using the checks from the qgis connector
    n_pipes, n_pipes_not_zero = get_feature_count(sewerage_layer)
    n_weirs, n_weirs_not_zero = get_feature_count(weir_layer)

    if not n_pipes_not_zero:
        raise ValueError("Sewerage should have pipe features.")

    if n_weirs_not_zero:
        network = StormWaterPipeNetwork()
    else:
        raise ValueError("Sewerage should have weir features.")

    # I loop through all features in the sewerage layer
    feature = sewerage_layer.GetNextFeature()
    while feature:
        pipe = pipe_from_feature(feature)
        network.add_pipe(pipe)
        feature = sewerage_layer.GetNextFeature()

    # I loop through all features in the weir layer and add them to the network
    feature = weir_layer.GetNextFeature()
    while feature:
        weir = weir_from_feature(feature)
        network.add_weir(weir)
        feature = weir_layer.GetNextFeature()

    # I add ids to the nodes
    network.add_id_to_nodes()
    
    # I validate the network
    pipes_in_loop, pipes_without_weir = validate_network(network)

    # I stop if there are network faults
    if len(pipes_in_loop) > 0:
        raise ValueError(
            f"Network has a loop, pipe FIDs: {pipes_in_loop}"
        )

    if len(pipes_without_weir) > 0:
        raise ValueError(
            f"Network has {len(pipes_without_weir)} pipes that are not connected to a weir, pipe FIDs: {pipes_without_weir}"
        )

    print("network created and validated...")
    
    # I create the BGTInloopTabel class
    start_t = time.time()
    BGT_inlooptabel = BGTInloopTabel(BGT_inlooptabel_path)
    print(f"loading BGT inlooptabel took this long: {time.time() - start_t} s")

    print("bgt inlooptabel loaded...")

    # I compute the cs areas
    for pipe in network.pipes.values():
        pipe.connected_surface_area = 0.0
        pipe.determine_connected_surface_area(BGT_inlooptabel)

    print("computed cs areas...")

    # I compute the accumulated cs areas
    network.accumulate_connected_surface_area()

    print("computed accumulated cs areas...")

    # I check if there are no pipes with empty accumulated cs areas
    val = [None, 0]
    pipes_with_empty_accumulated_fields = []
    for pipe in network.pipes.values():
        if pipe.accumulated_connected_surface_area in val:
            pipes_with_empty_accumulated_fields.append(pipe.fid)

    if not pipes_with_empty_accumulated_fields:
        print("The connected surfaces are computed. You can now proceed to compute the diameters.")

    else:
        raise ValueError(
            f"Some pipes have no accumulated connected surfaces, "
            f"pipe FIDs: {pipes_with_empty_accumulated_fields}"
             )

    return network

def test_compute_diameters(network, DEM_path, peak_intensity, minimum_freeboard, maximum_velocity):

    # I sample surface elevations based on the DEM
    network.add_elevation_to_network(DEM_path)

    # I calculate max hydraulic gradients with internal and external weirs
    network.calculate_max_hydraulic_gradient_weirs(
        freeboard=minimum_freeboard
    )

    # I calculate the discharge and try to set the smallest diameter for each pipe
    velocity_to_high_pipe_fids = []
    for pipe_id, pipe in network.pipes.items():
        pipe.calculate_discharge(intensity=peak_intensity)
        try:
            pipe.calculate_diameter(maximum_velocity)
        except Exception as e:
            #print(e)
            pipe.diameter = 9999
            pipe.velocity_to_high = True

        pipe.set_material()

        if pipe.velocity_to_high:
            velocity_to_high_pipe_fids.append(pipe_id)

    # I check the velocity criterion
    if not velocity_to_high_pipe_fids:
        print("The diameters are computed. You can now proceed to validate/ compute the depths.")
    else:
        raise ValueError(
            f"The velocity in {len(velocity_to_high_pipe_fids)} pipes is too large, "
            f"pipe FIDs: {velocity_to_high_pipe_fids}"
            )

    return network

def test_validate_depths(network, DEM_path, minimum_cover_depth):

    # I calculate the cover depths
    network.calculate_cover_depth()

    # I validate the cover depths
    validated = []
    not_validated = []
    for pipe in network.pipes.values():
        if pipe.cover_depth > minimum_cover_depth:
            validated.append(True)
        else:
            validated.append(False)
            not_validated.append(pipe.fid)

    if all(validated):
        print("Valid design! The cover depth of all pipes meet the minimum depth requirement.")
    else:
        print(
            f"Invalid design! The cover depth of {len(not_validated)} pipes do not meet the minimum depth requirement."
            f"These pipes are {not_validated}."
        )

    return network


# I copied the following functions from qgis_connector
# and made some changes to make it work for non QGIS layers:

def get_feature_count(layer):
    count = layer.GetFeatureCount()
    if count > 0:
        not_zero = True
    else:
        not_zero = False
    return count, not_zero

def pipe_from_feature(feature):
    '''
    similar to function in qgis_connector, however input is now osgeo.ogr.Feature, not QgsFeature
    '''

    fid = feature.GetFID()
    geom = feature.GetGeometryRef()
    wkb_type = geom.GetGeometryType()
    wkb_type_text = ogr.GeometryTypeToName(wkb_type)

    if wkb_type != ogr.wkbLineString or geom.GetGeometryCount() > 1:
        raise ValueError(
            f"Invalid geometry type: {wkb_type_text} for pipe with id {fid}. Pipes should be singlepart line geometries."
        )

    wkt_geometry = geom.ExportToWkt()
    pipe_signature = inspect.signature(Pipe).parameters
    pipe = Pipe(wkt_geometry=wkt_geometry, fid=fid)

    for variable, parameter in pipe_signature.items():
        if variable not in ["fid", "wkt_geometry"]:
            field_value = feature.GetField(variable)
            setattr(pipe, variable, field_value)

    return pipe


def weir_from_feature(feature):
    '''
    similar to function in qgis_connector, however input is now osgeo.ogr.Feature, not QgsFeature
    '''
    fid = feature.GetFID()

    wkt_geometry = feature.GetGeometryRef().ExportToWkt()
    weir_signature = inspect.signature(Weir).parameters
    weir = Weir(wkt_geometry=wkt_geometry, fid=fid)

    for variable, parameter in weir_signature.items():
        if variable not in ["fid", "wkt_geometry"]:
            field_value = feature.GetField(variable)
            setattr(weir, variable, field_value)

    return weir

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



if __name__ == "__main__":
    SD_db_path = r"C:\Users\stijn.overmeen\Documents\GitHub\sewerage-designer\sewerage_designer\tests\system_zundert\sewerage_designer.gpkg"
    BGT_inlooptabel_path = r"C:\Users\stijn.overmeen\Documents\GitHub\sewerage-designer\sewerage_designer\tests\system_zundert\bgt_inlooptabel.gpkg"
    DEM_path = r"C:\Users\stijn.overmeen\Documents\GitHub\sewerage-designer\sewerage_designer\tests\system_zundert\dem.tif"

    peak_intensity = 39.6
    minimum_freeboard = 0.25
    minimum_cover_depth = 0.5
    maximum_velocity = 2

    #STEP 1
    start_time = time.time()
    network = test_compute_cs(
        SD_db_path, BGT_inlooptabel_path
    )
    print(f"elapsed time for STEP 1 = {time.time() - start_time} s")

    '''
    with open('network_after_step_1.pkl', 'wb') as f:
        pickle.dump(network, f)

    #STEP 2
    network = pickle.load(open('network_after_step_1.pkl', 'rb'))
    start_time = time.time()
    network = test_compute_diameters(
        network, DEM_path, peak_intensity, minimum_freeboard, maximum_velocity
    )
    print(f"elapsed time for STEP 2 = {time.time() - start_time} s")

    with open('network_after_step_2.pkl', 'wb') as f:
        pickle.dump(network, f)

    #STEP 3
    network = pickle.load(open('network_after_step_2.pkl', 'rb'))
    start_time = time.time()
    network = test_validate_depths(
        network, DEM_path, minimum_cover_depth
    )
    print(f"elapsed time for STEP 3 = {time.time() - start_time} s")
    with open('network_after_step_3.pkl', 'wb') as f:
        pickle.dump(network, f)
    '''