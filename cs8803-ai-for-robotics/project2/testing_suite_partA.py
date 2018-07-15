#!/usr/bin/python

import math
# import random
import string
import sys
import copy

from functools import wraps
from Queue import Queue
from Queue import Empty as QueueEmptyError
from threading import Thread
from multiprocessing import TimeoutError

import unittest
import timeit

import partA

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


def execute_student_plan(warehouse, todo):

    student_planner = partA.DeliveryPlanner(copy.copy(warehouse), copy.copy(todo))
    action_list = student_planner.plan_delivery()

    state = State(warehouse)
    num_delivered = 0
    next_box_to_deliver = todo[num_delivered]

    for action in action_list:
        state.print_to_console()
        state.update_according_to(action)

        # check if new box has been delivered
        delivered = state.get_boxes_delivered()
        if len(delivered) > num_delivered:
            last_box_delivered = delivered[-1]
            if last_box_delivered == next_box_to_deliver:
                num_delivered += 1
                if num_delivered < len(todo):
                    next_box_to_deliver = todo[num_delivered]
                else:
                    # all boxes delivered: end test
                    break
            else:
                # wrong box delivered: kill test
                raise Exception('wrong box delivered: {} instead of {}'.format(last_box_delivered,
                                                                               next_box_to_deliver))

    state.print_to_console()

    if num_delivered < len(todo):
        raise Exception('task not accomplished: not all boxes delivered')

    return state.get_total_cost()


