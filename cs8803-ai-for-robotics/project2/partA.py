"""
Author: Vincent La; GTech ID: vla6
"""
##########
# === Introduction ===
#
# In this problem, you will build a planner that helps a robot
#   find the best path through a warehouse filled with boxes
#   that it has to pick up and deliver to a dropzone.
# 
# Your file must be called `partA.py` and must have a class
#   called `DeliveryPlanner`.
# This class must have an `__init__` function that takes three 
#   arguments: `self`, `warehouse`, and `todo`.
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
# '.' (period) : traversable space. The robot may enter from any adjacent space.
# '#' (hash) : a wall. The robot cannot enter this space.
# '@' (dropzone): the starting point for the robot and the space where all boxes must be delivered.
#   The dropzone may be traversed like a '.' space.
# [0-9a-zA-Z] (any alphanumeric character) : a box. At most one of each alphanumeric character 
#   will be present in the warehouse (meaning there will be at most 62 boxes). A box may not
#   be traversed, but if the robot is adjacent to the box, the robot can pick up the box.
#   Once the box has been removed, the space functions as a '.' space.
# 
# For example, 
#   warehouse = ['1#2',
#                '.#.',
#                '..@']
#   is a 3x3 warehouse.
#   - The dropzone is at the warehouse cell in row 2, column 2.
#   - Box '1' is located in the warehouse cell in row 0, column 0.
#   - Box '2' is located in the warehouse cell in row 0, column 2.
#   - There are walls in the warehouse cells in row 0, column 1 and row 1, column 1.
#   - The remaining five warehouse cells contain empty space.
#
# The argument `todo` is a list of alphanumeric characters giving the order in which the 
#   boxes must be delivered to the dropzone. For example, if 
#   todo = ['1','2']
#   is given with the above example `warehouse`, then the robot must first deliver box '1'
#   to the dropzone, and then the robot must deliver box '2' to the dropzone.
#
# === Rules for Movement ===
#
# - Two spaces are considered adjacent if they share an edge or a corner.
# - The robot may move horizontally or vertically at a cost of 2 per move.
# - The robot may move diagonally at a cost of 3 per move.
# - The robot may not move outside the warehouse.
# - The warehouse does not "wrap" around.
# - As described earlier, the robot may pick up a box that is in an adjacent square.
# - The cost to pick up a box is 4, regardless of the direction the box is relative to the robot.
# - While holding a box, the robot may not pick up another box.
# - The robot may put a box down on an adjacent empty space ('.') or the dropzone ('@') at a cost
#   of 2 (regardless of the direction in which the robot puts down the box).
# - If a box is placed on the '@' space, it is considered delivered and is removed from the ware-
#   house.
# - The warehouse will be arranged so that it is always possible for the robot to move to the 
#   next box on the todo list without having to rearrange any other boxes.
#
# An illegal move will incur a cost of 100, and the robot will not move (the standard costs for a 
#   move will not be additionally incurred). Illegal moves include:
# - attempting to move to a nonadjacent, nonexistent, or occupied space
# - attempting to pick up a nonadjacent or nonexistent box
# - attempting to pick up a box while holding one already
# - attempting to put down a box on a nonadjacent, nonexistent, or occupied space
# - attempting to put down a box while not holding one
#
# === Output Specifications ===
#
# `plan_delivery` should return a LIST of moves that minimizes the total cost of completing
#   the task successfully.
# Each move should be a string formatted as follows:
#
# 'move {i} {j}', where '{i}' is replaced by the row-coordinate of the space the robot moves
#   to and '{j}' is replaced by the column-coordinate of the space the robot moves to
# 
# 'lift {x}', where '{x}' is replaced by the alphanumeric character of the box being picked up
#
# 'down {i} {j}', where '{i}' is replaced by the row-coordinate of the space the robot puts 
#   the box, and '{j}' is replaced by the column-coordinate of the space the robot puts the box
#
# For example, for the values of `warehouse` and `todo` given previously (reproduced below):
#   warehouse = ['1#2',
#                '.#.',
#                '..@']
#   todo = ['1','2']
# `plan_delivery` might return the following:
#   ['move 2 1',
#    'move 1 0',
#    'lift 1',
#    'move 2 1',
#    'down 2 2',
#    'move 1 2',
#    'lift 2',
#    'down 2 2']
#
# === Grading ===
# 
# - Your planner will be graded against a set of test cases, each equally weighted.
# - If your planner returns a list of moves of total cost that is K times the minimum cost of 
#   successfully completing the task, you will receive 1/K of the credit for that test case.
# - Otherwise, you will receive no credit for that test case. This could happen for one of several 
#   reasons including (but not necessarily limited to):
#   - plan_delivery's moves do not deliver the boxes in the correct order.
#   - plan_delivery's output is not a list of strings in the prescribed format.
#   - plan_delivery does not return an output within the prescribed time limit.
#   - Your code raises an exception.
#
# === Additional Info ===
# 
# - You may add additional classes and functions as needed provided they are all in the file `partA.py`.
# - Upload partA.py to Project 2 on T-Square in the Assignments section. Do not put it into an 
#   archive with other files.
# - Your partA.py file must not execute any code when imported.
# - Ask any questions about the directions or specifications on Piazza.
#

