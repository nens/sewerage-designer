""" 
Script om de sewerage designer in python af te trappen.

"""


import sys

sys.path.insert(
    0,
    r"C:\Users\chris.kerklaan\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\sewerage_designer",
)
import os

from osgeo import gdal, ogr
import networkx as nx
import json

from designer.constants import *
from designer.designer import (
    Pipe,
    Weir,
    BGTInloopTabel,
    PipeNetwork,
    StormWaterPipeNetwork,
    SewerageDesigner,
)

if __name__ == "__main__":
    pipe_ds = ogr.Open(
        r"L:\chris\sewerage_designer\sewerage_designer\hwa_vd_toekomst.gpkg",
        1,
    )
    pipe_layer = pipe_ds.GetLayer("sewerage")
    weir_layer = pipe_ds.GetLayer("weir")

    # Settings
    network_type = "infiltratieriool"
    design_rain = "Bui09"
    waking = 0

    freeboard = 0.2
    vmax = 1.5
    peak_intensity = 57.6

    dem = r"L:\chris\sewerage_designer\sewerage_designer\Zundert.tif"
    bgt_inlooptabel_file = r"C:\Users\chris.kerklaan\Documents\Projecten\bgt_inlooptool\data3\inlooptabel3.gpkg"
    dem_datasource = gdal.Open(dem)
    dem_rasterband = dem_datasource.GetRasterBand(1)
    dem_geotransform = dem_datasource.GetGeoTransform()

    # Define a new pipe network
    stormwater_network = StormWaterPipeNetwork()
    n = stormwater_network

    # Add some pipes
    for i, feature in enumerate(pipe_layer):
        props = json.loads(feature.ExportToJson())["properties"]
        geom = feature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        try:
            pipe = Pipe(
                wkt_geometry=wkt, fid=feature.GetFID(), sewerage_type=props["sewerage_type"]
            )
        except Exception:
            print(feature.GetFID())
            continue
        pipe.connected_surface_area = 1
        pipe.sample_elevation_model(
            dem_rasterband=dem_rasterband, dem_geotransform=dem_geotransform
        )
        stormwater_network.add_pipe(pipe)

    # Add some weirs
    # Add some pipes
    for i, feature in enumerate(weir_layer):
        props = json.loads(feature.ExportToJson())["properties"]
        geom = feature.GetGeometryRef()
        wkt = geom.ExportToWkt()
        weir = Weir(
            wkt_geometry=wkt,
            fid=feature.GetFID(),
            crest_flow_depth=props["crest_flow_depth"],
            weir_level=props["weir_level"],
        )
        stormwater_network.add_weir(weir)

    # # Determine connected surface areas and the max hydraulic gradient for the whole network
    bgt_inlooptabel = BGTInloopTabel(bgt_inlooptabel_file)
    for pipe in stormwater_network.pipes.values():
        pipe.determine_connected_surface_area(bgt_inlooptabel)

    stormwater_network.add_id_to_nodes()
    stormwater_network.add_elevation_to_network(dem)
    
    stormwater_network.accumulate_connected_surface_area()
    n.calculate_max_hydraulic_gradient_weirs(freeboard)


    velocity_to_high_pipe_fids = []
    for pipe_id, pipe in stormwater_network.pipes.items():
        pipe.calculate_discharge(intensity=peak_intensity)
        pipe.calculate_diameter(vmax)
        pipe.set_material()
        if pipe.velocity_to_high:
            velocity_to_high_pipe_fids.append(pipe_id)


# Write some data # pip install threedi_raster_edits
import threedi_raster_edits as tre


for external_weir_id in n.gradients:
    for section in n.gradients[external_weir_id]:
        
        vector =  tre.Vector.from_scratch("design", 5, 28992)
        vector.add_field("hydraulic_gradient", float)
        vector.add_field("downstream_hydraulic_head", float)
        vector.add_field("upstream_hydraulic_head", float)
        vector.add_field("drowned", int)
        vector.add_field("internal", int)
        vector.add_field("branch", int)
        vector.add_field("external_weir", int)
        vector.add_field("downstream_weir", int)
        vector.add_field("downstream_weir_elevation", float)
        vector.add_field("upstream_weir", int)
        vector.add_field("upstream_weir_elevation", float)
        vector.add_field("from_upstream_pipe", int)
        vector.add_field("from_upstream_weir", int)
        vector.add_field("to_downstream_weir", int)
        vector.add_field("to_downstream_pipe", int)
        
        
        for section in n.gradients[external_weir_id]:
            # createe geometry
            all_points = [p.points for p in section.pipes]
            multi = tre.MultiLineString.from_points(all_points)
        
            if section.upstream_weir:
                upstream_weir = section.upstream_weir.fid
            else:
                upstream_weir = None
            
            if section.downstream_weir:
                downstream_weir = section.downstream_weir.fid
            else:
                downstream_weir = None
            
            
            vector.add(fid=section.id,
                        geometry=multi,
                        external_weir=external_weir_id,
                        internal=section.internal,
                        drowned=int(section.drowned),
                        hydraulic_gradient=section.hydraulic_gradient,
                        downstream_hydraulic_head=section.downstream_hydraulic_head,
                        downstream_weir=downstream_weir,
                        downstream_weir_elevation=section.downstream_weir_elevation,
                        upstream_hydraulic_head=section.upstream_hydraulic_head,
                        upstream_weir=upstream_weir,
                        upstream_weir_elevation=section.upstream_weir_elevation,
                        from_upstream_pipe=section.from_upstream_pipe,
                        from_upstream_weir=section.from_upstream_weir,
                        to_downstream_pipe=section.to_downstream_pipe,
                        to_downstream_weir=section.to_downstream_weir,
                       branch=section.branch
                       )
            
        vector.write(rf"C:\Users\chris.kerklaan\Documents\Projecten\sewerage_designer\results\rijsbergen/gradients_height_{external_weir_id}.gpkg")
        vector = None
# Write some data # pip install threedi_raster_edits
import threedi_raster_edits as tre

# write upstream
vector =  tre.Vector.from_scratch("design", 5, 28992)


for section in n.upstream:
    # createe geometry
    all_points = [p.points for p in section.pipes]
    multi = tre.MultiLineString.from_points(all_points)
    vector.add(fid=section.id, geometry=multi)

    

vector.write(rf"C:\Users\chris.kerklaan\Documents\Projecten\sewerage_designer\results\rijsbergen/upstream_13.gpkg")
vector = None

