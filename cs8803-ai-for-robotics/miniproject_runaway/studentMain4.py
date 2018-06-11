# ----------
# Part Four
#
# Author: Vincent La (vla6)
#
# Again, you'll track down and recover the runaway Traxbot. 
# But this time, your speed will be about the same as the runaway bot. 
# This may require more careful planning than you used last time.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time. 
#
# ----------
# GRADING
# 
# Same as part 3. Again, try to catch the target in as few steps as possible.
# 
# HINT
# https://piazza.com/class/jh0tfongvk362a?cid=118
# In part 4, I set the hunter to go n steps further ahead of the robot, and it can catch it most of the time. I am using 1*max_distance of the hunter. After the hunter gets into that distance range to the robot, it starts to jump to "t+n" future point. I get 8/10 cases pass most of the time, sometimes 10/10. It usually fails at case #9 and #10 when the circle is really big where the hunter can never get into that 1*max_distance range. But if I made that distance larger, it failed the other cases. Any good suggestions on how to choose this initial point? 

from robot import *
from math import *
from matrix import *
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
        next_xy, next_other = estimate_next_pos(previous_xy_measurement, previous_other)
        distance_to_next_estimated_target = distance_between(hunter_position, next_xy)
        # This is taken from hint:
        # https://piazza.com/class/jh0tfongvk362a?cid=118
        # See thread starting with Anonymous author starting with "In part 4, I set the hunter to go n steps further..."
        # Essentially, if we are within the max distance times number of turns, we move in that direction since
        # it's highly probable that we can cut it off once the lost robot gets there.
        if distance_to_next_estimated_target < max_distance * (turn + 1):
            distance = distance_to_next_estimated_target
            angle_to_target_robot = atan2((next_xy[1] - hunter_position[1]), (next_xy[0] - hunter_position[0]))
            turning = angle_to_target_robot - hunter_heading
            break
        # If the loop hasn't broken, that means we haven't found a cutoff point. That is, we aren't close enough
        # to estimate where we can cut off the target robot.
        # Thus, now continue the loop
        previous_xy_measurement = next_xy
        previous_other = next_other

    next_target_robot_position, OTHER = estimate_next_pos(target_measurement, OTHER)
    
    # What if we are so far out that we aren't within striking distance of the target robot at all?
    # Then, default to just move closer to the last known hunter position so that we can get more information.
    if turning is None:
        distance = distance_between(hunter_position, next_target_robot_position)
        angle_to_target_robot = atan2((next_target_robot_position[1] - hunter_position[1]),(next_target_robot_position[0] - hunter_position[0]))
        turning = angle_to_target_robot - hunter_heading

    return turning, distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.98 * target_bot.distance # 0.98 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught



def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER

# target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
# measurement_noise = .05*target.distance
# target.set_noise(0.0, 0.0, measurement_noise)

# hunter = robot(-10.0, -10.0, 0.0)

# print demo_grading(hunter, target, next_move)





