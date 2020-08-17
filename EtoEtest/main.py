# -*- coding: utf-8 -*-

import cansat
import cv2
from time import sleep
import RPi.GPIO as GPIO
import sys
import constant as ct

can=cansat.Cansat()
can.setup()

try:
    can.capture = cv2.VideoCapture(0)
    #while cv2.waitKey(1) < 0:
    while True:
        can.sensor()
        sleep(0.1)
        can.sequence()
        sleep(0.1)
except KeyboardInterrupt:
    print('finished')
    GPIO.output(ct.const.RELEASING_PIN,0) #焼き切りが危ないのでlowにしておく
    GPIO.cleanup()
    pass