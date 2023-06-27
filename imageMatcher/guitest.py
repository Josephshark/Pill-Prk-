import os
import cv2 as cv
import sys

events = [i for i in dir(cv) if 'EVENT' in i]

print( events )
