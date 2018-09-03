""" Define the GUI: main window. """

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from pso_car.gui.training_panel import TrainingPanel
from pso_car.gui.testing_panel import TestingPanel


class GUIBase(QMainWindow):
    """ The base of GUI, containing the status bar and menu. """

    def __init__(self, maps, datasets):
        super().__init__()
        self.setWindowTitle("Potential Significant Other")
        self.statusBar()

        # a container for threads created in GUI classes.
        # For more details:
        # https://stackoverflow.com/questions/28714630/qthread-destroyed-while-thread-is-still-running-on-quit
        self.threads = []

        self.setCentralWidget(BaseWidget(maps, datasets, self.threads))

    def closeEvent(self, _):
        """ Stop the new created threads and wait till them terminate. """
        for thread in self.threads:
            thread.stop()
            thread.wait()


class BaseWidget(QWidget):

    def __init__(self, maps, datasets, threads):
        super().__init__()
        layout = QHBoxLayout()
        panel_test = TestingPanel(maps, threads)
        panel_train = TrainingPanel(datasets, panel_test, threads)
        layout.addWidget(panel_train)
        layout.addWidget(panel_test)

        self.setLayout(layout)
