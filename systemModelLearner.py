import numpy as np
import serial
from beamDistance import Distance
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.optimizers import Adam
from AIModel import AIModel
import random
from beamDistance import Distance
import cv2
import os
import time
import math
from collections import deque
from time import sleep

if __name__ == "__main__":
	aimodel = AIModel()
	distance = Distance()
	ser = serial.Serial('/dev/ttyUSB0',115200)
	aimodel.load('modelTrained.h5')
	state = [0,0,0,0]
	rewardList = np.array([0,0,0])
	tilt = 87
	ser.write(chr(int(87)).encode())
	sleep(0.5)
	while True:
		for i in range(0,4):
			_,_,state[i],_ = distance.getDistance()
			while((state[i] == None) or (math.isnan(state[i]))):
				_,_,state[i],_ = distance.getDistance()
		#aimodel.rewardFunction(state)
		nextState = aimodel.model.predict(np.array([[state[0],state[1],state[2],state[3],tilt,aimodel.actionGradient]]))
		rewardList[0] = aimodel.rewardFunction(nextState)
		nextState = aimodel.model.predict(np.array([[state[0],state[1],state[2],state[3],tilt,0]]))
		rewardList[1] = aimodel.rewardFunction(nextState)
		nextState = aimodel.model.predict(np.array([[state[0],state[1],state[2],state[3],tilt,-1 * aimodel.actionGradient]]))
		rewardList[2] = aimodel.rewardFunction(nextState)
		actionVal = np.argmax(rewardList)
		print(actionVal)
		if (actionVal == 0):
			ser.write(chr(int(tilt + aimodel.actionGradient)).encode())
			tilt = tilt + aimodel.actionGradient
			if (tilt > 107):
				tilt = 107
			sleep(0.05)
		if (actionVal == 2):
			ser.write(chr(int(tilt - aimodel.actionGradient)).encode())
			tilt = tilt - aimodel.actionGradient
			if (tilt < 67):
				tilt = 67
			sleep(0.05)	
	#print(aimodel.model.predict(np.array([[-177.00282483621552,-168.01190434013895,-156.1569723067145,-149.27156460625713,90,-6]])));

