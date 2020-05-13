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
from time import sleep
from math import ceil as ceil
from math import floor as floor

# RainbowModel includes all the code necessary to generate
# each artwork
class RainbowModel(qtc.QObject):
    """ This class is the core of the ComputerRainbow app. It generates an
    artwork based on the parameters passed to it and keeps a copy. Render will
    be run in a subthread to allow the slow generation to run in the background. """
    # Signals
    rendering = qtc.pyqtSignal(qtg.QImage)
    finished = qtc.pyqtSignal(qtg.QImage)

    # Instantiation method with defaults
    def __init__(self, parent, settings):
        super().__init__()
        # Set basic parameters and create a blank canvas with the current settings
        self.first_render = True
        self.old_settings = settings
        self.current_image = qtg.QImage(
            settings['size_x'],
            settings['size_y'],
            qtg.QImage.Format_ARGB32)
        self.current_image.fill(qtg.QColor('Gray'))

    # render should be called in its own thread
    # it will send two signals:
    # "rendering" with the previous image and the "rendering" overlay
    # "finished" with the finished image
    @qtc.pyqtSlot(dict)
    def render(self, settings):
        size_x = settings["size_x"]
        size_y = settings["size_y"]

        rendering_image = self.current_image.convertToFormat(
                                    qtg.QImage.Format_Grayscale16
                                    )
        painter = qtg.QPainter(rendering_image)
        painter.setFont(qtg.QFont("Helvetica", pointSize = 32))
        painter.drawText(25, 
                        int(size_y/2 - 20),
                        size_x,
                        size_y,
                        0,
                        "RENDERING")
        self.rendering.emit(rendering_image)
        
        center_wavelength = settings["cent_lambda"]
        color_bits_start = settings["color_bits_start"]
        color_res_x = settings["color_res_x"]
        color_res_y = settings["color_res_y"]
        color_no_start = settings["color_no_start"]
        color_step_factor = settings["color_step_factor"]
        light = settings["lightness"]

        if size_x % color_res_x == 0:
            color_steps = size_x // color_res_x - 1
        else:
            color_steps = size_x // color_res_x
        no_of_colors_max = color_no_start + color_step_factor*color_steps
        no_colors_max_displayed = ceil(size_y/color_res_y)
        half_color_span = no_colors_max_displayed // 2

        # Fill a list of lists with the wavelenghts for each section
        # of the display
        color_grid = list()
        no_colors = color_no_start

        while no_colors <= no_of_colors_max:
            #print("Number of colors sought: ", no_colors)
            color_column, center_i = self.wavelengths(int(no_colors), center_wavelength)
            #print("Number of colors calculated: ", len(color_column))
            start_i = 0
            end_i = int(no_colors)
            if no_colors > no_colors_max_displayed:
                start_i = center_i - half_color_span
                if start_i < 0:
                    start_i = 0
                end_i = start_i + no_colors_max_displayed
                if end_i > no_colors:
                    end_i = int(no_colors) + 1
                    start_i = end_i - no_colors_max_displayed
            no_colors = no_colors + color_step_factor

            color_grid.append(color_column[start_i:end_i])
            #print("Displaying ", end_i - start_i, " colors. From ", start_i, ' to ', end_i)
            #print(*color_column, sep=', ')

        # Convert the list of lists from wavelenghts to rgb-values
        for col in range(len(color_grid)):
            for row in range(len(color_grid[col])):
                color_grid[col][row] = self.wavelength_to_RGB(color_grid[col][row], light, color_bits_start)

        if not (size_x == self.current_image.size().width() &
            size_y == self.current_image.size().height()):
            self.current_image = qtg.QImage(size_x, size_y, qtg.QImage.Format_ARGB32)
        self.current_image.fill(qtg.QColor('White'))
        painter = qtg.QPainter(self.current_image)

        # Variables for detemining when and where to draw color loss labels
        label_y_pos = 0
        color_loss_limit = 90 # First label at 90% unique
        label_list = list()

        x = 0
        x_step = color_res_x
        for col in color_grid:
            y = 0
            rows = len(col)
            # print(rows)
            mod_first_step = False
            #print(rows, " colors")

            # If the number of colors is insufficient to fill the height of the 
            # column with the standard block height, we need to adjust the standard
            # block height upwards. Use floor and ceil and pick the height that gives
            # the closest fit to the actual size_y.
            if color_res_y * rows < size_y:
                y_step_max = int(ceil(size_y/rows))
                y_step_min = int(floor(size_y/rows))
                if abs(y_step_max*rows - size_y) <= abs(y_step_min*rows - size_y):
                    y_step = y_step_max
                else:
                    y_step = y_step_min
            else:
                y_step = color_res_y


            # If the corrent number of rows with the adjusted block height does not
            # go nicely into the image height we need to adjust the heights of some of the blocks.
            # We can't do all the adjustments at the ends, because the adjustment
            # totals up to several blocks as the block heights get more numerous.
            total_adjustment = 0
            if size_y != y_step*rows:
                total_adjustment = abs(y_step*rows - size_y)
                # print('total adjustment', total_adjustment)
                adjustment = (size_y - y_step*rows)/total_adjustment
                freq = rows / total_adjustment
                current_freq = freq
            else:
                freq = rows + 2
                adjustment = 0
            
            current_freq = freq
            adjustments_completed = 0

            # RGB color list to examine color uniqueness
            rgb_list = list()

            for row, cell in enumerate(col):
                # if the row number for this row, counting from 1 is 0 modulo
                # freq, adjust it to make the total height match the image height
                #print('drawing row ', row, 'of ', rows)  
                painter.setPen(
                    cell)
                painter.setBrush(
                    cell)                
                x_end = min(x + x_step - 1, size_x)
                y_end = min(y + y_step - 1, size_y)
                if row > current_freq:
                    y_end = y_end + adjustment
                    adjustments_completed = adjustments_completed + adjustment
                    current_freq = current_freq + freq
                   # print('adjusting row height by', adjustment)

                painter.drawRect(x, y, x_end, y_end)

                rgb_list.append(cell.rgb())

                y = y_end + 1
            # We want a label informing of resolution loss when 10% or more 
            # of the boxes in one column have the same RGB code
            rgb_set = set(rgb_list)
            percent_unique = round(len(rgb_set)*100/len(rgb_list))
            if percent_unique < color_loss_limit + 1:
                print("Register percent unique ", percent_unique, "pct at x =", x)
                label_list.append(x)
                color_loss_limit = color_loss_limit - 10

            x = x_end + 1
            #print(f'Drew column with:{rows} color blox {y_step} high. Required adjustment {total_adjustment}. Completed adjustment {adjustments_completed}.')

        if label_list:
            print("Drawing percent unique", percent_unique)
            painter.setPen(qtg.QColor('White'))
            painter.setFont(qtg.QFont('Times', weight=12))
            percent_unique = 90
            for x_pos in label_list:
                print("At position ", x_pos)
                text = f"{percent_unique}% unique colors"
                painter.drawText(x_pos + 5, label_y_pos + 20, text)
                painter.drawEllipse(x_pos + color_res_x // 2, label_y_pos + 4, 3, 3)
                label_y_pos = label_y_pos + 25
                percent_unique = percent_unique - 10


        self.finished.emit(self.current_image)

    def wavelengths(self, no_of_colors, center_wavelength):
        delta_l = 360/no_of_colors
        mid_specter = 560
        wavelength_list = list()
        start = 1
        offset = 0
        if no_of_colors % 2 == 0:
            wavelength_list.append(mid_specter - delta_l*0.5)
            wavelength_list.append(mid_specter + delta_l*0.5)
            offset = 0.5
        else:
            wavelength_list.append(mid_specter)
        
        iterations = (no_of_colors - int(offset*4))//2
        for i in range(1, iterations+1):
            wavelength_list.append(mid_specter - delta_l*(i + offset))
            wavelength_list.append(mid_specter + delta_l*(i + offset))

        wavelength_list.sort()

        i_center_wavelength = no_of_colors//2
        deviation = abs(center_wavelength - wavelength_list[i_center_wavelength])

        for i, wavelength in enumerate(wavelength_list):
            this_deviation = abs(center_wavelength - wavelength)
            if this_deviation < deviation:
                i_center_wavelength = i
                deviation = this_deviation
        return wavelength_list, i_center_wavelength

    def wavelength_to_RGB(self, wavelength, light, bits):
        '''Based on code found at http://www.noah.org/wiki/Wavelength_to_RGB_in_Python,
        which again is based on FORTRAN code by Dan Bruton
        http://www.physics.sfasu.edu/astro/color/spectra.html '''
        wavelength = float(wavelength)
        gamma = 0.7999
        if wavelength >= 380 and wavelength <= 440:
            attenuation = 0.2999 + 0.6999 * (wavelength - 380) / (440 - 380)
            R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
            G = 0.0
            B = (1.0 * attenuation) ** gamma
        elif wavelength >= 440 and wavelength <= 490:
            R = 0.0
            G = ((wavelength - 440) / (490 - 440)) ** gamma
            B = 1.0
        elif wavelength >= 490 and wavelength <= 510:
            R = 0.0
            G = 1.0
            B = (-(wavelength - 510) / (510 - 490)) ** gamma
        elif wavelength >= 510 and wavelength <= 580:
            R = ((wavelength - 510) / (580 - 510)) ** gamma
            G = 1.0
            B = 0.0
        elif wavelength >= 580 and wavelength <= 645:
            R = 1.0
            G = (-(wavelength - 645) / (645 - 580)) ** gamma
            B = 0.0
        elif wavelength >= 645 and wavelength <= 750:
            attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
            R = (1.0 * attenuation) ** gamma
            G = 0.0
            B = 0.0
        else:
            R = 0.0
            G = 0.0
            B = 0.0
        if bits == 24:
            R *= 255
            G *= 255
            B *= 255
        elif bits == 12:
            R = int(15 * R)*17
            G = int(15 * G)*17
            B = int(15 * B)*17
        elif bits == 6:
            R = int(3 * R)*85
            G = int(3 * G)*85
            B = int(3 * B)*85
        
        color = qtg.QColor(int(R), int(G), int(B))
        color = color.lighter(100 + light*1.8) 

        return color