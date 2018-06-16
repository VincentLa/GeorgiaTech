"""Vincent La (vla6)"""
from math import *
from matrix import *
from robot import *
import random
import numpy as np
import copy

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

# This function will be called after each time the target moves. 
# The OTHER variable is a place for you to store any historical 
# information about the progress of the hunt (or maybe some 
# localization information). Your must return a tuple of three 
# values: turning, distance, OTHER
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
    # In this part, estimate the number of turns that the target will take in a circle.
    # If we don't have enough information, just assume 30 for now (as that is what's provided in test case in this file).
    if OTHER is not None and len(OTHER['turning_angles']) != 0:
        number_of_turns = abs(2*pi / (OTHER['turning_angles'][-1]))
        number_of_turns = int(number_of_turns)
    else:
        number_of_turns = 30

    # Now, we loop over all the turns
    # Basically the goal is to fine on which turn the hunter can intersect the target
    previous_xy_measurement, previous_other = target_measurement, copy.deepcopy(OTHER) if isinstance(OTHER, dict) else OTHER
    turning, distance = None, None
    for turn in range(number_of_turns):
        next_estimated_xy_measurement, next_other = estimate_next_pos(previous_xy_measurement, previous_other)
        distance_to_next_estimated_target = distance_between(hunter_position, next_estimated_xy_measurement)
        # This is taken from hint:
        # https://piazza.com/class/jh0tfongvk362a?cid=118
        # See thread starting with Anonymous author starting with "In part 4, I set the hunter to go n steps further..."
        # Essentially, if we are within the max distance times number of turns, we move in that direction since
        # it's highly probable that we can cut it off once the lost robot gets there.
        if distance_to_next_estimated_target < max_distance * (turn + 1):
            angle_to_target_robot = atan2((next_estimated_xy_measurement[1] - hunter_position[1]), (next_estimated_xy_measurement[0] - hunter_position[0]))
            turning = angle_to_target_robot - hunter_heading
            distance = distance_to_next_estimated_target
            break
        # If the loop hasn't broken, that means we haven't found a cutoff point. That is, we aren't close enough
        # to estimate where we can cut off the target robot.
        # Thus, now continue the loop
        previous_xy_measurement = next_estimated_xy_measurement
        previous_other = next_other

    next_target_robot_position, OTHER = estimate_next_pos(target_measurement, OTHER)
    
    # What if we are so far out that we aren't within striking distance of the target robot at all?
    # Then, default to just move closer to the last known hunter position so that we can get more information.
    if turning is None:
        angle_to_target_robot = atan2((next_target_robot_position[1] - hunter_position[1]),(next_target_robot_position[0] - hunter_position[0]))
        turning = angle_to_target_robot - hunter_heading
        distance = distance_between(next_target_robot_position, hunter_position)

    return turning, distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
