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

import os
import sys
sys.path.append(os.path.dirname(__file__))
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer, QgsMapLayerProxyModel

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
        self.mQgsFileWidget_PathEmptyGeopackage.setStorageMode(3) #set to save mode
        self.mQgsFileWidget_PathEmptyGeopackage.setFilter('*.gpkg')
        self.pushButton_CreateNewGeopackage.clicked.connect(self.pushbutton_create_new_geopackage_isChecked)
        self.mQgsFileWidget_PathGeopackage.setFilter('*.gpkg')
        self.pushButton_LoadGeopackage.clicked.connect(self.pushbutton_load_geopackage_isChecked)
        self.mMapLayerComboBox_DEM.setShowCrs(True)
        self.mMapLayerComboBox_DEM.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.mMapLayerComboBox_CS.setShowCrs(True)
        self.mMapLayerComboBox_CS.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.pushButton_ComputeCS.clicked.connect(self.pushbutton_computeCS_isChecked)        
        for key in AREA_WIDE_RAIN:
            self.comboBox_DesignRain.addItem(key)
        self.lineEdit_PeakIntensity.setText(str(max(AREA_WIDE_RAIN[list(AREA_WIDE_RAIN.keys())[0]]))) #initialise intensity with first event
        self.comboBox_DesignRain.currentTextChanged.connect(self.write_peak_intensity) #change intensity if users changes design event
        self.pushButton_ComputeDiameters.clicked.connect(self.pushbutton_computeDiameters_isChecked)        
        self.pushButton_ComputeDepths.clicked.connect(self.pushbutton_computeDepths_isChecked)
    
    def add_group(self,group_name):
        group=QgsProject.instance().layerTreeRoot().addGroup(group_name) 
        return group
    
    def add_layer_to_group(self,path,layername,group):       
        gpkg_layer=path+'|layername='f"{layername}"
        vlayer=QgsVectorLayer(gpkg_layer,layername,"ogr")
        if not vlayer.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vlayer,False)
            group.addLayer(vlayer)

    def get_geopackage_save_path(self):
        path=self.mQgsFileWidget_PathEmptyGeopackage.filePath()
        if not path.endswith('.gpkg'):
            path=path+'.gpkg'
        return path

    def get_geopackage_load_path(self):
        path=self.mQgsFileWidget_PathGeopackage.filePath()
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
        return layer
           
    def get_peak_intensity_design_event(self,AREA_WIDE_RAIN):
        event=self.comboBox_DesignRain.currentText()
        peak_intensity=max(AREA_WIDE_RAIN[event])
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
        
    def finished_computation_message(self,message):
        QtWidgets.QMessageBox.about(self,"Computation finished",message)
        
    def something_went_wrong_message(self,message):
        QtWidgets.QMessageBox.about(self,"Something went wrong",message)        

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
        network=create_sewerage_network(pipe_layer,weir_layer,pumping_station_layer,outlet_layer)
        return network
            
    def check_input(self):
        response=QtWidgets.QMessageBox.Yes #by definition if not changed
        intensity=self.get_final_peak_intensity_from_lineedit()
        check_intensity=self.get_peak_intensity_design_event(AREA_WIDE_RAIN)
        if not intensity==check_intensity:
            response=QtWidgets.QMessageBox.question(self,'Warning',('Peak intensity 'f"{intensity}"' mm/5min '
                                                        'does not match the peak intensity of the '
                                                        'design event. Want to continue?'),
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                    QtWidgets.QMessageBox.Cancel)
        return response

    def compute_CS(self):
        """Create a pipe network and calculate the connected surfaces
        Write back to QGIS layers"""
        if self.sewerage_network is None:
            self.sewerage_network=self.create_network_from_layers()
        for node in self.sewerage_network.network.nodes:
            print(self.sewerage_network.network.nodes[node])
        try:
            bgt_inlooptabel_fn=self.get_BGT_inlooptabel()
        except:
            message='BGT inlooptabel not defined.'
            self.something_went_wrong_message(message)          
        bgt_inlooptabel=BGTInloopTabel(bgt_inlooptabel_fn)
        #try:
        for pipe in self.sewerage_network.pipes.values():
            pipe.determine_connected_surface_area(bgt_inlooptabel)
            print(pipe.connected_surface_area)
            
        self.sewerage_network.accumulate_connected_surface_area()
        layers_list=self.get_list_of_sewerage_designer_layers()
        network_to_layers(self.sewerage_network,layers_list)
        message='The connected surfaces are computed. You can now proceed to compute the diameters.'
        self.finished_computation_message(message)
        #except Exception as ex:
            #message='Something went wrong: 'f"{ex}"
            #self.something_went_wrong_message(message)

    def read_attribute_values(self,layer,field):
        "return alls attribute values of a certain field of certain layer"
        values=[]
        for feature in layer.getFeatures():
            values.append(float(feature[field]))
        return values

    def compute_diameters(self):
        """Compute diameters for the current network and design rainfall event"""
        #TODO
        if self.sewerage_network is None:
            self.sewerage_network=self.create_network_from_layers()
        
        DEM=self.get_DEM()
        self.sewerage_network.add_elevation_to_network(DEM)
        weir=self.sewerage_network.weir
        global_settings_layer=self.get_map_layer('global_settings')
        minimum_freeboard=self.read_attribute_values(global_settings_layer,'minimum_freeboard')[0]
        print(minimum_freeboard);print(type(self.sewerage_network.weir.weir_level))
        self.sewerage_network.calculate_max_hydraulic_gradient(waking=minimum_freeboard[0])
        self.sewerage_network.evaluate_hydraulic_gradient_upstream(waking=minimum_freeboard)
        
        self.sewerage_network.calculate_discharge()
        self.sewerage_network.calculate_diameter()
        
        layers_list=self.get_list_of_sewerage_designer_layers()
        network_to_layers(self.sewerage_network,layers_list)
        message='The diameters are computed. You can now proceed to validate/ compute the depths.'
        self.finished_computation_message(message)
        
    def validate_depths(self,cover_depths):
        """Check if the computed depths fit the criteria of the minimum cover depth"""
        if self.sewerage_network is None:
            self.sewerage_network=self.create_network_from_layers()
        global_settings_layer=self.get_map_layer('global_settings')
        minimum_cover_depth=self.read_attribute_values(global_settings_layer,'minimum_cover_depth')[0]
        for pipe in self.sewerage_network.pipes.values():
            pipe.calculate_minimum_cover_depth(minimum_cover_depth)
        
        validated=True
        return validated

    def compute_depths(self):
        #try:
        DEM=self.get_DEM()
        cover_depths=hoofdfunctie_die_depths_berekent(DEM) #TODO
        validated=self.validate_depths(cover_depths)
        if validated:
            message='The depths are validated/ computed.'
            self.finished_computation_message(message)
        else:
            message='The depths could not be validated, please change design.'
            self.finished_computation_message(message)
        #except Exception as ex:
            #message='Something went wrong: 'f"{ex}"
            #self.something_went_wrong_message(message)        
    		   	
    def pushbutton_create_new_geopackage_isChecked(self):
        dest=self.get_geopackage_save_path()     
        if dest=='.gpkg':
            message='Please define file savepath'
            self.something_went_wrong_message(message)
            raise ValueError('No path defined')
        self.copy(GEOPACKAGE,dest)
        layernames=['global_settings','weir','pumping_station','outlet','manhole','sewerage']
        group_name='Sewerage Designer'
        group=self.add_group(group_name) 
        for layername in layernames:
            self.add_layer_to_group(dest,layername,group)
        
    def pushbutton_load_geopackage_isChecked(self):
        if QgsProject.instance().layerTreeRoot().findGroup('Sewerage Designer') != None:
            self.set_geopackage_load_path_if_group_in_project()
        else:
            gpkg=self.get_geopackage_load_path()
            if gpkg=='':
                message='Please define filepath'
                self.something_went_wrong_message(message) 
                raise ValueError('No path defined')
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
        self.compute_depths()
    
    def closeEvent(self,event):
        self.closingPlugin.emit()
        event.accept()
