from tkinter import *
from servoMotors import *
from camera import *        #module for the first method to see camera view
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import serial
#from frame2 import *       #module for the second method to see camera view
from threading import *

#creating window
root = Tk()
root.title("AXEpsilon")
root.geometry("1500x1300")
#root.geometry("600x400")
"""Motor instances"""
GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 12

Motor2A = 11
Motor2B = 13
Motor2E = 19
i=100

 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
pwm1 = GPIO.PWM(Motor1E,1100)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
pwm2 = GPIO.PWM(Motor2E,1100)
stage='down'
i_Duty_left=100
i_Duty_right=100
GPIO.output(Motor1A,GPIO.HIGH)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor2A,GPIO.HIGH)
GPIO.output(Motor2B,GPIO.LOW)

#servo instance
servo = ServoMotors(7.5,33,6.5,32)

labelText = StringVar()
labelText.set("Hello")
messagefriction = StringVar()
messagefriction.set(0)
messagepeak_to_peak = StringVar()
messagepeak_to_peak.set(0)
messageduty_cycle = StringVar()
messageduty_cycle.set(0)
messagetimes = StringVar()
messagetimes.set(0)
messageangular = StringVar()
messageangular.set(0)
messageaverage_speed = StringVar()
messageaverage_speed.set(0)
messageturning_period = StringVar()
messageturning_period.set(0)
messageOfAlt = StringVar()
messageOfLen = StringVar()

label = Label(textvariable = labelText,justify=LEFT,background = "#eee")
label.place(relx = 0.9,rely = 0.12,relheight = 0.04,relwidth = 0.06)

"""Parameters to get user input #FrontEnd"""
labelParameters = Label(text = "Friction",font = "Arial 7",justify = CENTER)
labelParameters.place(relx = 0.61,rely = 0.03,relheight = 0.02,relwidth = 0.05)
friction_coefficient = Entry(textvariable=messagefriction)
friction_coefficient.place(relx = 0.61,rely = 0.05,relheight = 0.04,relwidth = 0.06)

labelParameters1 = Label(text = "Peak To Peak",font = "Arial 7")
labelParameters1.place(relx = 0.69,rely = 0.03,relheight = 0.02,relwidth = 0.06)
peak_to_peak_distance = Entry(textvariable=messagepeak_to_peak)
peak_to_peak_distance.place(relx = 0.69,rely = 0.05,relheight = 0.04,relwidth = 0.06)

labelParameters2 = Label(text = "Duty cycle",font = "Arial 7")
labelParameters2.place(relx = 0.77,rely = 0.03,relheight = 0.02,relwidth = 0.05)
duty_cycle_distance = Entry(textvariable=messageduty_cycle)
duty_cycle_distance.place(relx = 0.77,rely = 0.05,relheight = 0.04,relwidth = 0.06)

labelParameters3 = Label(text = "Time",font = "Arial 7")
labelParameters3.place(relx = 0.84,rely = 0.03,relheight = 0.02,relwidth = 0.05)
times = Entry(textvariable=messagetimes)
times.place(relx = 0.85,rely = 0.05,relheight = 0.04,relwidth = 0.06)

labelParameters4 = Label(text = "Angular",font = "Arial 7")
labelParameters4.place(relx = 0.93,rely = 0.03,relheight = 0.02,relwidth = 0.05)
angular_coefficient = Entry(textvariable=messageangular)
angular_coefficient.place(relx = 0.93,rely = 0.05,relheight = 0.04,relwidth = 0.06)

labelParameters5 = Label(text = "Speed",font = "Arial 7")
labelParameters5.place(relx = 0.61,rely = 0.1,relheight = 0.02,relwidth = 0.05)
average_speed_of_a_vehicle = Entry(textvariable=messageaverage_speed)
average_speed_of_a_vehicle.place(relx = 0.61,rely = 0.12,relheight = 0.04,relwidth = 0.06)

