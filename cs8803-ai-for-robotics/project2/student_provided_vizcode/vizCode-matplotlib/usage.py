

warehouse = ['#######.',
             '#.......',
             '#@......']
todo = [(7.5, -1.5),
        (7.5, -0.5)]

planner = DeliveryPlanner(warehouse, todo, 5., pi / 2. + 0.01)
moves = planner.plan_delivery()
drawWH(warehouse, todo, moves)
