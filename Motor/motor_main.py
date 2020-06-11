import motor_class
import RPi.GPIO as GPIO
import time 

Motor = motor_class.motor(22,23,12)

print("motor run")
Motor.go(100)
time.sleep(5)
print("motor stop")
Motor.stopslowly()
time.sleep(3)

GPIO.cleanup()
