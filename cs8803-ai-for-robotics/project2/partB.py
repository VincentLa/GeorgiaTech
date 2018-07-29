"""
Author: Vincent La; GTech ID: vla6
"""
#
# === Introduction ===
#
# In this problem, you will again build a planner that helps a robot
#   find the best path through a warehouse filled with boxes
#   that it has to pick up and deliver to a dropzone. Unlike Part A,
#   however, in this problem the robot is moving in a continuous world
#   (albeit in discrete time steps) and has constraints on the amount
#   it can turn its wheels in a given time step.
#
# Your file must be called `partB.py` and must have a class
#   called `DeliveryPlanner`.
# This class must have an `__init__` function that takes five
#   arguments: `self`, `warehouse`, `todo`, `max_distance`, and
#   `max_steering`.
# The class must also have a function called `plan_delivery` that
#   takes a single argument, `self`.
#
# === Input Specifications ===
#
# `warehouse` will be a list of m strings, each with n characters,
#   corresponding to the layout of the warehouse. The warehouse is an
#   m x n grid. warehouse[i][j] corresponds to the spot in the ith row
#   and jth column of the warehouse, where the 0th row is the northern
#   end of the warehouse and the 0th column is the western end.
#
# The characters in each string will be one of the following:
#
# '.' (period) : traversable space.
# '#' (hash) : a wall. If the robot contacts a wall space, it will crash.
# '@' (dropzone): the space where all boxes must be delivered. The dropzone may be traversed like
#   a '.' space.
#
# Each space is a 1 x 1 block. The upper-left corner of space warehouse[i][j] is at the point (j,-i) in
#   the plane. Spaces outside the warehouse are considered walls; if any part of the robot leaves the
#   warehouse, it will be considered to have crashed into the exterior wall of the warehouse.
#
# For example,
#   warehouse = ['.#.',
#                '.#.',
#                '..@']
#   is a 3x3 warehouse. The dropzone is at space (2,-2) and there are walls at spaces (1,0)
#   and (1,-1). The rest of the warehouse is empty space.
#
# The robot is a circle of radius 0.25. The robot begins centered in the dropzone space.
#   The robot's initial bearing is 0.
#
# The argument `todo` is a list of points representing the center point of each box.
#   todo[0] is the first box which must be delivered, followed by todo[1], and so on.
#   Each box is a square of size 0.2 x 0.2. If the robot contacts a box, it will crash.
#
# The arguments `max_distance` and `max_steering` are parameters constraining the movement
#   of the robot on a given time step. They are described more below.
#
# === Rules for Movement ===
#
# - The robot may move any distance between 0 and `max_distance` per time step.
# - The robot may set its steering angle anywhere between -`max_steering` and
#   `max_steering` per time step. A steering angle of 0 means that the robot will
#   move according to its current bearing. A positive angle means the robot will
#   turn counterclockwise by `steering_angle` radians; a negative steering_angle
#   means the robot will turn clockwise by abs(steering_angle) radians.
# - Upon a movement, the robot will change its steering angle instantaneously to the
#   amount indicated by the move, and then it will move a distance in a straight line in its
#   new bearing according to the amount indicated move.
# - The cost per move is 1 plus the amount of distance traversed by the robot on that move.
#
# - The robot may pick up a box whose center point is within 0.5 units of the robot's center point.
# - If the robot picks up a box, it incurs a total cost of 2 for that move (this already includes
#   the 1-per-move cost incurred by the robot).
# - While holding a box, the robot may not pick up another box.
# - The robot may put a box down at a total cost of 1.5 for that move. The box must be placed so that:
#   - The box is not contacting any walls, the exterior of the warehouse, any other boxes, or the robot
#   - The box's center point is within 0.5 units of the robot's center point
# - A box is always oriented so that two of its edges are horizontal and the other two are vertical.
# - If a box is placed entirely within the '@' space, it is considered delivered and is removed from the
#   warehouse.
# - The warehouse will be arranged so that it is always possible for the robot to move to the
#   next box on the todo list without having to rearrange any other boxes.
#
# - If the robot crashes, it will stop moving and incur a cost of 100*distance, where distance
#   is the length it attempted to move that move. (The regular movement cost will not apply.)
# - If an illegal move is attempted, the robot will not move, but the standard cost will be incurred.
#   Illegal moves include (but are not necessarily limited to):
#     - picking up a box that doesn't exist or is too far away
#     - picking up a box while already holding one
#     - putting down a box too far away or so that it's touching a wall, the warehouse exterior,
#       another box, or the robot
#     - putting down a box while not holding a box
#
# === Output Specifications ===
#
# `plan_delivery` should return a LIST of strings, each in one of the following formats.
#
# 'move {steering} {distance}', where '{steering}' is a floating-point number between
#   -`max_steering` and `max_steering` (inclusive) and '{distance}' is a floating-point
#   number between 0 and `max_distance`
#
# 'lift {b}', where '{b}' is replaced by the index in the list `todo` of the box being picked up
#   (so if you intend to lift box 0, you would return the string 'lift 0')
#
# 'down {x} {y}', where '{x}' is replaced by the x-coordinate of the center point of where the box
#   will be placed and where '{y}' is replaced by the y-coordinate of that center point
#   (for example, 'down 1.5 -2.9' means to place the box held by the robot so that its center point
#   is (1.5,-2.9)).
#
# === Grading ===
#
# - Your planner will be graded against a set of test cases, each equally weighted.
# - Each task will have a "baseline" cost. If your set of moves results in the task being completed
#   with a total cost of K times the baseline cost, you will receive 1/K of the credit for the
#   test case. (Note that if K < 1, this means you earn extra credit!)
# - Otherwise, you will receive no credit for that test case. This could happen for one of several
#   reasons including (but not necessarily limited to):
#   - plan_delivery's moves do not deliver the boxes in the correct order.
#   - plan_delivery's output is not a list of strings in the prescribed format.
#   - plan_delivery does not return an output within the prescribed time limit.
#   - Your code raises an exception.
#
# === Additional Info ===
#
# - You may add additional classes and functions as needed provided they are all in the file `partB.py`.
# - Your partB.py file must not execute any code when it is imported.
# - Upload partB.py to Project 2 on T-Square in the Assignments section. Do not put it into an
#   archive with other files.
# - Ask any questions about the directions or specifications on Piazza.
#

