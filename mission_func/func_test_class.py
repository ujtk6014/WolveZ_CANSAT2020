import time
import constant as ct
import led_class
import sys

class simpleFunc():
    
    def __init__(self):
        #オブジェクト生成
        self.cnst = ct.constant()
        self.LED_Pre = led_class.led(self.cnst.LED_PRE_PIN)
        self.LED_Fly = led_class.led(self.cnst.LED_FLY_PIN)
        self.LED_G = led_class.led(self.cnst.LED_G_PIN)
        self.state = 0
        self.preparingTime = 0
        self.flyingTime = 0
        self.goalTime = 0
    
    def sequence(self):
        if self.state == 0:#初期化の必要あり
            self.preparing()
        elif self.state == 1:
            self.flying()
        elif self.state == 2:
            self.goal()
        elif self.state == 3:
            self.finish()
        else:
            self.state = 0
            
    def preparing(self):
        print('Now it is preparing state')
        self.LED_Pre.led_on()
        self.LED_Fly.led_off()
        self.LED_G.led_off()
        if self.preparingTime == 0:
            self.preparingTime = time.time()#現在の時刻を取得
            
        time.sleep(3)
        
        if not self.preparingTime == 0:
            if time.time() - self.preparingTime > self.cnst.LANDING_TIME_THRE:
                self.state = 1
                self.laststate = 1
    
    def flying(self):
        print('Now it is flying state')
        self.LED_Pre.led_off()
        self.LED_Fly.led_on()
        self.LED_G.led_off()
        if self.flyingTime == 0:
            self.flyingTime = time.time()#現在の時刻を取得
            
        time.sleep(3)
        
        if not self.flyingTime == 0:
            if time.time() - self.flyingTime > self.cnst.LANDING_TIME_THRE:
                self.state = 2
                self.laststate = 2

    def goal(self):
        self.LED_Pre.led_off()
        self.LED_Fly.led_off()
        self.LED_G.led_on()
        print('Judging goal..')
        if self.goalTime == 0:
            self.goalTime = time.time()#現在の時刻を取得
            
        time.sleep(3)
        
        if not self.goalTime == 0:
            if time.time() - self.goalTime > self.cnst.LANDING_TIME_THRE:
                self.state = 3
                self.laststate = 3
    
    def finish(self):
        print('GOAL!!')
        self.LED_Pre.led_off()
        self.LED_Fly.led_off()
        self.LED_G.led_off()
        self.LED_Pre.led_clean()
        sys.exit()
        
        