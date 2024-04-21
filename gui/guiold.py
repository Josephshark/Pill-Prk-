"""
Copyright <2024> <Joseph Bagheri>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
#! /lib/python3.9/site-packages
import PySimpleGUI as sg
import cv2
import numpy as np
import json
from timeit import default_timer
#import RPi.GPIO as GPIO
import time
import os

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT)
"""
takes in an img pointer and scale 
and returns the new scaled image
"""

CONFIG_FILE_NAME = "config.json"
CWD = os.getcwd()

CONFIG_FILE = os.path.join(CWD, "gui", CONFIG_FILE_NAME)

def resize_frame(img, scale):
    width = int(img.shape[1]*scale/100)
    height = int(img.shape[0]*scale/100)
    dim = (width, height)
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def save_color(color):
    # Convert img to hsv color space
    color = np.uint8([[[int(color[0]),int(color[1]), int(color[2])]]])
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    string = np.array2string(hsv, separator =',').replace('[[[','').replace(']]]','')
    tmp = string.split(",")
    out = []
    for i in range(len(tmp)):
        out.append(int(tmp[i]))
    configs[0]["color"] = out
    with open(CONFIG_FILE, "w") as outfile:
        json.dump(configs, outfile)

def color_from_file():
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    index = 0
    return configs[index]["color"]

def save_number(number):
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    
    configs[0]["number"] = number

    with open(CONFIG_FILE, "w") as outfile:
        json.dump(configs, outfile)

def load_number():
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    return configs[0]["number"]


def load_area():
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    
    return configs[0]["area"]

def save_area(area):
    with open(CONFIG_FILE) as f:
        configs = json.load(f)

    configs[0]["area"] = area

    with open(CONFIG_FILE, "w") as outfile:
        json.dump(configs, outfile)

def save_bounds(lower_bound, upper_bound):
    # Convert img to hsv color space
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    
    out = []
    for i in range(len(lower_bound)):
        out.append(int(lower_bound[i]))
    configs[0]["lower bound"] = out

    out = []
    for i in range(len(upper_bound)):
        out.append(int(upper_bound[i]))
    configs[0]["upper bound"] = out

    with open(CONFIG_FILE, "w") as outfile:
        json.dump(configs, outfile)
"""
bound_index: 0 for lower, 1 for upper
"""
def load_lower_bounds():
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    index = 0
    return configs[index]["lower bound"]

def load_upper_bounds():
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    index = 0
    return configs[index]["upper bound"]

# Draw a target for the pill
def draw_target(img, color = [0,0,255], radius=4):
    (h,w) = img.shape[:2]
    cv2.circle(img, (w//2,h//2),radius+2, (0,0,255), 2)
    cv2.circle(img, (w//2,h//2),radius, (int(color[0]),int(color[1]),int(color[2])), -1)
    

#Get the mean color of the 25 center pixels
def get_color(img):
    (h,w) = img.shape[:2]
    return img[h//2,w//2]

def save_time(time):
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    configs[0]["time"] = time

    with open(CONFIG_FILE, "w") as outfile:
        json.dump(configs, outfile)


def load_time():
    with open(CONFIG_FILE) as f:
        configs = json.load(f)
    return configs[0]["time"]
def calibrate():
    sg.theme("LightGreen")
    color = color_from_file()
    area = load_area()
    number = load_number()
    time = load_time()
    # Define the window layout
    image_viewer = [
        [sg.Text("OpenCV Demo", size=(60, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")]
    ]

    slider_list_column = [
        [
            sg.Radio("Color", "Radio", size=(10, 10), key="-COLOR-"),
            sg.Button("Save"),
        ],
        [
            sg.Radio("HSV", "Radio", size=(10, 1), key="-HSV-"), 
            sg.Button("Save hsv"),
            sg.Button("Load hsv")
        ],
        [
            sg.Text('Hue                ', key='-OUT H-', font=('Arial Bold', 10)),
            sg.Text('Value            ', key='-OUT S-', font=('Arial Bold', 10)),
            sg.Text('Saturation', key='-OUT V-', font=('Arial Bold', 10)),
        ],
        [
            sg.Slider(
                (0, 179),
                min(color[0]+10, 179),
                1,
                orientation="h",
                size=(10, 20),
                key="-UPPER H-",
            ),
            sg.Slider(
                (0, 255),
                min(color[1]+50,255),
                1,
                orientation="h",
                size=(10, 20),
                key="-UPPER S-",
            ),
            sg.Slider(
                (0, 255),
                min(color[2]+50,255),
                1,
                orientation="h",
                size=(10, 20),
                key="-UPPER V-",
            ),
        ],
        [
            sg.Slider(
                (0, 179),
                max(color[0]-10,0),
                1,
                orientation="h",
                size=(10, 20),
                key="-LOWER H-",
            ),
            sg.Slider(
                (0, 255),
                max(color[1]-50,0),
                1,
                orientation="h",
                size=(10, 20),
                key="-LOWER S-",
            ),
            sg.Slider(
                (0, 255),
                max(color[2]-50,0),
                1,
                orientation="h",
                size=(10, 20),
                key="-LOWER V-",
            ),
        ],
        [
            sg.Radio("Area", "Radio", size=(10, 10), key="-AREA-"),
            sg.Button("Save area"),
            sg.Button("Load area")
        ],
        [
            sg.Slider(
                (0, 1000),
                area,
                1,
                orientation="h",
                size=(20, 15),
                key="-AREA SLIDER-",
            ),
        ],
        [
            sg.Radio("Detect", "Radio", size=(10, 10), key="-DETECT-"),
            sg.Button("Save number"),
            sg.Button("Load number")
        ],
        [
            sg.Text('Number of Objects:', key='-OUT-', font=('Arial Bold', 6)),
            sg.Slider(
                        (0, 50),
                        number,
                        1,
                        orientation="h",
                        size=(20, 20),
                        key="-OBJECT SLIDER-",
                        ),    
        ],
        [
            sg.Button("Save delay"),
            sg.Button("Load delay"),           
            sg.Slider(
                        (0, 2),
                        number,
                        .1,
                        orientation="h",
                        size=(15, 15),
                        key="-TIME SLIDER-",
                        ),    
        ],
        [
            sg.Button("Reset", size=(10, 1)),
            sg.Button("Exit", size=(10, 1)),
        ],
    ]

    layout = [
        [
            sg.Column(image_viewer),
            sg.VSeperator(),
            sg.Column(slider_list_column),
        ]
    ]

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, size=(800,600), location=(0, 0))

    cap = cv2.VideoCapture(0)

    prev = [0,0]
    nex = [0,0]

    status = "ON"
    timer_started = False

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        ret, frame = cap.read()

        # If there are no more frames, break out of the loop
        if not ret:
            break

        # Initialize the contour
        objects = 0 

        if values["-COLOR-"]:
            color = get_color(frame)
            draw_target(frame, color)
            cv2.putText(frame, f"Color: {color}",(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if event == "Save":
                save_color(color)
                color = color_from_file()
                window["-UPPER H-"].update(min(color[0]+10, 179))
                window["-UPPER S-"].update(min(color[1]+50, 255))
                window["-UPPER V-"].update(min(color[2]+50, 255))
                window["-LOWER H-"].update(max(color[0]-10, 0))
                window["-LOWER S-"].update(max(color[1]-50, 0))
                window["-LOWER V-"].update(max(color[2]-50, 0))
        elif values["-HSV-"]:

            lower_bound = (values["-LOWER H-"],values["-LOWER S-"],values["-LOWER V-"])
            upper_bound = (values["-UPPER H-"],values["-UPPER S-"],values["-UPPER V-"])    
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame = cv2.inRange(hsv, lower_bound, upper_bound)
            if event == "Save hsv":
                save_bounds(lower_bound, upper_bound)
            elif event == "Load hsv":
                lower_bound = load_lower_bounds()
                upper_bound = load_upper_bounds()
                window["-UPPER H-"].update(upper_bound[0])
                window["-UPPER S-"].update(upper_bound[1])
                window["-UPPER V-"].update(upper_bound[2])
                window["-LOWER H-"].update(lower_bound[0])
                window["-LOWER S-"].update(lower_bound[1])
                window["-LOWER V-"].update(lower_bound[2])
        elif values["-AREA-"]:
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_bound = load_lower_bounds()
            lower_bound = (lower_bound[0],lower_bound[1],lower_bound[2])
            upper_bound = load_upper_bounds()
            upper_bound = (upper_bound[0],upper_bound[1], upper_bound[2])
             #Threshold the HSV image to get only green colors
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            contours, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Loop through the contours and count the number of green objects
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > values["-AREA SLIDER-"]:
                    objects += 1
                
                    x,y,w,h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)    
            
            if event == "Save area":
                save_area(values["-AREA SLIDER-"])
            elif event == "Load area":
                window["-AREA SLIDER-"].update(load_area())
        
        elif values["-DETECT-"]:
                    
            #Convert the frame to the HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_bound = load_lower_bounds()
            lower_bound = (lower_bound[0],lower_bound[1],lower_bound[2])
            upper_bound = load_upper_bounds()
            upper_bound = (upper_bound[0],upper_bound[1], upper_bound[2])
             #Threshold the HSV image to get only green colors
            mask = cv2.inRange(hsv,lower_bound, upper_bound)
            
            #result = cv2.bitwise_and(hsv, hsv, mask = mask) 
            
            contours, _= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
            # Loop through the contours and count the number of green objects
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > values["-AREA SLIDER-"]:
                    objects += 1
                
                    x,y,w,h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)    
                    nex[0] = x
                    nex[1] = y
            if pow(pow(nex[0]-prev[0],2) + pow(nex[1]-prev[1],2), 0.5) < 5 and objects != 0:
                # Motion stopped
                if timer_started == False:
                    start_delay = default_timer()
                    timer_started = True

                elif default_timer()-start_delay> values['-TIME SLIDER-'] and timer_started==True:
                    #delay over

                    # Check if the number of objects is correct
                    if objects != values['-OBJECT SLIDER-']:
                        status = "OFF"
                        #GPIO.output(18,GPIO.HIGH)  
                    
                    #Display the green object count for this frame
                    cv2.putText(frame, f"Object count: {objects}, Status: {status}",(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


            else:
                #Motion
                timer_started = False

            if event == "Save number":
                save_number(values['-OBJECT SLIDER-'])
            elif event == "Load number":
                window['-OBJECT SLIDER-'].update(load_number())
            
            if event == "Save delay":
                save_time(values['-TIME SLIDER-'])
            elif event == "Load delay":
                window['-TIME SLIDER-'].update(load_time())

            prev[0] = nex[0] 
            prev[1] = nex[1]
            if event == "Reset":
                status = "ON"  
                #GPIO.output(18,GPIO.LOW)
        frame = resize_frame(frame, 60)
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)


    window.close()
    #GPIO.cleanup()
calibrate()
