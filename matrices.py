import numpy as np

# transformation matrices
B = np.array([
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
])
B_0_1 = np.array([
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
])
B_NORM_ELBOW = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])
B_1_2 = np.array([
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
])
B_2_3 = np.array([
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
])
B_3_4 = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
])
B_NORM_WRIST = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])
B_4_5 = np.array([
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0],
])
B_NORM_PALM = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
])
