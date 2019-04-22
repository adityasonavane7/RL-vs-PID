from beamDistance import Distance
import serial
from simple_pid import PID
import cv2
import matplotlib.pyplot as plt	

if (__name__ == "__main__"):
	distancesarray = []
	ser = serial.Serial('/dev/ttyUSB0',115200)
	DistanceClass = Distance()
	pid = PID(0.05,0,0.055,setpoint = 2)
	while (True):
		maskBeam,frame,distance,maskBall = DistanceClass.getDistance()
		cv2.imshow('frame',maskBeam+maskBall)
		cv2.imshow('Beam',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		error = pid(-1*distance)
		if (error < -20):
			error = -20
		if (error > 20):
			error = 20
		data = (chr(int(88 - error))).encode()
		ser.write(data)
		distancesarray.append([-1*distance/10,2])
		print("{:.3}".format(float(-1 * distance)))
	plt.plot(distancesarray)
	plt.show()

