from systemModelLearner import AIModel
import numpy as np
import serial
from beamDistance import Distance
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.optimizers import Adam
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
	DataX = np.array([[0,0,0,0,0,0],[0,0,0,0,0,0]])
	DataY = np.array([[0,0,0,0,0],[0,0,0,0,0]])
	with open('pidStates.txt') as f:
		lines = f.read().splitlines()
	for line in lines:
		listofData = line.split(',')
		DataX = np.append(DataX,[[float(listofData[0]),float(listofData[1]),float(listofData[2]),float(listofData[3]),float(listofData[4]),float(listofData[5])]],axis = 0)
		DataY = np.append(DataY,[[float(listofData[6]),float(listofData[7]),float(listofData[8]),float(listofData[9]),float(listofData[10])]],axis=0)
	DataX = DataX[2:]
	DataY = DataY[2:]
	print(len(DataX))
	aimodel.train(DataX,DataY)
	aimodel.save('modelTrained.h5')
