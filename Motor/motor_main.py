import motor_class

Motor = motor_class.motor(8,10,12)

Motor.go(100)
Motor.stopslowly()
sleep(3)

GPIO.cleanup()
