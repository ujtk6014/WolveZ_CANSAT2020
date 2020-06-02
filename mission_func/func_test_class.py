import time
import constant as ct
import led_class
import sys
import datetime
global start_time

class simpleFunc():
    
    def __init__(self):
        #オブジェクト生成
        self.LED_Pre = led_class.led(ct.const.RED_LED_PIN)
        self.LED_Fly = led_class.led(ct.const.BLUE_LED_PIN)
        self.LED_G = led_class.led(ct.const.GREEN_LED_PIN)
        self.state = 0
        self.preparingTime = 0
        self.flyingTime = 0
        self.goalTime = 0
        self.startTime = time.time()
    
    def sensor(self): #センサーの値の読み取り
        #データの読み込み
        #gps.readgps()など
        self.writeData()
        #if not self.state == 2:
        #    sendRadio()
    
    def writeData(self): #txtファイルへの書き込み
        timer = 1000*(time.time() - self.startTime) #経過時間 (ms)
        timer = int(timer)
        """
        dt_now = str(datetime.datetime.now()) #現在の日付の取得
        dt_now = dt_now[0:19] #いらないところを切り取る
        """
        #ログデータ作成。\マークを入れることで改行してもコードを続けて書くことができる
        datalog = str(timer) + ","\
                  + str(self.state) + ","\
                  + str(self.LED_Pre.led_status) + ","\
                  + str(self.LED_Fly.led_status) + ","\
                  + str(self.LED_G.led_status)
        """
        try: #ファイルが存在しない場合は新規ファイルの作成
            with open("Test.txt",mode = 'w') as test: #with関数でclose作業を省略
               test.write(datalog + '\n')
        except FileExistsError: #ファイルが存在する場合は追記する
        """
        with open("test.txt",mode = 'a') as test: # [mode] x:ファイルの新規作成、r:ファイルの読み込み、w:ファイルへの書き込み、a:ファイルへの追記
            test.write(datalog + '\n')
          
    def sequence(self):
        if self.state == 0:#初期化の必要あり←initで初期化
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
        if self.preparingTime == 0:
            self.LED_Pre.led_on()
            self.LED_Fly.led_off()
            self.LED_G.led_off()
            self.preparingTime = time.time()#現在の時刻を取得
        
        if not self.preparingTime == 0:
            if time.time() - self.preparingTime > ct.const.LANDING_TIME_THRE:
                self.state = 1
                self.laststate = 1
    
    def flying(self):
        print('Now it is flying state')
        if self.flyingTime == 0:
            self.LED_Pre.led_off()
            self.LED_Fly.led_on()
            self.LED_G.led_off()
            self.flyingTime = time.time()#現在の時刻を取得
        
        if not self.flyingTime == 0:
            if time.time() - self.flyingTime > ct.const.LANDING_TIME_THRE:
                self.state = 2
                self.laststate = 2

    def goal(self):
        print('Judging goal..')
        if self.goalTime == 0:
            self.LED_Pre.led_off()
            self.LED_Fly.led_off()
            self.LED_G.led_on()
            self.goalTime = time.time()#現在の時刻を取得
        
        if not self.goalTime == 0:
            if time.time() - self.goalTime > ct.const.LANDING_TIME_THRE:
                self.state = 3
                self.laststate = 3
    
    def finish(self):
        print('GOAL!!')
        self.LED_Pre.led_off()
        self.LED_Fly.led_off()
        self.LED_G.led_off()
        self.LED_Pre.led_clean()
        sys.exit()
        
        