#python car_counting_video.py --input videos/test.mp4 --output processed_videos/out_test.avi

import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import numpy as np
import tensorflow as tf
import argparse
from cvlib.object_detection import draw_bbox

ap.add_argument("-i", "--input", type=str,
		help="path to optional input video file")
ap.add_argument("-o", "--output", type=str,
		help="path to optional output video file")	
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["input"])

# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video stream or file")
else:
    print('Input loaded successfully!')

# Getting frame dimensions for the output file    
r, img = cap.read()
fshape = img.shape
fheight = fshape[0]
fwidth = fshape[1]

# Defining the codec and create VideoWriter object.
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

# Definining the Output file
out = cv2.VideoWriter(args["output"],fourcc, 60.0, (fwidth,fheight))

# Executing detection on each frame and displaying processed frames
while True:
    r, img = cap.read()
    #img = cv2.resize(img, (int(fwidth*.8), int(fheight*.8)))
    #img = cv2.resize(img, (640, 480))

    bbox, label, conf = cv.detect_common_objects(img)
    label = [objects for objects in label if (objects == 'car' or objects == 'truck' or objects == 'motorcycle' or objects == 'bus')]
    output_image = draw_bbox(img, bbox, label, conf)

    text =f'No of cars : {str(label.count("car"))} \nNo of trucks : {str(label.count("truck"))} \nNo of motorcycles: {str(label.count("motorcycle"))}'
    y0, dy = 50, 30

    for i, line in enumerate(text.split('\n')):
	    y = y0 + i*dy
	    cv2.putText(output_image, line, (20,y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    # Writing the frame into the file 'output.avi'
    out.write(img)

    cv2.imshow("preview", output_image)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break


# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()