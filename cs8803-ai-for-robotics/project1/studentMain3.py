"""Vincent La (vla6)"""

from math import *
from matrix import *
from robot import *
import random
import numpy as np

def estimate_next_pos(measurement, OTHER = None):
    """Copied from Question 2"""
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


def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    """
    This function will be called after each time the target moves. 

    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.

    Strategy that we will take:
      From Part 2, copy work to estimate the hunter's new position
      Then have the robot move to that prediction as fast as possible.
    """
    if OTHER is None:
        OTHER = {
            'measurements': [target_measurement],
            'turning_angles': [],
            'distances': [],
        }
        xy_estimate = target_measurement
    else:
        xy_estimate, OTHER = estimate_next_pos(target_measurement, OTHER=OTHER)

    # get our distance and angle from the robot
    distance_to_target_robot = distance_between(hunter_position, xy_estimate)
    angle_to_target_robot = atan2((xy_estimate[1] - hunter_position[1]),(xy_estimate[0] - hunter_position[0]))
    turning = angle_to_target_robot - hunter_heading
    distance = min(distance_to_target_robot, max_distance)

    return turning, distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
