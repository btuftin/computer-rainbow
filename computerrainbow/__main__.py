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

# sys allows us to pass script arguments to the script
import sys
from PyQt5.QtWidgets import QApplication 
from .mainwindow import MainWindow

def main():
    # Creates our application object
    app = QApplication(sys.argv)

    # Creates our main window, which is added to the application
    # object behind the scenes
    mw = MainWindow()

    # calling app.exec from sys.exit means exit codes get passed to the OS
    sys.exit(app.exec())            

# Check that this script was called directly
if __name__ == '__main__':
    main()
