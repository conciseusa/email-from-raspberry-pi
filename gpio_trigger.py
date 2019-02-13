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
            print(now.isoformat(), "Movement!")
            email = Class_eMail()
            email.send_Text_Mail(To_Email_ID, 'Office Movement!', now.isoformat() + "Movement!")
            del email
            #captureImage()
            #camera = picamera.PiCamera()
            #camera.capture(now.isoformat()+'snapshot.jpg')
            
            subprocess.call("raspistill -o "+now.isoformat()+"cam.jpg", shell=True)

            # stop detection for x sec
            GPIO.remove_event_detect(26)
            sleep(60)
            GPIO.add_event_detect(26, GPIO.RISING, callback=my_callback, bouncetime=300)

GPIO.add_event_detect(26, GPIO.RISING, callback=my_callback, bouncetime=300)

while True:
    pass
