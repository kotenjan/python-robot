from constants import *
from matrices import *
import numpy as np
import math


def rad(angle):
    return math.radians(angle)


def yaw(angle):
    angle = rad(angle)
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0,              0, 1],
    ])


def get_elbow_matrix(rotations):
    R_0_1 = yaw(rotations[0]) @ B_0_1
    R_1_2 = yaw(rotations[1]) @ B_NORM_ELBOW
    return B @ R_0_1 @ R_1_2


def get_wrist_matrix(rotations):
    R_0_1 = yaw(rotations[0]) @ B_0_1
    R_1_2 = yaw(rotations[1]) @ B_1_2
    R_2_3 = yaw(ELBOW_PITCH) @ B_2_3
    R_3_4 = yaw(rotations[2])  @ B_3_4
    R_4_5 = yaw(rotations[3]) @ B_NORM_WRIST
    return B @ R_0_1 @ R_1_2 @ R_2_3 @ R_3_4 @ R_4_5


def get_palm_matrix(rotations):
    R_0_1 = yaw(rotations[0]) @ B_0_1
    R_1_2 = yaw(rotations[1]) @ B_1_2
    R_2_3 = yaw(ELBOW_PITCH) @ B_2_3
    R_3_4 = yaw(rotations[2]) @ B_3_4
    R_4_5 = yaw(rotations[3]) @ B_4_5
    R_5_6 = yaw(rotations[4]) @ B_NORM_PALM
    return B @ R_0_1 @ R_1_2 @ R_2_3 @ R_3_4 @ R_4_5 @ R_5_6


def get_relative_palm(rotations):
    V_top = np.array([
        HAND_OFFSET_X,
        0,
        0
    ])
    V = np.array([
        HAND_OFFSET_X,
        0,
        -HAND_OFFSET_Z
    ])
    R = get_palm_matrix(rotations)
    return R @ V_top, R @ V


def get_relative_wrist(rotations):
    V = np.array([
        LOWER_ARM_LENGTH,
        0,
        0
    ])
    R = get_wrist_matrix(rotations)
    return R @ V


def get_relative_elbow(rotations):
    V = np.array([
        UPPER_ARM_LENGTH,
        ELBOW_OFFSET_Y,
        0
    ])
    R = get_elbow_matrix(rotations)
    return R @ V


def get_relative_distance(position_start, position_dest, rotations):

    position_start = np.array(position_start)
    position_dest = np.array(position_dest)
    rotations = np.array(rotations)

    elbow_pos = get_relative_elbow(rotations)
    wrist_pos = get_relative_wrist(rotations)
    pos_top, pos = get_relative_palm(rotations)

    abs_pos_top = position_start + elbow_pos + wrist_pos + pos_top
    abs_pos = position_start + elbow_pos + wrist_pos + pos

    dist = np.linalg.norm(position_dest-abs_pos)

    return dist + 1 * (HAND_OFFSET_Z - (abs_pos_top[2] - abs_pos[2]))
