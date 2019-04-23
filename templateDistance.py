import cv2
import math
import numpy as np

cap = cv2.VideoCapture(0)

while True:
	_,v = cap.read()
	cv2.imshow('as',v)
	cv2.waitKey(1)

