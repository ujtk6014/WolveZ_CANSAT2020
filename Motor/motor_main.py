import motor_class
import RPi.GPIO as GPIO
import time

Motor = motor_class.motor(8,10,12)

print("motor run")
Motor.go(100)
Motor.stopslowly()
print("motor stop")
time.sleep(3)

GPIO.cleanup()
