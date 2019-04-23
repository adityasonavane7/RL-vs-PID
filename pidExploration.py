from beamDistance import Distance
import serial
from simple_pid import PID
import numpy as np
import cv2
import matplotlib.pyplot as plt	
from time import sleep
'''
Take 4 distances as current state
take an action wrt PID
Take 4 distances as next state
Correlate
'''
if (__name__ == "__main__"):
	distancesarray = []
	ser = serial.Serial('/dev/ttyUSB0',115200)
	DistanceClass = Distance()
	pid = PID(0.05,0.00009,0.027,setpoint = -250)
	ser.write(chr(int(87)).encode())
	tilt = 87
	currentState = [0,0,0,0,0]
	nextState = [0,0,0,0,0]	
	with open("pidStates.txt", "w") as myfile:
		myfile.write("");
	iteration = 0
	while (True):
		for i in range(0,4):
			_,_,currentState[i],_ = DistanceClass.getDistance()
		currentState[i+1] = tilt
		distanceArray = np.mean(currentState)
		error = pid(distanceArray)
		if (error < -20):
			error = -20
		if (error > 20):
			error = 20
		action = tilt
		tilt = int(87 - error)
		action = tilt - action
		data = (chr(tilt)).encode()
		ser.write(data)
		for i in range(0,4):
			_,_,nextState[i],_ = DistanceClass.getDistance()
		nextState[i+1] = tilt
		#Append Data here
		#print(str([currentState,action,nextState]))
		print(iteration)
		iteration = iteration + 1
		with open("pidStates.txt", "a") as myfile:
			data = "{},{},{},{},{},{},{},{},{},{},{}\r\n".format(currentState[0],currentState[1],currentState[2],currentState[3],currentState[4],action,nextState[0],nextState[1],nextState[2],nextState[3],nextState[4])
			myfile.write(data)
	plt.plot(distancesarray)
	plt.show()