class State:
    ORTHOGONAL_MOVE_COST = 2
    DIAGONAL_MOVE_COST = 3
    BOX_LIFT_COST = 4
    BOX_DOWN_COST = 2
    ILLEGAL_MOVE_PENALTY = 100

    def __init__(self, warehouse):
        self.boxes_delivered = []
        self.total_cost = 0
        self._set_initial_state_from(warehouse)

    def _set_initial_state_from(self, warehouse):
        rows = len(warehouse)
        cols = len(warehouse[0])

        self.warehouse_state = [[None for j in range(cols)] for i in range(rows)]
        self.dropzone = None
        self.boxes = dict()

        for i in range(rows):
            for j in range(cols):
                this_square = warehouse[i][j]

                if this_square == '.':
                    self.warehouse_state[i][j] = '.'

                elif this_square == '#':
                    self.warehouse_state[i][j] = '#'

                elif this_square == '@':
                    self.warehouse_state[i][j] = '*'
                    self.dropzone = (i, j)

                else:  # a box
                    box_id = this_square
                    self.warehouse_state[i][j] = box_id
                    self.boxes[box_id] = (i, j)

        self.robot_position = self.dropzone
        self.box_held = None

    def update_according_to(self, action):
        # what type of move is it?
        action = action.split()
        action_type = action[0]

        if action_type == 'move':
            row, col = action[1:]
            self._attempt_move(row, col)

        elif action_type == 'lift':
            box = action[1]
            self._attempt_lift(box)

        elif action_type == 'down':
            row, col = action[1:]
            self._attempt_down(row, col)

        else:
            # improper move format: kill test
            raise Exception('improperly formatted action: {}'.format(''.join(action)))

    def _attempt_move(self, row, col):
        # - The robot may not move outside the warehouse.
        # - The warehouse does not "wrap" around.
        # - Two spaces are considered adjacent if they share an edge or a corner.

        # - The robot may move horizontally or vertically at a cost of 2 per move.
        # - The robot may move diagonally at a cost of 3 per move.
        # Illegal move (100 cost):
        # - attempting to move to a nonadjacent, nonexistent, or occupied space

        try:
            destination = (int(row), int(col))
            
            destination_is_adjacent = self._are_adjacent(self.robot_position, destination)
            destination_is_traversable = self._is_traversable(destination)

            is_legal_move = destination_is_adjacent and destination_is_traversable
            if is_legal_move:
                self._move_robot_to(destination)
            else:
                self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

        except ValueError:
            raise Exception('improperly formatted move destination: {} {}'.format(row, col))
        except IndexError:  # (row, col) not in warehouse
            self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

    def _attempt_lift(self, box_id):
        # - The robot may pick up a box that is in an adjacent square.
        # - The cost to pick up a box is 4, regardless of the direction the box is relative to the robot.
        # - While holding a box, the robot may not pick up another box.
        # Illegal moves (100 cost):
        # - attempting to pick up a nonadjacent or nonexistent box
        # - attempting to pick up a box while holding one already
        try:
            box_position = self.boxes[box_id]

            box_is_adjacent = self._are_adjacent(self.robot_position, box_position)
            robot_has_box = self._robot_has_box()

            is_legal_lift = box_is_adjacent and (not robot_has_box)
            if is_legal_lift:
                self._lift_box(box_id)
            else:
                self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

        except KeyError:
            self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

    def _attempt_down(self, row, col):
        # - The robot may put a box down on an adjacent empty space ('.') or the dropzone ('@') at a cost
        #   of 2 (regardless of the direction in which the robot puts down the box).
        # Illegal moves (100 cost):
        # - attempting to put down a box on a nonadjacent, nonexistent, or occupied space
        # - attempting to put down a box while not holding one
        try:
            destination = (int(row), int(col))

            destination_is_adjacent = self._are_adjacent(self.robot_position, destination)
            destination_is_traversable = self._is_traversable(destination)
            robot_has_box = self._robot_has_box()

            is_legal_down = destination_is_adjacent and destination_is_traversable and robot_has_box
            if is_legal_down:
                self._down_box(destination)
            else:
                self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

        except ValueError:
            raise Exception('improperly formatted down destination: {} {}'.format(row, col))
        except IndexError:  # (row, col) not in warehouse
            self._increase_total_cost_by(self.ILLEGAL_MOVE_PENALTY)

    def _increase_total_cost_by(self, amount):
        self.total_cost += amount

    def _is_within_warehouse(self, coordinates):
        i, j = coordinates
        rows = len(self.warehouse_state)
        cols = len(self.warehouse_state[0])
        return (0 <= i < rows) and (0 <= j < cols)

    def _are_adjacent(self, coordinates1, coordinates2):
        return (self._are_horizontally_adjacent(coordinates1, coordinates2) or
                self._are_vertically_adjacent(coordinates1, coordinates2) or 
                self._are_diagonally_adjacent(coordinates1, coordinates2)
                )

    def _are_horizontally_adjacent(self, coordinates1, coordinates2):
        row1, col1 = coordinates1
        row2, col2 = coordinates2
        return (row1 == row2) and (abs(col1 - col2) == 1)

    def _are_vertically_adjacent(self, coordinates1, coordinates2):
        row1, col1 = coordinates1
        row2, col2 = coordinates2
        return (abs(row1 - row2) == 1) and (col1 == col2)

    def _are_diagonally_adjacent(self, coordinates1, coordinates2):
        row1, col1 = coordinates1
        row2, col2 = coordinates2
        return (abs(row1 - row2) == 1) and (abs(col1 - col2) == 1)

    def _is_traversable(self, coordinates):
        is_wall = self._is_wall(coordinates)
        has_box = self._space_contains_box(coordinates)
        return (not is_wall) and (not has_box)

    def _is_wall(self, coordinates):
        i, j = coordinates
        return self.warehouse_state[i][j] == '#'

    def _space_contains_box(self, coordinates):
        i, j = coordinates
        return self.warehouse_state[i][j] in (string.ascii_letters + string.digits)

    def _robot_has_box(self):
        return self.box_held is not None

    def _move_robot_to(self, destination):
        old_position = self.robot_position
        self.robot_position = destination

        i1, j1 = old_position
        if self.dropzone == old_position:
            self.warehouse_state[i1][j1] = '@'
        else:
            self.warehouse_state[i1][j1] = '.'

        i2, j2 = destination
        self.warehouse_state[i2][j2] = '*'

        if self._are_diagonally_adjacent(old_position, destination):
            self._increase_total_cost_by(self.DIAGONAL_MOVE_COST)
        else:
            self._increase_total_cost_by(self.ORTHOGONAL_MOVE_COST)

    def _lift_box(self, box_id):
        i, j = self.boxes[box_id]
        self.warehouse_state[i][j] = '.'

        self.boxes.pop(box_id)

        self.box_held = box_id

        self._increase_total_cost_by(self.BOX_LIFT_COST)

    def _down_box(self, destination):
        # - If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
        #   house.
        i, j = destination

        if self.warehouse_state[i][j] == '.':
            self.warehouse_state[i][j] = self.box_held
            self.boxes[self.box_held] = (i, j)
        else:
            self._deliver_box(self.box_held)

        self.box_held = None
        self._increase_total_cost_by(self.BOX_DOWN_COST)

    def _deliver_box(self, box_id):
        self.boxes_delivered.append(box_id)

    def get_boxes_delivered(self):
        return self.boxes_delivered

    def get_total_cost(self):
        return self.total_cost

    def print_to_console(self):
        print ''
        for row in self.warehouse_state:
            print ''.join(row)
        print 'total cost:', self.total_cost
        print 'box held:', self.box_held
        print 'delivered:', self.boxes_delivered
        print ''


