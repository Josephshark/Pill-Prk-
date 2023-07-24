# pillProject
Working set up for color calibration and detection for RPI
Sends a gpio output signal on pin 17 if the incorect number of objects is found in before the specified deadline after motion stops
This is to be used to detect when a pill package stops moving and the frame is clear count the number of objects and either send a signal notifying that
the package is inadequate or continue.
