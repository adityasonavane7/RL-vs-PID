import cv2
import serial
import numpy as np
import math
from time import sleep

'''
Beam Colours
90-110,140-155,165-180
'''
class Distance:
	def __init__(self):
		self.colorLowBall = np.array([10,120,20]) 
		self.colorHighBall = np.array([70,200,120])
		
		self.beamMinColor = np.array([10,10,120])
		self.beamMaxColor = np.array([50,50,190])
		self.cap = cv2.VideoCapture(0)
	
	def euclideanDistance(self,x1,y1,x2,y2):
		return math.sqrt((x1-x2)**2 + (y1-y2)**2)
	
	def getDistance(self):
		self.ret,self.frame = self.cap.read()
		#self.element = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
		self.maskBeam = cv2.inRange(self.frame,self.beamMinColor,self.beamMaxColor)
		self.maskBall = cv2.inRange(self.frame,self.colorLowBall,self.colorHighBall)		
		#self.maskBeam = cv2.erode(self.maskBeam, self.element, iterations = 1)
		self.centerBeam = cv2.moments(self.maskBeam)
		self.cXBeam = int(self.centerBeam["m10"]/self.centerBeam["m00"])
		self.cYBeam = int(self.centerBeam["m01"]/self.centerBeam["m00"])
		self.centerBall = cv2.moments(self.maskBall)
		self.cXBall = int(self.centerBall["m10"]/self.centerBall["m00"])
		self.cYBall = int(self.centerBall["m01"]/self.centerBall["m00"])
		self.maskBeam = cv2.cvtColor(self.maskBeam,cv2.COLOR_GRAY2BGR)
		self.outFrame = self.frame & self.maskBeam
		cv2.circle(self.frame,(self.cXBeam,self.cYBeam),5,(255,0,0),-1)
		cv2.circle(self.frame,(self.cXBall,self.cYBall),5,(0,255,0),-1)
		self.maskBall = cv2.cvtColor(self.maskBall,cv2.COLOR_GRAY2BGR)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			print("exit")
		self.distance = self.euclideanDistance(self.cXBeam,self.cYBeam,self.cXBall,self.cYBall)
		if (self.cXBeam > self.cXBall):
			self.distance = -1 * self.distance
		return self.outFrame,self.frame,self.distance,self.maskBall

if (__name__ == "__main__"):
	m = Distance()
	while True:
		q,z,d,b = m.getDistance() 
		cv2.imshow('asd',z)
		print(d-40)
