# ライブラリのインポート
import RPi.GPIO as GPIO
import wiringpi as pi
import time

# スイッチを接続したGPIOピンの定義
POWER_SW_PIN = 4

# モータードライバーを接続したGPIOピンの定義
IN1_MOTOR_PIN = 23
IN2_MOTOR_PIN = 24

# 各種設定
pi.wiringPiSetupGpio()
pi.pinMode( POWER_SW_PIN, pi.INPUT )
pi.pinMode( IN1_MOTOR_PIN, pi.OUTPUT )
pi.pinMode( IN2_MOTOR_PIN, pi.OUTPUT )
pi.pullUpDnControl( POWER_SW_PIN, pi.PUD_DOWN )

# モータードライバを接続したGPIOをPWM出力できるようにする
pi.softPwmCreate( IN1_MOTOR_PIN, 0, 100 )
pi.softPwmCreate( IN2_MOTOR_PIN, 0, 100 )

# モーターを停止した状態にする
pi.softPwmWrite( IN1_MOTOR_PIN, 0 )
pi.softPwmWrite( IN2_MOTOR_PIN, 0 )

# ボタンが押された回数を初期化
countPower = 0

# 正常処理
try:
    while True:
        # ボタンが押されたらif文内の処理を実行
        if ( pi.digitalRead( POWER_SW_PIN ) == pi.HIGH ):
            time.sleep( 0.5 )

            # ボタンが押された回数のカウントを1つ上げる
            countPower = countPower + 1

            # ボタンが押された回数によってモーターの制御を分岐
            if countPower % 5 == 1:
                pi.softPwmWrite( IN1_MOTOR_PIN, 0 )
                pi.softPwmWrite( IN2_MOTOR_PIN, 25 )
                print("微風")
            elif countPower % 5 == 2:
                pi.softPwmWrite( IN1_MOTOR_PIN, 0 )
                pi.softPwmWrite( IN2_MOTOR_PIN, 50 )
                print("弱風")
            elif countPower % 5 == 3:
                pi.softPwmWrite( IN1_MOTOR_PIN, 0 )
                pi.softPwmWrite( IN2_MOTOR_PIN, 75 )
                print("強風")
            elif countPower % 5 == 4:
                pi.softPwmWrite( IN1_MOTOR_PIN, 0 )
                pi.softPwmWrite( IN2_MOTOR_PIN, 100 )
                print("最大")
            else:
                pi.softPwmWrite( IN1_MOTOR_PIN, 100 )
                pi.softPwmWrite( IN2_MOTOR_PIN, 100 )
                print("停止\n")

            # スイッチのチャタリング防止
            while ( pi.digitalRead( POWER_SW_PIN ) == pi.LOW ):
                time.sleep( 0.1 )

            time.sleep( 0.1 )

# プログラム強制終了時にモーターを止める                        
except KeyboardInterrupt:
    pi.softPwmWrite( IN1_MOTOR_PIN, 0 )
    pi.softPwmWrite( IN2_MOTOR_PIN, 0 )
    print("Stop")