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


class DeliveryPlanner:

    def __init__(self, warehouse, todo, max_distance, max_steering):

        ######################################################################################
        # TODO: You may use this function for any initialization required for your planner  
        ######################################################################################

        pass

    def plan_delivery(self):

        # Sample of what a moves list should look like - replace with your planner results

        moves = ['move 1.570963 2.0',   # rotate and move north 2 spaces
                 'move 1.570963 0.1',   # rotate west and move closer to second box
                 'lift 1',              # lift the second box
                 'move 0.785398 1.5',   # rotate to sw and move down 1.5 squares
                 'down 3.5 -4.0',       # set the box out of the way
                 'move -0.785398 2.0',  # rotate to west and move 2.5 squares
                 'move -1.570963 2.7',  # rotate to north and move to pick up box 0
                 'lift 0',              # lift the first box
                 'move -1.570963 0.0',  # rotate to the south east
                 'move -0.785398 1.0',  # finish rotation
                 'move 0.785398 2.5',   # rotate to east and move
                 'move -1.570963 2.5',  # rotate and move south
                 'down 4.5 -4.5',       # set down the box in the dropzone
                 'move -1.570963 0.6',  # rotate to west and move towards box 1
                 'lift 1',              # lift the second box
                 'move 1.570963 0.0',   # rotate north
                 'move 1.570963 0.6',   # rotate east and move back towards dropzone
                 'down 4.5 -4.5']       # deliver second box

        return moves
