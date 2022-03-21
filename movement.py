# python 2

import motion
from naoqi import ALProxy


def stiffness_on(proxy):
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def wake_up(proxy):
    proxy.wakeUp()


def rest(proxy):
    proxy.rest()


def turn_off_balancer(proxy):
    isEnabled = False
    proxy.wbEnable(isEnabled)


def head_p(proxy, angle, pFractionMaxSpeed=0.5):
    angle = [angle]
    angle = [x * motion.TO_RAD for x in angle]
    proxy.angleInterpolationWithSpeed('HeadPitch', angle, pFractionMaxSpeed)


def hip_p(proxy, angle, pFractionMaxSpeed=0.5):
    angle = [-angle]
    angle = [x * motion.TO_RAD for x in angle]
    proxy.angleInterpolationWithSpeed('HipPitch', angle, pFractionMaxSpeed)


def shoulder_r(proxy, angle, pFractionMaxSpeed=0.5):
    angle = [angle]
    angle = [x * motion.TO_RAD for x in angle]
    proxy.angleInterpolationWithSpeed(
        'LShoulderRoll', angle, pFractionMaxSpeed)


def shoulder_p(proxy, angle, pFractionMaxSpeed=0.5):
    angle = [-angle]
    angle = [x * motion.TO_RAD for x in angle]
    proxy.angleInterpolationWithSpeed(
        'LShoulderPitch', angle, pFractionMaxSpeed)
    stiffness_on(proxy)


def elbow_y(proxy, angle, pFractionMaxSpeed=0.5):
    angle = [angle]
    angle = [x * motion.TO_RAD for x in angle]
    proxy.angleInterpolationWithSpeed('LElbowYaw', angle, pFractionMaxSpeed)


def elbow_r(proxy, angle, pFractionMaxSpeed=0.5):
    angle = [-angle]
    angle = [x * motion.TO_RAD for x in angle]
    proxy.angleInterpolationWithSpeed('LElbowRoll', angle, pFractionMaxSpeed)


def wrist_y(proxy, angle, pFractionMaxSpeed=0.5):
    angle = [angle]
    angle = [x * motion.TO_RAD for x in angle]
    proxy.angleInterpolationWithSpeed('LWristYaw', angle, pFractionMaxSpeed)


def grab(proxy, value, pFractionMaxSpeed=0.5):
    handName = "LHand"
    proxy.angleInterpolationWithSpeed(handName, value, pFractionMaxSpeed)


def hand_movement(proxy, rotations, pFractionMaxSpeed=0.5):
    rotations = [x * motion.TO_RAD for x in rotations]
    rotations[0] = -rotations[0]
    parts = ['LShoulderPitch', 'LShoulderRoll',
             'LElbowYaw', 'LElbowRoll', 'LWristYaw']
    proxy.angleInterpolationWithSpeed(parts, rotations, pFractionMaxSpeed)


def body_movement(proxy, rotations, pFractionMaxSpeed=0.5):
    rotations = [x * motion.TO_RAD for x in rotations]
    rotations[0] = -rotations[0]
    parts = ['HipPitch', 'HeadPitch', 'HeadYaw']
    proxy.angleInterpolationWithSpeed(parts, rotations + [0], pFractionMaxSpeed)


def autonomous(proxy, value):
    proxy.setAutonomousAbilityEnabled("AutonomousBlinking", value)
    proxy.setAutonomousAbilityEnabled("BackgroundMovement", value)
    proxy.setAutonomousAbilityEnabled("BasicAwareness", value)
    proxy.setAutonomousAbilityEnabled("ListeningMovement", value)
    proxy.setAutonomousAbilityEnabled("SpeakingMovement", value)


def get_proxy(robotIP):
    autonomousProxy = ALProxy("ALAutonomousLife", robotIP, 9559)
    motionProxy = ALProxy("ALMotion", robotIP, 9559)
    postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    return motionProxy, postureProxy, autonomousProxy


def get_position(proxy, name):
    frame = motion.FRAME_WORLD
    useSensorValues = True
    result = proxy.getPosition(name, frame, useSensorValues)
    return result
