
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
    
    # Test design to list of wkt's
    pipe_ds = ogr.Open('./tests/test_data/test_pipes_simple_split_design_max_gradient.gpkg')
    pipe_layer = pipe_ds.GetLayer(0)

    # Settings
    network_type = 'infiltratieriool'
    design_rain = 'Bui10'
    waking = 0
    dem = './tests/test_data/Zundert.tif'
    bgt_inlooptabel_file = './tests/test_data/bgt_inlooptabel_test.gpkg'
    dem_datasource = gdal.Open(dem)
    dem_rasterband = dem_datasource.GetRasterBand(1)
    dem_geotransform = dem_datasource.GetGeoTransform()

    # Define a new pipe network
    stormwater_network = StormWaterPipeNetwork()

    # Add some pipes
    for feature in pipe_layer:
        props = json.loads(feature.ExportToJson())['properties']
        geom = feature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        pipe = Pipe(wkt, props['id'])
        pipe.connected_surface_area = 100
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
    stormwater_network.accumulate_connected_surface_area()
    stormwater_network.calculate_max_hydraulic_gradient(weir.coordinate, waking=waking)
    stormwater_network.evaluate_hydraulic_gradient_upstream(waking=waking)

    # Calculate the capacity for all the pipes
    for pipe_id, pipe in stormwater_network.pipes.items():
        # Use Colebrook-White to estimate a diameter
        pipe.calculate_discharge(intensity=1, timestep = 300)
        pipe.calculate_diameter()
        pipe.set_material()
        pipe.calculate_minimum_cover_depth(minimal_cover_depth=1)

    # Determine the depth for all pipes
    stormwater_network.check_required_cover_depth()


    pipe= stormwater_network.pipes[30]
    node = (pipe.start_coordinate)

    visited = set()
    nodes = [stormwater_network.weir.coordinate]
    stormwater_network.distance_matrix_reversed[weir.coordinate][0][-1]

    for node in nodes:
                
        if node in visited:
            continue



        # Get the distance dictionary for the end node
        distance_dictionary = stormwater_network.distance_matrix_reversed[node][0]
        furthest_node, distance = list(distance_dictionary.items())[-1]
        furthest_edge = list(stormwater_network.network.edges(furthest_node))[0]
        # Get start elevation + waking for this edge 
        # Calculate hydraulic gradient
        hydraulic_gradient = 0.07
        
        # Assign hydraulic head to nodes along the path
        path_nodes = list(distance_dictionary.keys())
        for i in range(0, len(distance_dictionary.keys())-1):
            path_edge = (path_nodes[i+1],path_nodes[i])
            edge_hydraulic_gradient = 0.07
            # Evaluate hydraulic gradient with lowest surface level
            if edge_hydraulic_gradient is not None:
                # if new hydraulic gradient > current hydraulic gradient
                pass
            else:
                # new hydraulic gradient
                pass
                
        # Find where to continue
        stack = stormwater_network.network.predecessors(node)
        out_edges = []
        while stack:
            try:
                out_node = next(stack)
                out_edges += [(node, out_node)] 
                nodes.extend([out_node])
            except StopIteration:
                break
        
        # Visited nodes
        visited.add(node)
        
        
        
        
        nr_out_edges = len(out_edges)
        if nr_out_edges > 0:
            for edge in out_edges:
                split = 1 / nr_out_edges
                in_node_connected_area = nx.get_node_attributes(stormwater_network.network, 'connected_area')[edge[0]]
                out_node_connected_area = nx.get_node_attributes(stormwater_network.network, 'connected_area')[edge[1]]
                in_node_split = nx.get_node_attributes(stormwater_network.network, 'split')[edge[0]]
                 
                edge_connected_surface_area = nx.get_edge_attributes(stormwater_network.network, 'connected_area')[edge]
                edge_id = nx.get_edge_attributes(stormwater_network.network, 'fid')[edge]
                new_out_node_connected_area = edge_connected_surface_area + split * in_node_connected_area + out_node_connected_area
                new_edge_connected_surface_area = edge_connected_surface_area + split * in_node_connected_area
                
                out_node_attrs = {edge[1]: {'split':split, 'connected_area':new_out_node_connected_area}}
                nx.set_node_attributes(stormwater_network.network, out_node_attrs)
                
                edge_attrs = {edge: {'connected_area': new_edge_connected_surface_area}}
                nx.set_edge_attributes(stormwater_network.network, edge_attrs)
                print(edge_id)
                print(edge_attrs)
                
        visited.add(node)
        
