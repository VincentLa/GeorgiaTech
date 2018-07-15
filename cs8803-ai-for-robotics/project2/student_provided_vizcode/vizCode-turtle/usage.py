warehouse = ['.1.....2',
             '..##....',
             '....##..',
             '......#3',
             '.......@']



pt = centered((4,7))
robot = robot.Robot(pt[1], pt[0], np.pi)
tbot = drawwarehouse(warehouse,robot)
turtle.done()
