import motor
import RPi.GPIO as GPIO
import time 

GPIO.setwarnings(False)
Motor1 = motor.motor(5,6,19)
#Motor2 = motor.motor(20,21,12)
try: 
    print("motor run")
    Motor1.go(100)
    #Motor2.go(100)
    time.sleep(20)

    #Motor.back(100)
    #time.sleep(3)
    print("motor stop")
    Motor1.stop()
    #Motor2.stop()
    time.sleep(3)
except KeyboardInterrupt:
    Motor1.stop()
    #Motor2.stop()
    GPIO.cleanup()
