""" Define the GUI: main window. """

from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from pso_car.gui.training_panel import TrainingPanel
from pso_car.gui.testing_panel import TestingPanel

class GUIBase(QMainWindow):
    """ The base of GUI, containing the status bar and menu. """

    def __init__(self, maps, datasets):
        super().__init__()
        self.setWindowTitle("Potential Significant Other")
        self.statusBar()
        self.setCentralWidget(BaseWidget(maps, datasets))

class BaseWidget(QWidget):

    def __init__(self, maps, datasets):
        super().__init__()
        layout = QHBoxLayout()
        panel_test = TestingPanel(maps)
        panel_train = TrainingPanel(datasets, panel_test)
        layout.addWidget(panel_train)
        layout.addWidget(panel_test)

        self.setLayout(layout)
