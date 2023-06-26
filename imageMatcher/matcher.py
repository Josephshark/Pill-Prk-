import os

import cv2 as cv
import sys


# Initialise folder directories
CWD = os.getcwd()
CURRENT_FOLDER = 'imageMatcher'
PHOTO_FOLDER_NAME = 'photos'
PHOTO_FOLDER_PATH = os.path.join(CWD,CURRENT_FOLDER,PHOTO_FOLDER_NAME)

# Initializes the array of working images 
photos = []
for photo in os.listdir(PHOTO_FOLDER_PATH):
    photos.append(photo)
    print(photo)

# Initialises an image array from the file
photo_path = os.path.join(PHOTO_FOLDER_PATH, photos[0])
img = cv.imread(photo_path)
if img is None:
 sys.exit("Could not read the image.")

# Initialises the GUI for displaying the images
GUI_WINDOW_NAME = 'Main Window'

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#cv.namedWindow(GUI_WINDOW_NAME)

cv.imshow(GUI_WINDOW_NAME, img)
cv.resizeWindow(GUI_WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

cv.waitKey(0)

cv.destroyAllWindows()
print("Finished")
