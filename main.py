""" Author: Sean Wu 104502551 NCU CSIE 3B

An assignment of Computational Intelligence in NCU, Taiwan
to implement the particle swarm optimization with a car simulation.

This file is the entry point of whole project.

GitLab: https://gitlab.com/GLaDOS1105/pso-car

"""

import collections
import multiprocessing
import pathlib
import sys

from PySide2.QtWidgets import QApplication

from pso_car.gui import base


TrainingData = collections.namedtuple('TrainingData', ['i', 'o'])


def read_maps(folderpath='maps'):
    """ Read every data of maps in `folderpath` folder. Return the
    dictionary containing dataset.
    """
    maps = {}
    folderpath = pathlib.Path(folderpath)
    for filepath in folderpath.glob("*.txt"):
        with filepath.open() as casefile:
            contents = [tuple(map(float, line.split(',')))
                        for line in casefile]
        maps[filepath.stem] = {
            "start_pos": (contents[0][0], contents[0][1]),
            "start_angle": contents[0][2],
            "end_area_lt": contents[1],  # ending area - left-top
            "end_area_rb": contents[2],  # ending area - right-bottom
            "route_edge": contents[3:]
        }
    return collections.OrderedDict(sorted(maps.items()))


def read_training_datasets(folderpath='data'):
    dataset = {}
    folderpath = pathlib.Path(folderpath)
    for filepath in folderpath.glob("*.txt"):
        with filepath.open() as datafile:
            contents = list()
            for line in datafile:
                raw = tuple(map(float, line.split()))
                contents.append(TrainingData(raw[:-1], raw[-1]))
        dataset[filepath.stem] = contents
    return collections.OrderedDict(sorted(dataset.items()))


if __name__ == '__main__':
    multiprocessing.freeze_support()
    sys.argv += ['--style', 'fusion']

    # WARNING: QApplication and QMainWindow MUST stay in global scope for
    #          multiprocessing (only PySide2 has such error).
    #          More details:
    #          https://forum.qt.io/topic/93693/pyside2-with-python3-built-in-multiprocessing
    app = QApplication(sys.argv)
    window = base.GUIBase(read_maps(), read_training_datasets())
    window.show()
    sys.exit(app.exec_())
