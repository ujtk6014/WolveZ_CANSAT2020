import motor
import RPi.GPIO as GPIO
import time 

GPIO.setwarnings(False)
Motor1 = motor.motor(5,6,13)
Motor2 = motor.motor(20,21,12)

print("motor run")
Motor1.go(100)
Motor2.go(100)
time.sleep(10)
"""
Motor.back(100)
time.sleep(3)
print("motor stop")
Motor.stop()
time.sleep(3)
"""

GPIO.cleanup()
