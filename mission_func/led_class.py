import RPi.GPIO as GPIO
global led

class led():
    def __init__(self,pin):
        self.PIN = pin
        GPIO.setmode(GPIO.BCM) #enable GPIO
        GPIO.setup(self.PIN,GPIO.OUT) #using pin 25 as an output
        self.led_status = 0 #LEDが点滅してるかどうかを見る。初期化しないとバグる
    
    def led_on(self): #turn on the led
        GPIO.output(self.PIN,GPIO.HIGH)
        self.led_status = 1
        
    def led_off(self): #turn off the led
        GPIO.output(self.PIN,GPIO.LOW)
        self.led_status = 2
    
    #def ledread(self)
    #    return self.led_status
    
    def led_clean(self):
        GPIO.cleanup()
    

