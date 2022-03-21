# we're not using this code - this robot will never play any boardgame; not possible


import numpy as np
from matplotlib import pyplot as plt

import cv2

def read_file_x_json():
	for filename in (f"file_{i}.json" for i in range(1, 6)):
		with open(filename, "r", encoding='utf-16') as json_file:
			s = json_file.read()
			a = eval(s)
			print(a)


def read_image_x_json():
	for filename in (f"image_{i}.json" for i in range(1, 2)):
		with open(filename, "r") as json_file:
			# 1280 width, 960 height, 3 channels
			data, width, height = eval(json_file.read())
			assert(min(data) >= 0 and max(data) <= 255)
			img = np.array(data).reshape(height, width, 3).astype(np.uint8)


			img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
			img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

			plt.imshow(img)
			plt.show()

			pattern = (3, 3)
			detect_chessboard(img, pattern)


def json_to_img_file(json_filename, img_filename):
	"""
	The images are in HSY, not HSV, so the outputs are not correct
	"""
	with open(json_filename, "r") as json_file:
		# 1280 width, 960 height, 3 channels
		data, width, height = eval(json_file.read())
		assert(min(data) >= 0 and max(data) <= 255)
		img = np.array(data).reshape(height, width, 3).astype(np.uint8)

		img = cv2.cvtColor(img, cv2.COLOR_HSY2RGB)
		cv2.imwrite(img_filename, img)
"""
for filename in (f"image_{i}" for i in range(1, 6)):
	print(f"{filename}.json -> {filename}.jpg")
	json_to_img_file(filename + ".json", filename + ".jpg")
"""

VALS = {
	"kalvodas_board_HSY": {
		"light_bright": (0, 0, 112),
		"max_bright": (256, 256, 256),
		"contour_area": 20_000,
	},
	"tondas_board_HSY": {
		"light_bright": (0, 0, 128),
		"max_bright": (256, 256, 256),
		"contour_area": 20_000,
	}
}


def json_detect(json_filename, vals):
	"""
	The images are in HSY, not HSV, so the outputs are not correct
	"""
	with open(json_filename, "r") as json_file:
		# 1280 width, 960 height, 3 channels
		data, width, height = eval(json_file.read())
		assert(min(data) >= 0 and max(data) <= 255)
		img = np.array(data).reshape(height, width, 3).astype(np.uint8)

		## segment on img
		mask = cv2.inRange(img, vals["light_bright"], vals["max_bright"])


		cv2.imshow("mask", mask)
		cv2.waitKey(0)
		# detect_chessboard(mask, (3, 3))
		contour_drawn, _, contours = find_contours(mask, vals["contour_area"], fill=False)

		cv2.imshow("contour_drawn", contour_drawn)
		cv2.waitKey(0)

		print("poly")
		all_points = approx_by_poly(contours, img.copy())

		print("merge")
		# src for merge
		# https://stackoverflow.com/questions/44501723/how-to-merge-contours-in-opencv
		list_of_pts = [] 
		for ctr in contours:
			list_of_pts += [pt[0] for pt in ctr]
		ctr = np.array(list_of_pts).reshape((-1,1,2)).astype(np.int32)
		ctr = cv2.convexHull(ctr)
#		print(ctr)
		approx_by_poly([ctr], img.copy(), 0.01)
		print("/merge")

		cv2.imshow(f"{len(contours)} contours", contour_drawn)
		cv2.waitKey(0)

def approx_by_poly(contours, img, eps_val = 0.1):
	all_points = []
	for cnt in contours:
		epsilon = eps_val*cv2.arcLength(cnt,True)
		approx = cv2.approxPolyDP(cnt, epsilon, True)

		draw_poly(approx, img)
		all_points.extend(approx)
	cv2.imshow("drawn polys",  img)
	cv2.waitKey(0)
	return np.array(all_points)

def draw_poly(points, img):
	for start_point, end_point in zip(points, np.append(points[1:], [points[0]], axis=0)):
		cv2.line(img, start_point[0], end_point[0], (255, 0, 255), 4)

def find_contours(img_bin, min_area=0, max_area=1000000, fill=True, external=True):
    '''Finds contours in binary image and filters them using their area. Then it draws binary image
    from filtered contours. It counts contours as well.
    
    Parameters
    ----------
    img_bin : numpy.ndarray
        Input binary image.
    min_area : int
        Size of contour that is used to filter all smaller contours out.
    max_area : int
        Size of contour that is used to filter all larger contours out.
    Returns
    -------
    contour_drawn : numpy.ndarray
        Output binary image with drawn filled filtered contours.
    count : int
        Number of found and filtered contours.
    contours : list
        Found contours.
    '''
    mode = cv2.RETR_EXTERNAL
    if not external:
        mode = cv2.RETR_LIST
    contours, _  = cv2.findContours(img_bin, mode, cv2.CHAIN_APPROX_SIMPLE)
    contours =  [c for c in contours if cv2.contourArea(c) > min_area and cv2.contourArea(c) < max_area]
    thick = cv2.FILLED
    if not fill: thick = 2
    contour_drawn = cv2.drawContours(np.zeros(img_bin.shape, dtype=np.uint8), contours, -1, color=(255, 0, 0), thickness=thick)
    return contour_drawn, len(contours), contours

def detect_chessboard(img, pattern):
	found, corners = cv2.findChessboardCorners(img, pattern)

	print("for pattern:", pattern, "corners:", corners)

	img_with_corners = cv2.drawChessboardCorners(img, pattern, corners, found)

	cv2.imshow("img_with_corners", img_with_corners)
	cv2.waitKey(0)

def print_all_colors():
	flags = sorted([i for i in dir(cv2) if i.startswith('COLOR_')])
	for f in flags:
		print(f)


for filename in ("image_hsy",):# (f"image_{i}" for i in range(1, 6)):
	print(f"{filename}.json")
	json_detect(filename + ".json", VALS["tondas_board_HSY"])
#	json_detect(filename + ".json", VALS["kalvodas_board_HSY"])


"""
# image width 4 height 2, chanels 3
a = [[
		1, 2, 3,	4, 5, 6,	7, 8, 9,	10, 11, 12,
		13, 14, 15,	16, 17, 18,	19, 20, 21,	22, 23, 24.
	]]
b = np.array(a)
# height, width, channels
print(b.reshape(2, 4, 3))
"""

# read_image_x_json()
"""
filename = "image_1.jpg"
img_rgb = cv2.imread(filename)
cv2.imshow(filename, img_rgb)
cv2.waitKey(0)
"""
# detect_chessboard(img, (3, 3))
