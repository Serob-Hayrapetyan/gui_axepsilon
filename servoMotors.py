import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from pynput.keyboard import Key, Listener

class ServoMotors:
	"""Creating constructor"""
	def __init__(self,duty1,port1,duty2,port2):
		self.duty1 = duty1
		self.port1 = port1
		self.duty2 = duty2
		self.port2 = port2
		
	"""This function drive servo-motor"""    
	def SetPosition(self,angle,port):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(port,GPIO.OUT)

		p = GPIO.PWM(port,50)
		p.start(0)

		p.ChangeDutyCycle(angle)
		sleep(1)
    
		p.stop()
		#GPIO.cleanup()
		
	def on_press(key):
		print('{0}'.format(key))

	"""This function does the appropriate actions of the keys."""
	def on_release(self,key):
		print('{0}'.format(key))
		if '{0}'.format(key) == "u'a'":
			if self.duty1 >= 2.5 and self.duty1 <= 10:
				self.duty1 = self.duty1 + 2.5
				self.SetPosition(self.duty1,self.port1)
				print('qsheci dzax')
		elif '{0}'.format(key) == "u'd'":
			if self.duty1 >= 5 and self.duty1 <= 12.5:
				self.duty1 = self.duty1 - 2.5
				self.SetPosition(self.duty1,self.port1)
		elif '{0}'.format(key) == "u'w'":
			if self.duty2 == 2.5:
				self.duty2 = self.duty2 + 4
				self.SetPosition(self.duty2,self.port2)
			elif self.duty2 == 6.5:
				self.duty2 = self.duty2 + 2
				self.SetPosition(self.duty2,self.port2)
		elif '{0}'.format(key) == "u's'":
			if self.duty2 == 6.5:
				self.duty2 = self.duty2 - 4
				self.SetPosition(self.duty2,self.port2)
			elif self.duty2 == 8.5:
				self.duty2 = self.duty2 - 2
				self.SetPosition(self.duty2,self.port2)
		elif '{0}'.format(key) == "u'x'":
			self.duty1 = 7.5
			self.duty2 = 6.5
			self.SetPosition(self.duty1,self.port1)
			self.SetPosition(self.duty2,self.port2)
		elif '{0}'.format(key) == "u'q'":
			return False
        
        
	def Drive(self):
		#On this line we start key listening
		with Listener(on_press=self.on_press,on_release=self.on_release) as listener:
			listener.join()
