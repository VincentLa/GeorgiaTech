#!/usr/bin/python

import math
import sys
import numpy as np
import copy

from functools import wraps
from Queue import Queue
from Queue import Empty as QueueEmptyError
from threading import Thread
from multiprocessing import TimeoutError

import unittest
import timeit

import partB
import robot

PI = math.pi

########################################################################
# for debugging set the time limit to a big number
########################################################################
TIME_LIMIT = 10  # seconds


# The functions curr_time_millis, handler, and timeout are taken from 
# http://github.com/udacity/artificial-intelligence/blob/master/build-a-game-playing-agent/agent_test.py
# as of January 14, 2016, at 11:55 UTC.
# Copyright 2016 Udacity
# A claim of fair use under the copyright laws of the United States is made for the use
# of this code because:
# - It is a limited excerpt of the code from the file listed above.
# - It serves an auxiliary purpose for the code from the file listed above.
# - The code is being used for a nonprofit, educational purpose.
# - The use does not negatively affect the market for Udacity's product.

def curr_time_millis():
    return 1000 * timeit.default_timer()


def handler(obj, testcase, queue):
    try:
        queue.put((None, testcase(obj)))
    except Exception:
        queue.put((sys.exc_info(), None))


def timeout(time_limit):
    """
    Function decorator for unittest test cases to specify test case timeout.
    It is not safe to access system resources (e.g., files) within test
    cases wrapped by this timer.
    """

    def wrapUnitTest(testcase):

        @wraps(testcase)
        def testWrapper(self):

            queue = Queue()

            try:
                p = Thread(target=handler, args=(self, testcase, queue))
                p.daemon = True
                p.start()
                err, res = queue.get(timeout=time_limit)
                p.join()
                if err:
                    raise err[0], err[1], err[2]
                return res
            except QueueEmptyError:
                raise TimeoutError("Test aborted due to timeout. Test was " +
                                   "expected to finish in fewer than {} second(s).".format(time_limit))

        return testWrapper

    return wrapUnitTest


# End Udacity code.


def execute_student_plan(warehouse, todo, max_distance, max_steering):

    student_planner = partB.DeliveryPlanner(copy.copy(warehouse), copy.copy(todo),
                                            max_distance, max_steering)

    action_list = student_planner.plan_delivery()

    state = State(warehouse, todo, max_distance, max_steering)
    num_delivered = 0 
    next_box_to_deliver = num_delivered

    for action in action_list:
        state.print_to_console()
        state.update_according_to(action)

        # check if new box has been delivered
        delivered = state.get_boxes_delivered()
        if len(delivered) > num_delivered:
            last_box_delivered = int(delivered[-1])
            if last_box_delivered == next_box_to_deliver:
                num_delivered += 1
                if num_delivered < len(todo):
                    next_box_to_deliver = num_delivered
                else:
                    # all boxes delivered: end test
                    break
            else:
                # wrong box delivered: kill test
                raise Exception('wrong box delivered: {} instead of {}'.format(last_box_delivered,
                                                                               next_box_to_deliver))
    
    if num_delivered != len(todo):
        raise Exception("Did not deliver all boxes. Only delivered: {}".format(num_delivered))

    # print final state
    print "\n\n"
    print "Final State: "
    state.print_to_console()

    return state.get_total_cost(), state.get_boxes_delivered()


