# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SewerageDesignerDockWidget
                                 A QGIS plugin
 Design sewer systems 
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-01-12
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Nelen & Schuurmans
        email                : info@nelen-schuurmans.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import traceback
import os
import sys
sys.path.append(os.path.dirname(__file__))
from qgis import processing
from qgis.utils import iface
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal,QVariant
from qgis.core import QgsProject,QgsVectorLayer,QgsRasterLayer,QgsMapLayerProxyModel,QgsField,QgsLineSymbol
from qgis.core.additions.edit import edit

from qgis_connector import *
from sewerage_designer_core.sewerage_designer_classes import *
from sewerage_designer_core.constants import *

FORM_CLASS,_=uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'sewerage_designer_dockwidget_base.ui'))

GEOPACKAGE=os.path.join(os.path.dirname(__file__),'geopackage','sewerage.gpkg')
	
class SewerageDesignerDockWidget(QtWidgets.QDockWidget,FORM_CLASS):
    closingPlugin=pyqtSignal()
    
    def __init__(self,parent=None):
        """Constructor."""
        super(SewerageDesignerDockWidget,self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.setupUi(self)
        self.sewerage_network=None      
        if QgsProject.instance().layerTreeRoot().findGroup('Sewerage Designer') != None:
            self.set_geopackage_load_path_if_group_in_project()
        self.mQgsFileWidget_PathGeopackage.setStorageMode(3) #set to save mode
        self.mQgsFileWidget_PathGeopackage.setConfirmOverwrite(False)
        self.mQgsFileWidget_PathGeopackage.setFilter('*.gpkg')
        self.mQgsFileWidget_PathGeopackage.fileChanged.connect(self.filepath_create_or_load_geopackage_isChanged)
        self.mMapLayerComboBox_DEM.setShowCrs(True)
        self.mMapLayerComboBox_DEM.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.mMapLayerComboBox_CS.setShowCrs(True)
        self.mMapLayerComboBox_CS.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        self.pushButton_ComputeCS.clicked.connect(self.pushbutton_computeCS_isChecked)        
        for key in AREA_WIDE_RAIN:
            self.comboBox_DesignRain.addItem(key)
        self.lineEdit_PeakIntensity.setText(str(round(max(AREA_WIDE_RAIN[list(AREA_WIDE_RAIN.keys())[0]])*12,1))) #initialise intensity with first event
        self.comboBox_DesignRain.currentTextChanged.connect(self.write_peak_intensity) #change intensity if users changes design event
        self.pushButton_ComputeDiameters.clicked.connect(self.pushbutton_computeDiameters_isChecked)        
        self.pushButton_ComputeDepths.clicked.connect(self.pushbutton_computeDepths_isChecked)
    
    def add_group(self,group_name):
        root=QgsProject.instance().layerTreeRoot()
        for group in [child for child in root.children() if child.nodeType() == 0]:
            if group.name()==group_name:
                root.removeChildNode(group)
        group=root.insertGroup(0,group_name)
        return group
    
    def add_layer_to_group(self,path,layername,group):       
        gpkg_layer=path+'|layername='f"{layername}"
        vlayer=QgsVectorLayer(gpkg_layer,layername,"ogr")
        if not vlayer.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vlayer,False)
            group.addLayer(vlayer)

    def get_geopackage_create_or_load_path(self):
        path=self.mQgsFileWidget_PathGeopackage.filePath()
        if not path.endswith('.gpkg'):
            path=path+'.gpkg'
        return path
    
    def set_geopackage_load_path_if_group_in_project(self):
        path=self.get_map_layer('sewerage').source()
        if "|layername" in path: 
            path=path.split("|",1)[0] #remove layername (get path before)
        self.mQgsFileWidget_PathGeopackage.setFilePath(path)
            
    def get_DEM(self):
        path=self.mMapLayerComboBox_DEM.currentLayer().source()
        return path
    
    def get_BGT_inlooptabel(self):
        BGT_inlooptabel=self.mMapLayerComboBox_CS.currentLayer().source()
        if "|layername" in BGT_inlooptabel: 
            BGT_inlooptabel=BGT_inlooptabel.split("|",1)[0] #remove layername (get path before)
        return BGT_inlooptabel
    
    def get_map_layer(self,name):
        layer=QgsProject.instance().mapLayersByName(name)[0]
        if layer.isEditable():
            iface.actionToggleEditing().trigger()
        return layer
           
    def get_peak_intensity_design_event(self,AREA_WIDE_RAIN):
        event=self.comboBox_DesignRain.currentText()
        peak_intensity=round(max(AREA_WIDE_RAIN[event])*12,1)
        return peak_intensity
    
    def write_peak_intensity(self):
        peak_intensity=self.get_peak_intensity_design_event(AREA_WIDE_RAIN)
        self.lineEdit_PeakIntensity.setText(str(peak_intensity))
        
    def get_final_peak_intensity_from_lineedit(self):
        final_peak_intensity=float(self.lineEdit_PeakIntensity.text())
        return final_peak_intensity
        #final intensity can be changed by user from standard maximum corresponding to design event
          
    def copy(self,source,dest):
    	with open(source,'rb') as src, open(dest,'wb') as dst: dst.write(src.read())

    def info_message(self,message):
        QtWidgets.QMessageBox.about(self,"Info",'<FONT COLOR=''#ffffff>'f"{message}"'</FONT>')
        
    def finished_computation_message(self,message):
        QtWidgets.QMessageBox.about(self,"Computation finished",'<FONT COLOR=''#ffffff>'f"{message}"'</FONT>')
        
    def something_went_wrong_message(self,message):
        QtWidgets.QMessageBox.about(self,"Something went wrong",'<FONT COLOR=''#d6d6d6>'f"{message}"'</FONT>')        

    def get_sewerage_designer_layers(self):
        #get and check if all required SewerageDesigner layers exist in QGIS project
        #for now layer needs to exist in gpkg, can possibly be empty dependent on sewerage type
        #see create_network_from_layers
        try:
            global_settings_layer=self.get_map_layer('global_settings')
            pipe_layer=self.get_map_layer('sewerage')
            weir_layer=self.get_map_layer('weir')
            pumping_station_layer=self.get_map_layer('pumping_station')
            outlet_layer=self.get_map_layer('outlet')
        except:
            message='Your sewerage design is not complete, some layers are missing. Please re-load your design.'
            self.something_went_wrong_message(message)
        return global_settings_layer,pipe_layer,weir_layer,pumping_station_layer,outlet_layer
    
    def get_list_of_sewerage_designer_layers(self):
        global_settings_layer,pipe_layer,weir_layer,pumping_station_layer,outlet_layer=self.get_sewerage_designer_layers()
        list_of_layers=[pipe_layer,weir_layer,pumping_station_layer,outlet_layer]
        return list_of_layers
            
    def create_network_from_layers(self):
        global_settings_layer,pipe_layer,weir_layer,pumping_station_layer,outlet_layer=self.get_sewerage_designer_layers()
        network,loop,loop_pipe_fids=create_sewerage_network(pipe_layer,weir_layer,pumping_station_layer,outlet_layer)
        return network,loop,loop_pipe_fids
            
    def check_input(self):
        response=QtWidgets.QMessageBox.Yes #by definition if not changed
        intensity=self.get_final_peak_intensity_from_lineedit()
        check_intensity=self.get_peak_intensity_design_event(AREA_WIDE_RAIN)
        if not intensity==check_intensity:
            box=QtWidgets.QMessageBox()
            message='Peak intensity 'f"{intensity}"' mm/5min does not match the peak intensity of the design event. Want to continue?'
            styled_message='<FONT COLOR=''#ffffff>'f"{message}"'</FONT>'
            response=box.question(self,'Warning',styled_message,
                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                  QtWidgets.QMessageBox.Cancel)

        return response

    def compute_CS(self):
        """Create a pipe network and calculate the connected surfaces
        Write back to QGIS layers"""
        try:
            self.sewerage_network,loop,loop_pipe_fids=self.create_network_from_layers()
            if loop:
                message=f"Network has a loop, pipe FIDs: {loop_pipe_fids}"
                self.something_went_wrong_message(message)
                sewerage_layer=self.get_map_layer('sewerage')
                clone=self.make_clone(sewerage_layer,loop_pipe_fids,'pipes that form a loop')
                with edit(clone):            
                    field_ids=[]
                    fieldnames=set(['fid'])
                    for field in clone.fields():
                        if field.name() not in fieldnames:
                          field_ids.append(clone.fields().indexFromName(field.name()))
                    
                symbol=QgsLineSymbol.createSimple({'color':'red','capstyle':'round'})
                clone.renderer().setSymbol(symbol)
                clone.setBlendMode(QtGui.QPainter.CompositionMode_HardLight)
                clone.triggerRepaint()
            
                clone.dataProvider().deleteAttributes(field_ids)
                clone.updateFields()                
                QgsProject.instance().addMapLayer(clone)
                clone.selectAll()
                iface.actionZoomToSelected().trigger() 
                clone.removeSelection() 
                
                return
            
            try:
                bgt_inlooptabel_fn=self.get_BGT_inlooptabel()
            except:
                message='BGT inlooptabel not defined.'
                self.something_went_wrong_message(message)          
            bgt_inlooptabel=BGTInloopTabel(bgt_inlooptabel_fn)
            for pipe in self.sewerage_network.pipes.values():
                pipe.connected_surface_area = 0.0
                pipe.determine_connected_surface_area(bgt_inlooptabel)
                
            self.sewerage_network.accumulate_connected_surface_area()
            sewerage_layer=self.get_map_layer('sewerage')
            pipes_with_empty_accumulated_fields=core_to_layer(self.sewerage_network,sewerage_layer)
            if not pipes_with_empty_accumulated_fields:
                message='The connected surfaces are computed. You can now proceed to compute the diameters.'
                self.finished_computation_message(message)
            else: #we have some zeros accumulated connected surfaces
                message=f"Some pipes have no accumulated connected surfaces, pipe FIDs: {pipes_with_empty_accumulated_fields}"
                self.something_went_wrong_message(message)
                sewerage_layer=self.get_map_layer('sewerage')
                clone=self.make_clone(sewerage_layer,pipes_with_empty_accumulated_fields,'pipes with no accumulated connected surfaces')
                with edit(clone):            
                    field_ids=[]
                    fieldnames=set(['fid','accumulated_connected_surface_area'])
                    for field in clone.fields():
                        if field.name() not in fieldnames:
                          field_ids.append(clone.fields().indexFromName(field.name()))
                    
                symbol=QgsLineSymbol.createSimple({'color':'red','capstyle':'round'})
                clone.renderer().setSymbol(symbol)
                clone.setBlendMode(QtGui.QPainter.CompositionMode_HardLight)
                clone.triggerRepaint()
            
                clone.dataProvider().deleteAttributes(field_ids)
                clone.updateFields()                
                QgsProject.instance().addMapLayer(clone) 
                clone.selectAll()
                iface.actionZoomToSelected().trigger() 
                clone.removeSelection() 

        except Exception as ex:
            message='\n'.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
            self.something_went_wrong_message(message)

    def read_attribute_values(self,layer,field):
        "return alls attribute values of a certain field of certain layer"
        values=[]
        for feature in layer.getFeatures():
            values.append(float(feature[field]))
        return values

    def compute_diameters(self):
        """Compute diameters for the current network and design rainfall event"""
        try:
            self.sewerage_network,loop,loop_pipe_fids=self.create_network_from_layers()
            DEM=self.get_DEM()
            self.sewerage_network.add_elevation_to_network(DEM)
            global_settings_layer=self.get_map_layer('global_settings')
            minimum_freeboard=self.read_attribute_values(global_settings_layer,'minimum_freeboard')[0]
            self.sewerage_network.calculate_max_hydraulic_gradient(waking=minimum_freeboard)
            #self.sewerage_network.evaluate_hydraulic_gradient_upstream(waking=minimum_freeboard)
            vmax=self.read_attribute_values(global_settings_layer,'maximum_velocity')[0]
            peak_intensity = self.get_final_peak_intensity_from_lineedit()
            
            velocity_to_high_pipe_fids=[];d=[]
            for pipe_id, pipe in self.sewerage_network.pipes.items():
                pipe.calculate_discharge(intensity=peak_intensity)
                pipe.calculate_diameter(vmax)
                d.append(pipe.diameter)
                pipe.set_material()
                if pipe.velocity_to_high:
                    velocity_to_high_pipe_fids.append(pipe_id)
                
            sewerage_layer=self.get_map_layer('sewerage')
            core_to_layer(self.sewerage_network,sewerage_layer)
            if not velocity_to_high_pipe_fids:
                message='The diameters are computed. You can now proceed to validate/ compute the depths.'
                self.finished_computation_message(message)
            else:
                message=f"The velocity in some pipes is too large, pipe FIDs: {velocity_to_high_pipe_fids}"
                self.something_went_wrong_message(message)
                sewerage_layer=self.get_map_layer('sewerage')
                clone=self.make_clone(sewerage_layer,velocity_to_high_pipe_fids,'pipes with excessive velocities')
                with edit(clone):            
                    field_ids=[]
                    fieldnames=set(['fid','velocity'])
                    for field in clone.fields():
                        if field.name() not in fieldnames:
                          field_ids.append(clone.fields().indexFromName(field.name()))
                    
                symbol=QgsLineSymbol.createSimple({'color':'red','line_width':str((max(d))*9.2),'line_width_unit':'Pixel','capstyle':'round'})
                clone.renderer().setSymbol(symbol)
                clone.setBlendMode(QtGui.QPainter.CompositionMode_HardLight)
                clone.triggerRepaint()
            
                clone.dataProvider().deleteAttributes(field_ids)
                clone.updateFields()                
                QgsProject.instance().addMapLayer(clone)
                clone.selectAll()
                iface.actionZoomToSelected().trigger() 
                clone.removeSelection() 
                
        except Exception as ex:
            message='\n'.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
            self.something_went_wrong_message(message)

    def make_clone(self,layer,features_to_be_cloned,name):
        layer.select(features_to_be_cloned)
        clone=processing.run("native:saveselectedfeatures",{'INPUT':layer,'OUTPUT':'memory:'})['OUTPUT']
        layer.removeSelection()
        clone.setName(name)      
        return clone       
        
    def validate_depths(self):
        """Check if the computed depths fit the criteria of the minimum cover depth"""
        try:
            self.sewerage_network,loop,loop_pipe_fids=self.create_network_from_layers()
            global_settings_layer=self.get_map_layer('global_settings')
            minimum_cover_depth=self.read_attribute_values(global_settings_layer,'minimum_cover_depth')[0]
            DEM=self.get_DEM()
            self.sewerage_network.add_elevation_to_network(DEM) #re-do this because user can change the DEM after compute diameters
            validated=[];d=[]
            self.sewerage_network.calculate_cover_depth()
            for pipe in self.sewerage_network.pipes.values():
                d.append(pipe.diameter)
                if pipe.cover_depth>minimum_cover_depth:
                    validated.append(True)
                else:
                    validated.append(False)
            sewerage_layer=self.get_map_layer('sewerage')
            core_to_layer(self.sewerage_network,sewerage_layer)
            if all(validated):
                message='Valid design! The cover depth of all pipes meet the minimum depth requirement.'
                self.finished_computation_message(message)
            else:
                max_d=max(d)
                self.create_layer_of_faulty_cover_depths(minimum_cover_depth,max_d)
                message='Invalid design! The cover depth of some pipes do not meet the minimum depth requirement. These pipes have been colored red.'
                self.finished_computation_message(message)
        except Exception as ex:
            message='\n'.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
            self.something_went_wrong_message(message)

    def create_layer_of_faulty_cover_depths(self,minimum_cover_depth,max_d):
        layer=self.get_map_layer('sewerage')
        layer.selectAll()
        clone=processing.run("native:saveselectedfeatures",{'INPUT':layer,'OUTPUT':'memory:'})['OUTPUT']
        layer.removeSelection()
        clone.setName('pipes with unsufficient cover depth')
        clone.dataProvider().addAttributes([QgsField("minimum_cover_depth",QVariant.Double)])
        clone.dataProvider().addAttributes([QgsField("validated?",QVariant.Bool)])
        clone.updateFields()
        
        with edit(clone):            
            field_ids=[]
            fieldnames=set(['fid','cover_depth','minimum_cover_depth','validated?'])
            for field in clone.fields():
                if field.name() not in fieldnames:
                  field_ids.append(clone.fields().indexFromName(field.name()))
                if field.name()=='cover_depth':
                    features=clone.getFeatures()
                    for feature in features:
                        cover_depth=feature['cover_depth']
                        value=True if minimum_cover_depth<cover_depth else False
                        if value:
                            clone.deleteFeature(feature.id())
                        else:
                            feature['validated?']=QVariant(value)
                            clone.updateFeature(feature)
                elif field.name()=='minimum_cover_depth':
                    features=clone.getFeatures()
                    for feature in features:
                        feature['minimum_cover_depth']=minimum_cover_depth
                        clone.updateFeature(feature)
    
        clone.dataProvider().deleteAttributes(field_ids)
        clone.updateFields()
        
        symbol=QgsLineSymbol.createSimple({'color':'red','line_width':str(max_d*9.2),'line_width_unit':'Pixel','capstyle':'round'})
        clone.renderer().setSymbol(symbol)
        clone.setBlendMode(QtGui.QPainter.CompositionMode_HardLight)
        clone.triggerRepaint()
        
        QgsProject.instance().addMapLayer(clone)
        clone.selectAll()
        iface.actionZoomToSelected().trigger() 
        clone.removeSelection()

        
    		   	
    def filepath_create_or_load_geopackage_isChanged(self):
        gpkg=self.get_geopackage_create_or_load_path()
        if gpkg=='.gpkg':
            return
        else:
            if os.path.isfile(gpkg):
                message='Loaded your design.'
                self.info_message(message)
            else:
                self.copy(GEOPACKAGE,gpkg)
                message='New design created.'
                self.info_message(message)
        layernames=['global_settings','weir','pumping_station','outlet','manhole','sewerage']
        group_name='Sewerage Designer'
        group=self.add_group(group_name) 
        for layername in layernames:
            self.add_layer_to_group(gpkg,layername,group)        
                   
    def pushbutton_computeCS_isChecked(self):
        self.compute_CS()
        
    def pushbutton_computeDiameters_isChecked(self):
        response=self.check_input()
        if response==QtWidgets.QMessageBox.Yes:
            self.compute_diameters()
        
    def pushbutton_computeDepths_isChecked(self):
        self.validate_depths()
    
    def closeEvent(self,event):
        self.closingPlugin.emit()
        event.accept()
