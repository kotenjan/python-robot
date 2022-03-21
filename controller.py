import cv2
import execnet
import json
import numpy as np

from copy import copy
from PIL import Image
from time import sleep

from constants import *
from image_recognition import get_object_positions
from position_computation_genetic import rotations_to_position

def call_python_version(Version, Module, Function, ArgumentList):
    gw      = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec(
        """
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
        """ 
        % 
        (Module, Function)
    )
    channel.send(ArgumentList)
    return channel.receive()

def min_x_max(min_val, x, max_val):
    assert(min_val <= max_val)
    if x != min(max(min_val, x), max_val):
        print(f"Fixed from {x} to {min(max(min_val, x), max_val)}")
    return min(max(min_val, x), max_val)

def correct_rotations(hip_rotation, rotations):
    return [
        min_x_max(SHOULDER_PITCH_LO, rotations[0] + hip_rotation, SHOULDER_PITCH_HI),
        min_x_max(SHOULDER_ROLL_LO, rotations[1], SHOULDER_ROLL_HI),
        min_x_max(ELBOW_ROLL_LO, rotations[2], ELBOW_ROLL_HI),
        min_x_max(ELBOW_YAW_LO, rotations[3], ELBOW_YAW_HI),
        min_x_max(WRIST_YAW_LO, rotations[4], WRIST_YAW_HI),
    ]

def get_image():
    image = json.loads(call_python_version("2.7", "camera", "take_photo", [ROBOT_IP]))
    width = image[1]
    height = image[2]

    array = np.array(image[0], dtype=np.uint8).reshape((height, width, 3))
    array = cv2.cvtColor(array, cv2.COLOR_RGB2HSV)
    
    return array

def get_objects(absolute_head_pitch, z):
    image = get_image()
    positions = get_object_positions(image, absolute_head_pitch, z)
    return positions

def get_rotations_to_position(destination_position, relative_shoulder_position, current_arm_rotations, hip_rotation):
    accuracy, rotations = rotations_to_position(relative_shoulder_position, destination_position, current_arm_rotations, 1000, 30, 5)
    print(f'accuracy: {accuracy}')
    rotations = correct_rotations(hip_rotation, rotations)
    return rotations

def ints(current_rotations):
    return [int(x) for x in current_rotations]

def test(hip_rotation, table_height, object_height):

    current_rotations = [0, 0, 0, 0, 0]
    shoulder_position = json.loads(call_python_version("2.7", "positions", "get_shoulder_position", [ROBOT_IP]))
    camera_position = json.loads(call_python_version("2.7", "positions", "get_camera_position", [ROBOT_IP]))
    
    relative_shoulder_position = list(np.array(shoulder_position) - np.array(camera_position))
    z = (table_height + object_height) - camera_position[2]

    for x in range(100, 300, 50):
        for y in range(-100, 200, 50):
            current_obj = [x, y, z]
            print(f'current position: {current_obj}')
            current_rotations = get_rotations_to_position(current_obj, relative_shoulder_position, current_rotations, hip_rotation)
            relative_shoulder_position = json.loads(call_python_version("2.7", "positions", "set_arm", [ints(current_rotations), ROBOT_IP]))
            sleep(2)
            print(json.loads(call_python_version("2.7", "positions", "get_wrist_position", [ROBOT_IP])))

def build_tower(hip_rotation, head_rotation, table_height, object_height):
    current_rotations = [0, 0, 0, 0, 0]
    
    shoulder_position = json.loads(call_python_version("2.7", "positions", "get_shoulder_position", [ROBOT_IP]))
    camera_position = json.loads(call_python_version("2.7", "positions", "get_camera_position", [ROBOT_IP]))
    
    relative_shoulder_position = list(np.array(shoulder_position) - np.array(camera_position))
    z = camera_position[2] - (table_height + object_height)

    object_coords = get_objects(head_rotation + hip_rotation, z)

    if len(object_coords) == 0:
        return

    tower_pos = object_coords[-1]

    for current_obj in object_coords[:-1]:
        tower_pos[2] += object_height

        current_rotations = get_rotations_to_position(current_obj, relative_shoulder_position, current_rotations, hip_rotation)
        relative_shoulder_position = json.loads(call_python_version("2.7", "positions", "set_arm", [ints(current_rotations), ROBOT_IP]))
        sleep(2)
        call_python_version("2.7", "positions", "grab_object", [ROBOT_IP])

        raise_arm = copy(current_obj)
        raise_arm[2] = tower_pos[2] + object_height

        current_rotations = get_rotations_to_position(raise_arm, relative_shoulder_position, current_rotations, hip_rotation)
        relative_shoulder_position = json.loads(call_python_version("2.7", "positions", "set_arm", [ints(current_rotations), ROBOT_IP]))

        current_rotations = get_rotations_to_position(tower_pos, relative_shoulder_position, current_rotations, hip_rotation)
        relative_shoulder_position = json.loads(call_python_version("2.7", "positions", "set_arm", [ints(current_rotations), ROBOT_IP]))
        sleep(2)
        call_python_version("2.7", "positions", "release_object", [ROBOT_IP])

        raise_arm = copy(tower_pos)
        raise_arm[2] = tower_pos[2] + object_height

        current_rotations = get_rotations_to_position(raise_arm, relative_shoulder_position, current_rotations, hip_rotation)
        relative_shoulder_position = json.loads(call_python_version("2.7", "positions", "set_arm", [ints(current_rotations), ROBOT_IP]))

if __name__ == '__main__':
    head_rotation = -7
    hip_rotation = 25
    table_height = 743
    object_height = 40
    
    #test(hip_rotation, table_height, object_height)
    #call_python_version("2.7", "positions", "release_robot", [ROBOT_IP])
    build_tower(hip_rotation, head_rotation, table_height, object_height)
    
    #relative_shoulder_position = json.loads(call_python_version("2.7", "positions", "set_arm", [[115, 0, 0, 0, 0], ROBOT_IP]))