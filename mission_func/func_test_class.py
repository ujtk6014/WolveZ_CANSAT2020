import time
import constant as ct
import led_class as led

class simpleFunc():
    
    def __init__(self):
        cnst = ct.constant()
        self.state = 0
        self.preparingTime = 0
        self.flyingTime = 0
        self.LANDING_TIME_THRE = cnst.LANDING_TIME_THRE
    
    def sequence(self):
        if self.state == 0:#初期化の必要あり
            self.preparing()
        elif self.state == 1:
            self.flying()
        elif self.state == 2:
            self.goal()
        else:
            self.state = 0
            
    def preparing(self):
        print('Now it is preparing state')
        LED_Pre = led.led(25)
        LED_Pre.led_on()
        if self.preparingTime == 0:
            self.preparingTime = time.time()#現在の時刻を取得
            
        time.sleep(1)
        
        if not self.preparingTime == 0:
            if time.time() - self.preparingTime > self.LANDING_TIME_THRE:
                self.state = 1
                self.laststate = 1
    
    def flying(self):
        print('Now it is flying state')
        LED_Pre = led.led(25)
        LED_Pre.led_off()
        LED_Pre.led_clean()
        if self.flyingTime == 0:
            self.flyingTime = time.time()#現在の時刻を取得
            
        time.sleep(1)
        
        if not self.flyingTime == 0:
            if time.time() - self.flyingTime > 10: #cnst.LANDING_TIME_THRE:
                self.state = 2
                self.laststate = 2

    def goal(self):
        print('GOAL!!')
        time.sleep(3)
        
        