from cameraDistance import DistanceMetric
import serial
from simple_pid import PID
import cv2

if (__name__ == "__main__"):
	ser = serial.Serial('/dev/ttyUSB0',115200)
	q = DistanceMetric()
	pid = PID(0.5,0.05,0.3,setpoint = 20)
	while (True):
		b = (q.getDistance())
		cv2.imshow('frame',q.getFrame())
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if (b != None):
			error = pid(b)
			if (error < -20):
				error = -20
			if (error > 20):
				error = 20
			data = (chr(int(88 - error))).encode()
			ser.write(data)
			print("{:.3}".format(float(error)))
