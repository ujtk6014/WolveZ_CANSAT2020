import RPi.GPIO as GPIO

class led():
    def __init__(self,pin):
        self.PIN = pin
        GPIO.setmode(GPIO.BCM) #enable GPIO
        GPIO.setup(self.PIN,GPIO.OUT) #using pin 25 as an output
    
    def led_on(self): #turn on the led
        GPIO.output(self.PIN,GPIO.HIGH)
        
    def led_off(self): #turn off the led
        GPIO.output(self.PIN,GPIO.LOW)
    
    #def ledread(self)
    #    return self.led_status
    
    def led_clean(self):
        GPIO.cleanup()
    

