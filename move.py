import RPi.GPIO as GPIO                    #Import GPIO library

import time
import urllib.request as urllib2
import sys
import requests
URL='https://api.thingspeak.com/update?api_key=CFVAZHLSSIWSXT64&field1='

#Import time library

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)                  


#GPIO SETUP
flame =29 
gas=36

BUZZER=32

TRIG = 40

ECHO = 38

led = 13


m11=31

m12=33
m21=35

m22=37


GPIO.setup(flame, GPIO.IN)
GPIO.setup(gas, GPIO.IN)

GPIO.setup(BUZZER, GPIO.OUT)

GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs

GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input

GPIO.setup(led,GPIO.OUT)                  


GPIO.setup(m11,GPIO.OUT)

GPIO.setup(m12,GPIO.OUT)

GPIO.setup(m21,GPIO.OUT)

GPIO.setup(m22,GPIO.OUT)


GPIO.output(led, 1)


time.sleep(5)


def stop():

    print ("stop")

    GPIO.output(m11, 0)

    GPIO.output(m12, 0)

    GPIO.output(m21, 0)

    GPIO.output(m22, 0)


def forward():

    GPIO.output(m11, 1)

    GPIO.output(m12, 0)

    GPIO.output(m21, 1)

    GPIO.output(m22, 0)

    print ("Forward")


def back():

    GPIO.output(m11, 0)

    GPIO.output(m12, 1)

    GPIO.output(m21, 0)

    GPIO.output(m22, 1)

    print ("back")


def left():

    GPIO.output(m11, 0)

    GPIO.output(m12, 0)

    GPIO.output(m21, 1)

    GPIO.output(m22, 0)

    print ("left")


def right():

    GPIO.output(m11, 1)

    GPIO.output(m12, 0)

    GPIO.output(m21, 0)

    GPIO.output(m22, 0)

    print ("right")


stop()

count=0

while True:
     

 i=0

 avgDistance=0

 for i in range(5):

  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  time.sleep(0.1)                                   #Delay


  GPIO.output(TRIG, True)                  #Set TRIG as HIGH

  time.sleep(0.00001)                           #Delay of 0.00001 seconds

  GPIO.output(TRIG, False)                 #Set TRIG as LOW


  while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW

       GPIO.output(led, False)             

  pulse_start = time.time()


  while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH

       GPIO.output(led, False) 

  pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor


  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance

  distance = round(distance,2)                 #Round to two decimal points

  avgDistance=avgDistance+distance


 avgDistance=avgDistance/5

 print (avgDistance)
 
 data=avgDistance
 data1=GPIO.input(flame)
 data2=GPIO.input(gas)
 NEW_URL=URL+str(data)+'&field2='+str(data1)+'&field3='+str(data2)
 r=requests.get(NEW_URL)
 print(r)  

 flag=0

 if avgDistance < 15:      #Check whether the distance is within 15 cm range

    count=count+1

    stop()

    time.sleep(1)

    back()

    time.sleep(1.5)

    if (count%3 ==1) & (flag==0):

     right()

     flag=1

    else:

     left()

     flag=0

    time.sleep(1.5)

    stop()

    time.sleep(1)

 else:

    forward()

    flag=0



  

