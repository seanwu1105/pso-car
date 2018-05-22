import multiprocessing
import time
import random

class C(object):
    def __init__(self):
        self.__a = multiprocessing.Value('d', 0)

    def update_a(self):
        print('sleep start')
        time.sleep(1)
        self.__a.value += random.randint(1, 10)

    @property
    def a(self):
        return self.__a.value

l = [C() for _ in range(10)]

for i in l:
    print(i.a)

procs = [multiprocessing.Process(target=i.update_a) for i in l]

for p in procs:
    p.start()

for p in procs:
    p.join()

for i in l:
    print(i.a)
