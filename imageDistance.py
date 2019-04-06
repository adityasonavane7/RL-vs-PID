import numpy as np
import cv2
import sys
import math

cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,1024)
#Ball color definitions
colorHighBall = np.array([100,170,255])
colorLowBall = np.array([0,50,240])

#end color definitions
#colorHighBall = np.array([100,150,255]) 
#colorLowBall = np.array([50,100,250])

#End 1 Color Definitions
colorHighEnd = np.array([70,200,230]) 
colorLowEnd = np.array([0,170,150])

XYCoordinates = []
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	# Our operations on the frame come here
	mask = cv2.inRange(frame,colorLowBall,colorHighBall)
	maskEnd = cv2.inRange(frame,colorLowEnd,colorHighEnd)
	maskrgbBall = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
	maskrgbEnd = cv2.cvtColor(maskEnd,cv2.COLOR_GRAY2BGR)
	outputImg = frame & (maskrgbEnd | maskrgbBall)
	cv2.imshow('frame',frame)
	cv2.imshow('opimg',outputImg)
	XYCoordinatesBall = cv2.findNonZero(mask)
	XYCoordinatesEnd = cv2.findNonZero(maskEnd)
	if (len(np.shape(XYCoordinatesBall)) > 0):
		xBall = np.mean(np.transpose(XYCoordinatesBall)[0])
		yBall = np.mean(np.transpose(XYCoordinatesBall)[1])
		#print([xBall,yBall]) #Mean position of ball color
	if (len(np.shape(XYCoordinatesEnd)) > 0):
		xEnd = np.mean(np.transpose(XYCoordinatesEnd)[0])
		yEnd = np.mean(np.transpose(XYCoordinatesEnd)[1])
		#print([xEnd,yEnd]) #Mean position of ball color
	if ((len(np.shape(XYCoordinatesBall)) > 0) and (len(np.shape(XYCoordinatesEnd)) > 0)):
		print(math.sqrt((xBall-xEnd)*(xBall-xEnd) + (yBall-yEnd)*(yBall-yEnd)))
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
