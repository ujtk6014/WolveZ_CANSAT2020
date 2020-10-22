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

<<<<<<< HEAD
=======
try:
    print("motor run") 
    Motor1.go(90)
    Motor2.go(100)
    time.sleep(10)

>>>>>>> a1580ec6d89addfe56a7dc858d0680264009e7b0
    #Motor.back(100)
    #time.sleep(3)
    print("motor stop")
    Motor1.stop()
<<<<<<< HEAD
    #Motor2.stop()
    time.sleep(3)
except KeyboardInterrupt:
    Motor1.stop()
    #Motor2.stop()
    GPIO.cleanup()
=======
    Motor2.stop()
    time.sleep(1)
except KeyboardInterrupt:
    Motor1.stop()
    Motor2.stop()
    GPIO.cleanup()

GPIO.cleanup()
>>>>>>> a1580ec6d89addfe56a7dc858d0680264009e7b0
