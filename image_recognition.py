from turtle import position
from PIL import Image
from sklearn.cluster import KMeans
import cv2
import json
import numpy as np
import math
from constants import *


def rad(angle):
    return math.radians(angle)

def create_kMeans_hsv_mask(img_arr):
    img_arr = img_arr[:, [1]]
    kmeans = KMeans(n_clusters = 2, random_state = 1).fit(img_arr)
    
    color_args = np.array(kmeans.labels_).astype(bool)
    
    if np.sum(color_args == 0) < np.sum(color_args == 1):
        color_args = np.invert(color_args)
    
    colors = np.array([0, 255]).astype(np.uint8)
    
    return colors[color_args.astype(np.uint8)]

def segment_objects(img):
    img_arr = np.array(img)
    x, y, z = img_arr.shape
    img_arr_flat = img_arr.reshape((x*y, z))
    mask = create_kMeans_hsv_mask(img_arr_flat)

    return mask.reshape((x, y))

def find_contours(img_bin, min_area=0, max_area=1000000, fill=True, external=True):
    mode = cv2.RETR_EXTERNAL
    if not external:
        mode = cv2.RETR_LIST
    contours, _  = cv2.findContours(img_bin, mode, cv2.CHAIN_APPROX_SIMPLE)
    contours =  [c for c in contours if cv2.contourArea(c) > min_area and cv2.contourArea(c) < max_area]
    return contours

def get_rotations(center, x, y, head_pitch):
    rot_x = 90 + ( ( 0.5 - center[1]/x ) * DEG_X - ( X_OFF + head_pitch) )
    rot_y = ( 0.5 - center[0]/y)
    return (rad(rot_x), rot_y)

def get_relative_positions(centers, x_abs, y_abs, z_abs, head_pitch):

    positions = list()

    for center in centers:
        rotations = get_rotations(center, x_abs, y_abs, head_pitch)
        x_rel = math.tan(rotations[0])*z_abs
        y_rel = (rotations[1])*300 # constant
        z_rel = -z_abs
        positions.append(np.array([x_rel + 60, y_rel + 60, z_rel]))

    return np.array(positions)

def get_centers(contours):
    
    contour_centers = list()
    
    for contour in contours:
        M = cv2.moments(contour)
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
        contour_centers.append((cX, cY))
    
    contour_centers.sort()

    return contour_centers

def get_object_positions(image_arr, head_pitch, z):
    x, y, _ = np.array(image_arr).shape
    mask = segment_objects(image_arr)
    contours = find_contours(mask, min_area=1000)
    centers = get_centers(contours)
    positions = get_relative_positions(centers, x, y, z, head_pitch)

    for position in positions:
        print(position)
    
    for position_a in positions:
        for position_b in positions:
            if (np.array(position_a) != np.array(position_b)).any():
                a = np.array(position_a) 
                b = np.array(position_b)
                c = a - b
                print(c)
                print((c[0]**2 + c[1]**2)**0.5)
    
    return positions

if __name__ == '__main__':
    with open('image_5_RGB.json', 'r') as infile:
        img = json.load(infile)
    width = img[1]
    height = img[2]
    image = np.array(img[0], dtype=np.uint8).reshape((height, width, 3))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    print(get_object_positions(image, 0, 60))
    