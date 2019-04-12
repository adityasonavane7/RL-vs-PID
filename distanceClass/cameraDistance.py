import numpy as np
import cv2
import math
import time
import serial
import random

cap = cv2.VideoCapture(1)

class DistanceMetric():
	def __init__(self):
		#define Ball color range
		self.colorHighBall = np.array([40,90,255]) 
		self.colorLowBall = np.array([20,70,240])
		
		#define Smiley Color range
		self.colorHighEnd1= np.array([80,220,230]) 
		self.colorLowEnd1 = np.array([50,200,210])
		
		#define Cap Color range
		self.colorHighEnd2 = np.array([140,70,40]) 
		self.colorLowEnd2 = np.array([110,50,20])
		
	def euclideanDistance(self,x1,y1,x2,y2):
		return math.sqrt((x1-x2)**2 + (y1-y2)**2)
		
	def getDistance(self):
		#function to return distance of ball
		ret,frame = cap.read()
		self.maskBall = cv2.inRange(frame,self.colorLowBall,self.colorHighBall)
		self.maskEnd1 = cv2.inRange(frame,self.colorLowEnd1,self.colorHighEnd1)
		self.maskEnd2 = cv2.inRange(frame,self.colorLowEnd2,self.colorHighEnd2)
		
		self.CoordinatesBall = cv2.findNonZero(self.maskBall)
		self.CoordinatesEnd1 = cv2.findNonZero(self.maskEnd1)
		self.CoordinatesEnd2 = cv2.findNonZero(self.maskEnd2)
		
		#Coordinates of Ball
		if (len(np.shape(self.CoordinatesBall)) > 0):
			self.ballExists = True
			self.xBall = np.average(np.transpose(self.CoordinatesBall)[0][0])
			self.yBall = np.average(np.transpose(self.CoordinatesBall)[1][0])
		else:
			self.ballExists = False	
		
		#Coordinates of End 1
		if (len(np.shape(self.CoordinatesEnd1)) > 0):
			self.end1Exists = True	
			self.xEnd1 = np.average(np.transpose(self.CoordinatesEnd1)[0][0])
			self.yEnd1 = np.average(np.transpose(self.CoordinatesEnd1)[1][0])
		else:
			self.end1Exists = False
		
		#Coordinates of End 2
		if (len(np.shape(self.CoordinatesEnd2)) > 0):
			self.end2Exists = True	
			self.xEnd2 = np.average(np.transpose(self.CoordinatesEnd2)[0][0])
			self.yEnd2 = np.average(np.transpose(self.CoordinatesEnd2)[1][0])
		else:
			self.end2Exists = False
		
		if (self.ballExists and self.end1Exists and self.end2Exists):
			return (self.euclideanDistance(self.xBall,self.yBall,self.xEnd2,self.yEnd2)/self.euclideanDistance(self.xEnd2,self.yEnd2,self.xEnd1,self.yEnd1)) * 40 
	
	def getFrame(self):
		ret,frame = cap.read()
		return frame

