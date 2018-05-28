#!/usr/bin/python

import math
import random
import robot
import sys

from functools import wraps
from Queue import Queue
from Queue import Empty as QueueEmptyError
from threading import Thread
from multiprocessing import TimeoutError

import unittest
import timeit

try:
    import studentMain1
except Exception as e:
    print "Error importing studentMain1:", e

try:
    import studentMain2
except Exception as e:
    print "Error importing studentMain2:", e

try:
    import studentMain3
except Exception as e:
    print "Error importing studentMain3:", e

try:
    import studentMain4
except Exception as e:
    print "Error importing studentMain4:", e


PI = math.pi

GLOBAL_SEEDS = [None, 
  None,
  'air_nomads',
  'water_tribes',
  'earth_kingdom',
  'fire_nation'
]

TIME_LIMIT = 5 # seconds

CREDIT_PER_PASS = 2.5 # points

GLOBAL_PARAMETERS = [None,

     {'test_case': 1,
     'target_x': 9.84595717195,
     'target_y': -3.82584680823,
     'target_heading': 1.95598927002,
     'target_period': -6,
     'target_speed': 2.23288537085,
     'target_line_length': 12, 
     'hunter_x': -18.9289073476,
     'hunter_y': 18.7870153895,
     'hunter_heading': -1.94407132569
    },
    {'test_case': 2,
     'target_x': 9.26465282849,
     'target_y': -5.37198134722,
     'target_heading': 1.50733100266,
     'target_period': -3,
     'target_speed': 4.97835577487,
     'target_line_length': 15, 
     'hunter_x': -18.7956415381,
     'hunter_y': 12.4047226453,
     'hunter_heading': -1.35305387284
    },
    {'test_case': 3,
     'target_x': -8.23729263767,
     'target_y': 0.167449172934,
     'target_heading': -2.90891604491,
     'target_period': -8,
     'target_speed': 2.86280919028,
     'target_line_length': 5, 
     'hunter_x': -1.26626321675,
     'hunter_y': 10.2766202621,
     'hunter_heading': -2.63089786461
    },
    {'test_case': 4,
     'target_x': -2.18967022691,
     'target_y': 0.255925949831,
     'target_heading': 2.69251137563,
     'target_period': -12,
     'target_speed': 2.74140955105,
     'target_line_length': 15, 
     'hunter_x': 4.07484976298,
     'hunter_y': -10.5384658671,
     'hunter_heading': 2.73294117637
    },
    {'test_case': 5,
     'target_x': 0.363231634197,
     'target_y': 15.3363820727,
     'target_heading': 1.00648485361,
     'target_period': 7,
     'target_speed': 4.01304863745,
     'target_line_length': 15, 
     'hunter_x': -19.6386687235,
     'hunter_y': -13.6078079345,
     'hunter_heading': -2.18960549765
    },
    {'test_case': 6,
     'target_x': 19.8033444747,
     'target_y': 15.8607456499,
     'target_heading': 2.91674681677,
     'target_period': 10,
     'target_speed': 4.11574616586,
     'target_line_length': 1, 
     'hunter_x': -13.483627167,
     'hunter_y': 7.60284054436,
     'hunter_heading': 2.45511184918
    },
    {'test_case': 7,
     'target_x': -17.2113204789,
     'target_y': 10.5496426749,
     'target_heading': -2.07830482038,
     'target_period': 3,
     'target_speed': 4.58689282387,
     'target_line_length': 10, 
     'hunter_x': -7.95068213364,
     'hunter_y': -4.00088251391,
     'hunter_heading': 0.281505756944
    },
    {'test_case': 8,
     'target_x': 10.5639252231,
     'target_y': 13.9095062695,
     'target_heading': -2.92543870157,
     'target_period': 10,
     'target_speed': 2.2648280036,
     'target_line_length': 11, 
     'hunter_x': 4.8678066293,
     'hunter_y': 4.61870594164,
     'hunter_heading': 0.356679261444
    },
    {'test_case': 9,
     'target_x': 13.6383033581,
     'target_y': -19.2494482213,
     'target_heading': 3.08457233661,
     'target_period': -5,
     'target_speed': 4.8813691359,
     'target_line_length': 8, 
     'hunter_x': -0.414540470517,
     'hunter_y': 13.2698415309,
     'hunter_heading': -2.21974457597
    },
    {'test_case': 10,
     'target_x': -2.97944715844,
     'target_y': -18.7085807377,
     'target_heading': 2.80820284661,
     'target_period': 8,
     'target_speed': 3.67540398247,
     'target_line_length': 8, 
     'hunter_x': 16.7631157868,
     'hunter_y': 8.8386686632,
     'hunter_heading': -2.91906838766
    },

]

NOT_FOUND = """
Part {}, Test Case {}, did not succeed within {} steps.
"""

def distance(p, q):
    x1, y1 = p
    x2, y2 = q

    dx = x2 - x1
    dy = y2 - y1

    return math.sqrt(dx**2 + dy**2)


def truncate_angle(t):
    return ((t+PI)%(2*PI)) - PI


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
    except:
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


