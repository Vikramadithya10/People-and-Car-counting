#python person_counting.py --image images/1.jpg --output Output/1_test.jpg

import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import imutils
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-o", "--output", required=True,
	help="path to output image")

args = vars(ap.parse_args())

im = cv2.imread(args["image"])
im = imutils.resize(im, width = min(800, im.shape[1]))

bbox, label, conf = cv.detect_common_objects(im)
label = [objects for objects in label if (objects == 'person')]
output_image = draw_bbox(im, bbox, label, conf)

cv2.putText(output_image, f'No of People : {str(label.count("person"))}', (20,35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
#print('Number of cars in the image is '+ str(label.count('car')))
cv2.imshow("image",output_image)
cv2.imwrite(args["output"], output_image)
cv2.waitKey(0)