labelParameters6 = Label(text = "Period",font = "Arial 7")
labelParameters6.place(relx = 0.69,rely = 0.1,relheight = 0.02,relwidth = 0.05)
turning_period = Entry(textvariable=messageturning_period)
turning_period.place(relx = 0.69,rely = 0.12,relheight = 0.04,relwidth = 0.06)


"""GPS coordinates"""
gpsParameters1 = Label(text = "ALT",font = "Arial 7",justify = CENTER)
gpsParameters1.place(relx = 0.69,rely = 0.27,relheight = 0.02,relwidth = 0.05)
altitude = Entry(textvariable=messageOfAlt)
altitude.place(relx = 0.69,rely = 0.29,relheight = 0.04,relwidth = 0.1)

gpsParameters2 = Label(text = "LEN",font = "Arial 7",justify = CENTER)
gpsParameters2.place(relx = 0.88,rely = 0.27,relheight = 0.02,relwidth = 0.08)
lentitude = Entry(textvariable=messageOfLen)
lentitude.place(relx = 0.88,rely = 0.29,relheight = 0.04,relwidth = 0.11)

#Functions to make programm alive. Backend
def click_left(event = ' '):
    if servo.duty1 >= 2.5 and servo.duty1 <= 10:
        servo.duty1 = servo.duty1 + 2.5
        servo.SetPosition(servo.duty1,servo.port1)
    labelText.set(servo.duty1)
    
def click_right(event = ' '):
    if servo.duty1 >= 5 and servo.duty1 <= 12.5:
        servo.duty1 = servo.duty1 - 2.5
        servo.SetPosition(servo.duty1,servo.port1)
    labelText.set(servo.duty1)
    
def click_up(event = ' '):
    if servo.duty2 == 2.5:
        servo.duty2 = servo.duty2 + 4
        servo.SetPosition(servo.duty2,servo.port2)
    elif servo.duty2 == 6.5:
        servo.duty2 = servo.duty2 + 2
        servo.SetPosition(servo.duty2,servo.port2)
    labelText.set(servo.duty2)
    
def click_down(event = ' '):
    if servo.duty2 == 6.5:
        servo.duty2 = servo.duty2 - 4
        servo.SetPosition(servo.duty2,servo.port2)
    elif servo.duty2 == 8.5:
        servo.duty2 = servo.duty2 - 2
        servo.SetPosition(servo.duty2,servo.port2)
    labelText.set(servo.duty2)
    
def click_reset(event = ' '):
    servo.duty1 = 7.5
    servo.duty2 = 6.5
    servo.SetPosition(servo.duty1,servo.port1)
    servo.SetPosition(servo.duty2,servo.port2)
    labelText.set(str(servo.duty1) + ', ' + str(servo.duty2))

def click_apply():
    labelText.set('Apply')

def AutoPilot():
    labelText.set('Autopilot is started')

def HandControl():
    labelText.set('Now,you can control the robot yourself')

