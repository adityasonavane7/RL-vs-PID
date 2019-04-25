from beamDistance import Distance
import serial
from simple_pid import PID
import cv2
import matplotlib.pyplot as plt	

if (__name__ == "__main__"):
	setpt = -250
	distancesarray = []
	ser = serial.Serial('/dev/ttyUSB0',115200)
	DistanceClass = Distance()
	pid = PID(0.05,0.00009,0.027,setpoint = setpt)
	while (True):
		maskBeam,frame,distance,maskBall = DistanceClass.getDistance()
		cv2.imshow('frame',maskBeam+maskBall)
		cv2.imshow('Beam',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		error = pid(distance)
		if (error < -20):
			error = -20
		if (error > 20):
			error = 20
		data = (chr(int(88 - error))).encode()
		ser.write(data)
		distancesarray.append([distance,setpt])
		print("{}".format(float(distance)))
	plt.plot(distancesarray)
	plt.show()

