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
                
        p_source_dem = dem_rb.ReadAsArray(p_source_x,p_source_y,1,1)
        p_target_dem = dem_rb.ReadAsArray(p_target_x,p_target_y,1,1)
        
        if p_source_dem is None:
            print('Startpoint of pipe {leiding_id} is outside DEM extent'.format(leiding_id = feature_id))
            raise Exception('Startpoint of pipe {leiding_id} is outside DEM extent'.format(leiding_id = feature_id))
        if p_target_dem is None:
            print('Endpoint of pipe {leiding_id} is outside DEM extent'.format(leiding_id = feature_id))
            raise Exception('Endpoint of pipe {leiding_id} is outside DEM extent'.format(leiding_id = feature_id))
        
        p_source_dem = p_source_dem[0]
        p_target_dem = p_target_dem[0]
                        
        if p_source_dem == demNoData:
            raise Exception('No Data value in DEM for startpoint of pipe {leiding_id}'.format(leiding_id = feature_id))
        if p_target_dem == demNoData:
            raise Exception('No Data value in DEM for endpoint of pipe {leiding_id}'.format(leiding_id = feature_id))  

        cover_depth=float(min(p_source_dem-feature.lvl_start,p_target_dem-feature.lvl_end)[0])
        
        feature.SetField("coverdepth",cover_depth)
        trace_layer.SetFeature(feature)
        feature = None
           
    return p_source_dem,p_target_dem,cover_depth

if __name__ == "__main__":
    create_shp(trace_fn)
    p_source_dem,p_target_dem,cover_depth=calculate_cover_depth(dem_fn,trace_fn)