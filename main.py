
import os

from osgeo import gdal, ogr
import networkx as nx
import json

from constants import *
from pipe import Pipe, Outlet, BGTInloopTabel, PipeNetwork    

if __name__ == '__main__':
    
    # Generate a pipe network from a tracing
    # Tracing will be geopackage containing the following layers: pipes, outlets, weirs, pumpstations
    # Settings from QGIS gui will be :
        # Sewerage type (IT)
        # BGT Inlooptabel from a ogr datasource
        
    #TODO Check network for amount of outlets
    #TODO Check tracing for correct projection
    #TODO opnkippen stelsel o.b.v stuwputten, optellen debieten
    #TODO checken diameters opeenvolgende buizen, ook bij stuwputten nooit kleiner
    #TODO Stuwputten bepalen voor stelsels met uitlaten, indicatie voor uitlaat stelsel zonder stuwputten
    #TODO NWRW model factors implementeren voor bgt inlooptabel
    #TODO Niet dubbel oppervlak tellen bij aangesloten oppervlak
        
    test_tracing = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\zundert_test_28992.gpkg'
    dem_fn = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\Zundert.tif'
    bgt_inlooptabel = r'C:\Users\Emile.deBadts\Documents\repos\sewerage-designer\test_data\bgt_inlooptabel.gpkg'
    network_type = 'gemengd_riool'
    design_rain = '9'
    test_tracing_ds = ogr.Open(test_tracing)
    
    # Load BGT Inlooptabel
    bgt_inlooptabel = BGTInloopTabel(bgt_inlooptabel)
    
    # Load DEM rasterband and geotransform
    dem_ds = gdal.Open(dem_fn)
    dem_rb = dem_ds.GetRasterBand(1)
    gt = dem_ds.GetGeoTransform()

    # Get pipes 
    pipes = test_tracing_ds.GetLayer('pipe')
    outlets = test_tracing_ds.GetLayer('outlet')
    
    # Define a new pipe network
    it_sewerage = PipeNetwork()
    it_sewerage.sewerage_type = network_type
    
    # Add some pipes
    for feature in pipes:
        pipe = Pipe(feature)
        pipe.calculate_elevation(elevation_rasterband=dem_rb, gt=gt)            
        it_sewerage.add_pipe(pipe)        

    it_sewerage.add_id_to_nodes()

    # Add some outlets
    for feature in outlets:
        outlet = Outlet(feature)
        if outlet.coordinate in it_sewerage.network.nodes(data=True):
            attr = {outlet.coordinate : {'type': 'outlet'}}
            nx.set_node_attributes(it_sewerage.network, attr)
        else:
            raise KeyError('Outlet coordinate is not a node in the network')
        
    # Calculate max hydraulic gradient possible for the network
    it_sewerage.calculate_max_hydraulic_gradient(outlet.coordinate)
    it_sewerage.determine_connected_surface_area_totals(bgt_inlooptabel = bgt_inlooptabel)
    
    # Calculate the capacity for all the pipes 
    for pipe_id, pipe in it_sewerage.pipes.items():
        # Use Colebrook-White to estimate a diameter
        pipe.calculate_discharge(design_rain=design_rain)
        pipe.calculate_diameter()


