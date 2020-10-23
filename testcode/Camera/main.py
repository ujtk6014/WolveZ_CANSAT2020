import cansat
import cv2
from time import sleep

can=cansat.Cansat()
can.setup()

try:
    can.capture = cv2.VideoCapture(0)
    #while cv2.waitKey(1) < 0:
    while True:
        can.run()
        sleep(0.1)
except KeyboardInterrupt:
    print('finished')
    pass
