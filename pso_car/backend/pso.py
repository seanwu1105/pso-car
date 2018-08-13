import copy
import random
import multiprocessing as mp
import operator
import time

from PySide2.QtCore import QThread, Slot, Signal

from pso_car.backend.individual import Individual
from pso_car.backend.rbfn import RBFN


class PSO(QThread):
    sig_console = Signal(str)
    sig_current_iter_time = Signal(int)
    sig_current_error = Signal(float)
    sig_iter_error = Signal(float, float, float)
    sig_indicate_busy = Signal()
    sig_rbfn = Signal(RBFN)

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
        self.rbfn = RBFN(nneuron, (0, 40), sd_max)

    def run(self):
        total_best = copy.deepcopy(self.population[0])
        for i in range(self.iter_times):
            print('in')
            if self.abort:
                break
            self.sig_current_iter_time.emit(i)

            # get the best individual in current iteration
            global_best = self.__get_best_individual()

            # save the best individual in whole training
            total_best = copy.deepcopy(
                min((total_best, global_best), key=operator.attrgetter('err')))
            self.__show_errs(global_best, total_best)

            # update the position and velocity for each individual
            for indiv in self.population:
                indiv.update_position(self.inertia_weight,
                                      random.uniform(
                                          0, self.cognitive_const_upper),
                                      random.uniform(
                                          0, self.social_const_upper),
                                      global_best.position)
        self.sig_indicate_busy.emit()
        self.sig_console.emit('Selecting the best individual...')
        global_best = self.__get_best_individual()
        total_best = copy.deepcopy(
            min((total_best, global_best), key=operator.attrgetter('err')))
        self.__show_errs(global_best, total_best)
        self.sig_console.emit('The least error: %f' % total_best.err)
        self.sig_console.emit(
            'The best individual: \n{}'.format(total_best.position))
        self.rbfn.load_model(total_best.position)
        self.sig_rbfn.emit(self.rbfn)

    @Slot()
    def stop(self):
        if self.isRunning():
            self.sig_console.emit(
                'WARNING: User interrupts running thread. The thread will be '
                'stop in next iteration. Please wait a second...')

        self.abort = True

    def __get_best_individual(self):
        """Update every individual's fitness and return the best individual."""
        # XXX: using multiprocessing with PySide2 will occur fatal error
        # if self.is_multicore:
        if False:
            with mp.Pool() as pool:
                res = pool.map(get_indiv_fitness_update, self.population)
                for indiv, result in zip(self.population, res):
                    indiv.fitness = result
            return max(self.population, key=lambda indiv: indiv.fitness)
        return max(self.population, key=lambda indiv: indiv.update_fitness())

    def __show_errs(self, global_best, total_best):
        for indiv in self.population:
            time.sleep(0.001)
            self.sig_current_error.emit(indiv.err)
        self.sig_iter_error.emit(
            sum(i.err for i in self.population) / len(self.population),
            global_best.err, total_best.err)


def get_indiv_fitness_update(indiv):
    """ This function is designed for multiprocessing.Pool() """
    return indiv.update_fitness()
