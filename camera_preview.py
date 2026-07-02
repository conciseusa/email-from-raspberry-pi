#!/usr/bin/env python3

from picamera2 import Picamera2, Preview
from time import sleep

camera = Picamera2()

camera.start_preview(True)
preview_config = camera.create_preview_configuration()
camera.configure(preview_config)
camera.start()

sleep(15)
#camera.capture_file("test_image.jpg") # needs start()  stop()

# had error when sleep was 20 but unclear how to fix
# seemed to go away when sleep was 15
# g_object_unref: assertion 'G_IS_OBJECT (object)' failed