# CREDIT TO: Jay W J for rewriting the test case class
class PartATestCase(unittest.TestCase):
    results = ['', 'PART A TEST CASE RESULTS']
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
        with open('results_partA.txt', 'w') as f:
            for line in cls.results:
                f.write(line)
            f.write("\n-----------")
            f.write('\nTotal Credit: {:.2f}'.format(sum(cls.credit)))

    def run_test_with_params(self, params):
        errorMessage = ''
        accomplished = False
        try:
            cost = execute_student_plan(params['warehouse'], params['todo'])
            accomplished = True
        except Exception as e:
            errorMessage = repr(e)
            self.results.append(self.FAIL_TEMPLATE.format(message=errorMessage, **params))

        print accomplished, errorMessage
        self.assertTrue(accomplished, errorMessage)

        score = float(params['min_cost'])/float(cost)
        self.results.append(self.SCORE_TEMPLATE.format(cost=cost, score=score, **params))
        self.credit.append(score)

        return score

    @timeout(TIME_LIMIT)
    def test_case1(self):
        params = {
            'test_case': 1,
            'warehouse': ['1#2',
                          '.#.',
                          '..@'],
            'todo': ['1', '2'],
            'min_cost': 23,
         }
        score = self.run_test_with_params(params)
        print 'credit: {}'.format(score)

# Notice that we have included several extra test cases below.
# You can uncomment one or more of these for extra tests.
#
    # @timeout(TIME_LIMIT)
    # def test_case2(self):
    #     params = {
    #         'test_case': 2,
    #         'warehouse': ['@....1'],
    #         'todo': ['1'],
    #         'min_cost': 20,
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # @timeout(TIME_LIMIT)
    # def test_case3(self):
    #     params = {
    #         'test_case': 3,
    #         'warehouse': ['1.#@#.4',
    #                       '2#.#.#3'],
    #         'todo': ['1', '2', '3', '4'],
    #         'min_cost': 57,
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # *** CREDIT TO: Kowsalya Subramanian for adding this test case
    # @timeout(TIME_LIMIT)
    # def test_case4(self):
    #     params = {
    #         'test_case': 4,
    #         'warehouse': ['3#@',
    #                       '2#.',
    #                       '1..'],
    #         'todo': ['1', '2', '3'],
    #         'min_cost': 44,
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # *** CREDIT TO: Gideon Rossman for adding this test case
    # @timeout(TIME_LIMIT)
    # def test_case5(self):
    #     params = {
    #         'test_case': 5,
    #         'warehouse': ['..1.',
    #                       '..@.',
    #                       '....',
    #                       '2...'],
    #         'todo': ['1', '2'],
    #         'min_cost': 16,
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # *** CREDIT TO: venkatasatyanarayana kamisetti for adding this test case
    # @timeout(TIME_LIMIT)
    # def test_case6(self):
    #     params = {
    #         'test_case': 6,
    #         'warehouse': ['1..',
    #                       '...',
    #                       '@.2'],
    #         'todo': ['1', '2'],
    #         'min_cost': 16,
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # *** CREDIT TO: Dana Johnson for adding this test case
    # @timeout(TIME_LIMIT)
    # def test_case7(self):
    #     params = {
    #         'test_case': 7,
    #         'warehouse': ['#J######',
    #                       '#I#2345#',
    #                       '#H#1##6#',
    #                       '#G#0@#7#',
    #                       '#F####8#',
    #                       '#EDCBA9#',
    #                       '########'],
    #         'todo': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    #                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    #         'min_cost': 636.0,
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # *** CREDIT TO: Dana Johnson for adding this test case
    # @timeout(TIME_LIMIT)
    # def test_case8(self):
    #     params = {
    #         'test_case': 8,
    #         'warehouse': ['#######2',
    #                       '#......1',
    #                       '#@......'],
    #         'todo': ['1', '2'],
    #         'min_cost': 47.0,
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # @timeout(TIME_LIMIT)
    # def test_case9(self):
    #     params = {
    #         'test_case': 9,
    #         'warehouse': ['..#1..',
    #                       '......',
    #                       '..####',
    #                       '..#2.#',
    #                       '.....@'],
    #         'todo': ['1', '2'],
    #         'min_cost': 43.0
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)

    # # Test Case 10
    # @timeout(TIME_LIMIT)
    # def test_case10(self):
    #     params = {
    #         'test_case': 10,
    #         'warehouse': ['..#1..',
    #                       '#....#',
    #                       '..##.#',
    #                       '..#2.#',
    #                       '#....@'],
    #         'todo': ['1','2'],
    #         'min_cost': 30.0
    #     }
    #     score = self.run_test_with_params(params)
    #     print 'credit: {}'.format(score)
   
#Only run all of the test automatically if this file was executed from the command line. Otherwise, let Nose/py.test do it's own thing with the test cases. 
if __name__ == "__main__":
    all_suites = map(lambda x: unittest.TestLoader().loadTestsFromTestCase(x), [PartATestCase])
    all_tests = unittest.TestSuite(all_suites)
    unittest.TextTestRunner(verbosity=2).run(all_tests)
