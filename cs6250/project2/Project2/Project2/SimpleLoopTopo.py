# Simple Single Loop Topology:
# 1 --- 2
# |     |
# |     |
# 3 --- 4

topo = { 1 : [2, 3], 
         2 : [1, 4],
         3 : [1, 4], 
         4 : [2, 3] }