def TurnLeft(event = ' '):
    global i_Duty_left
    global i_Duty_right
    global stage
    if stage == 'up'or'down'or'right'or'stop':
        for i in range(0,100):
            if i_Duty_left != 0:
                i_Duty_left=i_Duty_left-1
            if i_Duty_right!=0:
                i_Duty_right=i_Duty_right-1
                
        pwm1.start(i_Duty_left)
        pwm2.start(i_Duty_right)
        labelText.set('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))
        sleep(0.001)

        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        stage='left'
        labelText.set("Going left")
        for i in range(0,100):
            i_Duty_left=i_Duty_left+1
            i_Duty_right=i_Duty_right+1
            pwm1.start(i_Duty_left)
            pwm2.start(i_Duty_right)
            sleep(0.001)
            labelText.set('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))
    labelText.set('Turned left')

def TurnRight(event = ' '):
    global i_Duty_left
    global i_Duty_right
    global stage
    
    if stage == 'up'or'down'or'left'or'stop':         
        for i in range(0,100):
            if i_Duty_left!=0:
                i_Duty_left=i_Duty_left-1
        if i_Duty_right!=0:   
                i_Duty_right=i_Duty_right-1
        pwm1.start(i_Duty_left)
        pwm2.start(i_Duty_right)
        labelText.set('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))
        sleep(0.001)
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        stage='right'
        labelText.set("Going right")
        for i in range(0,100):
            i_Duty_left=i_Duty_left+1
            i_Duty_right=i_Duty_right+1
            pwm1.start(i_Duty_left)
            pwm2.start(i_Duty_right)
            sleep(0.001)
            labelText.set('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))

def GoForward(event = ' '):
    global i_Duty_left
    global i_Duty_right
    global stage
    if stage == 'down' or 'left'or 'right' or 'stop':       
            GPIO.output(Motor1E,GPIO.HIGH)
            GPIO.output(Motor2E,GPIO.HIGH) 
            for i in range(0,100):                              
                if i_Duty_left!=0:          
                   i_Duty_left=i_Duty_left-1
                if i_Duty_right!=0:   
                   i_Duty_right=i_Duty_right-1
                   
            pwm1.start(i_Duty_left)
            pwm2.start(i_Duty_right)
            labelText.set('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))
            sleep(0.001)
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    stage='up'
    labelText.set("Going up")
     
    for i in range(0,100):
        i_Duty_left=i_Duty_left+1
        i_Duty_right=i_Duty_right+1
        pwm1.start(i_Duty_left)
        pwm2.start(i_Duty_right)
        sleep(0.001)
        labelText.set('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))

def GoBack(event = ' '):
    global i_Duty_left
    global i_Duty_right
    global stage
    if stage == 'up'or 'left' or 'right' or 'stop':      
        for i in range(0,100):
            if i_Duty_left!=0:
                i_Duty_left=i_Duty_left-1
                if i_Duty_right!=0:   
                    i_Duty_right=i_Duty_right-1
                    
            pwm1.start(i_Duty_left)
            pwm2.start(i_Duty_right)
            labelText.set('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))
            sleep(0.001)
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        stage='down'
        labelText.set("Going up")
        for i in range(0,100):
            i_Duty_left=i_Duty_left+1
            i_Duty_right=i_Duty_right+1
            pwm1.start(i_Duty_left)
            pwm2.start(i_Duty_right)
            sleep(0.001)
            labelText.set('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))
    

def Stop(event = ' '):
    global i_Duty_left
    global i_Duty_right
    global stage
    if stage == 'up'or'down'or'left'or'right':         
        for i in range(0,100):
            if i_Duty_left!=0:
                i_Duty_left=i_Duty_left-1
            if i_Duty_right!=0:   
                i_Duty_right=i_Duty_right-1
             
            pwm1.start(i_Duty_left)
            pwm2.start(i_Duty_right)
            print('Duty for left motor is ' + str(i_Duty_left) + 'Duty for right motor is ' + str(i_Duty_right))
            sleep(0.001)
            GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
        stage='stop'
        print("stop")
        GPIO
    labelText.set("Stop")




"""Camera controlling buttons
"""
left_btn = Button(text = 'Left (A)',background = "#bbb",foreground = "black",padx = "10",pady = "4",font = "14",bd = "2",command = click_left)
right_btn = Button(text = 'Right (D)',background = "#bbb",foreground = "black",padx = "10",pady = "4",font = "14",bd = "2",command = click_right)
up_btn = Button(text = 'Up (W)',background = "#bbb",foreground = "black",padx = "10",pady = "4",font = "14",bd = "2",command = click_up)
down_btn = Button(text = 'Down (S)',background = "#bbb",foreground = "black",padx = "10",pady = "4",font = "14",bd = "2",command = click_down)
reset_btn = Button(text = 'Reset (X)',background = "#bbb",foreground = "black",padx = "10",pady = "4",font = "14",bd = "2",command = click_reset)
apply_btn = Button(text = 'Apply',background = "#bbb",foreground = "black",padx = "10",pady = "4",font = "14",bd = "2",command = click_apply)

left_btn.place(relx = 0.01,rely = 0.73,relheight = 0.08,relwidth = 0.09) 
right_btn.place(relx = 0.18,rely = 0.73,relheight = 0.08,relwidth = 0.09) 
up_btn.place(relx = 0.11,rely = 0.59,relheight = 0.12,relwidth = 0.06) 
down_btn.place(relx = 0.11,rely = 0.83,relheight = 0.12,relwidth = 0.06) 
reset_btn.place(relx = 0.11,rely = 0.73,relheight = 0.08,relwidth = 0.06) 
apply_btn.place(relx = 0.61,rely = 0.2,relheight = 0.04,relwidth = 0.05)




"""Motors controlling buttons
"""
leftArrow = PhotoImage(file = r"/home/pi/Desktop/AXEpsilon/images/left.png")
rightArrow = PhotoImage(file = r"/home/pi/Desktop/AXEpsilon/images/right.png")
forwardArrow = PhotoImage(file = r"/home/pi/Desktop/AXEpsilon/images/up.png")
backArrow = PhotoImage(file = r"/home/pi/Desktop/AXEpsilon/images/down.png")


autoPilotButton = Button(text = 'Auto',background = "#bbb",foreground = "black",padx = "10",pady = "4",font = "14",bd = "1",command = AutoPilot)
autoPilotButton.place(relx = 0.69,rely = 0.4,relheight = 0.08,relwidth = 0.1)
handcontrolButton = Button(text = 'Hand',background = "#bbb",foreground = "black",padx = "10",pady = "4",font = "14",bd = "1",command = HandControl)
handcontrolButton.place(relx = 0.88,rely = 0.4,relheight = 0.08,relwidth = 0.11)
goLeft = Button(text = '',foreground = "#bbb",padx = "10",pady = "4",font = "14",bd = "1",image = leftArrow,command = TurnLeft)
goRight = Button(text = '',foreground = "#ccc",padx = "10",pady = "4",font = "14",bd = "1",image = rightArrow,command = TurnRight)
goForward = Button(text = '',foreground = "#ccc",padx = "10",pady = "4",font = "14",bd = "1",image = forwardArrow,command = GoForward)
goBack = Button(text = '',foreground = "#ccc",padx = "10",pady = "4",font = "14",bd = "1",image = backArrow,command = GoBack)
StopMotors = Button(text = 'STOP',foreground = "red",padx = "10",pady = "4",font = "14",bd = "1",command = Stop)

goLeft.place(relx = 0.69,rely = 0.73,relheight = 0.08,relwidth = 0.1)
goRight.place(relx = 0.89,rely = 0.73,relheight = 0.08,relwidth = 0.1) 
goForward.place(relx = 0.81,rely = 0.59,relheight = 0.12,relwidth = 0.06) 
goBack.place(relx = 0.81,rely = 0.83,relheight = 0.12,relwidth = 0.06)
StopMotors.place(relx = 0.81,rely = 0.73,relheight = 0.08,relwidth = 0.06) 


#Keyboard control events
root.bind('a',click_left)
root.bind('d',click_right)
root.bind('w',click_up)
root.bind('s',click_down)
root.bind('x',click_reset)
root.bind('<Left>',TurnLeft)
root.bind('<Right>',TurnRight)
root.bind('<Up>',GoForward)
root.bind('<Down>',GoBack)
root.bind('<Shift_L>',Stop)
root.bind('<Shift_R>',Stop)

def Update_gps(): 
    sleep(1)
    gps = serial.Serial("/dev/ttyACM0",baudrate = 4800) 
    line = gps.readline()
    lineString = str(line)
    data = lineString.split(",")
    #data1 = data[1].split(",")
    if data[0] == "$GPRMC":
        if data[2] == "A":
            messageOfAlt.set(float(data[3])/100)
            messageOfLen.set(float(data[5])/100)

def LoopUpdate():
	while True:
		Update_gps()

thread_for_gps = Thread(target = LoopUpdate)
thread_for_gps.start()

App(root, "AXEpsilon")                             #Method 1

#thread = Thread(target = Preview,args = (root,))   #Method 2
#thread.start()



#root.mainloop()