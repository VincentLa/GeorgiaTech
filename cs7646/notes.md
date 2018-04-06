# Decision Trees
The basic setup of a DT are:

1. Factors: X1, X2, X3. These are your features/
2. Labels: Y
3. Nodes: each node has 4 parameters
    1. Factor Used: Which feature do you choose to split on
    2. Split Value: What is the split value
    3. Left Link: The Left Child
    4. Right Link: The Right Child
4. Root
5. Leaves 

# Q Learning
What is Q?
Q(s, a) = immediate reward + discounted reward (note Q is not greedy)

How to use Q?
pi(s) = argmax_a(Q[s, a]) -- The optimal policy given a state is the action that maximizes Q. 
