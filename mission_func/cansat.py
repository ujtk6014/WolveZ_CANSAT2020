"""
Keio Wolve'Z cansat2020
mission function
Author Yuji Tanaka
date:2020/05/26
"""
#ライブラリの読み込み
import time
import RPi.GPIO as GPIO

#クラス読み込み
import constant as ct
import camera
import gps
import motor
import radio
import ultrasonic
import bno055
import led

class Cansat(object):
    
    def __init__(self):
        #オブジェクトの生成
        self.rightmotor = motor.motor(ct.const.RIGHT_MOTOR_VREF_PIN,ct.const.RIGHT_MOTOR_IN1_PIN,ct.const.RIGHT_MOTOR_IN2_PIN)
        self.leftmotor = motor.motor(ct.const.LEFT_MOTOR_VREF_PIN,ct.const.LEFT_MOTOR_IN1_PIN,ct.const.LEFT_MOTOR_IN2_PIN)
        self.gps = gps.GPS()
        self.bno055 = bno055.BNO()
        self.radio = radio.radio()
        self.ultrasonic = ultrasonic.Ultrasonic()
        self.RED_LED = led.led(ct.const.RED_LED_PIN)
        self.BLUE_LED = led.led(ct.const.BLUE_LED_PIN)
        self.GREEN_LED = led.led(ct.const.GREEN_LED_PIN)
        
        #開始時間の記録
        self.startTime = time.time()
        self.timer = 0
        
        #変数
        self.state = 0
        self.laststate = 0
        
        #stateに入っている時刻の初期化
        self.preparingTime = 0
        self.flyingTime = 0
        self.droppingTime = 0
        self.landingTime = 0
        self.waitingTime = 0
        self.runningTime = 0
        self.goalTime = 0
        
        #state管理用変数初期化
        self.countPreLoop = 0
        self.countFlyLoop = 0
        self.countDropLoop = 0
        self.countGoal = 0
        
        #GIOP設定
        GPIO.setmode(GPIO.BCM) #GPIOの設定
        GPIO.setup(ct.const.FLIGHTPIN_PIN,GPIO.IN) #フライトピン用
        GPIO.setup(ct.const.BURNING_PIN,GPIO.OUT) #焼き切り用のピンの設定
    
    def setup(self):
        gps.setupGps()
        bno055.setupBno()
        radio.setupRadio()
        ultrasonic.setupUltrasonic()
        
    def sensor(self):
        self.gps.gpsread()
        self.bno055.bnoread()
        self.ultrasonic.getDistance()
        self.writeData()#txtファイルへのログの保存
        if not self.state == 1 and not self.state == 2: #preparingとflyingのときは電波を発しない
            self.sendRadio()#LoRaでログを送信
    
    def writeData(self):
        self.timer = 1000*(time.time() - self.startTime) #経過時間 (ms)
        self.timer = int(timer)
        #ログデータ作成。\マークを入れることで改行してもコードを続けて書くことができる
        datalog = str(self.timer) + ","\
                  + str(self.state) + ","\
                  + str(self.gps.Time) + ","\
                  + str(self.gps.Lat) + ","\
                  + str(self.gps.Lon) + ","\
                  + str(self.bno055.gx) + ","\
                  + str(self.bno055.gy) + ","\
                  + str(self.bno055.gz) + ","\
                  + str(self.bno055.Ax) + ","\
                  + str(self.bno055.Ay) + ","\
                  + str(self.bno055.Az) + ","\
                  + str(self.ultrasonic.distance) + ","\
                  + str(self.rightmotor.velocity) + ","\
                  + str(self.leftmotor.velocity)
        
        with open("test.txt",mode = 'a') as test: # [mode] x:ファイルの新規作成、r:ファイルの読み込み、w:ファイルへの書き込み、a:ファイルへの追記
            test.write(datalog + '\n')
          
    def sendRadio(self):
        datalog = str(self.timer) + ","\
                  + str(self.state) + ","\
                  + str(self.gps.Time) + ","\
                  + str(self.gps.Lat) + ","\
                  + str(self.gps.Lon) + ","\
                  + str(self.bno055.gx) + ","\
                  + str(self.bno055.gy) + ","\
                  + str(self.bno055.gz) + ","\
                  + str(self.ultrasonic.distance) + ","\
                  + str(self.rightmotor.velocity) + ","\
                  + str(self.leftmotor.velocity)
        self.radio.sendData(datalog) #データを送信
    
    def sequence(self):
        if self.state == 0:
            self.preparing()
        elif self.state == 1:
            self.flying()
        elif self.state == 2:
            self.dropping()
        elif self.state == 3:
            self.landing()
        elif self.state == 4:
            self.waiting()
        elif self.state == 5:
            self.running()
        elif self.state == 6:
            self.goal()
        else:
            self.state = self.laststate #どこにも引っかからない場合何かがおかしいのでlaststateに戻してあげる
    
    def preparing(self):#フライトピンを使う場合はいらないかも（暫定：時間が立ったら移行）
        if self.preparingTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            self.preparingTime = time.time()
            self.RED_LED.led_on()
            self.BLUE_LED.led_off()
            self.GREEN_LED.led_off()
            
        self.rightmotor.stop()
        self.leftmotor.stop()
        #self.countPreLoop+ = 1
        if not self.preparingTime == 0:
            if time.time() - self.preparingTime > ct.const.PREPARING_TIME_THRE:
                self.state = 1
                self.laststate = 1
    
    def flying(self):#フライトピンが外れたのを検知して次の状態へ以降
        if self.flyingTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            self.flyingTime = time.time()
            self.RED_LED.led_off()
            self.BLUE_LED.led_off()
            self.GREEN_LED.led_off()
            
        self.rightmotor.stop()
        self.leftmotor.stop()
        if GPIO.input(ct.const.FLIGHTPIN_PIN) == GPIO.HIGH:#highかどうか＝フライトピンが外れているかチェック
            self.countFlyLoop+=1
            if self.countFlyLoop > ct.const.COUNT_FLIGHTPIN_THRE:#一定時間HIGHだったらステート移行
                self.state = 2
                self.laststate = 2
        else:
            self.countFlyLoop = 0 #何故かLOWだったときカウントをリセット
                
    def dropping(self):
        if self.droppingTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            self.droppingTime = time.time()
            self.RED_LED.led_off()
            self.BLUE_LED.led_on()
            self.GREEN_LED.led_off()
            
        if (pow(bno055.Ax,2) + pow(bno055.Ay,2) + pow(bno055.Az,2)) < pow(self.ACC_THRE,2):#加速度が閾値以下で着地判定
            self.countDropLoop+=1
            if self.countDropLoop > ct.const.COUNT_ACC_LOOP_THRE:
                self.state = 3
                self.laststate = 3
        else:
            self.countDropLoop = 0 #初期化の必要あり
        """
        #時間で着地判定
        if not self.droppingTime == 0:
            if time.time() - self.droppingTime > ct.const.LANDING_TIME_THRE:
                self.state = 3
                self.laststate = 3
        """
        
    def landing(self):
        if self.landingTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            self.landingTime = time.time()
            self.RED_LED.led_off()
            self.BLUE_LED.led_off()
            self.GREEN_LED.led_on()
            
        GPIO.output(self.RELEASING_PIN,HIGH)
        
        if not self.landingTime == 0:
            if time.time()-self.landingTime > ct.const.RELEASING_TIME_THRE:
                GPIO.output(ct.const.RELEASING_PIN,LOW) #焼き切りが危ないのでlowにしておく
                self.state = 4
                self.laststate = 4
            
    def waiting(self):
        if self.waitingTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            GPIO.output(ct.const.RELEASING_PIN,LOW) #焼き切りしっぱなしでは怖いので保険
            self.waitingTime = time.time()
            self.RED_LED.led_off()
            self.BLUE_LED.led_on()
            self.GREEN_LED.led_on()
        #以下に超音波センサによる動的物体発見プログラム
            
        if #動的物体の認知反転の完了
            self.state = 5
            self.laststate = 5
    
    def running(self):
        if self.runningTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            self.runningTime = time.time()
            self.RED_LED.led_on()
            self.BLUE_LED.led_on()
            self.GREEN_LED.led_on()
            
        #以下に画像処理走行プログラム
        
        if #見失い判定
            self.state = 4
            self.laststate = 4
            
        if #終了判定
            self.state = 6
            self.laststate = 6
    
    def goal(self):
        if self.goalTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            self.goalTime = time.time()
            self.RED_LED.led_off()
            self.BLUE_LED.led_off()
            self.GREEN_LED.led_off()
            
        if self.countGoal < ct.const.COUNT_GOAL_LOOP_THRE:
            self.rightmotor.stopSlowly()
            self.leftmotor.stopSlowly()
        else:
            self.rightmotor.stop()
            self.leftmotor.stop()
        self.countGoal+ = 1
            
if __name__ == "__main__":
    pass
