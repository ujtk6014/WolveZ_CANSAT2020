"""
Keio Wolve'Z cansat2020
mission function
Author Yuji Tanaka
date:2020/05/26
"""
#ライブラリの読み込み
import time
import RPi.GPIO as GPIO
import sys
import cv2
import numpy

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
        self.gps = gps.Gps()
        self.bno055 = bno055.BNO055()
        self.radio = radio.radio()
        self.ultrasonic = ultrasonic.Ultrasonic()
        self.RED_LED = led.led(ct.const.RED_LED_PIN)
        self.BLUE_LED = led.led(ct.const.BLUE_LED_PIN)
        self.GREEN_LED = led.led(ct.const.GREEN_LED_PIN)
        self.camera=camera.Camera()
        
        #開始時間の記録
        self.startTime = time.time()
        self.timer = 0
        self.timestep=0#写真撮影用
        
        #変数
        self.state = 0
        self.laststate = 0
        self.following=0 # state1の中で、カメラによる検知中か追従中かを区別、どちらもカメラを回しながら行いたいため
        
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
        self.countAreaLoopEnd=0 # 終了判定用
        self.countAreaLoopStart=0 # 開始判定用
        self.countAreaLoopLose=0 # 見失い判定用
        self.countDistanceLoopStart=0 # 距離による開始判定
        self.countDistanceLoopEnd=0 # 距離による終了判定
        
        #GIOP設定
        GPIO.setmode(GPIO.BCM) #GPIOの設定
        GPIO.setup(ct.const.FLIGHTPIN_PIN,GPIO.IN) #フライトピン用
        GPIO.setup(ct.const.RELEASING_PIN,GPIO.OUT) #焼き切り用のピンの設定
    
    def setup(self):
        gps.setupGps()
        radio.setupRadio()
        bno055.setupBno()
        if self.bno055.begin() is not True:
            print("Error initializing device")
            exit()
        
    def sensor(self):
        self.gps.gpsread()
        self.bno055.bnoread()
        self.ultrasonic.getDistance()
        self.writeData()#txtファイルへのログの保存
        if not self.state == 1 and not self.state == 2: #preparingとflyingのときは電波を発しない
            self.sendRadio()#LoRaでログを送信
    
    def writeData(self):
        self.timer = 1000*(time.time() - self.startTime) #経過時間 (ms)
        self.timer = int(self.timer)
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
                  + str(self.ultrasonic.dist) + ","\
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
                  + str(self.ultrasonic.dist) + ","\
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
            
        if (pow(self.bno055.Ax,2) + pow(self.bno055.Ay,2) + pow(self.bno055.Az,2)) < pow(ct.const.ACC_THRE,2):#加速度が閾値以下で着地判定
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
        if self.ultrasonic.dist<ct.const.DISTANCE_THRE_START:
            self.countDistanceLoopStart+=1
            if self.countDistanceLoopStart>ct.const.COUNT_DISTANCE_LOOP_THRE_START:
                print("対象認知＆カメラ処理開始")
                self.state=5
                self.laststate=5
                self.countDistanceLoopStart=0
        else:
            self.countDistanceLoopStart=0
    
    def running(self):
        if self.runningTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            self.runningTime = time.time()
            self.RED_LED.led_on()
            self.BLUE_LED.led_on()
            self.GREEN_LED.led_on()
            
        #以下に画像処理走行プログラム
        
        #写真撮影用
        self.timestep+=1
        
        _, frame = self.capture.read() # 動画の読み込み
        # frame=cv2.resize(frame, (640,480)) # プレビューサイズ（いじらなくてよい）
        rects = self.camera.find_rect_of_target_color(frame) # 矩形の情報作成
        
        # 一定間隔で状況を撮影
        if self.timestep%200==0:
            imName=str(self.timestep)+'image.jpg'
            cv2.imwrite(imName,frame)
        
        if len(rects) > 0:
            rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
            
            #各パラメータの計算
            self.camera.find_center_of_gravity(rect) # 重心の計算
            self.camera.find_angle(self.camera.cgx) # 角度の計算、絶対値
            self.camera.find_direction(self.camera.cgx) # 進む方向
            self.camera.find_area(rect) # 矩形の面積算出
            
            #追従開始判定
            if self.following==0 and self.camera.area>ct.const.AREA_THRE_START:
                self.countAreaLoopStart+=1
                if self.countAreaLoopStart==1:
                    self.camera.cgxs=self.camera.cgx
                    self.camera.cgys=self.camera.cgy
                if self.countAreaLoopStart>ct.const.COUNT_AREA_LOOP_THRE_START:
                    if pow(self.camera.cgx-self.camera.cgxs,2)+pow(self.camera.cgy-self.camera.cgys,2)>ct.const.COG_THRE_START:
                        print("追従開始")
                        self.following=1
                        self.countAreaLoopStart=0
            else:
                self.countAreaLoopStart=0
            
            #モーターへの指示を行う
            if self.following==1:
                #print('モーターへの指示')
                if self.camera.direct==0:
                    print('right motor:', 100)
                    print('left motor:', 100)
                if self.camera.direct==1:
                    print('right motor:', round(100*(1-self.camera.angle/180)))
                    print('left motor:', 100)
                if self.camera.direct==-1:
                    print('right motor:', 100)
                    print('left motor:', round(100*(1-self.camera.angle/180)))
                #ここにモーターへの指示内容をかく！
            
            #見失い判定
            if self.following==1 and self.camera.area<ct.const.AREA_THRE_LOSE:
                self.countAreaLoopLose+=1
                if self.countAreaLoopLose>ct.const.COUNT_AREA_LOOP_THRE_LOSE:
                    self.state=4
                    self.laststate=4
                    self.countAreaLoopLose=0
                    self.following=0
                    print('見失った！')
                    cv2.destroyAllWindows()
            else:
                self.countAreaLoopLose=0
          
            #超音波センサを用いた終了判定
            #self.ultrasonic.getDistance()
            if self.following==1 and self.ultrasonic.dist<ct.const.DISTANCE_THRE_END:
                self.countDistanceLoopEnd+=1
                if self.countDistanceLoopEnd>ct.const.COUNT_DISTANCE_LOOP_THRE_END:
                    print("追従終了")
                    cv2.imwrite('finish.jpg',frame)
                    self.state=6
                    self.lastsate=6
            else:
                self.countDistanceLoopEnd=0
            #矩形の面積を用いた終了判定
            """
            if self.camera.area>ct.const.AREA_THRE_END:
                self.countAreaLoopEnd+=1
                if self.countAreaLoopEnd>ct.const.COUNT_AREA_LOOP_THRE_END:
                    break
            else:
                self.countAreaLoopEnd=0
            """
            
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) # フレームを生成
        cv2.drawMarker(frame,(self.camera.cgx,self.camera.cgy),(60,0,0))
        cv2.imshow('red', frame)
        cv2.waitKey(1)
        
        #画面に赤い要素が全くない場合の見失い判定
        if self.following==1 and len(rects)==0:
            self.countAreaLoopLose+=1
            if self.countAreaLoopLose>ct.const.COUNT_AREA_LOOP_THRE_LOSE:
                self.state=4
                self.laststate=4
                self.countAreaLoopLose=0
                self.following=0
                print('見失った2！')
                cv2.destroyAllWindows()

    
    def goal(self):
        if self.goalTime == 0:#時刻を取得してLEDをステートに合わせて光らせる
            self.goalTime = time.time()
            self.RED_LED.led_off()
            self.BLUE_LED.led_off()
            self.GREEN_LED.led_off()
            
        if self.countGoal < ct.const.COUNT_GOAL_LOOP_THRE:
            self.rightmotor.stopslowly()
            self.leftmotor.stopslowly()
        else:
            self.rightmotor.stop()
            self.leftmotor.stop()
        self.countGoal+ = 1
        
        if self.goalTime==0:
            self.capture.release()
            cv2.destroyAllWindows()
            
        #sys.exit()
            
if __name__ == "__main__":
    pass
