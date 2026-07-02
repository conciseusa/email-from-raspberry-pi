#!/usr/bin/env python3

# Simple script to email a picture when a GPIO pin is triggered

from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import subprocess
from email_handler import Class_eMail

gpio_pin = 26
var=1
To_Email_ID = ""

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def my_callback(channel):
    if var == 1:
        sleep(1.5)  # confirm the movement by waiting 1.5 sec 
        if GPIO.input(gpio_pin): # and check again the input
            now = datetime.now()
            print(now.isoformat(), " Movement!")

            pic_file = now.strftime("%Y-%m-%dT%H-%M-%S")+"cam.jpg"
            # fix raspistill error caused by full rez, moved to rpicam-still
            # https://www.raspberrypi.org/forums/viewtopic.php?t=232533#p1478436
            subprocess.call("rpicam-still -o "+pic_file, shell=True)

            email = Class_eMail()
            email.send_HTML_Attachment_Mail(To_Email_ID, 'Movement Detected!', now.isoformat() + " Movement!", pic_file)
            del email

            # stop detection for x sec
            GPIO.remove_event_detect(gpio_pin)
            sleep(15)
            GPIO.add_event_detect(gpio_pin, GPIO.RISING, callback=my_callback, bouncetime=300)

GPIO.add_event_detect(gpio_pin, GPIO.RISING, callback=my_callback, bouncetime=300)

while True:
    sleep(1)
    pass