def simulate_without_hunter(params):

    estimate_next_pos = params['student_method']

    target = robot.robot(params['target_x'],
                         params['target_y'],
                         params['target_heading'],
                         2.0 * PI / params['target_period'],
                         params['target_speed'],
			 params['target_line_length'])
    target.set_noise(0.0,
                     0.0,
                     params['noise_ratio'] * params['target_speed'])

    tolerance = params['tolerance_ratio'] * target.distance
    other_info = None
    steps = 0

    random.seed(GLOBAL_SEEDS[params['part']])
    while steps < params['max_steps']:

        target_pos = (target.x, target.y)
        target_meas = target.sense()

        estimate, other_info = estimate_next_pos(target_meas, other_info)

        target.move_in_polygon()
        target_pos = (target.x, target.y)

        separation = distance(estimate, target_pos)
        if separation < tolerance:
            return True, steps

        steps += 1

    return False, steps


def simulate_with_hunter(params):

    next_move = params['student_method']

    target = robot.robot(params['target_x'],
                         params['target_y'],
                         params['target_heading'],
                         2.0 * PI / params['target_period'],
                         params['target_speed'],
	 		 params['target_line_length'])
    target.set_noise(0.0,
                     0.0,
                     params['noise_ratio'] * params['target_speed'])

    hunter = robot.robot(params['hunter_x'],
                         params['hunter_y'],
                         params['hunter_heading'])

    tolerance = params['tolerance_ratio'] * target.distance
    max_speed = params['speed_ratio'] * params['target_speed']
    other_info = None
    steps = 0
    
    random.seed(GLOBAL_SEEDS[params['part']])
    while steps < params['max_steps']:

        hunter_pos = (hunter.x, hunter.y)
        target_pos = (target.x, target.y)

        separation = distance(hunter_pos, target_pos)
        if separation < tolerance:
            return True, steps

        target_meas = target.sense()
        turn, dist, other_info = next_move(hunter_pos, hunter.heading, target_meas, max_speed, other_info)

        dist = min(dist, max_speed)
        dist = max(dist, 0)
        turn = truncate_angle(turn)

        hunter.move(turn, dist)
        target.move_in_polygon()

        steps += 1

    return False, steps


class GenericPartTestCase(unittest.TestCase):

    params = {}
    params['tolerance_ratio'] = 0.02

    def run_with_params(self, k):
        params = self.params.copy()
        params.update(GLOBAL_PARAMETERS[k]) # how to make k vary?
        found, steps = params['test_method'](params)
        self.assertTrue(found,
            NOT_FOUND.format(params['part'], params['test_case'], steps))

    @timeout(TIME_LIMIT)
    def test_case01(self):
        self.run_with_params(1)

    @timeout(TIME_LIMIT)
    def test_case02(self):
        self.run_with_params(2)

    @timeout(TIME_LIMIT)
    def test_case03(self):
        self.run_with_params(3)

    @timeout(TIME_LIMIT)
    def test_case04(self):
        self.run_with_params(4)

    @timeout(TIME_LIMIT)
    def test_case05(self):
        self.run_with_params(5)

    @timeout(TIME_LIMIT)
    def test_case06(self):
        self.run_with_params(6)

    @timeout(TIME_LIMIT)
    def test_case07(self):
        self.run_with_params(7)

    @timeout(TIME_LIMIT)
    def test_case08(self):
        self.run_with_params(8)

    @timeout(TIME_LIMIT)
    def test_case09(self):
        self.run_with_params(9)

    @timeout(TIME_LIMIT)
    def test_case10(self):
        self.run_with_params(10)

class Part1TestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 1
        params['method_name'] = 'estimate_next_pos'
        params['max_steps'] = 10
        params['noise_ratio'] = 0.00
        params['test_method'] = simulate_without_hunter
        params['student_method'] = studentMain1.estimate_next_pos


class Part2TestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 2
        params['method_name'] = 'estimate_next_pos'
        params['max_steps'] = 1000
        params['noise_ratio'] = 0.05
        params['test_method'] = simulate_without_hunter
        params['student_method'] = studentMain2.estimate_next_pos


class Part3TestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 3
        params['method_name'] = 'next_move'
        params['max_steps'] = 1000
        params['noise_ratio'] = 0.05
        params['speed_ratio'] = 2.00
        params['test_method'] = simulate_with_hunter
        params['student_method'] = studentMain3.next_move


class Part4TestCase(GenericPartTestCase):
    def setUp(self):
        params = self.params
        params['part'] = 4
        params['method_name'] = 'next_move'
        params['max_steps'] = 1000
        params['noise_ratio'] = 0.05
        params['speed_ratio'] = 0.99
        params['test_method'] = simulate_with_hunter
        params['student_method'] = studentMain4.next_move




suites = map(lambda x: unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(x)), 
    [Part1TestCase, Part2TestCase, Part3TestCase, Part4TestCase ])

total_passes = 0

for i, suite in zip(range(1,1+len(suites)),suites):
    print "====================\nTests for Part {}:".format(i)

    result = unittest.TestResult()
    suite.run(result)

    for x in result.errors:
        print x[0], x[1]
    for x in result.failures:
        print x[0], x[1]

    num_errors = len(result.errors)
    num_fails = len(result.failures)
    num_passes = result.testsRun - num_errors - num_fails
    total_passes += num_passes

    print "Successes: {}\nFailures: {}\n".format(num_passes, num_errors + num_fails)

print "====================\nOverall Score: {}".format(total_passes * CREDIT_PER_PASS)