class DeliveryPlanner:

    # delta is a dictionary with keys as moves and values as costs
    # delta = {(-1, 0): 2,
    #          (0, -1): 2,
    #          (1, 0): 2,
    #          (0, 1): 2,
    #          (-1, -1): 3,
    #          (1, -1): 3,
    #          (-1, 1): 3,
    #          (1, 1): 3,
    #          }

    def __init__(self, warehouse, todo):
        """Initialize the Class"""
        # Create a Set of all the items in the warehouse
        # Then, remove items until only boxes remain
        items = {item for row in warehouse for item in row}
        items.discard('.')
        items.discard('#')
        items.discard('@')        

        self.warehouse = warehouse
        self.todo = todo
        self.boxes = items.copy()
        self.original_boxes = self.boxes.copy()

        # Futhermore, we define a list called "delta" which contains all possible moves.
        # Same as in: https://classroom.udacity.com/courses/cs373/lessons/48646841/concepts/486468390923
        self.delta = [(-1, 0),  # go up
                      (0, -1),  # go left
                      (1, 0),  # go down
                      (0, 1),  # go right
                      (-1, -1),  # go Up-Left
                      (1, -1),  # Go Down-Left
                      (-1, 1),  # Go Up Right
                      (1, 1),  # Go Down Right
                     ]

        print('HELLO')
        print(warehouse)
        print(self.original_boxes)
        print(self.boxes)

    #
    # DEFINING HELPER FUNCTIONS
    #
    def score_moves(self, move):
        """
        Score Movement. From Rules:

        - The robot may move horizontally or vertically at a cost of 2 per move.
        - The robot may move diagonally at a cost of 3 per move.
        """
        # If movement is up, down, left, or right, the movement coordinates abs value will sum to 1
        # If movement is diagonal, the movement coordinates will sum to 2
        # Since there are only up down left right or diagonal movement we can return 3 in all other cases.
        if abs(move[0] + move[1]) == 1:
            return 2
        else:
            return 3

    def check_adjacent(self, coord_1, coord_2):
        if coord_1 == coord_2:
            return False
        elif coord_1[0] in [coord_2[0] - 1, coord_2[0], coord_2[0] + 1] and \
                        coord_1[1] in [coord_2[1] - 1, coord_2[1], coord_2[1] + 1]:
            return True
        else:
            return False

    def get_location(self, item):
        """
        Finds the location of the item.

        In some cases there can be multiple locations. Return the first
        """
        locations = []
        for row in range(0, len(self.warehouse)):
            for column in range(len(self.warehouse[0])):
                if self.warehouse[row][column] == item:
                    locations.append((row, column))
                    return (row, column)

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
        num_rows_away = abs(current_location[0] - goal[0])
        num_cols_away = abs(current_location[1] - goal[1])
        heuristic = num_rows_away + num_cols_away
        return heuristic

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
        print('In Search Function')
        print(init)

        print('PRINTING GOAL')
        print(goal)
        if init == goal:
        #     print('ILLEGAL')
        #     print(init, goal)
            return init, ['move {} {}'.format(init[0], init[1])]
            # return init, ['illegal']

        ### All this code is from Udacity Lecture essentially
        closed = [[0 for row in range(len(self.warehouse[0]))] for col in range(len(self.warehouse))]
        closed[init[0]][init[1]] = 1
        action = [[-1 for row in range(len(self.warehouse[0]))] for col in range(len(self.warehouse))]

        x = init[0]
        y = init[1]
        g = 0
        current_location = (x, y)
        h = self.heuristic(current_location, goal)

        open = [[g, h, x, y]]

        found = False  # flag that is set when search is complete
        resign = False  # flag set if we can't find expand

        print("Line 271")
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

                print('line 284')
                if x == goal[0] and y == goal[1]:
                    print('in if statement')
                    print(found)
                    found = True
                    print('End of if')
                else:
                    print('line 288')
                    for i in range(len(self.delta)):
                        move = self.delta[i]
                        cost = self.score_moves(move)
                        x2 = x + move[0]
                        y2 = y + move[1]

                        print('line 294')
                        if x2 >= 0 and x2 < len(self.warehouse) and y2 >= 0 and y2 < len(self.warehouse[0]):
                            obstacles_and_boxes = ['#'] + list(self.boxes)
                            obstacles = ['#']
                            if closed[x2][y2] == 0 and self.warehouse[x2][y2] not in obstacles_and_boxes:
                            # if closed[x2][y2] == 0 and self.warehouse[x2][y2] not in obstacles:
                                g2 = g + cost
                                expanded_node = (x2, y2)
                                h2 = self.heuristic(expanded_node, goal)
                                open.append([g2, h2, x2, y2])
                                closed[x2][y2] = 1
                                action[x2][y2] = move
                    print('BEFORE BEFORE WHILE')
                    print(init == goal)
                    print('BEFORE WHILE')

        print('line 314')
        print('printing goal')
        print(goal)
        print('printing action')
        print(action)
        print(action[goal[0]][goal[1]])

        x = goal[0] - action[goal[0]][goal[1]][0]
        y = goal[1] - action[goal[0]][goal[1]][1]
        print('line 317')
        final_location = (x, y)
        
        print('printing final location')
        print(final_location)

        path = []
        while x != init[0] or y != init[1]:
            # As per format required by assignment
            path = ['move {x} {y}'.format(x=x, y=y)] + path
            x2 = x - action[x][y][0]
            y2 = y - action[x][y][1]
            x = x2
            y = y2

        return final_location, path

    # def handle_illegal(self, moves):
    #     if 'illegal' not in moves:
    #         return moves

    #     legal_move_list = []
    #     curr_loc = self.get_location('@')
    #     skip_flag = False
    #     for idx, move in enumerate(moves):
    #         if move != 'illegal' and skip_flag == False:
    #             legal_move_list.append(move)
    #             continue
    #         if skip_flag == True:
    #             skip_flag = False
    #         else:
    #             if (idx + 2 < len(moves) - 1) and ('move' in moves[idx + 2]):
    #                 moves[idx + 1], moves[idx + 2] = moves[idx + 2], moves[idx + 1]
    #             else:
    #                 for move in self.delta:
    #                     cost = self.score_moves(move)
    #                     x2 = curr_loc[0] + move[0]
    #                     y2 = curr_loc[1] + move[1]
    #                     # TODO: This is hacky
    #                     if 'lift' in moves[idx-1] and 'down' in moves[min(idx + 1, len(moves)-1)]:
    #                         try:
    #                             self.original_boxes.remove(moves[idx-1][-1])
    #                         except:
    #                             pass
    #                         if x2 >= 0 and x2 < len(self.warehouse) and y2 >= 0 and y2 < len(self.warehouse[0]) \
    #                                 and self.warehouse[y2][x2] not in ['#'] + list(self.original_boxes):
    #                             legal_move_list.append('move {} {}'.format(y2, x2))
    #                             legal_move_list.append(moves[min(idx + 1, len(moves)-1)])
    #                             legal_move_list.append('move {} {}'.format(curr_loc[0], curr_loc[1]))
    #                             skip_flag = True
    #                             break
    #                     else:
    #                         if (idx + 2 < len(moves) - 1):
    #                             req_adj = self.get_location(moves[idx + 2][-1])
    #                         else:
    #                             req_adj = (x2 + 1, y2)
    #                         if x2 >= 0 and x2 < len(self.warehouse) and y2 >= 0 and y2 < len(self.warehouse[0])\
    #                             and self.warehouse[x2][y2] != '#' and self.check_adjacent((x2, y2), req_adj):
    #                             legal_move_list.append('move {} {}'.format(x2, y2))
    #                             break
    #         if 'move' in move:
    #             curr_loc = (int(move[5]), int(move[7]))
    #     return legal_move_list

    def plan_delivery(self):
        """
        Final Function. Plan the Delivery using functions defined above.
        """
        moves = []

        # initializing the initial coordinates/end coordinates
        dropzone = self.get_location('@')
        final_location = dropzone

        # while to-do list exists
        while self.todo:
            next_todo = self.todo[0]
            print('next to do')
            print(next_todo)
            goal = self.get_location(next_todo)
            self.boxes.remove(next_todo)

            # Search Path To the next Goal
            final_location, next_move = self.search(final_location, goal)
            moves += next_move

            # Pick up Box
            moves += ['lift {}'.format(next_todo)]

            # Search Path to the Dropzone (which is the end goal)
            final_location, next_move = self.search(final_location, dropzone)
            moves += next_move

            # drop the item
            moves += ['down {} {}'.format(dropzone[0], dropzone[1])]

            # pop the first item from to-do list
            self.todo = self.todo[1:]
        # legal_moves = self.handle_illegal(moves)
        legal_moves = moves
        print(legal_moves)
        return legal_moves
