# ----------
# Background
# 
# A robotics company named Trax has created a line of small self-driving robots 
# designed to autonomously traverse desert environments in search of undiscovered
# water deposits.
#
# A Traxbot looks like a small tank. Each one is about half a meter long and drives
# on two continuous metal tracks. In order to maneuver itself, a Traxbot can do one
# of two things: it can drive in a straight line or it can turn. So to make a 
# right turn, A Traxbot will drive forward, stop, turn 90 degrees, then continue
# driving straight.
#
# This series of questions involves the recovery of a rogue Traxbot. This bot has 
# gotten lost somewhere in the desert and is now stuck driving in an almost-circle: it has
# been repeatedly driving forward by some step size, stopping, turning a certain 
# amount, and repeating this process... Luckily, the Traxbot is still sending all
# of its sensor data back to headquarters.
#
# In this project, we will start with a simple version of this problem and 
# gradually add complexity. By the end, you will have a fully articulated
# plan for recovering the lost Traxbot.
# 
# ----------
# Part One
#
# Let's start by thinking about circular motion (well, really it's polygon motion
# that is close to circular motion). Assume that Traxbot lives on 
# an (x, y) coordinate plane and (for now) is sending you PERFECTLY ACCURATE sensor 
# measurements. 
#
# With a few measurements you should be able to figure out the step size and the 
# turning angle that Traxbot is moving with.
# With these two pieces of information, you should be able to 
# write a function that can predict Traxbot's next location.
#
# You can use the robot class that is already written to make your life easier. 
# You should re-familiarize yourself with this class, since some of the details
# have changed. 
#
# ----------
# YOUR JOB
#
# Complete the estimate_next_pos function. You will probably want to use
# the OTHER variable to keep track of information about the runaway robot.
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *
from math import *
from matrix import *
import random


# Helper Function to Move
def move(motion, orientation, measurement):
    """
    Helper function returning coordinates after a move

    Keyword Args:
      motion: list of two elements. First element is the turn, second is the distance,
      orientation: Current orientation in radians
      measurement: tuple (x, y)
    """

    length = 1  # An assumption -- maybe should be 0.5?
    alpha = motion[0]
    d = motion[1]
    theta = orientation
    beta = d / length * tan(alpha)
    x, y = measurement[0], measurement[1]
    
    if abs(beta) <= 0.001:
        x = x + d * cos(theta)
        y = y + d * sin(theta)
    else:
        R = d / beta
        cx = x - sin(theta) * R
        cy = y + cos(theta) * R
        x = cx + sin(theta + beta) * R
        y = cy - cos(theta + beta) * R
        orientation = (theta + beta) % (2 * pi)
    measurement = (x, y)
    
    return measurement  #, orientation


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
            'orientations': [atan(measurement[1] / measurement[0])],
            'step_size': None,
            'turning_angle': None,
        }
        xy_estimate = measurement
        return xy_estimate, OTHER 

    previous_point = OTHER['measurements'][len(OTHER['measurements']) - 1]
    current_orientation = (atan((measurement[1] - previous_point[1]) / (measurement[0] - previous_point[0]))) % (2 * pi)
    OTHER['orientations'].append(current_orientation)
    OTHER['measurements'].append(measurement)
    xy_estimate = measurement

    if len(OTHER['measurements']) == 3:
        # Find initial orientation
        x0, y0 = OTHER['measurements'][0]
        x1, y1 = OTHER['measurements'][1]
        x2, y2 = OTHER['measurements'][2]

        step_size = distance_between((x0, y0), (x1, y1))
        initial_orientation = atan((y1 - y0) / (x1 - x0))

        # Next, find turning angle
        # Prime is the third point if robot continues to go straight
        # prime = move(motion=[0, step_size], orientation=initial_orientation, measurement=(x1, y1))
        # xprime, yprime = prime

        # # Law of cosines: https://www.mathsisfun.com/algebra/trig-solving-sss-triangles.html
        # b = distance_between((x1, y1), prime)
        # c = distance_between((x2, y2), prime)
        # a = distance_between((x1, y1), (x2, y2))
        # cos_angle_prime = (b**2 + c**2 - a**2) / (2 * b * c) 

        # print('printing prime')
        # print(prime)
        turning_angle = (atan2(y1 - y0, x1 - x0) - atan2(y2 - y1, x2 - x1)) % (2 * pi)

        # turning_angle = acos(cos_angle_prime)
        OTHER['step_size'] = step_size
        OTHER['turning_angle'] = turning_angle
        xy_estimate = measurement
    elif len(OTHER['measurements']) > 3:
        print('printing current_orientation')
        print(current_orientation)
        turning_angle = OTHER['turning_angle']
        step_size = OTHER['step_size']
        new_orientation = (current_orientation + turning_angle) % (2 * pi)
        xy_estimate = move(motion=[0, step_size], orientation=new_orientation, measurement=measurement)

    print(OTHER)
    print(xy_estimate)
    print('')
    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    return xy_estimate, OTHER 

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 10: 
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 10:
            print "Sorry, it took you too many steps to localize the target."
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    print(xy_estimate, OTHER)
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
test_target.set_noise(0.0, 0.0, 0.0)

demo_grading(estimate_next_pos, test_target)
