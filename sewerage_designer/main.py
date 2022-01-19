
import os

from osgeo import gdal, ogr
import networkx as nx
import json

from constants import *
from sd import Pipe, Outlet, BGTInloopTabel, PipeNetwork, ITPipeNetwork, SewerageDesigner

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
        
    test_tracing = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\zundert_test_28992.gpkg'
    dem_fn = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\Zundert.tif'
    bgt_inlooptabel_fn = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\bgt_inlooptabel.gpkg'
    
    # Settings
    network_type = 'infiltratieriool'
    design_rain = '7'
    waking = 0

    test_tracing_ds = ogr.Open(test_tracing, 1)

    sd = SewerageDesigner()

    # Load DEM rasterband and geotransform
    sd.set_dem(dem_fn)

    # Load BGT Inlooptabel
    sd.set_bgt_inlooptabel(bgt_inlooptabel_fn)

    # Define a new pipe network
    it_pipe_network = ITPipeNetwork()
    it_pipe_network.outlet_level = 6.0

    # Get pipes 
    pipes = test_tracing_ds.GetLayer('pipe')
    outlets = test_tracing_ds.GetLayer('outlet')

    # Add some pipes
    for feature in pipes:
        pipe = Pipe(feature)
        pipe.calculate_elevation(elevation_rasterband=dem_rb, gt=gt)            
        it_pipe_network.add_pipe(pipe)

    it_pipe_network.add_id_to_nodes()

    # Add some outlets
    for feature in outlets:
        outlet = Outlet(feature)
        if outlet.coordinate in it_pipe_network.network.nodes(data=True):
            attr = {outlet.coordinate : {'type': 'outlet'}}
            nx.set_node_attributes(it_sewerage.network, attr)
        else:
            raise KeyError('Outlet coordinate is not a node in the network')
    
    # Determine connected surface areas and the max hydraulic gradient for the whole network
    it_pipe_network.determine_connected_surface_area_totals(bgt_inlooptabel = bgt_inlooptabel)
    it_pipe_network.calculate_max_hydraulic_gradient(outlet.coordinate)

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

    
   
        
    
        


