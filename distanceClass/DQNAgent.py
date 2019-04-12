import numpy as np
import serial
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random
from cameraDistance import DistanceMetric
import cv2
import os
import time
import math
class DQNAgent():
	def __init__(self):
		self.actionValue = 88
		self.state_size = 5
		self.iterationNumber = 0
		self.epsilon = 1.0
		self.epsilon_decay = 0.9995
		self.epsilon_min = 0.001
		self.n_actions = 3
		self.actionClampMax = 108
		self.actionClampMin = 68
		self.gamma = 0.95
		self.learning_rate = 0.001
		self.memory = deque(maxlen = 3000)
		self.model = self._buildModel()
	
	def actConvert(self,action):
		if (action == 0):
			self.actionValue = self.actionValue - 4
			if (self.actionValue <= 68):
				self.actionValue = 68
		if (action == 2):
			self.actionValue = self.actionValue + 4
			if (self.actionValue >= 108):
				self.actionValue = 108
		return self.actionValue
	
	def _buildModel(self):
		model = Sequential()
		model.add(Dense(24,input_dim=self.state_size,activation='relu'))
		model.add(Dense(50,activation='relu'))
		model.add(Dense(50,activation='relu'))
		model.add(Dense(50,activation='relu'))
		model.add(Dense(50,activation='relu'))
		model.add(Dense(self.n_actions,activation='linear'))
		model.compile(loss = 'mse',optimizer=Adam(lr=self.learning_rate))
		return model
	
	def remember(self,currentState,action,reward,nextState):
		self.memory.append((currentState,action,reward,nextState))
		#stateFile = open(str("states/statesArray" + str(iterationNumber) + ".txt"),"a+")
		#stateFile.write([state1,state2,state3,state4,angle,action,reward,nextState1,nextState2,nextState3,nextState4,nextAngle])
		#stateFile.close()
		#states defined as state1,state2,state3,state4,angle,action
	
	def act(self,states):
		if ((np.random.rand() <= self.epsilon) and (self.epsilon >= 0.01)):
			print("rand")
			actionValNow = math.floor(random.random()*3)
			return actionValNow
		else:
			print("NN")
			actValue = self.model.predict(states)
			return np.argmax(actValue[0])
			
	def replay(self,batch_size):
		minibatch = random.sample(self.memory,batch_size)
		#print(minibatch)
		for state,action,reward,nextState in minibatch:
			next_rewardState = self.gamma * np.amax(self.model.predict(nextState)[0])
			target = reward + next_rewardState
			target_f = self.model.predict(state)
			target_f[0][action] = target + next_rewardState
			self.model.fit(state,target_f,epochs = 1,verbose = 0)
		if (self.epsilon > self.epsilon_min):
			#print("decayed")
			self.epsilon = self.epsilon * self.epsilon_decay
	
	def load(self,name):
		self.model.load_weights(name)
	
	def save(self,name):
		self.model.save_weights(name)
	
if (__name__ == "__main__"):
	
	outputDir = 'StateData/'
	if not os.path.exists(outputDir):
		os.makedirs(outputDir)
	e = 0
	ser = serial.Serial('/dev/ttyUSB0',115200)
	ser.write(chr(65).encode())
	agent = DQNAgent()
	state = [0,0,0,0,0]
	nextState = [0,0,0,0,0]
	distance = DistanceMetric()
	state[0] = distance.getDistance()
	while(state[0] == None):
		state[0] = distance.getDistance()
	state[1] = distance.getDistance()
	while(state[1] == None):
		state[1] = distance.getDistance()
	state[2] = distance.getDistance()
	while(state[2] == None):
		state[2] = distance.getDistance()
	state[3] = distance.getDistance()
	while(state[3] == None):
		state[3] = distance.getDistance()
	state[4] = agent.actionValue
	state = np.reshape(state,[1,5])
	time.sleep(0.1)
	while True:
		cv2.imshow('frame',distance.getFrame())
		e = e + 0.1
		action = agent.act(state)
		#print(action)
		outAction = agent.actConvert(action)
		#print(action)
		ser.write(chr(outAction).encode())
		nextState[0] = distance.getDistance()
		while(nextState[0] == None):
			nextState[0] = distance.getDistance()
		
		nextState[1] = distance.getDistance()
		while(nextState[1] == None):
			nextState[1] = distance.getDistance()
		
		nextState[2] = distance.getDistance()
		while(nextState[2] == None):
			nextState[2] = distance.getDistance()
		
		nextState[3] = distance.getDistance()
		while(nextState[3] == None):
			nextState[3] = distance.getDistance()
		
		nextState[4] = agent.actionValue
		reward = 0
		for i in nextState:
			if (i == None):
				print(nextState)
			reward = 40 + reward - (i - 16)
		nextStatelist = np.reshape(nextState,[1,5])
		currState = np.reshape(state,[1,5])
		agent.remember(currState,action,reward,nextStatelist)
		print("e is {:.3}, epsilon is {:.3} action was {}".format(e,agent.epsilon,action))
		state = np.reshape(nextState,[1,5])
		if len(agent.memory) > 32:
			if (e < 850):
				agent.replay(32)
		if ((e % 0.3) == 0):
			agent.save(outputDir + "weights_" + '{:04}'.format(e) + ".hdf5")
		
		
		
		
		
		
		
