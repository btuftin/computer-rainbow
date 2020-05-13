'''ComputerRainbow - a toy program rendering rainbows at different resolutions
    Copyright (C) 2020  Bjoernar Tuftin

    This file is part of ComputerRainbow, a small PyQt based program.
    The program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

# Basic QT classes
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc

class SettingsDialog(qtw.QDialog):

    def __init__(self, parent, settings, current_settings):
        super().__init__(parent, modal=True)
        self.settings = settings
        self.setLayout(qtw.QFormLayout())
        self.layout().addRow(
            qtw.QLabel('<h1>Application settings</h1>')
        )
        # Make inputs for all the settings
        self.size_x_field = qtw.QSpinBox(self,
                                        maximum = 2000,
                                        minimum = 0,
                                        suffix = 'px')
        # Setting value separately since the constructor cannot handle
        # values over 99
        self.size_x_field.setValue(current_settings['size_x'])
        self.size_y_field = qtw.QSpinBox(self,
                                        maximum = 2000,
                                        minimum = 0,
                                        suffix = 'px')
        self.size_y_field.setValue(current_settings['size_y'])
        self.lightness_field = qtw.QSpinBox(self,
                                        value = current_settings['lightness'],
                                        maximum = 50,
                                        minimum = -50)
        self.lambda_field = qtw.QSpinBox(self,
                                        maximum = 750,
                                        minimum = 380,
                                        suffix = 'nm')
        self.lambda_field.setValue(current_settings['cent_lambda'])
        self.color_no_start_field = qtw.QSpinBox(self,
                                        value = current_settings['color_no_start'],
                                        maximum = 256,
                                        minimum = 3)
        self.color_step_start_field = qtw.QSpinBox(self,
                                        value = current_settings['color_step_factor'],
                                        maximum = 16,
                                        minimum = 1)
        self.color_res_field = qtw.QComboBox(self)
        self.color_res_field.addItem('6 bit', 6)
        self.color_res_field.addItem('12 bit', 12)
        self.color_res_field.addItem('24 bit', 24)
        color_res = current_settings['color_bits_start']
        if color_res == 6:
            self.color_res_field.setCurrentIndex(0)
        elif color_res == 12:
            self.color_res_field.setCurrentIndex(1)
        else:
             self.color_res_field.setCurrentIndex(2)
        self.color_res_x_field = qtw.QSpinBox(self,
                                        value = current_settings['color_res_x'],
                                        maximum = 100,
                                        minimum = 1,
                                        suffix = 'px')
        self.color_res_y_field = qtw.QSpinBox(self,
                                        value = current_settings['color_res_y'],
                                        maximum = 100,
                                        minimum = 1,
                                        suffix = 'px')

        # Arrange settings in form
        canvas_x_y_box = qtw.QHBoxLayout()
        canvas_x_y_box.addWidget(self.size_x_field)
        canvas_x_y_box.addWidget(qtw.QLabel(', '))
        canvas_x_y_box.addWidget(self.size_y_field)
        self.layout().addRow('Canvas size', canvas_x_y_box)
        self.layout().addRow('Lightness correction', self.lightness_field)
        self.layout().addRow('Central wavelength', self.lambda_field)
        self.layout().addRow('Starting no. colors', self.color_no_start_field)
        self.layout().addRow('Color no. step', self.color_step_start_field)
        self.layout().addRow('Minimum color bits', self.color_res_field)
        color_x_y_box = qtw.QHBoxLayout()
        color_x_y_box.addWidget(self.color_res_x_field)
        color_x_y_box.addWidget(qtw.QLabel(', '))
        color_x_y_box.addWidget(self.color_res_y_field)
        self.layout().addRow('Minimum color band', color_x_y_box)

        self.accept_btn = qtw.QPushButton('Save', clicked=self.accept)
        self.cancel_btn = qtw.QPushButton('Cancel', clicked=self.reject)
        self.layout().addRow(self.accept_btn, self.cancel_btn)

    def accept(self):
        # Store the changed settings
        self.settings.setValue('size_x', self.size_x_field.value())
        self.settings.setValue('size_y', self.size_y_field.value())
        self.settings.setValue('lightness', self.lightness_field.value())
        self.settings.setValue('cent_lambda', self.lambda_field.value())
        self.settings.setValue('color_bits_start', self.color_res_field.currentData())
        self.settings.setValue('color_res_x', self.color_res_x_field.value())
        self.settings.setValue('color_res_y', self.color_res_y_field.value())
        self.settings.setValue('color_no_start', self.color_no_start_field.value())
        self.settings.setValue('color_step_factor', self.color_step_start_field.value())    
        super().accept()