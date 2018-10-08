"""
Define the individual for PSO.
Note: The initialization for each individual is especially designed for RBFN
      parameters.
"""

import math
import numpy as np

from .rbfn import RBFN


class Individual(object):

    def __init__(self, dataset, nneuron, v_max, sd_max=1):
        """Define an individual in swarm.

        Arguments:
            dataset {list of TrainingData} -- The training data defined in
                main.py.
            nneuron {int} -- Number of neuron in RBFN without the threshold.
            v_max {float} -- The maximum of velocity.

        Keyword Arguments:
            sd_max {int} -- The upper bound of standard deviation for each
                neuron in RBFN. (default: {1})
        """

        self.dataset = dataset
        self.nneuron = nneuron
        self.sd_max = sd_max
        self.mean_range = (min(min(d.i) for d in self.dataset),
                           max(max(d.i) for d in self.dataset))
        data_dim = len(self.dataset[0].i)

        self.position = np.random.uniform(-1, 1, nneuron + 1)
        self.position = np.append(self.position, np.random.uniform(
            *self.mean_range, nneuron * data_dim))
        self.position = np.append(self.position, np.random.uniform(
            0.01, sd_max, nneuron))

        self.best_position = self.position

        self.v_max = v_max
        self.velocity = np.random.uniform(-self.v_max, self.v_max,
                                          len(self.position))

        self.__fitness = 0.0
        self.err = math.inf
        self.best_fitness = 0.0

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, value):
        self.__fitness = value
        self.err = 1 / self.__fitness
        self.__update_best()

    def update_fitness(self):
        """Calculate the fitness and error for this individual.

        Returns:
            float: The result of fitting function.
        """

        rbfn = RBFN(self.nneuron, self.mean_range, self.sd_max)
        rbfn.load_model(self.position)
        res = sum(abs(d.o - rbfn.output(d.i, antinorm=True))
                  for d in self.dataset)
        self.err = res / len(self.dataset)
        self.__fitness = 1 / self.err
        self.__update_best()

        return self.__fitness

    def update_position(self, inertia_weight, cognitive_const,
                        social_const, global_best_position):
        self.velocity = inertia_weight * self.velocity + \
            cognitive_const * (self.best_position - self.position) + \
            social_const * (global_best_position - self.position)

        # limit the velocity
        np.clip(self.velocity, -self.v_max, self.v_max, out=self.velocity)

        self.position += self.velocity

        # limit the position
        np.clip(self.position[:self.nneuron + 1], -1,
                1, out=self.position[:(self.nneuron + 1)])
        np.clip(self.position[(self.nneuron + 1):-self.nneuron], *
                self.mean_range, out=self.position[(self.nneuron + 1):-self.nneuron])
        np.clip(self.position[-self.nneuron:], 0.001,
                None, out=self.position[-self.nneuron:])

    def __update_best(self):
        if self.__fitness > self.best_fitness:
            self.best_fitness = self.__fitness
            self.best_position = self.position
