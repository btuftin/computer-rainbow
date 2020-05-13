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

# sys lets us check what platform we are on to do some
# custom Mac stuff
import sys

# Basic QT classes
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc

from .rainbow_model import RainbowModel
from .settings_dialog import SettingsDialog
from .images import resources

# MainWindow includes all the GUI code
class MainWindow(qtw.QMainWindow):

    changed = qtc.pyqtSignal(dict)
    def __init__(self):
        """MainWindowConstructor"""
        super().__init__()
        # Main UI code goes here
        size_x_default = int(800)
        size_y_default = int(600)
        lightness_default = int(0)
        cent_lambda_default = int(560)
        color_bits_start_default = int(24)
        color_res_x_default = int(10)
        color_res_y_default = int(10)
        color_no_start_default = int(3)
        color_step_factor_default = int(1)     
        self.debug = False

        self.setWindowTitle('ComputerRainbow')
        self.setWindowIcon(qtg.QIcon(':/icons/icon.png'))

        self.settings = qtc.QSettings('NAITA Software', 'ComputerRainbow')

        # Set default values if the appropriate settings are not in the system

        if len(self.settings.allKeys()) < 9:
            self.settings.setValue('size_x', size_x_default)
            self.settings.setValue('size_y', size_y_default)
            self.settings.setValue('lightness', lightness_default) 
            # The default lightness for the generated rainbow
            self.settings.setValue('cent_lambda', cent_lambda_default)
            # The default center wavelength for the rightmost colors
            self.settings.setValue('color_bits_start', color_bits_start_default) 
            # The number of color bits for the leftmost column
            self.settings.setValue('color_res_x', color_res_x_default) 
            # The width in pixels of the column for each color resolution
            self.settings.setValue('color_res_y', color_res_y_default) 
            # The height in pixels for each separate color
            self.settings.setValue('color_no_start', color_no_start_default) 
            # The number of colors in the first 'rainbow' in the image
            self.settings.setValue('color_step_factor', color_step_factor_default) 
            # A multiplier for increasing the number of colors 

        # changing the settings object changes values continuously in the registry
        # so we create a dictionary to use in the program
        self.current_settings = dict()
        for key in self.settings.allKeys():
            self.current_settings[key] = self.settings.value(key, type=int)
        
        # Put together the elements of the central widget in a QWidget
        central_widget = qtw.QWidget(self)

        # First create the different controls and images
        self.image = qtg.QImage(self.current_settings['size_x'], 
                                self.current_settings['size_y'],
                                qtg.QImage.Format_ARGB32)
        self.image.fill(qtg.QColor('black'))

        lightness_tooltip = 'Lightness correction'
        lightness_box = qtw.QGroupBox('Light', self)
        lightness_box.setToolTip(lightness_tooltip)
        self.lightness_slider = qtw.QSlider(qtc.Qt.Vertical)
        self.lightness_slider.setMinimum(-50)
        self.lightness_slider.setMaximum(50)
        self.lightness_slider.setPageStep(10)
        self.lightness_slider.setSingleStep(1)
        self.lightness_slider.setTickInterval(50)
        self.lightness_slider.setTickPosition(qtw.QSlider.TicksRight)
        self.lightness_slider.setTracking(False)
        self.lightness_spin = qtw.QSpinBox(self, maximum = 50, minimum = -50)

        colors_start_box = qtw.QGroupBox('Colors start')
        colors_start_box.setToolTip('Number of colors in first column')
        self.colors_start = qtw.QSpinBox(self, maximum=256, minimum=3)

        lambda_tooltip = 'Focus wavelength'
        lambda_box = qtw.QGroupBox('Focus wavelength', self)
        lambda_box.setToolTip(lambda_tooltip)
        self.lambda_slider = qtw.QSlider(qtc.Qt.Vertical)
        self.lambda_slider.setInvertedAppearance(True)
        self.lambda_slider.setToolTip(lambda_tooltip)
        self.lambda_slider.setMinimum(380)
        self.lambda_slider.setMaximum(740)
        self.lambda_slider.setPageStep(100)
        self.lambda_slider.setSingleStep(10)
        self.lambda_slider.setTickInterval(50)
        self.lambda_slider.setTickPosition(qtw.QSlider.TicksRight)
        self.lambda_slider.setTracking(False)
        self.lambda_spin = qtw.QSpinBox(self, maximum = 740, minimum = 380, suffix = 'nm')

        colors_step_box = qtw.QGroupBox('Color step')
        colors_step_box.setToolTip('Change in number of of colors from one column to the next')
        self.colors_step = qtw.QSpinBox(self, maximum=16, minimum=1)

        self.rainbow_model = RainbowModel(self, self.current_settings)
        self.rainbow_view = qtw.QLabel(pixmap = qtg.QPixmap(self.image))

        rainbow_box = qtw.QScrollArea()
        rainbow_box.setWidget(self.rainbow_view)

        button_values = 6, 12, 24
        self.color_bits_start_button_list = list()
        for i in range(0,3):
            if button_values[i] == self.current_settings['color_bits_start']:
                check = True
            else:
                check = False
            self.color_bits_start_button_list.append(
                qtw.QRadioButton(str(button_values[i]), self, checked = check))
        
        color_bits_start_group = qtw.QButtonGroup(self)
        for button in self.color_bits_start_button_list:
            color_bits_start_group.addButton(button)

        # Controls for the x and y resolution can come later

        # Assemble the different parts of the GUI
        self.setCentralWidget(central_widget)
        top_layout = qtw.QHBoxLayout()
        central_widget.setLayout(top_layout)

        first_col = qtw.QVBoxLayout()

        light_box_layout = qtw.QVBoxLayout()
        light_box_layout.addWidget(self.lightness_slider)
        light_box_layout.addWidget(self.lightness_spin)
        lightness_box.setLayout(light_box_layout)

        colors_start_layout = qtw.QVBoxLayout()
        colors_start_layout.addWidget(self.colors_start)
        colors_start_box.setLayout(colors_start_layout)

        first_col.addWidget(lightness_box)
        first_col.addWidget(colors_start_box)

        top_layout.addLayout(first_col)

        scnd_col = qtw.QVBoxLayout()

        lambda_box_layout = qtw.QVBoxLayout()
        lambda_box_layout.addWidget(self.lambda_slider)
        lambda_box_layout.addWidget(self.lambda_spin)
        lambda_box.setLayout(lambda_box_layout)

        colors_step_layout = qtw.QVBoxLayout()
        colors_step_layout.addWidget(self.colors_step)
        colors_step_box.setLayout(colors_step_layout)

        scnd_col.addWidget(lambda_box)
        scnd_col.addWidget(colors_step_box)

        top_layout.addLayout(scnd_col)


        third_col = qtw.QVBoxLayout()
        third_col.addWidget(rainbow_box)

        color_res_box = qtw.QGroupBox('Color bits')
        color_res_area = qtw.QHBoxLayout()
        for button in self.color_bits_start_button_list:
            color_res_area.addWidget(button)
        blocker = qtw.QLabel()
        blocker.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        color_res_box.setLayout(color_res_area)

        fifth_column = qtw.QHBoxLayout()
        fifth_column.addWidget(color_res_box)
        fifth_column.addWidget(blocker)
        third_col.addLayout(fifth_column)

        # update the values of each contol to the loaded defaults
        self.update_active_settings()

        top_layout.addLayout(third_col)

        # Add a status bar
        self.statusBar().showMessage('Welcome to ComputerRainbow!')
    
        # Create thread for RainbowModel and connect its signals
        self.render_thread = qtc.QThread()
        self.rainbow_model.moveToThread(self.render_thread)
        self.rainbow_model.finished.connect(self.render_thread.quit)
        self.render_thread.start()
        self.rainbow_model.rendering.connect(self.rendering_view)
        self.rainbow_model.finished.connect(self.finished_view)

        # Add menus and connect them
        menubar = self.menuBar()
        if sys.platform.startswith('darwin'):
            app_menu = menubar.addMenu("Rainbow")
        else:
            app_menu = menubar.addMenu("File")
        about_action = app_menu.addAction('About Rainbow', self.show_about_dialog)
        app_menu.addSeparator()
        pref_action = app_menu.addAction('Preferences...', self.show_pref_dialog)
        quit_action = app_menu.addAction('Quit Rainbow', self.destroy)


       # Connecting signals and slots for controls
        self.lightness_slider.valueChanged.connect(self.on_light_change)
        self.lightness_spin.valueChanged.connect(self.on_light_change)
        self.colors_start.valueChanged.connect(self.on_colors_start_change)
        self.lambda_slider.valueChanged.connect(self.on_lambda_change)
        self.lambda_spin.valueChanged.connect(self.on_lambda_change)
        self.colors_step.valueChanged.connect(self.on_colors_step_change)
        color_bits_start_group.buttonClicked.connect(self.on_color_bits_start_change)
        self.changed.connect(self.render_thread.start)
        self.changed.connect(self.rainbow_model.render)

        # End main UI code
        self.show()
        self.changed.emit(self.current_settings)

    def rendering_view(self, image):
        self.statusBar().showMessage('Rendering image.')
        self.update_view(image)

    def finished_view(self, image):
        self.statusBar().showMessage('Computer Rainbow! by NAITA Software')
        self.update_view(image)

    def update_view(self, image):
        self.rainbow_view.setPixmap(qtg.QPixmap(image))
        self.rainbow_view.resize(image.width(), image.height())

    def on_light_change(self, light):
        if light != self.current_settings['lightness']:
            self.current_settings['lightness'] = light
            # light is controlled from two controlls, so we set them
            # both to this value rather than go through the bother
            # of finding out which one was changed
            self.lightness_slider.setValue(light)
            self.lightness_spin.setValue(light)
            self.changed.emit(self.current_settings)
    
    def on_colors_start_change(self, colors):
        if colors != self.current_settings['color_no_start']:
            self.current_settings['color_no_start'] = colors
            self.changed.emit(self.current_settings)

    def on_lambda_change(self, c_lambda):
        if c_lambda != self.current_settings['cent_lambda']:
            self.current_settings['cent_lambda'] = c_lambda
            # c_lambda is controlled from two controlls, so we set them
            # both to this value rather than go through the bother
            # of finding out which one was changed
            self.lambda_slider.setValue(c_lambda)
            self.lambda_spin.setValue(c_lambda)
            self.changed.emit(self.current_settings)

    def on_colors_step_change(self, step):
        if step != self.current_settings['color_step_factor']:
            self.current_settings['color_step_factor'] = step
            self.changed.emit(self.current_settings)

    def on_color_bits_start_change(self, color_res):
        if int(color_res.text()) != self.current_settings['color_bits_start']:
            self.current_settings['color_bits_start'] = int(color_res.text())
            self.changed.emit(self.current_settings)

    def update_active_settings(self):
        self.lightness_slider.setSliderPosition(self.current_settings['lightness'])
        self.lightness_spin.setValue(self.current_settings['lightness'])
        self.colors_start.setValue(self.current_settings['color_no_start'])
        self.lambda_slider.setSliderPosition(self.current_settings['cent_lambda'])
        self.lambda_spin.setValue(self.current_settings['cent_lambda'])
        self.colors_step.setValue(self.current_settings['color_step_factor'])

        for button in self.color_bits_start_button_list:
            if button.text() == str(self.current_settings['color_bits_start']):
                button.setChecked(True)

    def show_about_dialog(self):
        qtw.QMessageBox.about(
            self,
            "<h1>About ComputerRainbow</h1>",
            '''<program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
'''
        )

    def show_pref_dialog(self):
        settings_dialog = SettingsDialog(self, self.settings, self.current_settings)
        if settings_dialog.exec():
            for key in self.settings.allKeys():
                self.current_settings[key] = self.settings.value(key, type=int)
            self.update_active_settings()
        self.changed.emit(self.current_settings)