class State:
    MOVE_COST = 1.0
    BOX_LIFT_COST = 2.0
    BOX_DOWN_COST = 1.5
    ILLEGAL_MOVE_PENALTY = 100.
    BOX_SIZE = 0.1        # 1/2 of box width and height
    BOX_DIAG = 0.1414
    ROBOT_RADIUS = 0.25
    OBSTACLE_DIAG = 1.414
    ROBOT_STEP_SIZE = 0.1

    def __init__(self, warehouse, todo, max_distance, max_steering):
        self.boxes_delivered = []
        self.total_cost = 0
        self.max_distance = max_distance
        self.max_steering = max_steering
        self._set_initial_state_from(warehouse, todo)
        self.robot_is_crashed = False

    def _set_initial_state_from(self, warehouse, todo):

        rows = len(warehouse)
        cols = len(warehouse[0])

        self.dropzone = dict()
        self.boxes = dict()
        self.obstacles = []

        # set the warehouse limits:  min_x = 0.0,  max_y = 0.0
        self.warehouse_limits = {'max_x': float(cols), 'min_y': float(-rows), 'segments': []}

        # West segment (x0,y0) -> (x1,y1)
        self.warehouse_limits['segments'].append(
                    [(self.ROBOT_RADIUS, 0.0),
                     (self.ROBOT_RADIUS, self.warehouse_limits['min_y'])])
        # South segment
        self.warehouse_limits['segments'].append(
                    [(0.0,                            self.warehouse_limits['min_y'] + self.ROBOT_RADIUS),
                     (self.warehouse_limits['max_x'], self.warehouse_limits['min_y'] + self.ROBOT_RADIUS)])
        # East segment
        self.warehouse_limits['segments'].append( 
                    [(self.warehouse_limits['max_x'] - self.ROBOT_RADIUS, self.warehouse_limits['min_y']),
                     (self.warehouse_limits['max_x'] - self.ROBOT_RADIUS, 0.0)])
        # North segment
        self.warehouse_limits['segments'].append( 
                    [(self.warehouse_limits['max_x'], -self.ROBOT_RADIUS),
                     (0.0,                            -self.ROBOT_RADIUS)])

        for i in range(rows):
            for j in range(cols):
                this_square = warehouse[i][j]
                x, y = float(j), -float(i)
                
                # set the obstacle limits, centers, and edges compensated for robot radius
                # precompute these values to save time later
                if this_square == '#':
                    obstacle = dict()
                    
                    # obstacle edges
                    obstacle['min_x'] = x
                    obstacle['max_x'] = x + 1.0
                    obstacle['min_y'] = y - 1.0
                    obstacle['max_y'] = y
                    
                    # center of obstacle
                    obstacle['ctr_x'] = x + 0.5
                    obstacle['ctr_y'] = y - 0.5

                    # compute clearance parameters for robot
                    obstacle = self._dilate_obstacle_for_robot(obstacle)

                    self.obstacles.append(obstacle)

                # set the dropzone limits
                elif this_square == '@':
                    self.dropzone['min_x'] = x
                    self.dropzone['max_x'] = x + 1.0
                    self.dropzone['min_y'] = y - 1.0
                    self.dropzone['max_y'] = y
                    self.dropzone['ctr_x'] = x + 0.5
                    self.dropzone['ctr_y'] = y - 0.5

        for i in range(len(todo)):
            # set up the parameters for processing the box as an obstacle and for 
            # picking it up and setting it down
            box = dict()                    
            # box edges
            box['min_x'] = todo[i][0] - self.BOX_SIZE
            box['max_x'] = todo[i][0] + self.BOX_SIZE
            box['min_y'] = todo[i][1] - self.BOX_SIZE
            box['max_y'] = todo[i][1] + self.BOX_SIZE
                    
            # center of obstacle
            box['ctr_x'] = todo[i][0]
            box['ctr_y'] = todo[i][1]

            # compute clearance parameters for robot
            box = self._dilate_obstacle_for_robot(box)
            
            self.boxes[str(i)] = box

        # initialize the robot in the center of the dropzone at a bearing pointing due east            
        self.robot = robot.Robot(x=self.dropzone['ctr_x'], y=self.dropzone['ctr_y'], bearing=0.0, 
                                 max_distance=self.max_distance, max_steering=self.max_steering)

        self.box_held = None

    # Update the system state according to the specified action
    def update_according_to(self, action):
 
        # what type of move is it?
        action = action.split()
        action_type = action[0]

        if action_type == 'move':
            steering, distance = action[1:]
            self._attempt_move(float(steering), float(distance))

        elif action_type == 'lift':
            box = action[1]
            self._attempt_lift(box)

        elif action_type == 'down':
            x, y = action[1:]
            self._attempt_down(float(x), float(y))

        else:
            # improper move format: kill test
            raise Exception('improperly formatted action: {}'.format(''.join(action)))

    def _attempt_move(self, steering, distance):
        # - The robot may move between 0 and max_distance
        # - The robot may turn between -max_steering and +max_steering
        # - The warehouse does not "wrap" around.
        # Costs
        # - 1+ distance traversed on that turn
        # - Crash: 100*distance attempted.

        # Illegal moves - the robot will not move, but the standard cost will be incurred.
        # - Moving a distance outside of [0,max_distance]
        # - Steering angle outside [-max_steering, max_steering]
        
        try:
            distance_ok = 0.0 <= distance <= self.max_distance
            steering_ok = (-self.max_steering) <= steering <= self.max_steering
            path_is_traversable = True

            destination = self.robot.find_next_point(steering, distance)
            if distance > 0.0:
                path_is_traversable, clear_distance = self._is_traversable(destination, distance, steering)
               
            is_legal_move = distance_ok and steering_ok and path_is_traversable
            if is_legal_move:
                self.robot.move(steering, distance)
                self._increase_total_cost_by(self.MOVE_COST + distance)
            elif not path_is_traversable:
                self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY * distance)
                self.robot.move(steering, clear_distance)

        except ValueError:
            raise Exception('improperly formatted move destination: {} {}'.format(steering, distance))

    def _attempt_lift(self, box_id):
        # - The robot may pick up a box that is within a distance of 0.5 of the robot's center.
        # - The cost to pick up a box is 2, regardless of the direction the box is relative to the robot.
        # - While holding a box, the robot may not pick up another box.
        # Illegal lifts (do not lift a box but incur cost of lift):
        # - picking up a box that doesn't exist or is too far away
        # - picking up a box while already holding one

        try:
            self._increase_total_cost_by(self.BOX_LIFT_COST)
            box_position = (self.boxes[box_id]['ctr_x'], self.boxes[box_id]['ctr_y'])

            box_is_adjacent = robot.compute_distance((self.robot.x, self.robot.y), box_position) <= 0.5
            robot_has_box = self._robot_has_box()

            is_legal_lift = box_is_adjacent and (not robot_has_box)
            if is_legal_lift:
                self._lift_box(box_id)
            else:
                print "*** Could not lift box: box_is_adjacent = {}, robot_has_box = {} ".format(box_is_adjacent,
                                                                                                 robot_has_box)
 
        except KeyError:
            raise Exception('improper key {}'.format(box_id))

    def _attempt_down(self, x, y):
        # - The robot may put a box down within a distance of 0.5 of the robot's center.
        #   The cost to set a box down is 1.5 (regardless of the direction in which the robot puts down the box).
        # - If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
        #   house.
        # Illegal moves (do not set box down but incur cost):
        # - putting down a box too far away or so that it's touching a wall, the warehouse exterior, 
        #   another box, or the robot
        # - putting down a box while not holding a box 

        try:

            self._increase_total_cost_by(self.BOX_DOWN_COST)
            destination = (x, y)

            destination_is_adjacent = robot.compute_distance((self.robot.x, self.robot.y), destination) <= 0.5
            destination_is_open = self._is_open(destination, self.BOX_SIZE)
            destination_is_within_warehouse = self._is_within_warehouse(destination, self.BOX_SIZE)
            robot_has_box = self._robot_has_box()

            is_legal_down = (destination_is_adjacent and destination_is_open
                             and destination_is_within_warehouse and robot_has_box)
            
            if is_legal_down:
                self._down_box(destination)               

        except ValueError:
            raise Exception('improperly formatted down destination: {} {}'.format(x, y))

    # Increment the total cost
    def _increase_total_cost_by(self, amount):
        self.total_cost += amount

    # Assumes the warehouse NW corner is (0,0) and SE corner is (max_x, min_y)
    def _is_within_warehouse(self, coordinates, size):
        x, y = coordinates
        return (size < x < (self.warehouse_limits['max_x']-size)
                and (self.warehouse_limits['min_y'] + size) < y < -size)

    # Check if the box within the dropzone
    def _is_box_within_dropzone(self, coordinates):
        x, y = coordinates
        return ((self.dropzone['min_x'] + self.BOX_SIZE) < x < (self.dropzone['max_x'] - self.BOX_SIZE)
                and (self.dropzone['min_y'] + self.BOX_SIZE) < y < (self.dropzone['max_y'] - self.BOX_SIZE))
   
    # Verify a box or the robot can occupy the desired coordinates
    # size is either the robot radius or 1/2 the box width or height
    def _is_open(self, coordinates, size):
        
        # process all boxes still remaining
        for b in self.boxes:
            if not self._is_outside_obstacle(coordinates, self.boxes[b], size):
                print '*** Space not open - box {} in the way ***'.format(b) 
                return False

        # process all obstacles
        for o in self.obstacles:
            if not self._is_outside_obstacle(coordinates, o, size):
                print '*** Space not open - obstacle {} in the way ***'.format(o) 
                return False

        return True

    # Check the box  or the robot to make sure it is outside an obstacle (or other box)
    # Note that in the case of a robot, a square bounding box is used.
    def _is_outside_obstacle(self, coordinates, obstacle, size):

        # the center coordinates of the box or robot to be tested
        x, y = coordinates  

        if (x - size) >= obstacle['max_x']:
            return True
        elif (x + size) <= obstacle['min_x']:
            return True
        elif (y - size) >= obstacle['max_y']:
            return True
        elif (y + size) <= obstacle['min_y']:
            return True
        else:
            return False

    # Check the path to make sure the robot can traverse it without running into
    # boxes, obstacles, or the warehouse walls
    def _is_traversable(self, destination, distance, steering):

        NUDGE_DISTANCE = 0.01
        
        # end points of trajectory
        t1 = destination
        if not self.robot_is_crashed:
            t0 = (self.robot.x, self.robot.y)
            # the distance to check against
            chk_distance = distance

        else:
            # in the event the robot is crashed don't use the current robot point to evaluate
            # collisions because by definition it is colliding.  Define the trajectory line
            # segment start point just a bit farther out to see if a new collision will occur.
            t0 = self.robot.find_next_point(steering, NUDGE_DISTANCE)
            chk_distance = distance - NUDGE_DISTANCE

        # check that the robot will start inside the warehouse and outside any obstacles 
        # a sanity check on initial location and deals with potential edge cases with NUDGE
        if (not self._is_within_warehouse(t0, self.ROBOT_RADIUS) or
                not self._is_open(t0, self.ROBOT_RADIUS)):
            print "*** Robot stuck at {p[0]:6.2f} {p[1]:6.2f}: Try a different heading ***".format(p=(self.robot.x,
                                                                                                      self.robot.y))
            return False, 0.0

        # Is the path too close to any box
        min_distance_to_intercept = chk_distance
        self.robot_is_crashed = False
        for box_id, box in self.boxes.iteritems():
            # do a coarse check to see if the center of the obstacle
            # is too far away to be concerned with
            dst = self._distance_point_to_line_segment((box['ctr_x'], box['ctr_y']), t0, t1)
            if dst <= self.BOX_DIAG + self.ROBOT_RADIUS:
                # refine the intercept computation
                dst, intercept_point = self._check_intersection(t0, t1, box)
                if dst < min_distance_to_intercept:
                    min_distance_to_intercept = dst
                    min_intercept_point = intercept_point
                    
        # Is the path too close to any obstacle
        for o in self.obstacles:
            # do a coarse check to see if the center of the obstacle
            # is too far away to be concerned with
            dst = self._distance_point_to_line_segment((o['ctr_x'], o['ctr_y']), t0, t1)
            if dst <= self.OBSTACLE_DIAG + self.ROBOT_RADIUS:
                # refine the intercept computation
                dst, intercept_point = self._check_intersection(t0, t1, o)
                if dst < min_distance_to_intercept:
                    min_distance_to_intercept = dst 
                    min_intercept_point = intercept_point

        # Check the edges of the warehouse
        dst, intercept_point = self._check_intersection(t0, t1, self.warehouse_limits)
        if dst < min_distance_to_intercept:
            min_distance_to_intercept = dst 
            min_intercept_point = intercept_point
            
        if min_distance_to_intercept < chk_distance:
            self.robot_is_crashed = True
            print "*** Robot crashed at {p[0]:6.2f} {p[1]:6.2f} ***".format(p=min_intercept_point)
            return False, robot.compute_distance((self.robot.x, self.robot.y), min_intercept_point)

        return True, distance     

    # Check if the trajectory intersects with a square obstacle
    def _check_intersection(self, t0, t1, obstacle):

        min_distance_to_intercept = 1.e6
        min_intercept_point = (0., 0.)

        # check each segment
        for s in obstacle['segments']:
            dst, intercept_point = self._linesegment_intersection(t0, t1, s[0], s[1])
            if dst < min_distance_to_intercept:
                min_distance_to_intercept = dst 
                min_intercept_point = intercept_point 
            
        # if circular corners are defined - check them
        # circular corners occur when dilating a rectangle with a circle
        if 'corners' in obstacle:
            for c in obstacle['corners']:
                dst, intercept_point = self._corner_intersection(t0, t1, c)
                if dst < min_distance_to_intercept:
                    min_distance_to_intercept = dst 
                    min_intercept_point = intercept_point
            
        return min_distance_to_intercept, min_intercept_point

    # Find the intersection of a line segment and a semicircle as defined in 
    # the corner dictionary 
    # Use quadratic solution to solve simultaneous equations for
    # (x-a)^2 + (y-b)^2 = r^2 and y = mx + c
    def _corner_intersection(self, t0, t1, corner):

        dst = 1.e6
        intercept_point = (0., 0.)

        # Note:  changing nomenclature here so that circle center is a,b
        # and line intercept is c (not b as above)
        a = corner['ctr_x']                 # circle ctrs
        b = corner['ctr_y']
        r = corner['radius']

        # check the case for infinite slope
        dx = t1[0] - t0[0]

        # Find intersection assuming vertical trajectory
        if abs(dx) < 1.e-6:
            x0 = t0[0] - a
            # qa = 1.
            qb = -2. * b
            qc = b * b + x0 * x0 - r * r
            disc = qb * qb - 4. * qc

            if disc >= 0.:
                sd = math.sqrt(disc)
                xp = xm = t0[0]
                yp = (-qb + sd) / 2.
                ym = (-qb - sd) / 2.
      
        # Find intersection assuming non vertical trajectory
        else:
            m = (t1[1] - t0[1]) / dx  # slope of line
            c = t0[1] - m*t0[0]       # y intercept of line
  
            qa = 1. + m * m
            qb = 2. * (m * c - m * b - a)
            qc = a * a + b * b + c * c - 2. * b * c - r * r

            disc = qb * qb - 4. * qa * qc
  
            if disc >= 0.:
                sd = math.sqrt(disc)
                xp = (-qb + sd) / (2. * qa)
                yp = m * xp + c
                xm = (-qb - sd) / (2. * qa)
                ym = m * xm + c
        
        if disc >= 0.:
            dp2 = dm2 = 1.e6
            if corner['min_x'] <= xp <= corner['max_x'] and corner['min_y'] <= yp <= corner['max_y']:
                dp2 = (xp - t0[0])**2 + (yp - t0[1])**2

            if corner['min_x'] <= xm <= corner['max_x'] and corner['min_y'] <= ym <= corner['max_y']:
                dm2 = (xm - t0[0])**2 + (ym - t0[1])**2

            if dp2 < dm2:
                # make sure the intersection point is actually on the trajectory segment
                if self._distance_point_to_line_segment((xp, yp), t0, t1) < 1.e-6:
                    dst = math.sqrt(dp2)
                    intercept_point = (xp, yp)
            else:
                if self._distance_point_to_line_segment((xm, ym), t0, t1) < 1.e-6:
                    dst = math.sqrt(dm2)
                    intercept_point = (xm, ym)

        return dst, intercept_point

    # Find the distance from a point to a line segment
    # This function is used primarily to find the distance between a trajectory
    # segment defined by l0,l1 and the center of an obstacle or box specified
    # by point p.  For a reference see the lecture on SLAM and the segmented CTE
    def _distance_point_to_line_segment(self, p, l0, l1):
  
        dx = l1[0] - l0[0]
        dy = l1[1] - l0[1]

        # check that l0,l1 don't describe a point
        d2 = (dx * dx + dy * dy)

        if abs(d2) > 1.e-6:
        
            t = ((p[0] - l0[0]) * dx + (p[1] - l0[1]) * dy) / d2

            # if point is on line segment
            if 0.0 <= t <= 1.0:
                intx, inty = l0[0] + t * dx, l0[1] + t * dy
                dx, dy = p[0] - intx, p[1] - inty
   
            # point is beyond end point
            elif t > 1.0:
                dx, dy = p[0] - l1[0], p[1] - l1[1]
            
            # point is before beginning point
            else:
                dx, dy = p[0] - l0[0], p[1] - l0[1]
                
            dst = math.sqrt(dx * dx + dy * dy)

        else:
            dx, dy = p[0] - l0[0], p[1] - l0[1]
            dst = math.sqrt(dx * dx + dy * dy)

        return dst

    # Check for the intersection of two line segments.  This function assumes that the robot
    # trajectory starts at p0 and ends at p1.  The segment being checked is q0 and q1
    # There is no check for colinearity because the obstacle is assumed to have orthogonal 
    # sides and so the intersection for a trajectory that is colinear and overlapping with 
    # one side will intersect with the orthogonal side, since by definition the starting 
    # point of the trajectory is always outside the obstacle.
    # For a reference see:
    #  http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect/565282#565282
    def _linesegment_intersection(self, p0, p1, q0, q1):

        eps = 1.0e-6
        dst = 1.0e6
        intersection = (0., 0.)

        r = p1[0] - p0[0], p1[1] - p0[1]
        s = q1[0] - q0[0], q1[1] - q0[1]
        qmp = q0[0] - p0[0], q0[1] - p0[1]

        rxs = r[0] * s[1] - r[1] * s[0]
        qmpxr = qmp[0] * r[1] - qmp[1] * r[0]

        if abs(rxs) >= eps:

            # check for intersection
            # parametric equations for intersection
            # t = (q - p) x s / (r x s)
            t = (qmp[0] * s[1] - qmp[1] * s[0]) / rxs

            # u = (q - p) x r / (r x s)
            u = qmpxr / rxs

            # Note that u and v can be slightly out of this range due to
            # precision issues so we round them 
            if (0.0 <= np.round(t, 4) <= 1.0) and (0.0 <= np.round(u, 4) <= 1.0):
                dx, dy = t * r[0], t * r[1]
                dst = math.sqrt(dx * dx + dy * dy)
                intersection = (p0[0] + dx, p0[1] + dy)

        return dst, intersection
  
    # Check whether or not robot is holding a box
    def _robot_has_box(self):
        return self.box_held is not None

    # Lift the box
    def _lift_box(self, box_id):

        self.boxes.pop(box_id)
        self.box_held = box_id

    # Set the box down at the specified destination and recompute its parameters
    # for obstacle avoidance computation
    def _down_box(self, destination):

        # - If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
        #   house.
        x, y = destination

        if self._is_box_within_dropzone(destination):
            self._deliver_box(self.box_held)
        else:
            # set up the parameters for processing the box as an obstacle and for 
            # picking it up and setting it down later
            box = dict()                    
            # box edges
            box['min_x'] = x - self.BOX_SIZE
            box['max_x'] = x + self.BOX_SIZE
            box['min_y'] = y - self.BOX_SIZE
            box['max_y'] = y + self.BOX_SIZE
                    
            # center of obstacle
            box['ctr_x'] = x
            box['ctr_y'] = y

            # compute clearance parameters for robot
            box = self._dilate_obstacle_for_robot(box)
            
            self.boxes[self.box_held] = box            

        self.box_held = None

    # Deliver the box by appending to the list of delivered boxes
    def _deliver_box(self, box_id):
        self.boxes_delivered.append(box_id)

    # Compute the clearance parameters for the robot by dilating the object using
    # a circle the radius of the robot.  The resulting shape is rectangular with
    # rounded corners
    def _dilate_obstacle_for_robot(self, obstacle):

        # line segments dilated for robot intersection
        obstacle['segments'] = []
        # West segment
        obstacle['segments'].append([(obstacle['min_x'] - self.ROBOT_RADIUS, obstacle['max_y']),
                                     (obstacle['min_x'] - self.ROBOT_RADIUS, obstacle['min_y'])])
        # South segment
        obstacle['segments'].append([(obstacle['min_x'], obstacle['min_y'] - self.ROBOT_RADIUS),
                                     (obstacle['max_x'], obstacle['min_y'] - self.ROBOT_RADIUS)])
        # East segment
        obstacle['segments'].append([(obstacle['max_x'] + self.ROBOT_RADIUS, obstacle['min_y']),
                                     (obstacle['max_x'] + self.ROBOT_RADIUS, obstacle['max_y'])])
        # North segment
        obstacle['segments'].append([(obstacle['max_x'], obstacle['max_y'] + self.ROBOT_RADIUS),
                                     (obstacle['min_x'], obstacle['max_y'] + self.ROBOT_RADIUS)])

        obstacle['corners'] = []
        # NW corner
        cornerdef = dict()
        cornerdef['ctr_x'] = obstacle['min_x']
        cornerdef['ctr_y'] = obstacle['max_y']
        cornerdef['radius'] = self.ROBOT_RADIUS
        cornerdef['min_x'] = obstacle['min_x'] - self.ROBOT_RADIUS
        cornerdef['max_x'] = obstacle['min_x']
        cornerdef['min_y'] = obstacle['max_y']
        cornerdef['max_y'] = obstacle['max_y'] + self.ROBOT_RADIUS
        obstacle['corners'].append(cornerdef)

        # SW corner
        cornerdef = dict()
        cornerdef['ctr_x'] = obstacle['min_x']
        cornerdef['ctr_y'] = obstacle['min_y']
        cornerdef['radius'] = self.ROBOT_RADIUS
        cornerdef['min_x'] = obstacle['min_x'] - self.ROBOT_RADIUS
        cornerdef['max_x'] = obstacle['min_x']
        cornerdef['min_y'] = obstacle['min_y'] - self.ROBOT_RADIUS
        cornerdef['max_y'] = obstacle['min_y']
        obstacle['corners'].append(cornerdef)

        # SE corner
        cornerdef = dict()
        cornerdef['ctr_x'] = obstacle['max_x']
        cornerdef['ctr_y'] = obstacle['min_y']
        cornerdef['radius'] = self.ROBOT_RADIUS
        cornerdef['min_x'] = obstacle['max_x'] 
        cornerdef['max_x'] = obstacle['max_x'] + self.ROBOT_RADIUS 
        cornerdef['min_y'] = obstacle['min_y'] - self.ROBOT_RADIUS
        cornerdef['max_y'] = obstacle['min_y']
        obstacle['corners'].append(cornerdef)

        # NE corner
        cornerdef = dict()
        cornerdef['ctr_x'] = obstacle['max_x']
        cornerdef['ctr_y'] = obstacle['max_y']
        cornerdef['radius'] = self.ROBOT_RADIUS
        cornerdef['min_x'] = obstacle['max_x'] 
        cornerdef['max_x'] = obstacle['max_x'] + self.ROBOT_RADIUS 
        cornerdef['min_y'] = obstacle['max_y']
        cornerdef['max_y'] = obstacle['max_y'] + self.ROBOT_RADIUS 
        obstacle['corners'].append(cornerdef)

        return obstacle

    def get_boxes_delivered(self):
        return self.boxes_delivered

    def get_total_cost(self):
        return self.total_cost

    def print_to_console(self):
        print ''
        print 'Robot state:'
        print '\t x = {:6.2f}, y = {:6.2f}, hdg = {:6.2f}'.format(self.robot.x, self.robot.y,
                                                                  self.robot.bearing * 180. / PI)
        print 'Box state:'
        for box_id, box in self.boxes.iteritems():   
            print '\tbox id {}, x = {:6.2f}, y = {:6.2f}'.format(box_id, box['ctr_x'], box['ctr_y'])
        print 'Total cost:', self.total_cost
        print 'Box id held:', self.box_held
        print 'Delivered:', self.boxes_delivered
        print ''


