"""Vincent La (vla6)"""
# These import steps give you access to libraries which you may (or may
# not) want to use.
from math import *
from robot import *
from matrix import *
import random
import numpy as np

# This is the function you have to write. The argument 'measurement' is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    # If first measurement, create a list.
    if OTHER is None:
        OTHER = {
            'measurements': [measurement],
            'turning_angles': [],
            'distances': [],
        }
        xy_estimate = measurement
        return xy_estimate, OTHER 
    elif len(OTHER['measurements']) < 3:
        OTHER['measurements'].append(measurement)
        xy_estimate = measurement
        return xy_estimate, OTHER 
    else:
        OTHER['measurements'].append(measurement)
        number_measurements = len(OTHER['measurements'])

        # Find initial orientation
        x0, y0 = OTHER['measurements'][number_measurements - 3]
        x1, y1 = OTHER['measurements'][number_measurements - 2]
        x2, y2 = OTHER['measurements'][number_measurements - 1]

        step_size = distance_between((x1, y1), (x2, y2))

        heading1 = atan2(y1 - y0, x1 - x0)
        heading2 = atan2(y2 - y1, x2 - x1)
        turning_angle = (heading2 - heading1) % (2 * pi)
        if turning_angle > pi:
            turning_angle -= 2 * pi
        elif turning_angle < -pi:
            turning_angle += 2 * pi

        # Take overall average to account for noise
        distances = np.array(OTHER['distances'] + [step_size])
        turning_angles = np.array(OTHER['turning_angles'] + [turning_angle])

        step_size = np.mean(distances)
        turning_angle = np.mean(turning_angles)
        OTHER['distances'].append(step_size)
        OTHER['turning_angles'].append(turning_angle)

        new_orientation = heading2 + turning_angle
        myrobot = robot(x=x2, y=y2)
        myrobot.move(new_orientation, step_size)
        xy_estimate = (myrobot.x, myrobot.y)

    return xy_estimate, OTHER 

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
