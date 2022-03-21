# python 2

from movement import *
import numpy as np
import json


def prepare_for_movement(robotIP):
    robotIP = str(robotIP)
    mv_proxy, pos_proxy, aut_proxy = get_proxy(robotIP)
    wake_up(mv_proxy)
    stiffness_on(mv_proxy)
    turn_off_balancer(mv_proxy)
    pos_proxy.goToPosture("StandInit", 0.5)
    autonomous(aut_proxy, False)


def release_robot(robotIP):
    robotIP = str(robotIP)
    _, pos_proxy, aut_proxy = get_proxy(robotIP)
    pos_proxy.goToPosture("StandInit", 0.5)
    autonomous(aut_proxy, True)


def set_body(rotations, robotIP):
    robotIP = str(robotIP)
    mv_proxy, _, _ = get_proxy(robotIP)
    body_movement(mv_proxy, rotations)
    camera = np.array(get_position(mv_proxy, 'CameraBottom'))
    shoulder = np.array(get_position(mv_proxy, 'LShoulderRoll'))
    relative_shoulder_position = list((shoulder - camera)[:3]*1000)
    return json.dumps(relative_shoulder_position)


def set_arm(rotations, robotIP):
    robotIP = str(robotIP)
    mv_proxy, _, _ = get_proxy(robotIP)
    hand_movement(mv_proxy, rotations)
    camera = np.array(get_position(mv_proxy, 'CameraBottom'))
    shoulder = np.array(get_position(mv_proxy, 'LShoulderRoll'))
    relative_shoulder_position = list((shoulder - camera)[:3]*1000)
    return json.dumps(relative_shoulder_position)

def get_camera_position(robotIP):
    robotIP = str(robotIP)
    mv_proxy, _, _ = get_proxy(robotIP)
    camera = np.array(get_position(mv_proxy, 'CameraBottom'))
    camera = list((camera)[:3]*1000)
    return json.dumps(camera)

def get_shoulder_position(robotIP):
    robotIP = str(robotIP)
    mv_proxy, _, _ = get_proxy(robotIP)
    camera = np.array(get_position(mv_proxy, 'LShoulderRoll'))
    camera = list((camera)[:3]*1000)
    return json.dumps(camera)

def get_wrist_position(robotIP):
    robotIP = str(robotIP)
    mv_proxy, _, _ = get_proxy(robotIP)
    camera = np.array(get_position(mv_proxy, 'LWristYaw'))
    camera = list((camera)[:3]*1000)
    return json.dumps(camera)

def grab_object(robotIP):
    robotIP = str(robotIP)
    mv_proxy, _, _ = get_proxy(robotIP)
    grab(mv_proxy, 0)


def release_object(robotIP):
    robotIP = str(robotIP)
    mv_proxy, _, _ = get_proxy(robotIP)
    grab(mv_proxy, 1)
