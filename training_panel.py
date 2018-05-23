""" Define the contents of training panel. """

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
                             QComboBox, QSpinBox, QDoubleSpinBox, QLabel,
                             QProgressBar, QPushButton, QCheckBox)

from panel import Panel
from testing_panel import TestingPanel
from error_linechart import ErrorLineChart
from rbfn import RBFN
from pso import PSO


class TrainingPanel(Panel):

    def __init__(self, datasets, testing_panel):
        super().__init__()
        if isinstance(testing_panel, TestingPanel):
            self.testing_panel = testing_panel
        else:
            raise TypeError('"testing_panel" must be the instance of '
                            '"TestingPanel"')
        self.datasets = datasets

        self.__set_execution_ui()
        self.__set_options_ui()
        self.__set_outputs_ui()
        self.__set_graphic_ui()

    def __set_execution_ui(self):
        group_box = QGroupBox('Training Execution')
        inner_layout = QHBoxLayout()
        group_box.setLayout(inner_layout)

        self.data_selector = QComboBox()
        self.data_selector.addItems(self.datasets.keys())
        self.data_selector.setStatusTip('Select the training dataset.')

        self.start_btn = QPushButton('Train')
        self.start_btn.setStatusTip('Start training.')
        self.start_btn.clicked.connect(self.__run)

        self.stop_btn = QPushButton('Stop')
        self.stop_btn.setStatusTip('Force the training stop running.')
        self.stop_btn.setDisabled(True)

        self.multicore_cb = QCheckBox('Multicore')
        self.multicore_cb.setStatusTip('Use multiprocessing in calculating '
                                       'fitting for populations.')
        self.multicore_cb.setChecked(True)

        inner_layout.addWidget(self.data_selector, 1)
        inner_layout.addWidget(self.start_btn)
        inner_layout.addWidget(self.stop_btn)
        inner_layout.addWidget(self.multicore_cb)

        self._layout.addWidget(group_box)

    def __set_options_ui(self):
        group_box = QGroupBox('Training Options')
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.iter_times = QSpinBox()
        self.iter_times.setRange(1, 1000000)
        self.iter_times.setValue(200)
        self.iter_times.setStatusTip('The total iterating times for training.')

        self.population_size = QSpinBox()
        self.population_size.setRange(1, 100000)
        self.population_size.setValue(100)
        self.population_size.setStatusTip('The population size for the PSO.')

        self.inertia_weight = QDoubleSpinBox()
        self.inertia_weight.setRange(0.1, 50)
        self.inertia_weight.setValue(1)
        self.inertia_weight.setSingleStep(0.1)
        self.inertia_weight.setStatusTip('The inertia weight of the velocity '
                                         ' for each individual.')

        self.cognitive_const_rand_upper = QDoubleSpinBox()
        self.cognitive_const_rand_upper.setRange(0.5, 50)
        self.cognitive_const_rand_upper.setValue(2)
        self.cognitive_const_rand_upper.setSingleStep(0.1)
        self.cognitive_const_rand_upper.setStatusTip(
            'The random upper bound for cognitive accelerate constant.')

        self.social_const_rand_upper = QDoubleSpinBox()
        self.social_const_rand_upper.setRange(0.5, 50)
        self.social_const_rand_upper.setValue(3)
        self.social_const_rand_upper.setSingleStep(0.1)
        self.social_const_rand_upper.setStatusTip(
            'The random upper bound for social accelerate constant.')

        self.v_max = QDoubleSpinBox()
        self.v_max.setRange(0.5, 100)
        self.v_max.setValue(10)
        self.v_max.setSingleStep(1)
        self.v_max.setStatusTip('The maximum of velocity for each individual.')

        self.nneuron = QSpinBox()
        self.nneuron.setRange(1, 100)
        self.nneuron.setValue(6)
        self.nneuron.setStatusTip('The number of RBFN neuron.')

        self.sd_max = QDoubleSpinBox()
        self.sd_max.setRange(0.01, 20)
        self.sd_max.setValue(10)
        self.sd_max.setSingleStep(0.1)
        self.sd_max.setStatusTip('The random range maximum of standard '
                                 'deviation of each neuron in RBFN (only for '
                                 'initialization).')

        inner_layout.addRow('Iterating Times:', self.iter_times)
        inner_layout.addRow('Population Size:', self.population_size)
        inner_layout.addRow('Inertia Weight:', self.inertia_weight)
        inner_layout.addRow('Cognitive Const Upper:',
                            self.cognitive_const_rand_upper)
        inner_layout.addRow('Social Const Upper:',
                            self.social_const_rand_upper)
        inner_layout.addRow('Maximum of Velocity:', self.v_max)
        inner_layout.addRow('Number of Neuron:', self.nneuron)
        inner_layout.addRow('Maximum of SD:', self.sd_max)

        self._layout.addWidget(group_box)

    def __set_outputs_ui(self):
        group_box = QGroupBox('Training Details')
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.current_iter_time = QLabel('--')
        self.current_error = QLabel('--')
        self.avg_error = QLabel('--')
        self.global_best_error = QLabel('--')
        self.total_best_error = QLabel('--')
        self.progressbar = QProgressBar()

        self.current_iter_time.setAlignment(Qt.AlignCenter)
        self.current_error.setAlignment(Qt.AlignCenter)
        self.avg_error.setAlignment(Qt.AlignCenter)
        self.global_best_error.setAlignment(Qt.AlignCenter)
        self.total_best_error.setAlignment(Qt.AlignCenter)

        self.current_iter_time.setStatusTip('The current iterating time of '
                                            'the PSO.')
        self.current_error.setStatusTip('The current error from the fitting '
                                        'function.')
        self.avg_error.setStatusTip('The average error from the fitting '
                                    'function in current iteration.')
        self.global_best_error.setStatusTip(
            'The error of global best individual from the fitting function in '
            'current iteration.')
        self.total_best_error.setStatusTip(
            'The error of total best individual from the fitting function in '
            'training.')

        inner_layout.addRow('Current Iterating Time:', self.current_iter_time)
        inner_layout.addRow('Current Error:', self.current_error)
        inner_layout.addRow('Average Error:', self.avg_error)
        inner_layout.addRow('Global Best Error:', self.global_best_error)
        inner_layout.addRow('Total Best Error:', self.total_best_error)
        inner_layout.addRow(self.progressbar)

        self._layout.addWidget(group_box)

    def __set_graphic_ui(self):
        group_box = QGroupBox('Error Line Charts:')
        inner_layout = QVBoxLayout()
        group_box.setLayout(inner_layout)

        self.err_chart = ErrorLineChart(1)
        self.err_chart.setStatusTip('The history of error from the fitting '
                                    'of the PSO for each data.')
        self.__err_x = 1

        self.iter_err_chart = ErrorLineChart(
            3, ('Avg', 'Global Best', 'Total Best'))
        self.iter_err_chart.setStatusTip('The history of average and least '
                                         'error from the fitting of the PSO '
                                         'for each iteration.')
        self.iter_err_chart.setMinimumHeight(150)

        inner_layout.addWidget(QLabel('Current Error'))
        inner_layout.addWidget(self.err_chart)
        inner_layout.addWidget(QLabel('Average Error'))
        inner_layout.addWidget(self.iter_err_chart)
        self._layout.addWidget(group_box)

    @pyqtSlot()
    def __init_widgets(self):
        self.start_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)
        self.multicore_cb.setDisabled(True)
        self.data_selector.setDisabled(True)
        self.iter_times.setDisabled(True)
        self.population_size.setDisabled(True)
        self.inertia_weight.setDisabled(True)
        self.cognitive_const_rand_upper.setDisabled(True)
        self.social_const_rand_upper.setDisabled(True)
        self.v_max.setDisabled(True)
        self.nneuron.setDisabled(True)
        self.sd_max.setDisabled(True)
        self.err_chart.clear()
        self.iter_err_chart.clear()
        self.__err_x = 1

    @pyqtSlot()
    def __reset_widgets(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setDisabled(True)
        self.multicore_cb.setEnabled(True)
        self.data_selector.setEnabled(True)
        self.iter_times.setEnabled(True)
        self.population_size.setEnabled(True)
        self.inertia_weight.setEnabled(True)
        self.cognitive_const_rand_upper.setEnabled(True)
        self.social_const_rand_upper.setEnabled(True)
        self.v_max.setEnabled(True)
        self.nneuron.setEnabled(True)
        self.sd_max.setEnabled(True)

    @pyqtSlot(int)
    def __show_current_iter_time(self, value):
        self.current_iter_time.setText(str(value + 1))
        self.progressbar.setValue(value + 1)

    @pyqtSlot(float)
    def __show_current_error(self, value):
        self.current_error.setText('{:.7f}'.format(value))
        self.err_chart.append_point(self.__err_x, value)
        self.__err_x += 1

    @pyqtSlot(float, float, float)
    def __show_iter_error(self, avg, glob, total):
        self.avg_error.setText('{:.7f}'.format(avg))
        self.global_best_error.setText('{:.7f}'.format(glob))
        self.total_best_error.setText('{:.7f}'.format(total))
        self.iter_err_chart.append_point(
            int(self.current_iter_time.text()), total, 2)
        self.iter_err_chart.append_point(
            int(self.current_iter_time.text()), glob, 1)
        self.iter_err_chart.append_point(
            int(self.current_iter_time.text()), avg, 0)

    def __run(self):
        self.progressbar.setMaximum(self.iter_times.value())

        self.__current_dataset = self.datasets[
            self.data_selector.currentText()]

        self.__pso = PSO(self.iter_times.value(), self.population_size.value(),
                         self.inertia_weight.value(),
                         self.cognitive_const_rand_upper.value(),
                         self.social_const_rand_upper.value(),
                         self.v_max.value(), self.nneuron.value(),
                         self.__current_dataset, self.sd_max.value(),
                         is_multicore=self.multicore_cb.isChecked())
        self.stop_btn.clicked.connect(self.__pso.stop)
        self.__pso.started.connect(self.__init_widgets)
        self.__pso.finished.connect(self.__reset_widgets)
        self.__pso.sig_current_iter_time.connect(self.__show_current_iter_time)
        self.__pso.sig_current_error.connect(self.__show_current_error)
        self.__pso.sig_iter_error.connect(self.__show_iter_error)
        self.__pso.sig_console.connect(self.testing_panel.print_console)
        self.__pso.sig_rbfn.connect(self.testing_panel.load_rbfn)
        self.__pso.start()
