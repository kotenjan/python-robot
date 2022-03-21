# python 2

from naoqi import ALProxy
from constants import ROBOT_IP
import json
import numpy as np


def take_photo(robotIP):
    robotIP = str(robotIP)
    tts_video = ALProxy("ALVideoDevice", robotIP, 9559)
    cam_id = "subscribeID"
    
    CAMERA_TYPE = 1
    RESOLUTION = 2
    COLOR_RGB = 11
    FPS = 1

    cam_id = tts_video.subscribeCamera(cam_id, CAMERA_TYPE, RESOLUTION, COLOR_RGB, FPS)
    
    img = tts_video.getImageRemote(cam_id)
    image = np.frombuffer(img[6], dtype=np.uint8).tolist()
    image_width = img[0]
    image_height = img[1]
    try:
        tts_video.unsubscribe(cam_id)
    except:
        pass
    
    return json.dumps([image, image_width, image_height])


if __name__ == '__main__':
    take_photo(ROBOT_IP)