# CREDIT TO: Jay W J for test class (See testing_suite_partA.py)
class PartBTestCase(unittest.TestCase):
    results = ['', 'PART B TEST CASE RESULTS']
    SCORE_TEMPLATE = "\n".join((
        "\n-----------",
        "Test Case {test_case}",
        "cost: {cost:.2f}  (expected min {min_cost:.2f})",
        "credit: {score:.2f}"
    ))
    FAIL_TEMPLATE = "\n".join((
        "\n-----------",
        "Test Case {test_case}",
        "Failed: {message}",
        "credit: 0"
    ))

    credit = []

    @classmethod
    def tearDownClass(cls):
        # Prints results after all tests complete
        with open('results_partB.txt', 'w') as f:
            for line in cls.results:
                f.write(line)
            f.write("\n-----------")
            f.write('\nTotal Credit: {:.2f}'.format(sum(cls.credit)))

    def run_test_with_params(self, params):

        accomplished = False
        errorMessage = ''
        try:
            cost, delivered = execute_student_plan(params['warehouse'],
                                                   params['todo'],
                                                   params['max_distance'],
                                                   params['max_steering'])
            accomplished = True
        except Exception as e:
            errorMessage = repr(e)
            self.results.append(self.FAIL_TEMPLATE.format(message=errorMessage, **params))
        
        self.assertTrue(accomplished, errorMessage)

        score = params['min_cost']/cost * float(len(delivered))/float(len(params['todo'])) 
        self.results.append(self.SCORE_TEMPLATE.format(cost=cost, score=score, **params))
        self.credit.append(score)
       
        return score

    @timeout(TIME_LIMIT)
    def test_case1(self):
        params = {
            'test_case': 1,
            'warehouse': ['..#..',
                          '.....',
                          '..#..',
                          '.....',
                          '....@'],
            'todo': [(1.5, -0.5),
                     (4.0, -2.5)],
            'max_distance': 5.0,
            'max_steering': PI / 2. + 0.01,
            'min_cost': 38.
        }
        score = self.run_test_with_params(params)
        print 'credit: {}'.format(score)

