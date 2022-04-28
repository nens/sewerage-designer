
import sys
sys.path.append(r"C:\Users\chris.kerklaan\Documents\Github\sewerage-designer\sewerage_designer")
import os

from osgeo import gdal, ogr
import networkx as nx
import json

from sewerage_designer_core.constants import *
from sewerage_designer_core.sewerage_designer_classes import Pipe, Weir, BGTInloopTabel, PipeNetwork, StormWaterPipeNetwork, SewerageDesigner

if __name__ == '__main__':
    pipe_ds = ogr.Open(r'C:\Users\chris.kerklaan\Documents\Projecten\sewerage_designer\results\rijsbergen/sewerage_design_internal_weirs_try.gpkg', 1)
    pipe_layer = pipe_ds.GetLayer('sewerage')
    weir_layer =  pipe_ds.GetLayer('weir')

    # Settings
    network_type = 'infiltratieriool'
    design_rain = 'Bui10'
    waking = 0
    
    freeboard = 0.2
    vmax=1.5
    peak_intensity = 75.6

    dem = r'C:\Users\chris.kerklaan\Documents\Projecten\sewerage_designer\data\rijsbergen/rijsbergen.tif'
    bgt_inlooptabel_file = r'C:\Users\chris.kerklaan\Documents\Projecten\sewerage_designer\data\rijsbergenbgt_inlooptabel_zundert.gpkg'
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
        
    
    
    # Add some weirs
    # Add some pipes
    for i,feature in enumerate(weir_layer):
        props = json.loads(feature.ExportToJson())['properties']
        geom = feature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        weir = Weir(wkt_geometry=wkt, 
                    fid=feature.GetFID(),
                    crest_flow_depth=props['crest_flow_depth'],
                    weir_level=props['weir_level']
                    )
        stormwater_network.add_weir(weir)
    
        
    stormwater_network.add_id_to_nodes()
    stormwater_network.add_elevation_to_network(dem)
    stormwater_network.accumulate_connected_surface_area()
    stormwater_network.calculate_max_hydraulic_gradient_interally(freeboard)
    
    
    
    velocity_to_high_pipe_fids=[]
    for pipe_id, pipe in stormwater_network.pipes.items():
        pipe.calculate_discharge(intensity=peak_intensity)
        pipe.calculate_diameter(vmax)
        pipe.set_material()
        if pipe.velocity_to_high:
            velocity_to_high_pipe_fids.append(pipe_id)
            
    # Reset the diameters.
    for pipe_id, pipe in stormwater_network.pipes.items():
        
        feature = pipe_layer.GetFeature(pipe_id)
        feature.SetField('diameter', pipe.diameter) 
        pipe_layer.SetFeature(feature)
        
    driver = ogr.GetDriverByName("GPKG")

    # create output file
    out_ds = driver.CreateDataSource(r'C:\Users\chris.kerklaan\Documents\Projecten\sewerage_designer\results\rijsbergen/sewerage_design_internal_weirs_1.gpkg')
    
    for layer in pipe_ds:
        out_ds.CopyLayer(layer, layer.GetName())
        
    out_ds = None
    

        
    pipe_layer = None
    pipe_ds = None
    
    pipe_fids = []
    cycles = nx.simple_cycles(stormwater_network.network)
    for cycle in cycles:
        for i in range(0,len(cycle)-1):
            edge = (cycle[i], cycle[i+1])
            pipe = stormwater_network.get_pipe_with_edge(edge)
            pipe_fids += [pipe.fid]
            
    string = 'asdfdas {}'.format(pipe_fids)
    print(string)
    
    # Add an weir
    # We can use the final pipe's coordinate
    weir_1 = stormwater_network.pipes[43].end_coordinate
    weir_2 = stormwater_network.pipes[31].end_coordinate
    weir_1_geometry = 'POINT ' + str(weir_1).replace(',', '')
    weir_2_geometry = 'POINT ' + str(weir_2).replace(',', '')
    weirs = [weir_1_geometry, weir_2_geometry]
    weir_levels = [6, 6.1]
    for i, weir in enumerate(weirs):
        weir = Weir(weir, i)
        weir.crest_flow_depth = 0.1
        weir.weir_level = weir_levels[i]
        stormwater_network.add_weir(weir)
    
    # Determine connected surface areas and the max hydraulic gradient for the whole network
    bgt_inlooptabel = BGTInloopTabel(bgt_inlooptabel_file)
    for pipe in stormwater_network.pipes.values():
        pipe.determine_connected_surface_area(bgt_inlooptabel)

    # Network connected surface area    
    stormwater_network.accumulate_connected_surface_area()
    stormwater_network.calculate_max_hydraulic_gradient(waking=waking)
    stormwater_network.evaluate_hydraulic_gradient_upstream(waking=waking)

    # Calculate the capacity for all the pipes
    for pipe_id, pipe in stormwater_network.pipes.items():
        pipe.calculate_discharge(intensity=0.01)
        pipe.calculate_diameter()
        pipe.set_material()
        
    # Determine the depth for all pipes
    stormwater_network.set_invert_levels()
    stormwater_network.check_invert_levels()
    
    # Draw network with a property
    stormwater_network.draw_network(node_label_attr='id', edge_label_attr='fid')
    

    # Hydraulic gradient calculations 
    G = stormwater_network.network
    weirs = stormwater_network.weirs
    
    # Get all weirs (out-degree=0) nodes in the network
    # Calculate the hydraulic gradient to the furthest upstream point
    # Calculate the hydraulic head at it's predecessors
    # If the hydraulic head at the end of the pipe is lower than the lowest elevation
        # Set the end hydraulic head to the lowest elevation
        # Walk the network downstream using this hydraulic head and
    # Walk the network upstream from each of these nodes
    # At each pipe, calculate if the estmated hydraulic gradient is sufficient for it's lowest elevation
    # If not, lower the gradient for all downstream pipes
    # Calculate what the new hydraulic head will be at the start of the pipe
    # Calculate the new hydraulic gradient for upstream pipes using the new hydraulic head
    
    def calculate_hydraulic_head_upstream():
        pass
    
    def upstream_hydraulic_gradient(node):

        if stormwater_network.network.in_degree[node] == 0:
            return
        else:
            stack = stormwater_network.network.predecessors(node)
            upstream_nodes = []
            while stack:
                try:
                    in_node = next(stack)
                    upstream_nodes += [in_node]
                except StopIteration:
                    break

            distance_dictionary = stormwater_network.distance_matrix_reversed[node][0]
            furthest_node, distance = list(distance_dictionary.items())[-1]
            furthest_edge = list(stormwater_network.network.edges(furthest_node))[0]
            furthest_pipe = stormwater_network.get_pipe_with_edge(furthest_edge)
            
            node_hydraulic_head = stormwater_network.network.nodes[node]['hydraulic_head']
            
            hydraulic_gradient = (
                (furthest_pipe.start_elevation + waking)
                - node_hydraulic_head
            ) / distance
            
            for upstream_node in upstream_nodes:

                upstream_edge = (upstream_node, node)
                pipe = stormwater_network.get_pipe_with_edge(upstream_edge)
                pipe_length = stormwater_network.network.edges[upstream_edge]['length']
                upstream_hydraulic_head = node_hydraulic_head + (hydraulic_gradient * pipe_length)
                
                if upstream_hydraulic_head > pipe.lowest_elevation:
                    upstream_hydraulic_head = pipe.lowest_elevation
    
                head_difference = (pipe.lowest_elevation - waking) - upstream_hydraulic_head
                if head_difference < 0:
                    hydraulic_gradient = hydraulic_gradient - (
                        head_difference / pipe_length
                    )
                    upstream_hydraulic_head = node_hydraulic_head + (hydraulic_gradient * pipe_length)
                    
                # If the calculated hydraulic head is lower than present, write to downstream nodes
                node_attrs = {upstream_node:{'hydraulic_head': upstream_hydraulic_head}}
                nx.set_node_attributes(stormwater_network.network, node_attrs)
                
                edge_attrs = {upstream_node:{'max_hydraulic_gradient': hydraulic_gradient}}
                nx.set_edge_attributes(stormwater_network.network, edge_attrs)
            
                _ = upstream_hydraulic_gradient(upstream_node)
            
            
    for node in stormwater_network.network.nodes:
        node_attrs = {node:{'hydraulic_head': None}}
        nx.set_node_attributes(stormwater_network.network, node_attrs)
            
    for weir in stormwater_network.weirs.values():
        weir_node = weir._node_coordinate
        
        # Set the hydraulic gradient at the weir node
        node_attrs = {weir_node:{'hydraulic_head': weir.weir_level + weir.crest_flow_depth}}
        nx.set_node_attributes(stormwater_network.network, node_attrs)
        
        _ = upstream_hydraulic_gradient(weir_node)

        
                        
        
        


    
    stormwater_network.draw_network(node_label_attr='fid', edge_label_attr='accumulated_connected_surface_area')
        
        
        
    
    
    
    
    
    

