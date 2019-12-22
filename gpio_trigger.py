#!/usr/bin/env python3

from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import picamera
import subprocess
from email_handler import Class_eMail

var=1
counter = 0
To_Email_ID = ""

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def my_callback(channel):
    if var == 1:
        sleep(1.5)  # confirm the movement by waiting 1.5 sec 
        if GPIO.input(26): # and check again the input
            now = datetime.now()
            #timestamp = datetime.timestamp(now)
            print(now.isoformat(), " Movement!")

            #captureImage()
            #camera = picamera.PiCamera()
            #camera.capture(now.isoformat()+'snapshot.jpg')
            
            pic_file = now.strftime("%Y-%m-%dT%H-%M-%S")+"cam.jpg"
            # fix raspistill error caused by full rez
            # https://www.raspberrypi.org/forums/viewtopic.php?t=232533#p1478436
            subprocess.call("raspistill -o "+pic_file, shell=True)

            email = Class_eMail()
            email.send_HTML_Attachment_Mail(To_Email_ID, 'Movement Detected!', now.isoformat() + " Movement!", pic_file)
            del email

            # stop detection for x sec
            GPIO.remove_event_detect(26)
            sleep(15)
            GPIO.add_event_detect(26, GPIO.RISING, callback=my_callback, bouncetime=300)

GPIO.add_event_detect(26, GPIO.RISING, callback=my_callback, bouncetime=300)

while True:
    sleep(1)
    pass
