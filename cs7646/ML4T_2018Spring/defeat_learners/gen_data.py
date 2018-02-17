"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    """
    Create a dataset (X and Y) that will work better for linear regression than decision trees

    To do this, create a Matrix and then construct Y such that it is a linear combination of features
    from X.
    """
    # Generating X
    np.random.seed(seed)
    num_rows = np.random.randint(low=10, high=1000)
    num_cols = np.random.randint(low=2, high=1000)
    X = np.random.normal(size=(num_rows, num_cols))
    error = np.random.normal(size=num_rows)

    Y = X[:, 0]
    for i in range(1, num_cols):
        coef = np.random.normal()
        Y = Y + coef * X[:, i]
    Y = Y + error  # Add a normal error term

    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)

    # Generating X
    num_rows = np.random.randint(low=10, high=1000)
    num_cols = np.random.randint(low=2, high=1000)
    X = np.random.normal(size=(num_rows, num_cols))
    error = np.random.normal(size=num_rows)

    # Generating Y using Decision Rules
    Y = np.array([])
    col_idx = np.random.randint(low=0, high=num_cols)
    slice_col = X[:, col_idx]
    col_mean = np.mean(slice_col)
    for i in range(num_rows):
        if(X[i, col_idx] < col_mean):
            Y = np.append(Y, 0.5 * col_mean)
        else:
            Y = np.append(Y, 2 * col_mean)

    return X, Y

def author():
    return 'vla6' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
