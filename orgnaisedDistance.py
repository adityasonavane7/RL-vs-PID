import numpy as np
import cv2
import sys
import math
import serial
import time
from serial import Serial
from simple_pid import PID
import matplotlib
import matplotlib.pyplot as plt	
pid = PID(0.5,0.05,0.3,setpoint = 16)

cap = cv2.VideoCapture(0)
#Ball color definitions Bouncy
colorHighBall = np.array([40,90,255])
colorLowBall = np.array([20,70,240])

End1End2Dist = 0
#Ball color definitions pong
#colorHighBall = np.array([70,170,220])
#colorLowBall = np.array([30,140,200])

normalisedDistance = 0

#end color definitions
#colorHighBall = np.array([100,150,255]) 
#colorLowBall = np.array([50,100,250])

#End 1 Color Definitions
colorHighEnd2 = np.array([80,220,230]) 
colorLowEnd2 = np.array([50,200,210])


#End 2 Color Definitions
colorHighEnd = np.array([140,70,40]) 
colorLowEnd = np.array([110,50,20])
BallEnd1 = False
End1End2 = False

graphErrors = []
timeMap = 0
error = 0
errorPrev = 0
data = "0"
dataprev = "0"
plt.plot(error)
plt.show()
ser = serial.Serial('/dev/ttyUSB0',baudrate = 115200)
time.sleep(2)
XYCoordinates = []
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	# Our operations on the frame come here
	mask = cv2.inRange(frame,colorLowBall,colorHighBall)
	maskEnd = cv2.inRange(frame,colorLowEnd,colorHighEnd)
	maskEnd2 = cv2.inRange(frame,colorLowEnd2,colorHighEnd2)
		
	maskrgbBall = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
	maskrgbEnd = cv2.cvtColor(maskEnd,cv2.COLOR_GRAY2BGR)
	maskrgbEnd2 = cv2.cvtColor(maskEnd2,cv2.COLOR_GRAY2BGR)
	
	outputImg = frame & (maskrgbEnd2)
	XYCoordinatesBall = cv2.findNonZero(mask)
	XYCoordinatesEnd = cv2.findNonZero(maskEnd)
	XYCoordinatesEnd2 = cv2.findNonZero(maskEnd2)
	
	#Coordinates of Ball
	if (len(np.shape(XYCoordinatesBall)) > 0):
		xBall = np.average(np.transpose(XYCoordinatesBall)[0][0])
		yBall = np.average(np.transpose(XYCoordinatesBall)[1][0])
		#print([xBall,yBall]) #Mean position of ball color
	
	#Coordinates of End 1
	if (len(np.shape(XYCoordinatesEnd)) > 0):	
		xEnd = np.average(np.transpose(XYCoordinatesEnd)[0][0])
		yEnd = np.average(np.transpose(XYCoordinatesEnd)[1][0])
		#print([xEnd,yEnd]) #Mean position of ball color
	
	#Coordinates of End 2
	if (len(np.shape(XYCoordinatesEnd2)) > 0):	
		xEnd2 = np.average(np.transpose(XYCoordinatesEnd2)[0][0])
		yEnd2 = np.average(np.transpose(XYCoordinatesEnd2)[1][0])
		#print([xEnd,yEnd]) #Mean position of ball color
	
	#Distance End1 And Ball
	if ((len(np.shape(XYCoordinatesBall)) > 0) and (len(np.shape(XYCoordinatesEnd)) > 0)):
		BallEnd1 = True		
		BallEnd1Dist = math.sqrt((xBall-xEnd)*(xBall-xEnd) + (yBall-yEnd)*(yBall-yEnd))
		frame = cv2.line(frame,(int(xBall),int(yBall)),(int(xEnd),int(yEnd)),[0,0,255])
	
	#Distance End1 And End2
	if ((len(np.shape(XYCoordinatesEnd2)) > 0) and (len(np.shape(XYCoordinatesEnd)) > 0)):
		End1End2 = True		
		End1End2Dist = math.sqrt((xEnd2-xEnd)*(xEnd2-xEnd) + (yEnd2-yEnd)*(yEnd2-yEnd))
		frame = cv2.line(frame,(int(xEnd2),int(yEnd2)),(int(xEnd),int(yEnd)),[255,0,0])
	
	if (BallEnd1 and End1End2):
		normalisedDistance = ((BallEnd1Dist/End1End2Dist)*40)
		#print(str(normalisedDistance))
		cv2.putText(frame, str(normalisedDistance), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
	
	cv2.imshow('frame',frame)
	dataprev = data
	error = pid(normalisedDistance)
	plt.plot(error)
	plt.show(block = False)
	#errorPrev = error
	#error = (proportional * (normalisedDistance-21)) + (derivative * (errorPrev - error))
	if (error < -20):
		error = -20
	if (error > 20):
		error = 20
	data = (chr(int(88 - error))).encode()
	print(normalisedDistance)
	ser.write(data)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
