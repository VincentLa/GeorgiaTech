#######################
# by James Peng (jpeng63)
# CS8803
#######################
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
PI = math.pi

# Taken from robot.py
def compute_distance(p, q):
    x1, y1 = p
    x2, y2 = q

    dx = x2 - x1
    dy = y2 - y1

    return math.sqrt(dx**2 + dy**2)


# Taken from robot.py
def compute_bearing(p, q):
    x1, y1 = p
    x2, y2 = q

    dx = x2 - x1
    dy = y2 - y1

    return math.atan2(dy, dx)


# Taken from robot.py
def truncate_angle(t):
    return ((t+PI) % (2*PI)) - PI


class DeliveryPlanner:

    # delta is a dictionary with keys as moves and values as costs
    delta = {(-1, 0): 1,
             (0, -1): 1,
             (1, 0): 1,
             (0, 1): 1,
             }

    def __init__(self, warehouse, todo, max_distance, max_steering):

        ######################################################################################
        # TODO: You may use this function for any initialization required for your planner
        ######################################################################################

        self.warehouse = warehouse
        self.todo = todo
        self.scale = 8
        self.max_distance = (max_distance - 0.01) * self.scale
        self.max_steering = max_steering - 0.01
        self.scaled_todo_set = set()
        for item in todo:
            self.scaled_todo_set.add((int(item[0] * self.scale), int(item[1] * self.scale)))

        self.discretize()

    def discretize(self):
        """
        returns scaled discrete version of the warehouse
        """
        # scaling
        self.scaled_todo = [(x[0] * self.scale, x[1] * self.scale) for x in self.todo]

        self.discrete_warehouse = []
        for str_map in self.warehouse:
            new_str = []
            for letter in str_map:
                new_str += [letter for i in range(self.scale)]
            self.discrete_warehouse += [new_str for j in range(self.scale)]

        for k in range(3):
            real_warehouse = [[ None for i in range(len(self.discrete_warehouse[0]))]for j in range(len(self.discrete_warehouse))]
            for i in range(len(self.discrete_warehouse)):
                for j in range(len(self.discrete_warehouse[0])):
                    if self.discrete_warehouse[min(i + 1, len(self.discrete_warehouse)-1)][j] == '#' or \
                                    self.discrete_warehouse[max(i - 1, 0)][j] == '#' or \
                                    self.discrete_warehouse[i][min(j + 1, len(self.discrete_warehouse[0])-1)] == '#' or \
                                    self.discrete_warehouse[i][max(j - 1, 0)] == '#' or \
                                    self.discrete_warehouse[max(i - 1, 0)][min(j + 1, len(self.discrete_warehouse[0])-1)] == '#' or \
                                    self.discrete_warehouse[max(i - 1, 0)][max(j - 1, 0)] == '#' or \
                                    self.discrete_warehouse[min(i + 1, len(self.discrete_warehouse)-1)][min(j + 1, len(self.discrete_warehouse[0])-1)] == '#' or \
                                    self.discrete_warehouse[min(i + 1, len(self.discrete_warehouse)-1)][max(j - 1, 0)] == '#' or \
                                    i + 1 > len(self.discrete_warehouse) - 1 or j + 1 > len(self.discrete_warehouse[0]) - 1 or \
                                    i - 1 < 0 or j - 1 < 0:
                            real_warehouse[i][j] = '#' if self.discrete_warehouse[i][j] != '@' else '@'
                    else:
                        real_warehouse[i][j] = self.discrete_warehouse[i][j]
            self.discrete_warehouse = real_warehouse

        self.discrete_warehouse = [''.join(sublist) for sublist in real_warehouse]

    def traverse(self, init, goal, cut_last = False):
        """ 
        finds the shortest path from the init to the goal and the location of the final spot
        """
        # structure of this code copied from Udacity lecture
        # https://classroom.udacity.com/courses/cs373/lessons/48646841/concepts/486468390923

        closed = {}
        action = {}

        x = init[0]
        y = init[1]
        g = 0
        h = self.heuristic((x,y), goal)

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
                    for move, cost in self.delta.iteritems():
                        x2 = x + move[0]
                        y2 = y + move[1]
                        #TODO: handle case where you go through box
                        if x2 >= 0 and x2 < len(self.discrete_warehouse[0]) and y2 <= 0 and y2 > -len(self.discrete_warehouse):
                            if closed.get((x2, y2),0) == 0 and self.discrete_warehouse[-y2][x2] != '#' and \
                                    (x2, y2) not in self.scaled_todo_set:
                                g2 = g + cost
                                h2 = self.heuristic((x2, y2), goal)
                                open.append([g2, h2, x2, y2])
                                closed[(x2,y2)] = 1
                                action[(x2,y2)] = move


        x = goal[0] - action[(goal[0],goal[1])][0]
        y = goal[1] - action[(goal[0],goal[1])][1]
        last_loc = (x, y)

        moves = []

        while x != init[0] or y != init[1]:
            if not (cut_last and compute_distance((x,y), goal) < 0.3 * self.scale):
                moves = [action[(x, y)]] + moves
            x2 = x - action[(x,y)][0]
            y2 = y - action[(x,y)][1]
            x = x2
            y = y2

        return last_loc, moves  # make sure you return the shortest path

    def find_coord(self, symbol):
        """
        returns the coordinates of either an item or the origin
        """
        coord = [(sublist.index(symbol), -sub_idx,0)
                for sub_idx, sublist
                in enumerate(self.discrete_warehouse) if symbol in sublist][0]
        return (coord[0] + self.scale/2, coord[1] - self.scale/2, 0)

    def heuristic(self, curr, goal):
        return abs(curr[0] - goal[0]) + abs(curr[1] - goal[1])

    def translate_move_list(self, moves, start):
        new_moves = []
        point = (start[0], start[1])
        bearing = start[2]
        for move in moves:
            new_point = (point[0] + move[0], point[1] + move[1])
            dist, steering = self.measure_distance_and_steering_to(point, new_point, bearing)
            bearing = truncate_angle(bearing + steering)
            point = new_point
            while abs(steering) > self.max_steering:
                new_moves.append('move {} {}'.format(self.max_steering if steering > 0 else -self.max_steering, 0))
                if steering > 0:
                    steering -= self.max_steering
                else:
                    steering += self.max_steering

            need_steering = True
            while dist > 0:
                dist_to_move = min(dist, self.max_distance)
                if need_steering:
                    new_moves.append('move {} {}'.format(steering, dist_to_move / float(self.scale) + 0.002))
                    need_steering = False
                else:
                    new_moves.append('move {} {}'.format(0, dist_to_move / float(self.scale) + 0.002))
                dist -= dist_to_move

        return new_moves, (point[0], point[1], bearing)

    def prune_steps(self, moves):
        pruned_moves = []
        prev_move = moves[0]
        new_move = moves[0]
        for idx, move in enumerate(moves[1:]):
            if move == prev_move:
                new_move = (move[0] + new_move[0], move[1] + new_move[1])
            else:
                pruned_moves.append(new_move)
                prev_move = move
                new_move = move
            if idx == len(moves) - 2:
                pruned_moves.append(new_move)
        return pruned_moves

    # copy and edited from robot.py
    def measure_distance_and_steering_to(self, start, point, init_bearing):
        """
        measures distance and bearing from one point to another 
        """
        distance_to_point = compute_distance(start, point)
        bearing_to_point = compute_bearing(start, point)

        steering = truncate_angle(bearing_to_point - init_bearing)

        return distance_to_point, steering

    def plan_delivery(self):
        """
        :returns moves
        """
        moves = []
        # initializing the initial coordinates/end coordinates
        base_loc = self.find_coord('@')
        last_loc = (base_loc[0], base_loc[1], 0)

        i = 0
        # while to-do list exists
        while self.todo:
            next_todo = self.todo[0]
            goal = (int(round(next_todo[0] * self.scale)), int(round(next_todo[1] * self.scale)))
            self.scaled_todo_set.remove(goal)

            # traverse to the item
            _, next_move = self.traverse(last_loc, goal, cut_last = True)
            new_moves, last_loc = self.translate_move_list(self.prune_steps(next_move), last_loc)
            moves += new_moves

            # pick up the item
            moves += ['lift {}'.format(i)]

            # traverse to the base
            _, next_move = self.traverse(last_loc, base_loc)
            new_moves, last_loc = self.translate_move_list(self.prune_steps(next_move), last_loc)
            moves += new_moves

            # drop the item
            moves += ['down {base_x} {base_y}'.format(base_x = base_loc[0] / float(self.scale), base_y = base_loc[1] / float(self.scale))]

            # pop the first item from to-do list
            self.todo = self.todo[1:]
            i += 1

        return moves