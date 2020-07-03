import cansat
import cv2
from time import sleep

can=cansat.Cansat()
can.setup()

try:
    can.capture = cv2.VideoCapture(0)
    #while cv2.waitKey(1) < 0:
    while True:
        can.sensor()
        sleep(0.001)
        can.sequence()
        sleep(0.001)
except KeyboardInterrupt:
    print('finished')
    pass