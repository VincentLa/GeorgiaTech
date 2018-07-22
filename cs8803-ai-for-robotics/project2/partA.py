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

###
### DEFINING HELPER FUNCTIONS
###
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

    def get_location(self, item):
        """
        Finds the location of the item.

        In cases where there are multiple locations. Return the first
        """
        for row in range(0, len(self.warehouse)):
            for column in range(len(self.warehouse[0])):
                if self.warehouse[row][column] == item:
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
        num_rows_away = abs(goal[0] - current_location[0])
        num_cols_away = abs(goal[1] - current_location[1])
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
        if init == goal:
            # If trying to take in action in the already occupied space, this is an illegal move.
            # Implement a hack-around fix to move to the next adjacent unoccupied space
            for i in range(len(self.delta)):
                move = self.delta[i]
                x2 = init[0] + move[0]
                y2 = init[1] + move[1]

                # Locations of Obstacles and Boxes
                obstacles_and_boxes = ['#'] + list(self.boxes)

                # If (x2, y2) still within limits of the warehouse and the space is not an obstacle or existing box
                if x2 >= 0 and x2 < len(self.warehouse) and y2 >= 0 and y2 < len(self.warehouse[0]) and self.warehouse[x2][y2] not in obstacles_and_boxes:
                    return (x2, y2), ['move {} {}'.format(x2, y2)]

        ### All this code is from Udacity Lecture essentially to implement A*
        closed = [[0 for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]
        closed[init[0]][init[1]] = 1
        
        action = [[-1 for col in range(len(self.warehouse[0]))] for row in range(len(self.warehouse))]

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
                        cost = self.score_moves(move)
                        x2 = x + move[0]
                        y2 = y + move[1]

                        if x2 >= 0 and x2 < len(self.warehouse) and y2 >= 0 and y2 < len(self.warehouse[0]):
                            # Note it is illegal to move into an existing box as well (until we pick it up)
                            # This works because in plan_delivery function, we pop self.boxes when we lift
                            obstacles_and_boxes = ['#'] + list(self.boxes)
                            if closed[x2][y2] == 0 and self.warehouse[x2][y2] not in obstacles_and_boxes:
                                g2 = g + cost
                                expanded_node = (x2, y2)
                                h2 = self.heuristic(expanded_node, goal)
                                open.append([g2, h2, x2, y2])
                                closed[x2][y2] = 1
                                action[x2][y2] = move

        x = goal[0] - action[goal[0]][goal[1]][0]
        y = goal[1] - action[goal[0]][goal[1]][1]
        final_location = (x, y)

        path = []
        while (x, y) != (init[0], init[1]):
            # As per format required by assignment
            path = ['move {x} {y}'.format(x=x, y=y)] + path
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
        previous_location = dropzone

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
            next_box_location = self.get_location(next_box)
            self.boxes.remove(next_box)

            # 2. Search the path to the next box
            previous_location, next_move = self.search(previous_location, next_box_location)
            moves += next_move

            # 3. Pick up the box
            moves += ['lift {}'.format(next_box)]

            # 4. Search Path to the Dropzone
            previous_location, next_move = self.search(previous_location, dropzone)
            moves += next_move

            # 5. Return Box to the Dropzone
            moves += ['down {} {}'.format(dropzone[0], dropzone[1])]

            # 6. Remove box from the list of to do's
            self.todo.remove(next_box)
        return moves
