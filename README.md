# Car Control Simulator Based on Particle Swarm Optimization

[![Requirements Status](https://requires.io/github/GLaDOS1105/pso-car/requirements.svg?branch=master)](https://requires.io/github/GLaDOS1105/pso-car/requirements/?branch=master)

A sandbox practice for the particle swarm optimization.

![preview](https://i.imgur.com/tFWTts2.gif)

## Objective

Use PSO to find the best the RBFN parameters, which input is the distances detected from car radar and output is the angle of wheel.

### Objective Function

Minimize the `err`:

``` python
err = (1 / N) * sum(abs(d.expected_output - RBFN(d.input)) for d in training_dataset)
```

`N` is the total number of training data.

On the other word, we want to maximize the fitness value (`1 / err` ).

## PSO Position and Velocity Update Formula

The position and velocity for each individual in population of PSO is updated by following formula.

* Velocity

``` python
self.velocity = inertia_weight * self.velocity + \
    cognitive_const * (self.best_position - self.position) + \
    social_const * (global_best_position - self.position)

# limit the velocity
np.clip(self.velocity, -self.v_max, self.v_max, out=self.velocity)

self.position += self.velocity

# limit the position to fit the range of RBFN parameters
rbfn_params_limiter(self.position)
```

## Installation

* Download this project

``` bash
git clone https://gitlab.com/GLaDOS1105/pso-car.git
```

* Change directory to the root of the project

``` bash
cd pso-car/
```

* Run with Python interpreter

``` bash
python3 main.py
```

## Training Data Format

|        Input (Distances)       |Output (Wheel Angle)|
|:------------------------------:|:------------------:|
|`22.0000000 8.4852814 8.4852814`|    `-16.0709664`   |

``` python
# Front_Distance Right_Distance Left_Distance Wheel_Angle

22.0000000 8.4852814 8.4852814 -16.0709664
21.1292288 9.3920089 7.7989045 -14.7971418
20.3973643 24.4555821 7.2000902 16.2304876
19.1995799 25.0357595 7.5129743 16.0825385
18.1744869 42.5622911 8.0705896 15.5075777
```

## Add Customized Map Cases

### The data location

The data location is `/data`. The application will load every files with `*.txt` extension automatically after the execution.

### Example Format

``` c
0,0,90  // the starting position and angle of car (x, y, degree)
18,40   // the top-left coordinate of the ending area
30,37   // the bottom-right coordinate of the ending area
-6,-3   // the first point for the wall in map
-6,22
18,22
18,50
30,50
30,10
6,10
6,-6
-6,-3   // the last point for the wall in map
```

Every coordinates between the fourth and last line are the corner point of the walls in map.

## Dependencies

* [numpy](http://www.numpy.org/)

``` bash
pip3 install numpy
```

* [matplotlib](https://matplotlib.org/)

``` bash
pip3 install matplotlib
```

* [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)

``` bash
pip3 install pyqt5
```

* [PyQtChart5](https://www.riverbankcomputing.com/software/pyqtchart/intro)

``` bash
pip3 install PyQtChart
```
