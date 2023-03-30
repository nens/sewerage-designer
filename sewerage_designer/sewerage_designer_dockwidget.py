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
import subprocess

sys.path.append(os.path.dirname(__file__))
from qgis import processing
from qgis.utils import iface
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import QThread, pyqtSignal, QVariant
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsMapLayerProxyModel,
    QgsField,
    QgsLineSymbol,
    QgsProperty,
    QgsLayerTreeLayer,
)
from qgis.core.additions.edit import edit

from qgis_connector import *
from designer.designer import *
from designer.constants import *

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "sewerage_designer_dockwidget_base.ui")
)

GEOPACKAGE = os.path.join(os.path.dirname(__file__), "geopackage", "sewerage.gpkg")

class SewerageDesignerDockWidget(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(SewerageDesignerDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.setupUi(self)

        #initialise progress
        self.QProgressBar.setValue(0)
        self.QLabel_ProgressBar.setText("")

        self.sewerage_network = None
        if QgsProject.instance().layerTreeRoot().findGroup("Sewerage Designer") != None:
            self.set_geopackage_load_path_if_group_in_project()
        self.mQgsFileWidget_PathGeopackage.setStorageMode(3)  # set to save mode
        self.mQgsFileWidget_PathGeopackage.setConfirmOverwrite(False)
        self.mQgsFileWidget_PathGeopackage.setFilter("*.gpkg")
        self.mQgsFileWidget_PathGeopackage.fileChanged.connect(
            self.filepath_create_or_load_geopackage_isChanged
        )
        self.mMapLayerComboBox_DEM.setShowCrs(True)
        self.mMapLayerComboBox_DEM.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.mMapLayerComboBox_CS.setShowCrs(True)
        self.mMapLayerComboBox_CS.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        for key in AREA_WIDE_RAIN:
            self.comboBox_DesignRain.addItem(key)
        self.lineEdit_PeakIntensity.setText(
            str(round(max(AREA_WIDE_RAIN[list(AREA_WIDE_RAIN.keys())[0]]) * 12, 1))
        )  # initialise intensity with first event
        self.comboBox_DesignRain.currentTextChanged.connect(
            self.write_peak_intensity
        )  # change intensity if users changes design event

        self.pushButton_ComputeCS.clicked.connect(self.pushbutton_computeCS_isChecked)
        self.pushButton_ComputeDiameters.clicked.connect(self.pushbutton_computeDiameters_isChecked)
        self.pushButton_ComputeDepths.clicked.connect(self.pushbutton_computeDepths_isChecked)

        #self.connect_button_clicked(self.pushButton_ComputeCS, self.pushbutton_computeCS_isChecked)
        #self.connect_button_clicked(self.pushButton_ComputeDiameters, self.pushbutton_computeDiameters_isChecked)
        #self.connect_button_clicked(self.pushButton_ComputeDepths, self.pushbutton_computeDepths_isChecked)

        self.radioButton_Help.clicked.connect(self.radiobutton_help_isChecked)

    def connect_button_clicked(self, button, slot):
        #disable panel and run [not used]
        #button.clicked.connect(lambda: self.enable_plugin(disable = True))
        button.clicked.connect(slot)

    def update_progress(self, value):
        # Update the progress bar
        self.QProgressBar.setValue(value)

    def update_status(self, status_text):
        # Update the status label
        self.QLabel_ProgressBar.setText(status_text)

    def finished_computation_message(self, message):
        QtWidgets.QMessageBox.about(
            self,
            "Computation finished",
            "<FONT COLOR=" "#ffffff>" f"{message}" "</FONT>",
        )

    def something_went_wrong_message(self, message):
        QtWidgets.QMessageBox.about(
            self,
            "Something went wrong",
            "<FONT COLOR=" "#d6d6d6>" f"{message}" "</FONT>",
        )

    def traceback_message(self, trace):
        QtWidgets.QMessageBox.about(
            self, "Something went wrong", "<FONT COLOR=" "#d6d6d6>" f"{trace}" "</FONT>"
        )

    def info_message(self, message):
        QtWidgets.QMessageBox.about(
            self, "Info", "<FONT COLOR=" "#ffffff>" f"{message}" "</FONT>"
        )

    def something_went_wrong_message_with_traceback(self, ex):
        box = QtWidgets.QMessageBox()
        styled_message = "<FONT COLOR=" "#d6d6d6>" f"{ex}" "</FONT>"
        trace = "\n".join(
            traceback.format_exception(
                etype=type(ex), value=ex, tb=ex.__traceback__
            )
        )
        response = box.question(
            self,
            "Something went wrong",
            styled_message,
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Help,
            QtWidgets.QMessageBox.Ok,
        )
        if response == QtWidgets.QMessageBox.Help:
            QtWidgets.QMessageBox.about(
                self,
                "Something went wrong",
                "<FONT COLOR=" "#d6d6d6>" f"{trace}" "</FONT>",
            )

    def add_group(self, group_name):
        root = QgsProject.instance().layerTreeRoot()
        for group in [child for child in root.children() if child.nodeType() == 0]:
            if group.name() == group_name:
                root.removeChildNode(group)
        group = root.insertGroup(0, group_name)
        return group

    def add_layer_to_group(self, path, layername, group):
        gpkg_layer = path + "|layername=" f"{layername}"
        vlayer = QgsVectorLayer(gpkg_layer, layername, "ogr")
        if not vlayer.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vlayer, False)
            group.addLayer(vlayer)

    def get_geopackage_create_or_load_path(self):
        path = self.mQgsFileWidget_PathGeopackage.filePath()
        if not path.endswith(".gpkg"):
            path = path + ".gpkg"
        return path

    def set_geopackage_load_path_if_group_in_project(self):
        path = self.get_map_layer("sewerage").source()
        if "|layername" in path:
            path = path.split("|", 1)[0]  # remove layername (get path before)
        self.mQgsFileWidget_PathGeopackage.setFilePath(path)

    def get_DEM(self):
        path = self.mMapLayerComboBox_DEM.currentLayer().source()
        return path

    def get_BGT_inlooptabel(self):
        BGT_inlooptabel = self.mMapLayerComboBox_CS.currentLayer().source()
        if "|layername" in BGT_inlooptabel:
            BGT_inlooptabel = BGT_inlooptabel.split("|", 1)[
                0
            ]  # remove layername (get path before)
        return BGT_inlooptabel

    def get_map_layer(self, name):
        layer = QgsProject.instance().mapLayersByName(name)[0]
        if layer.isEditable():
            iface.actionToggleEditing().trigger()
        return layer

    def get_peak_intensity_design_event(self, AREA_WIDE_RAIN):
        event = self.comboBox_DesignRain.currentText()
        peak_intensity = round(max(AREA_WIDE_RAIN[event]) * 12, 1)
        return event, peak_intensity

    def write_peak_intensity(self):
        event, peak_intensity = self.get_peak_intensity_design_event(AREA_WIDE_RAIN)
        self.lineEdit_PeakIntensity.setText(str(peak_intensity))

    def get_final_peak_intensity_from_lineedit(self):
        final_peak_intensity = float(self.lineEdit_PeakIntensity.text())
        return final_peak_intensity
        # final intensity can be changed by user from standard maximum corresponding to design event

    def copy(self, source, dest):
        with open(source, "rb") as src, open(dest, "wb") as dst:
            dst.write(src.read())

    def check_input(self):
        response = QtWidgets.QMessageBox.Yes  # by definition if not changed
        intensity = self.get_final_peak_intensity_from_lineedit()
        event, check_intensity = self.get_peak_intensity_design_event(AREA_WIDE_RAIN)
        rain_sum = round(sum(AREA_WIDE_RAIN[event]), 1)
        if not intensity == check_intensity:
            altered_event = [intensity if x == max(AREA_WIDE_RAIN[event]) else x for x in AREA_WIDE_RAIN[event]]
            rain_sum = round(sum(altered_event), 1)
            box = QtWidgets.QMessageBox()
            message = (
                "Peak intensity "
                f"{intensity}"
                " mm/hour does not match the peak intensity of the design event. Want to continue?"
            )
            styled_message = "<FONT COLOR=" "#ffffff>" f"{message}" "</FONT>"
            response = box.question(
                self,
                "Warning",
                styled_message,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.Cancel,
            )

        return response, rain_sum

    def mistakes_in_network_error(
        self, pipe_fids, layer_name, fields_of_interest, message
    ):
        """
        Reports mistakes in design in message and adds a layer that highlights the faulty pipes
        """
        self.something_went_wrong_message(message)
        sewerage_layer = self.get_map_layer("sewerage")
        clone = self.make_clone(sewerage_layer, pipe_fids, layer_name)
        with edit(clone):
            field_ids = []
            fieldnames = set(fields_of_interest)
            for field in clone.fields():
                if field.name() not in fieldnames:
                    field_ids.append(clone.fields().indexFromName(field.name()))

        if "diameter" in fields_of_interest:
            symbol = QgsLineSymbol.createSimple(
                {"color": "red", "capstyle": "round", "line_width_unit": "Pixel"}
            )
            symbol.setDataDefinedWidth(QgsProperty.fromExpression('"diameter"*9.2'))
        else:
            symbol = QgsLineSymbol.createSimple(
                {
                    "color": "red",
                    "line_width": "6",
                    "line_width_unit": "Pixel",
                    "capstyle": "round",
                }
            )
        clone.renderer().setSymbol(symbol)
        clone.setBlendMode(QtGui.QPainter.CompositionMode_HardLight)
        clone.triggerRepaint()

        clone.dataProvider().deleteAttributes(field_ids)
        clone.updateFields()
        QgsProject.instance().addMapLayer(clone)
        clone.selectAll()
        iface.actionZoomToSelected().trigger()
        clone.removeSelection()

    def read_global_settings_value(self, layer, field):
        "return attribute field"
        values = []
        for feature in layer.getFeatures():
            values.append(float(feature[field]))
        if not values:
            message = "Global settings layer is empty. Please define settings."
            self.something_went_wrong_message(message)
            raise ValueError(message)
        if len(values) == 1:
            return values[0]
        if len(values) > 1:
            message = "Multiple settings have been defined in the global settings layer. "\
                             "Please fill in only once."
            self.something_went_wrong_message(message)
            raise ValueError(message)

    def make_clone(self, layer, features_to_be_cloned, name):
        layer.select(features_to_be_cloned)
        clone = processing.run(
            "native:saveselectedfeatures", {"INPUT": layer, "OUTPUT": "memory:"}
        )["OUTPUT"]
        layer.removeSelection()
        clone.setName(name)
        return clone

    def filepath_create_or_load_geopackage_isChanged(self):
        gpkg = self.get_geopackage_create_or_load_path()
        if gpkg == ".gpkg":
            return
        else:
            if os.path.isfile(gpkg):
                message = "Loaded your design."
                self.info_message(message)
            else:
                self.copy(GEOPACKAGE, gpkg)
                message = "New design created."
                self.info_message(message)
        layernames = [
            "global_settings",
            "weir",
            "pumping_station",
            "outlet",
            "manhole",
            "sewerage",
        ]
        group_name = "Sewerage Designer"
        group = self.add_group(group_name)
        for layername in layernames:
            self.add_layer_to_group(gpkg, layername, group)

    def get_sewerage_designer_layers(self):
        # get and check if all required SewerageDesigner layers exist in QGIS project
        # for now layer needs to exist in gpkg, can possibly be empty dependent on sewerage type
        # see create_network_from_layers
        try:
            global_settings_layer = self.get_map_layer("global_settings")
            sewerage_layer = self.get_map_layer("sewerage")
            weir_layer = self.get_map_layer("weir")
            pumping_station_layer = self.get_map_layer("pumping_station")
            outlet_layer = self.get_map_layer("outlet")
        except:
            message = "Your sewerage design is not complete, some layers are missing. Please re-load your design."
            self.something_went_wrong_message(message)
        return (
            global_settings_layer,
            sewerage_layer,
            weir_layer,
            pumping_station_layer,
            outlet_layer,
        )

    def pushbutton_computeCS_isChecked(self):
        """Create a pipe network and calculate the connected surfaces
        Write back to QGIS layers"""

        (
            global_settings_layer,
            sewerage_layer,
            weir_layer,
            pumping_station_layer,
            outlet_layer,
        ) = self.get_sewerage_designer_layers()

        #TODO CHECK CHECKERS ON THIS INPUT
        try:
            bgt_inlooptabel_fn = self.get_BGT_inlooptabel()
        except:
            message = "BGT inlooptabel not defined."
            self.something_went_wrong_message(message)

        self.worker_compute_cs = Worker(
            process = "Compute CS",
            global_settings_layer = global_settings_layer,
            sewerage_layer = sewerage_layer,
            weir_layer = weir_layer,
            outlet_layer = outlet_layer,
            pumping_station_layer = pumping_station_layer,
            bgt_inlooptabel_fn = bgt_inlooptabel_fn
        )
        self.worker_compute_cs.progress_changed.connect(self.update_progress)
        self.worker_compute_cs.status_changed.connect(self.update_status)
        self.worker_compute_cs.mistakes_in_network.connect(self.mistakes_in_network_error)
        self.worker_compute_cs.computation_finished.connect(self.finished_computation_message)
        self.worker_compute_cs.exception.connect(self.something_went_wrong_message_with_traceback)
        self.worker_compute_cs.enable_plugin.connect(self.enable_plugin)

        self.worker_compute_cs.start()

    def pushbutton_computeDiameters_isChecked(self):
        """Compute diameters for the current network and design rainfall event"""

        (
            global_settings_layer,
            sewerage_layer,
            weir_layer,
            pumping_station_layer,
            outlet_layer,
        ) = self.get_sewerage_designer_layers()

        #TODO CHECK CHECKERS ON THIS INPUT
        dem = self.get_DEM()
        global_settings_layer = self.get_map_layer("global_settings")
        minimum_freeboard = self.read_global_settings_value(
            global_settings_layer, "minimum_freeboard"
        )
        vmax = self.read_global_settings_value(
            global_settings_layer, "maximum_velocity"
        )
        peak_intensity = self.get_final_peak_intensity_from_lineedit()

        check, rain_sum = self.check_input()

        self.worker_compute_diameters = Worker(
            process = "Compute Diameters",
            global_settings_layer = global_settings_layer,
            sewerage_layer = sewerage_layer,
            weir_layer = weir_layer,
            outlet_layer = outlet_layer,
            pumping_station_layer = pumping_station_layer,
            dem = dem,
            minimum_freeboard = minimum_freeboard,
            vmax = vmax,
            peak_intensity = peak_intensity,
            rain_sum = rain_sum,
        )
        self.worker_compute_diameters.progress_changed.connect(self.update_progress)
        self.worker_compute_diameters.status_changed.connect(self.update_status)
        self.worker_compute_diameters.mistakes_in_network.connect(self.mistakes_in_network_error)
        self.worker_compute_diameters.computation_finished.connect(self.finished_computation_message)
        self.worker_compute_diameters.exception.connect(self.something_went_wrong_message_with_traceback)
        self.worker_compute_diameters.enable_plugin.connect(self.enable_plugin)

        if check == QtWidgets.QMessageBox.Yes:
            self.worker_compute_diameters.start()

    def pushbutton_computeDepths_isChecked(self):
        """Check if the computed depths fit the criteria of the minimum cover depth"""

        (
            global_settings_layer,
            sewerage_layer,
            weir_layer,
            pumping_station_layer,
            outlet_layer,
        ) = self.get_sewerage_designer_layers()

        #TODO CHECK CHECKERS ON THIS INPUT
        global_settings_layer = self.get_map_layer("global_settings")
        minimum_cover_depth = self.read_global_settings_value(
            global_settings_layer, "minimum_cover_depth"
        )
        dem = self.get_DEM()
        
        self.worker_validate_depths = Worker(
            process = "Validate Depths",
            global_settings_layer = global_settings_layer,
            sewerage_layer = sewerage_layer,
            weir_layer = weir_layer,
            outlet_layer = outlet_layer,
            pumping_station_layer = pumping_station_layer,
            dem = dem,
            minimum_cover_depth = minimum_cover_depth
        )
        self.worker_validate_depths.progress_changed.connect(self.update_progress)
        self.worker_validate_depths.status_changed.connect(self.update_status)
        self.worker_validate_depths.mistakes_in_network.connect(self.mistakes_in_network_error)
        self.worker_validate_depths.computation_finished.connect(self.finished_computation_message)
        self.worker_validate_depths.exception.connect(self.something_went_wrong_message_with_traceback)
        self.worker_validate_depths.enable_plugin.connect(self.enable_plugin)

        self.worker_validate_depths.start()

    def enable_plugin(self, integer):

        buttons = [
            self.pushButton_ComputeCS,
            self.pushButton_ComputeDiameters,
            self.pushButton_ComputeDepths,
            self.mMapLayerComboBox_DEM,
            self.mMapLayerComboBox_CS,
            self.mQgsFileWidget_PathGeopackage,
            self.comboBox_DesignRain,
            self.lineEdit_PeakIntensity
        ]

        if integer == 1:
            # we enable
            for button in buttons:
                button.setEnabled(True)
                while not button.isEnabled():
                    # we keep pushing the process as long as button is still disabled before we continue
                    QtWidgets.QApplication.processEvents()

        elif integer == 0:
            # we disable
            for button in buttons:
                button.setEnabled(False)
                while button.isEnabled():
                    # we keep pushing the process as long as button is still enabled before we continue
                    QtWidgets.QApplication.processEvents()

        else:
            raise ValueError(f"Signal {integer} not recognised, should be in [0, 1]")

    def radiobutton_help_isChecked(self):
        url = r"https://github.com/nens/sewerage-designer/blob/main/20220524%20Gebruikershandleiding%20Sewerage%20Designer.pdf"
        self.open_url(url)
        self.radioButton_Help.setChecked(False)
        
    def open_url(self, url):
        if sys.platform=='win32':
            os.startfile(url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
                self.info_message('Please open a browser on: '+url)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

class Worker(QThread): #TODO change name thread

    progress_changed = pyqtSignal(int)
    status_changed = pyqtSignal(str)
    mistakes_in_network = pyqtSignal(list, str, list, str)
    computation_finished = pyqtSignal(str)
    exception = pyqtSignal(Exception)
    enable_plugin = pyqtSignal(int)

    def __init__(self, 
                 process,
                 global_settings_layer,
                 sewerage_layer,
                 weir_layer,
                 outlet_layer,
                 pumping_station_layer,
                 bgt_inlooptabel_fn = None,
                 dem = None,
                 minimum_freeboard= None,
                 vmax = None,
                 peak_intensity = None,
                 rain_sum = None,
                 minimum_cover_depth = None,
                 parent = None
                 ):
        
        super().__init__(parent)
        self.process = process
        self.global_settings_layer = global_settings_layer
        self.sewerage_layer = sewerage_layer
        self.weir_layer = weir_layer
        self.outlet_layer = outlet_layer
        self.pumping_station_layer = pumping_station_layer
        self.bgt_inlooptabel_fn = bgt_inlooptabel_fn
        self.dem = dem
        self.minimum_freeboard = minimum_freeboard
        self.vmax = vmax
        self.peak_intensity = peak_intensity
        self.rain_sum = rain_sum
        self.minimum_cover_depth = minimum_cover_depth
        
    def compute_cs(self):

        self.progress_changed.emit(0)
        self.status_changed.emit("Creating and validating network...")
        (
            self.sewerage_network,
            pipes_in_loop,
            pipes_without_weir,
            fault_network,
        ) = self.create_network_from_layers()

        if fault_network:
            if len(pipes_in_loop) > 0:
                message = f"Network has a loop, pipe FIDs: {pipes_in_loop}"
                layer_name = "Pipes that are in a loop"
                fields_of_interest = ["fid"]
                self.mistakes_in_network.emit(
                    pipes_in_loop, layer_name, fields_of_interest, message
                )

            if len(pipes_without_weir) > 0:
                message = f"Network has pipes {len(pipes_without_weir)} \
                that are not connected to a weir, pipe FIDs: {pipes_without_weir}"
                layer_name = "Pipes without a weir"
                fields_of_interest = ["fid"]
                self.mistakes_in_network.emit(
                    pipes_without_weir, layer_name, fields_of_interest, message
                )

            return

        self.progress_changed.emit(25)
        self.status_changed.emit("Loading BGT Inlooptabel...")

        bgt_inlooptabel = BGTInloopTabel(self.bgt_inlooptabel_fn)

        self.progress_changed.emit(50)
        self.status_changed.emit("Computing connected surfaces...")

        for pipe in self.sewerage_network.pipes.values():
            pipe.connected_surface_area = 0.0
            pipe.determine_connected_surface_area(bgt_inlooptabel)

        self.progress_changed.emit(75)
        self.status_changed.emit("Computing accumulated connected surfaces...")
        self.sewerage_network.accumulate_connected_surface_area()

        pipes_with_empty_accumulated_fields = core_to_layer(
            self.sewerage_network, self.sewerage_layer
        )

        self.progress_changed.emit(100)

        if not pipes_with_empty_accumulated_fields:
            message = "The connected surfaces are computed. You can now proceed to compute the diameters."
            self.computation_finished.emit(message)
        else:  # we have some zeros accumulated connected surfaces
            message = f"Some pipes have no accumulated connected surfaces, pipe FIDs: {pipes_with_empty_accumulated_fields}"
            layer_name = "Pipes without accumulated connected surface"
            fields_of_interest = [
                "fid",
                "connected_surface_area",
                "accumulated_connected_surface_area",
            ]
            self.mistakes_in_network.emit(
                pipes_with_empty_accumulated_fields,
                layer_name,
                fields_of_interest,
                message,
            )

    def compute_diameters(self):

        self.progress_changed.emit(0)
        self.status_changed.emit("Creating and validating network...")
        (
            self.sewerage_network,
            pipes_in_loop,
            pipes_without_weir,
            fault_network,
        ) = self.create_network_from_layers()

        if fault_network:
            if len(pipes_in_loop) > 0:
                message = f"Network has a loop, pipe FIDs: {pipes_in_loop}"
                layer_name = "Pipes that are in a loop"
                fields_of_interest = ["fid"]
                self.mistakes_in_network.emit(
                    pipes_in_loop, layer_name, fields_of_interest, message
                )

            if len(pipes_without_weir) > 0:
                message = f"Network has pipes that are not connected to a weir, pipe FIDs: {pipes_without_weir}"
                layer_name = "Pipes without a weir"
                fields_of_interest = ["fid"]
                self.mistakes_in_network.emit(
                    pipes_without_weir, layer_name, fields_of_interest, message
                )

            return

        self.progress_changed.emit(25)
        self.status_changed.emit("Sample elevations for network...")

        self.sewerage_network.add_elevation_to_network(self.dem)

        self.progress_changed.emit(50)
        self.status_changed.emit("Computing maximum hydraulic gradients...")

        self.sewerage_network.calculate_max_hydraulic_gradient_weirs(
            freeboard=self.minimum_freeboard
        )
        # self.sewerage_network.calculate_max_hydraulic_gradient(waking=minimum_freeboard)

        self.progress_changed.emit(75)
        self.status_changed.emit("Computing diameters...")

        velocity_to_high_pipe_fids = []
        for pipe_id, pipe in self.sewerage_network.pipes.items():
            pipe.calculate_discharge(intensity=self.peak_intensity)
            pipe.calculate_volume(rain_sum=self.rain_sum)
            try:
                pipe.calculate_diameter(self.vmax)
            except Exception as e:
                print(e)
                pipe.diameter = 9999
                pipe.velocity_to_high = True

            pipe.set_material()

            if pipe.velocity_to_high:
                velocity_to_high_pipe_fids.append(pipe_id)

        core_to_layer(self.sewerage_network, self.sewerage_layer)

        self.progress_changed.emit(100)

        if not velocity_to_high_pipe_fids:
            message = "The diameters are computed. You can now proceed to validate/ compute the depths."
            self.computation_finished.emit(message)
        else:
            message = f"The velocity in some pipes is too large, pipe FIDs: {velocity_to_high_pipe_fids}"
            layer_name = "Pipes with excessive velocity"
            fields_of_interest = [
                "fid",
                "diameter",
                "discharge",
                "velocity",
                "max_hydraulic_gradient",
            ]
            self.mistakes_in_network.emit(
                velocity_to_high_pipe_fids, layer_name, fields_of_interest, message
            )

    def validate_depths(self):

        self.progress_changed.emit(0)
        self.status_changed.emit("Creating and validating network...")
        (
            self.sewerage_network,
            pipes_in_loop,
            pipes_without_weir,
            fault_network,
        ) = self.create_network_from_layers()

        if fault_network:
            if len(pipes_in_loop) > 0:
                message = f"Network has a loop, pipe FIDs: {pipes_in_loop}"
                layer_name = "Pipes that are in a loop"
                fields_of_interest = ["fid"]
                self.mistakes_in_network.emit(
                    pipes_in_loop, layer_name, fields_of_interest, message
                )

            if len(pipes_without_weir) > 0:
                message = f"Network has pipes that are not connected to a weir, pipe FIDs: {pipes_without_weir}"
                layer_name = "Pipes without a weir"
                fields_of_interest = ["fid"]
                self.mistakes_in_network.emit(
                    pipes_without_weir, layer_name, fields_of_interest, message
                )

            return

        self.progress_changed.emit(33)
        self.status_changed.emit("Sample elevations for network...")

        self.sewerage_network.add_elevation_to_network(
            self.dem
        )  # re-do this because user can change the DEM after compute diameters

        self.progress_changed.emit(67)
        self.status_changed.emit("Calculate cover depths...")

        validated = []
        self.sewerage_network.calculate_cover_depth()
        for pipe in self.sewerage_network.pipes.values():
            if pipe.cover_depth > self.minimum_cover_depth:
                validated.append(True)
            else:
                validated.append(False)

        core_to_layer(self.sewerage_network, self.sewerage_layer)

        self.progress_changed.emit(100)

        if all(validated):
            message = "Valid design! The cover depth of all pipes meet the minimum depth requirement."
            self.computation_finished.emit(message)
        else:
            self.create_layer_of_faulty_cover_depths(self.minimum_cover_depth)
            message = "Invalid design! The cover depth of some pipes do not meet the minimum depth requirement. These pipes have been colored red."
            self.computation_finished.emit(message)

    def create_network_from_layers(self):

        (
            network,
            pipes_in_loop,
            pipes_without_weir,
            fault_network,
        ) = create_sewerage_network(
            self.sewerage_layer, self.weir_layer, self.pumping_station_layer, self.outlet_layer
        )
        return network, pipes_in_loop, pipes_without_weir, fault_network

    def create_layer_of_faulty_cover_depths(self, minimum_cover_depth):

        layer = self.sewerage_layer
        layer.selectAll()
        clone = processing.run(
            "native:saveselectedfeatures", {"INPUT": layer, "OUTPUT": "memory:"}
        )["OUTPUT"]
        layer.removeSelection()
        clone.setName("pipes with unsufficient cover depth")
        clone.dataProvider().addAttributes(
            [QgsField("minimum_cover_depth", QVariant.Double)]
        )
        clone.dataProvider().addAttributes([QgsField("validated?", QVariant.Bool)])
        clone.updateFields()

        with edit(clone):
            field_ids = []
            fieldnames = set(
                ["fid", "diameter", "cover_depth", "minimum_cover_depth", "validated?"]
            )
            for field in clone.fields():
                if field.name() not in fieldnames:
                    field_ids.append(clone.fields().indexFromName(field.name()))
                if field.name() == "cover_depth":
                    features = clone.getFeatures()
                    for feature in features:
                        cover_depth = feature["cover_depth"]
                        value = True if minimum_cover_depth < cover_depth else False
                        if value:
                            clone.deleteFeature(feature.id())
                        else:
                            feature["validated?"] = QVariant(value)
                            clone.updateFeature(feature)
                elif field.name() == "minimum_cover_depth":
                    features = clone.getFeatures()
                    for feature in features:
                        feature["minimum_cover_depth"] = minimum_cover_depth
                        clone.updateFeature(feature)

        clone.dataProvider().deleteAttributes(field_ids)
        clone.updateFields()

        symbol = QgsLineSymbol.createSimple(
            {"color": "red", "capstyle": "round", "line_width_unit": "Pixel"}
        )
        symbol.setDataDefinedWidth(QgsProperty.fromExpression('"diameter"*9.2'))
        clone.renderer().setSymbol(symbol)
        clone.setBlendMode(QtGui.QPainter.CompositionMode_HardLight)
        clone.triggerRepaint()

        QgsProject.instance().addMapLayer(clone)

        clone.selectAll()
        iface.actionZoomToSelected().trigger()
        clone.removeSelection()

    def run(self):

        self.enable_plugin.emit(0)

        try:
            if self.process == "Compute CS":
                self.compute_cs()

            elif self.process == 'Compute Diameters':
                self.compute_diameters()

            elif self.process == "Validate Depths":
                self.validate_depths()

            self.progress_changed.emit(0)
            self.status_changed.emit("")
            self.enable_plugin.emit(1)

        except Exception as ex:
            self.exception.emit(ex)
            self.progress_changed.emit(0)
            self.status_changed.emit("")
            self.enable_plugin.emit(1)
