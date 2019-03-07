# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UrbanDataInputDockWidget
                                 A QGIS plugin
 Urban Data Input Tool for QGIS
                             -------------------
        begin                : 2016-06-03
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Abhimanyu Acharya/(C) 2016 by Space Syntax Limited’.
        email                : a.acharya@spacesyntax.com
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
from PyQt4 import QtCore, QtGui, uic
from utility_functions import getQGISDbs
from DbSettings_dialog import DbSettingsDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'CreateNew_dialog_base.ui'))


class CreatenewDialog(QtGui.QDialog, FORM_CLASS):
    create_new_layer = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(CreatenewDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # setup signals
        self.closePopUpButton.clicked.connect(self.closePopUp)
        self.pushButtonSelectLocation.clicked.connect(self.selectSaveLocation)
        self.pushButtonNewFileDLG.clicked.connect(self.createLayer)

        available_dbs = getQGISDbs()
        self.dbsettings_dlg = DbSettingsDialog(available_dbs)
        self.dbsettings_dlg.nameLineEdit.setText('frontages')

        self.f_memory_radioButton.setChecked(True)
        self.lineEditFrontages.setPlaceholderText('Save as temporary layer')
        self.lineEditFrontages.setDisabled(True)
        self.f_shp_radioButton.setChecked(False)
        self.f_postgis_radioButton.setChecked(False)

        self.f_shp_radioButton.clicked.connect(self.setOutput)
        self.f_postgis_radioButton.clicked.connect(self.setOutput)
        self.f_memory_radioButton.clicked.connect(self.setOutput)

        self.dbsettings_dlg.setDbOutput.connect(self.setOutput)

    # Close create new file pop up dialogue when cancel button is pressed
    def closePopUp(self):
        self.close()

    # Open Save file dialogue and set location in text edit
    def selectSaveLocation(self):
        if self.f_shp_radioButton.isChecked():
            filename = QtGui.QFileDialog.getSaveFileName(None, "Select Save Location ", "", '*.shp')
            self.lineEditFrontages.setText(filename)
        elif self.f_postgis_radioButton.isChecked():
            self.setOutput()
            self.dbsettings_dlg.show()

            self.dbsettings = self.dbsettings_dlg.getDbSettings()
            db_layer_name = "%s:%s:%s" % (
                self.dbsettings['dbname'], self.dbsettings['schema'], self.dbsettings['table_name'])
            print 'db_layer_name'
            self.lineEditFrontages.setText(db_layer_name)
        elif self.f_memory_radioButton.isChecked():
            pass

    def createLayer(self):
        self.create_new_layer.emit()

    def setOutput(self):
        if self.f_shp_radioButton.isChecked():
            self.lineEditFrontages.clear()
            self.lineEditFrontages.setPlaceholderText('')
            self.lineEditFrontages.setDisabled(False)
        elif self.f_postgis_radioButton.isChecked():
            self.dbsettings = self.dbsettings_dlg.getDbSettings()
            print self.dbsettings
            db_layer_name = "%s:%s:%s" % (
                self.dbsettings['dbname'], self.dbsettings['schema'], self.dbsettings['table_name'])
            self.lineEditFrontages.setText(db_layer_name)
            self.lineEditFrontages.setDisabled(False)
        elif self.f_memory_radioButton.isChecked():
            self.lineEditFrontages.clear()
            self.lineEditFrontages.setPlaceholderText('Save as temporary layer')
            self.lineEditFrontages.setDisabled(True)