import math
import operator

## IMPORTED FROM ROBOT.py
PI = math.pi

def compute_distance(p, q):
    x1, y1 = p
    x2, y2 = q

    dx = x2 - x1
    dy = y2 - y1

    return math.sqrt(dx**2 + dy**2)

def compute_bearing(p, q):
    x1, y1 = p
    x2, y2 = q

    dx = x2 - x1
    dy = y2 - y1

    return math.atan2(dy, dx)


def truncate_angle(t):
    return ((t+PI) % (2*PI)) - PI

def measure_distance_and_steering_to(start, point, init_bearing):
    """
    measures distance and bearing from one point to another 
    """
    distance_to_point = compute_distance(start, point)
    bearing_to_point = compute_bearing(start, point)

    steering = truncate_angle(bearing_to_point - init_bearing)

    return distance_to_point, steering

def check_sign(x):
    """Returns the sign of a number"""
    return x / abs(x)

class DeliveryPlanner:

    def __init__(self, warehouse, todo, max_distance, max_steering):
        """Initialize the class"""
        self.warehouse = warehouse
        self.todo = todo

        # In discretizing the warehouse, scaling each cell by 8x8
        self.scale = 8

        # Add some fake constants to make it so robot doesn't crash into box.
        self.max_distance = (max_distance - 0.02) * self.scale
        self.max_steering = max_steering - 0.02

        # Scale the boxes appropriately as well
        self.boxes_scaled = set([(self.scale * box[0], self.scale * box[1]) for box in self.todo])

        # Futhermore, we define a list called "delta" which contains all possible moves.
        # Same as in: https://classroom.udacity.com/courses/cs373/lessons/48646841/concepts/486468390923
        self.delta = [(-1, 0),  # go up
                      (0, -1),  # go left
                      (1, 0),  # go down
                      (0, 1),  # go right
                     ]

        # Finally, discretize the warehouse (based on hints in https://piazza.com/class/jh0tfongvk362a?cid=427)
        self.create_discrete_warehouse()

    def _check_adjacent_cells(self, warehouse, row, column, value):
        """
        Helper Function to check adjacent cells for a wall.

        Keyword Args:
            warehouse: The warehouse in consideration
            row: The current row in warehouse to find adjacent cells
            columns: The current column in warehouse in consideration
            value: The value to check adjacent cells against. If not None will check if
                   any adjacent cells contains that value
        """
        adjacent_cells = []
        warehouse_cols = len(warehouse[0])
        warehouse_rows = len(warehouse)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    new_row = max(min(row + i, warehouse_rows - 1), 0)
                    new_col = max(min(column + j, warehouse_cols - 1), 0)
                    adjacent_cells.append(warehouse[new_row][new_col])

        truths = 0
        if value:
            for adjacent_cell in adjacent_cells:
                if adjacent_cell == value:
                    return True
            return False
        else:
            return False

    def create_discrete_warehouse(self):
        """
        Based on hints in https://piazza.com/class/jh0tfongvk362a?cid=427, discretize the Warehouse
        """
        # In the first step to discrete the warehouse, simply blow up each cell to 8x8 version of it.
        self.discrete_warehouse = []
        for row in self.warehouse:
            new_items = []
            for item in row:
                new_items += [item for i in range(self.scale)]
            self.discrete_warehouse += [new_items for j in range(self.scale)]

        number_of_iterations = 3
        for iteration in range(number_of_iterations):
            discrete_warehouse_cols = len(self.discrete_warehouse[0])
            discrete_warehouse_rows = len(self.discrete_warehouse)
            new_warehouse = [[ None for i in range(discrete_warehouse_cols)] for j in range(discrete_warehouse_rows)]
            for i in range(discrete_warehouse_rows):
                for j in range(discrete_warehouse_cols):
                    if self._check_adjacent_cells(self.discrete_warehouse, i, j, '#'):
                        """If any adjacent cell is a wall, make this cell also a wall, unless it's a dropzone"""
                        if self.discrete_warehouse[i][j] != '@':
                            new_warehouse[i][j] = '#'
                        else:
                            new_warehouse[i][j] = '@'
                    else:
                        """Else; just keep the original value of discrete warehouse"""
                        new_warehouse[i][j] = self.discrete_warehouse[i][j]
            self.discrete_warehouse = new_warehouse

        # Collapse 2-day array back to single array with each element as a string.
        self.discrete_warehouse = [''.join(row) for row in new_warehouse]

    def get_location(self, item):
        """
        Finds the location of the item.

        In cases where there are multiple locations. Return the first. This is similar
        to function I wrote in Part A
        """
        for row in range(0, len(self.discrete_warehouse)):
            for column in range(len(self.discrete_warehouse[0])):
                if self.discrete_warehouse[row][column][0] == item:
                    return (column + self.scale / 2, -1 * row - self.scale / 2, 0)

    def heuristic(self, current_location, goal):
        """
        Define a Heuristic for the A* Algorithm

        The Heuristic needs to be admissable. That is, the estimated cost must always be lower
        than or equal to the actual cost of reaching the goal state. In this case, we simply calculate
        the number of rows and columns that we are currently away from the goal. This is admissable 
        since we know there are # barriers that we may not be able to pass through.

        The Heuristic being defined as the number of steps to the goal is consistent with the heuristic
        defined in https://classroom.udacity.com/courses/cs373/lessons/48646841/concepts/487510240923.
        """
        num_rows_away = abs(goal[0] - current_location[0])
        num_cols_away = abs(goal[1] - current_location[1])
        heuristic = num_rows_away + num_cols_away
        return heuristic

    def collapse_moves(self, moves):
        """
        Define Helper Function.

        Collapse Moves Vector so that if you're always moving in the same direction,
        collapse into single command
        """
        actual_moves_vector = []
        actual_move = moves[0]
        for i in range(1, len(moves) - 1):
            current_move = moves[i]
            previous_move = moves[i - 1]
            if current_move == previous_move:
                actual_move = tuple(map(operator.add, current_move, actual_move))
            else:
                actual_moves_vector.append(actual_move)
                actual_move = current_move
        actual_moves_vector.append(actual_move)
        return actual_moves_vector

    def _correct_submovement(self, movement_param_label, movement_param, max_param):
        """
        Helper Function for correct_moves

        There are limits to how much we can steer and how much we can move per turn.
        This is a helper function to break down actual moves into legal steps

        Keyword Args:
            movement_param_label: Either 'distance' or 'steering'
            movement_param: Either distance or steering value
            max_param: Either max distance or max steering
        """
        actual_moves = []
        while abs(movement_param) > max_param:
            if movement_param_label == 'steering':
                actual_moves.append('move {} {}'.format(max_param if movement_param > 0 else -max_param, 0))
            if movement_param_label == 'distance':
                actual_moves.append('move {} {}'.format(0, max_param / float(self.scale)))
            movement_param -= check_sign(movement_param) * max_param
        return actual_moves, movement_param

    def correct_moves(self, moves, previous_location):
        """
        Correct Moves returned by Algorithm.

        At this point, we've discretized the warehouse, and we've also implemented A* over this
        warehouse. The previous functions, search and return to us the correct
        set of rules assuming our max steering and max distance were infinite. However,
        we are constrained by max steering and max distance parameters. Thus, we have to
        implement a correction if we go over the max steering and max distance.

        Keyword Args:
            moves: List of Moves
            previous_location: Last Previous Location to start from; (x, y, direction)
        """
        actual_moves = []
        point, direction = (previous_location[0], previous_location[1]), previous_location[2]
        for move in moves:
            new_point = tuple(map(operator.add, point, move))
            distance_to_new_point, steering = measure_distance_and_steering_to(point, new_point, direction)
            direction = truncate_angle(direction + steering)

            new_actual_moves, steering = self._correct_submovement('steering', steering, self.max_steering)
            actual_moves += new_actual_moves

            # There's one more steering we have to do that is less than max steering
            actual_moves.append('move {} {}'.format(steering, 0))

            new_actual_moves, distance_to_new_point = self._correct_submovement('distance', distance_to_new_point, self.max_distance)
            actual_moves += new_actual_moves

            # There's one more distance we have to do that is less than max distance
            actual_moves.append('move {} {}'.format(0, distance_to_new_point / float(self.scale)))

            point = new_point
        return actual_moves, (new_point[0], new_point[1], direction)

    def search(self, init, goal):
        """
        Use A* to Search the Warehouse and find the path to the goal.

        Note that a lot of the search code comes from the A* Lecture in Udacity.
        (https://classroom.udacity.com/courses/cs373/lessons/48646841/concepts/487510240923)
        
        Keyword Args:
            init: Initial Location
            goal: Goal Location

        Returns:
            search will return the shortest path from init to goal
        """
        ### All this code is from Udacity Lecture essentially to implement A*        
        closed = [[0 for col in range(len(self.discrete_warehouse))] for row in range(len(self.discrete_warehouse[0]))]
        action = [[-1 for col in range(len(self.discrete_warehouse))] for row in range(len(self.discrete_warehouse[0]))]

        x = init[0]
        y = init[1]
        g = 0
        current_location = (x, y)
        h = self.heuristic(current_location, goal)

        open = [[g, h, x, y]]

        found = False  # flag that is set when search is complete
        resign = False  # flag set if we can't find expand

        while not found and not resign:
            if len(open) == 0:
                resign = True
                return 'fail'
            else:
                open.sort()
                open.reverse()
                next = open.pop()
                x = next[2]
                y = next[3]
                g = next[0]

                if x == goal[0] and y == goal[1]:
                    found = True
                else:
                    for i in range(len(self.delta)):
                        move = self.delta[i]
                        cost = 1
                        x2 = x + move[0]
                        y2 = y + move[1]

                        if x2 >= 0 and x2 < len(self.discrete_warehouse[0]) and y2 <= 0 and y2 > -len(self.discrete_warehouse):
                            if closed[x2][y2] == 0 and self.discrete_warehouse[-y2][x2] != '#' and (x2, y2) not in self.boxes_scaled:
                                g2 = g + cost
                                expanded_node = (x2, y2)
                                h2 = self.heuristic(expanded_node, goal)
                                open.append([g2, h2, x2, y2])
                                closed[x2][y2] = 1
                                action[x2][y2] = move

        if len(goal) == 3:
            action_goal = (action[goal[0]][goal[1]][0], action[goal[0]][goal[1]][1], 0)
        else:
            action_goal = (action[goal[0]][goal[1]][0], action[goal[0]][goal[1]][1])
        final_location = tuple(map(operator.sub, goal, action_goal))

        path = []
        while (x, y) != (init[0], init[1]):
            if compute_distance((x, y), (goal[0], goal[1])) >= .15 * self.scale:
                """
                If you get within sufficiently close to the goal then stop

                We don't want to go all the way to the goal or else you will hit it and crash
                """
                action_list = [action[x][y]]
                path = action_list + path
            x2 = x - action[x][y][0]
            y2 = y - action[x][y][1]
            x = x2
            y = y2

        return final_location, path

    def plan_delivery(self):
        """
        Final Function. Plan the Delivery using functions defined above.
        """
        moves = []
        dropzone = self.get_location('@')

        # Initialize first location to the drop zone since this is where we start
        previous_location = (dropzone[0], dropzone[1], 0)

        box_index = 0
        while self.todo:
            """
            At this point, the remaining steps are straightforward.

            If there are boxes remaining in the to-do list:

            1. Find the location of the next box
            2. Search the path to the next box
            3. Pick up the box
            4. Search Path to the Dropzone
            5. Return Box to the Dropzone
            6. Remove box from the list of to do's
            7. Repeat until To do list is empty
            """
            # 1. Find the location of the next box
            next_box = self.todo[0]
            next_box_location = (int(next_box[0] * self.scale), int(next_box[1] * self.scale))
            self.boxes_scaled.remove(next_box_location)

            # 2. Search the path to the next box
            last_location, next_move = self.search(previous_location, next_box_location)
            new_moves, previous_location = self.correct_moves(self.collapse_moves(next_move), previous_location)
            moves += new_moves

            # 3. Pick up the box
            moves += ['lift {}'.format(box_index)]

            # 4. Search Path to the Dropzone
            last_location, next_move = self.search(previous_location, dropzone)
            new_moves, previous_location = self.correct_moves(self.collapse_moves(next_move), previous_location)
            moves += new_moves

            # 5. Return Box to the Dropzone
            moves += ['down {} {}'.format(dropzone[0] / float(self.scale), dropzone[1] / float(self.scale))]

            # 6. Remove box from the list of to do's
            self.todo = self.todo[1:]
            box_index = box_index + 1

        return moves
