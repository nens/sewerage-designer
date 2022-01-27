
import os

from osgeo import gdal, ogr
import networkx as nx
import json

from sewerage_designer_core.constants import *
from sewerage_designer_core.sewerage_designer_classes import Pipe, Weir, BGTInloopTabel, PipeNetwork, StormWaterPipeNetwork, SewerageDesigner

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
    pipe_ds = ogr.Open('./tests/test_data/test_pipes_mesh_design_2.gpkg')
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
    
    stormwater_network.draw_network('connected_area')
    
    #stormwater_network.draw_network('connected_area')
    for pipe in stormwater_network.pipes.values():
        print(pipe.fid)
        print(pipe.accumulated_connected_surface_area)
    
    
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

    #### Recursive method

    # Define sink and tank nodes   
    
    
    sink_nodes = [n for n, d in stormwater_network.network.in_degree() if d == 0]
    tank_nodes = [n for n, d in stormwater_network.network.out_degree() if d == 0]
    
    out_degree_nodes = stormwater_network.network.out_degree()
    in_degree_nodes = stormwater_network.network.in_degree()
    
    for node in stormwater_network.network.nodes:
        attrs = {node: {"connected_area":100}}
        nx.set_node_attributes(stormwater_network.network, attrs)
            

    def get_score(node, ready_nodes):
        if node in ready_nodes:
            return ready_nodes[node]
        else:
            stack = stormwater_network.network.predecessors(node)
            upstream_nodes = []
            while stack:
                try:
                    in_node = next(stack)
                    upstream_nodes += [in_node]
                except StopIteration:
                    break
            
            #nx.get_node_attributes(stormwater_network.network,'connected_area')[node]
            node_output = stormwater_network.network.nodes[node]['connected_area']
            for in_node in upstream_nodes:
                node_output += get_score(in_node, ready_nodes)
    
            if out_degree_nodes[node] > 0:
                node_output /= out_degree_nodes[node]

            attrs = {node: {'connected_area': node_output}}
            nx.set_node_attributes(stormwater_network.network, attrs)

            ready_nodes[node] = node_output
            return node_output
        
    
    # set all starting flows to 1
    ready_nodes = {sink: 100 for sink in sink_nodes}
    for tank in tank_nodes:
        score = get_score(tank, ready_nodes)
        
    pos = nx.get_node_attributes(stormwater_network.network,'position')
    labels = nx.get_node_attributes(stormwater_network.network, 'connected_area') 
    nx.draw(stormwater_network.network,pos,labels=labels,node_size=100)
    
    for node, area in ready_nodes.items():
        node_successors = []
        for succesor_node in stormwater_network.network.successors(node):
            node_successors += [node]
            
        for successor in node_successors:
            edge = (node, successor)
            edge_flow = stormwater_network.network.nodes[node]['connected_area']
            pipe = stormwater_network.get_pipe_with_edge(edge)
            pipe.accumulated_connected_surface_area = edge_flow
        
        downstream = [n for n in nx.traversal.bfs_tree(stormwater_network.network, node) if n != 2]
        break
        
    

    ## Cumulative method

    for node in stormwater_network.network.nodes:
        if out_degree_nodes[node] > 1:
            attrs = attrs = {node: {"flow_split_frac": 1/out_degree_nodes[node]}}
        else:
            attrs = {node: {"flow_split_frac": 1}}
        nx.set_node_attributes(stormwater_network.network, attrs)
        

    def accumulate_downstream(G, accum_attr, cumu_attr_name=None,
                              split_attr='flow_split_frac'):
        """
        pass through the graph from upstream to downstream and accumulate the value
        an attribute found in nodes and edges, and assign the accumulated value
        as a new attribute in each node and edge.
        Where there's a flow split, apply an optional split fraction to
        coded in the upstream edge.
        """
        G1 = G.copy()
    
        if cumu_attr_name is None:
            cumu_attr_name = 'accumulated_{}'.format(accum_attr)
    
        for n in nx.topological_sort(G1):
    
            # grab value in current node
            attrib_val = G1.nodes[n].get(accum_attr, 0)
    
            # sum with cumulative values in upstream nodes and edges
            for p in G1.predecessors(n):
                # add cumulative attribute val in upstream node, apply flow split fraction
                attrib_val += G1.nodes[p][cumu_attr_name] * G1[p][n].get(split_attr, 1)
    
                # add area routed directly to upstream edge/sewer
                attrib_val += G1[p][n].get(accum_attr, 0)
    
                # store cumulative value in upstream edge
                G1[p][n][cumu_attr_name] = attrib_val
    
            # store cumulative attribute value in current node
            G1.nodes[n][cumu_attr_name] = attrib_val
    
        return G1
    
    accumulated_graph = accumulate_downstream(stormwater_network.network, accum_attr='connected_area')
        
    for node in stormwater_network.network.nodes:
        attrs = {node: {"pos": node}}
        nx.set_node_attributes(stormwater_network.network, attrs)
        
    pos = nx.get_node_attributes(accumulated_graph,'pos')
    labels = nx.get_node_attributes(accumulated_graph, 'cumulative_connected_area') 
    nx.draw(accumulated_graph,pos,labels=labels,node_size=100)

            
