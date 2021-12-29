# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 12:25:26 2021

@author: stijn.overmeen
"""

'''
Input is path to DEM and line element representing pipe:
Pipe consists of the following attributes (empty or not):
    id
    invert_level_start
    invert_level_end
    sewertype
    material
    diameter
    capacity
    area_basin
    cover_depth
Output is cover depth
'''
from osgeo import gdal
from osgeo import ogr,osr
import json

dem_fn='C:/Users/stijn.overmeen/Documents/GitHub/sewerage-designer/test/zundert.tif'
trace_fn='C:/Users/stijn.overmeen/Documents/GitHub/sewerage-designer/test_data/pipe.shp'

def create_shp(trace_fn):
    #Example pipe shapefile with two features
    
    # Set up the shapefile driver 
    driver = ogr.GetDriverByName("ESRI Shapefile")
    
    # Create the data source
    ds = driver.CreateDataSource(trace_fn)
    
    # Create the spatial reference system
    srs =  osr.SpatialReference()
    srs.ImportFromEPSG(28992)
    
    # Create one layer 
    layer = ds.CreateLayer("line", srs, ogr.wkbLineString)
    
    # Adding fields
    layer.CreateField(ogr.FieldDefn("id", ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn("lvl_start", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("lvl_end", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("sewertype", ogr.OFTString))
    layer.CreateField(ogr.FieldDefn("material", ogr.OFTString))
    layer.CreateField(ogr.FieldDefn("diameter", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("capacity", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("area_basin", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("coverdepth", ogr.OFTReal))
    
    point_x=[102913,103053,103153]
    point_y=[385634,385486,385374]
    lvl_start=[8,7.8]
    lvl_end=[7.8,7.6]
    
    # Creating a line geometry (Diepstraat, Wernhout (gemeente Zundert)) with two features
    for i in range(2):
        linegeo = ogr.Geometry(ogr.wkbLineString)
        linegeo.AddPoint(point_x[i],point_y[i])
        linegeo.AddPoint(point_x[i+1],point_y[i+1])
                       
        # Create the feature and set values
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetGeometry(linegeo)
        feature.SetField("id",i+1)
        feature.SetField("lvl_start",lvl_start[i])    
        feature.SetField("lvl_end",lvl_end[i])
        feature.SetField("diameter",0.5)
        layer.CreateFeature(feature)
        
        feature = None
    
    # Save and close DataSource
    ds = None   

def calculate_cover_depth(dem_fn,trace_fn):
    #cover_depth as minimum of cover_depth at start and end node
    
    p_source_dem_list=[];p_target_dem_list=[]
    
    dem_ds = gdal.Open(dem_fn)
    dem_rb = dem_ds.GetRasterBand(1)
    demNoData =  dem_rb.GetNoDataValue()
    gt = dem_ds.GetGeoTransform()
           
    trace_ds = ogr.Open(trace_fn,1)
    trace_layer = trace_ds.GetLayer(0)
    trace_layer.ResetReading()
    for feature in trace_layer:
        print(feature.GetFID())
        if feature.id is None:
            raise Exception('Not all pipes have an ID')
                
        feature_id = feature.id
        feature_geometry = feature.GetGeometryRef()
        geometry_json = feature_geometry.ExportToJson()
        geometry_coordinates = json.loads(geometry_json)['coordinates']
        geometry_length = feature_geometry.Length()
        
        edge_source_coordinates = tuple(geometry_coordinates[0])
        edge_target_coordinates = tuple(geometry_coordinates[-1]) 
        edge_key = (edge_source_coordinates, edge_target_coordinates)
           
        # sample dem voor begin en eindpunt van de leiding
        p_source_x = int((edge_source_coordinates[0] - gt[0]) / gt[1]) #x pixel
        p_source_y = int((edge_source_coordinates[1] - gt[3]) / gt[5]) #y pixel
    
        p_target_x = int((edge_target_coordinates[0] - gt[0]) / gt[1]) #x pixel
        p_target_y = int((edge_target_coordinates[1] - gt[3]) / gt[5]) #y pixel
        
        # sample dem voor tussenliggende punten
        def intermediates(p1,p2,nb_points):
            x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
            y_spacing = (p2[1] - p1[1]) / (nb_points + 1)
        
            return [[p1[0] + i * x_spacing, p1[1] +  i * y_spacing] 
                    for i in range(1, nb_points+1)]
        
        points=[]
        points.append([p_source_x,p_source_y])
        for point in intermediates([p_source_x,p_source_y],[p_target_x,p_target_y],100):
            points.append(point)
        points.append([p_target_x,p_target_y])
        
        dem_elevation=[]
        for point in points:
            dem_elevation.append(dem_rb.ReadAsArray(point[0],point[1],1,1)[0][0])

        # bereken ook de bovenkant buis ter hoogte van deze punten
        diameter = 0.4 #voorbeeld diameter
        thickness = 0.1 #voorbeeld wanddikte
        pipe_elevation=[]
        pipe_elevation.append(feature.lvl_start)
        for elevation in intermediates([feature.lvl_start,feature.lvl_start],[feature.lvl_end,feature.lvl_end],100):
            pipe_elevation.append(elevation[0])
        pipe_elevation.append(feature.lvl_end)

        # bereken de cover depths
        cover_depths=[]
        for i in range(len(points)):
            cover_depths.append(dem_elevation[i]-(pipe_elevation[i]+diameter+thickness))
        
        # minimale cover depth
        cover_depth=min(cover_depths)
        
        feature.SetField("coverdepth",cover_depth)
        trace_layer.SetFeature(feature)
        feature = None
                   
    return p_source_x,p_source_y,p_target_x,p_target_y,int_points,points,dem_elevation,pipe_elevation,cover_depths,cover_depth

if __name__ == "__main__":
    #create_shp(trace_fn)
    p_source_x,p_source_y,p_target_x,p_target_y,int_points,points,dem_elevation,pipe_elevation,cover_depths,cover_depth=calculate_cover_depth(dem_fn,trace_fn)