# Note that we have included several more test cases below
# after you have your system working with the first test
# case, you can uncomment one/more of the following as well.
#

    # @timeout(TIME_LIMIT)
    # def test_case2(self):
    #     params = {
    #         'test_case': 2,
    #         'warehouse': ['..#..@',
    #                       '......',
    #                       '..####',
    #                       '..#...',
    #                       '......'],
    #         'todo': [(3.5, -3.5),
    #                  (0.5, -1.0)],
    #         'max_distance': 5.0,
    #         'max_steering': PI / 2. + 0.01,
    #         'min_cost': 56.
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # Test Case 3
    # @timeout(TIME_LIMIT)
    # def test_case3(self):
    #     params = {
    #         'test_case': 3,
    #         'warehouse': ['..#...',
    #                       '......',
    #                       '..####',
    #                       '..#..#',
    #                       '.....@'],
    #         'todo': [(4.5, -1.0),
    #                  (3.5, -3.5)],
    #     'max_distance': 5.0,
    #     'max_steering': PI / 2. + 0.01,
    #     'min_cost': 43.0
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # Test Case 4 - The path should be shorter than test case 3
    # @timeout(TIME_LIMIT)
    # def test_case4(self):
    #     params = {
    #         'test_case': 4,
    #         'warehouse': ['..#...',
    #                       '......',
    #                       '..##.#',
    #                       '..#..#',
    #                       '.....@'],
    #         'todo': [(4.5, -1.0),
    #                  (3.5, -3.5)],
    #         'max_distance': 5.0,
    #         'max_steering': PI / 2. + 0.01,
    #         'min_cost': 30.0
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # Test Case 5
    # @timeout(TIME_LIMIT)
    # def test_case5(self):
    #     params = {
    #         'test_case': 5,
    #         'warehouse': ['..#...',
    #                       '#....#',
    #                       '..##.#',
    #                       '..#..#',
    #                       '#....@'],
    #         'todo': [(1.0, -.5),
    #                  (0.5, -3.5)],
    #         'max_distance': 5.0,
    #         'max_steering': PI / 2. + 0.01,
    #         'min_cost': 50.0
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # Test Case 6
    # @timeout(TIME_LIMIT)
    # def test_case6(self):
    #     params = {
    #         'test_case': 6,
    #         'warehouse': ['@.#...#',
    #                       '#...#..'],
    #         'todo': [(4.5, -.5),
    #                  (6.0, -1.5)],
    #         'max_distance': 5.0,
    #         'max_steering': PI / 2. + 0.01,
    #         'min_cost': 61.5
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # *** CREDIT TO: James Corbitt for the following test cases

    # @timeout(TIME_LIMIT)
    # def test_case7(self):
    #     params = {
    #         'test_case': 7,
    #         'warehouse': ['#.@.#',
    #                       '..#..'],
    #         'todo': [(0.5, -1.5),
    #                  (4.5, -1.5)],
    #         'max_distance': 5.0,
    #         'max_steering': PI / 2. + 0.01,
    #         'min_cost': 29.4857865623
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # @timeout(TIME_LIMIT)
    # def test_case8(self):
    #     params = {
    #         'test_case': 8,
    #         'warehouse': ['#.@.#'],
    #         'todo': [(1.5, -0.5),
    #                  (3.5, -0.5)],
    #         'max_distance': 5.0,
    #         'max_steering': PI / 2. + 0.01,
    #         'min_cost': 15.9980798485
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # @timeout(TIME_LIMIT)
    # def test_case9(self):
    #     params = {
    #         'test_case': 9,
    #         'warehouse': ['#.######',
    #                       '#.#....#',
    #                       '#.#.##.#',
    #                       '#.#.@#.#',
    #                       '#.####.#',
    #                       '#......#',
    #                       '########'],
    #         'todo': [(3.5, -3.5), (3.5, -2.5), (3.5, -1.5), (4.5, -1.5),
    #                  (5.5, -1.5), (6.5, -2.5), (6.5, -3.5), (6.5, -4.5),
    #                  (6.5, -5.5), (5.5, -5.5), (4.5, -5.5), (3.5, -5.5),
    #                  (2.5, -5.5), (1.5, -4.5), (1.5, -3.5), (1.5, -2.5),
    #                  (1.5, -1.5), (1.5, -0.5)
    #                  ],
    #         'max_distance': 3.0,
    #         'max_steering': PI / 2. + 0.01,
    #         'min_cost': 603.432133513
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # @timeout(TIME_LIMIT)
    # def test_case10(self):
    #     params = {
    #         'test_case': 10,
    #         'warehouse': ['#######.',
    #                       '#.......',
    #                       '#@......'],
    #         'todo': [(7.5, -1.5),
    #                  (7.5, -0.5)],
    #         'max_distance': 3.0,
    #         'max_steering': PI / 2. + 0.01,
    #         'min_cost': 42.8704538273
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

#Only run the test suites automatically if this file was executed on the command line, leaving nose/py.test free to handle the test cases if loaded in an IDE
if __name__ == "__main__":
     all_suites = map(lambda x: unittest.TestLoader().loadTestsFromTestCase(x), [PartBTestCase])
     all_tests = unittest.TestSuite(all_suites)
     unittest.TextTestRunner(verbosity=2).run(all_tests)
