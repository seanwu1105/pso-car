import multiprocessing as mp

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

from individual import Individual
from rbfn import RBFN


class PSO(QThread):
    sig_console = pyqtSignal(str)
    sig_current_iter_time = pyqtSignal(int)
    sig_current_error = pyqtSignal(float)
    sig_iter_error = pyqtSignal(float, float)
    sig_rbfn = pyqtSignal(RBFN)

    def __init__(self, iter_times, population_size, inertia_weight,
                 cognitive_const_upper, social_const_upper, v_max, nneuron,
                 dataset, sd_max=1, is_multicore=True):
        super().__init__()
        self.abort = False
        self.iter_times = iter_times
        self.population_size = population_size
        self.inertia_weight = inertia_weight
        self.cognitive_const_upper = cognitive_const_upper
        self.social_const_upper = social_const_upper
        self.dataset = dataset
        self.is_multicore = is_multicore

        self.population = [Individual(self.dataset, nneuron, v_max, sd_max)
                           for _ in range(self.population_size)]

    def run(self):
        for i in range(self.iter_times):
            if self.abort:
                break
            self.sig_current_iter_time.emit(i)

            best = self.__get_best_individual()
            print(best.fitness, best.best_fitness, best.best_position)

    @pyqtSlot()
    def stop(self):
        if self.isRunning():
            self.sig_console.emit(
                'WARNING: User interrupts running thread. The thread will be '
                'stop in next iteration. Please wait a second...')

        self.abort = True

    def __get_best_individual(self):
        if self.is_multicore:
            with mp.Pool() as pool:
                res = pool.map(get_indiv_fitness_update, self.population)
                for indiv, result in zip(self.population, res):
                    indiv.fitness = result
            return max(self.population, key=lambda indiv: indiv.fitness)
        return max(self.population, key=lambda indiv: indiv.update_fitness())


def get_indiv_fitness_update(indiv):
    """ This function is designed for multiprocessing.Pool() """
    return indiv.update_fitness()
