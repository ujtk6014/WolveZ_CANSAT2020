import const

#ピン番号の指定
const.LEFT_MOTOR_VREF_PIN = 13
const.LEFT_MOTOR_IN1_PIN = 5
const.LEFT_MOTOR_IN2_PIN = 6
const.RIGHT_MOTOR_VREF_PIN = 12
const.RIGHT_MOTOR_IN1_PIN = 20
const.RIGHT_MOTOR_IN2_PIN = 21
const.RED_LED_PIN = 7
const.BLUE_LED_PIN = 24
const.GREEN_LED_PIN = 8
const.RELEASING_PIN = 26
const.FLIGHTPIN_PIN = 4
const.ULTRASONIC_TRIG = 18 # GPIO02(Pin3)
const.ULTRASONIC_ECHO = 23 # GPIO03(Pin5)

#閾値
const.PREPARING_TIME_THRE = 10
const.FLYING_TIME_THRE = 10
const.ACC_THRE = 1
const.COUNT_ACC_LOOP_THRE = 400
const.COUNT_FLIGHTPIN_THRE = 300
const.LANDING_TIME_THRE = 5
const.RELEASING_TIME_THRE = 30
const.PRE_MOTOR_TIME_THRE = 5
const.COUNT_GOAL_LOOP_THRE = 50
const.DISTANCE_THRE_START=300.0#以下4つは超音波センサの閾値
const.COUNT_DISTANCE_LOOP_THRE_START=10
const.DISTANCE_THRE_END=70.0
const.DISTANCE_COUNT_LIMIT = 2
const.COUNT_DISTANCE_LOOP_THRE_END=20
const.AREA_THRE_END=20000#以下7つはカメラに関する閾値
const.COUNT_AREA_LOOP_THRE_END=30
const.AREA_THRE_LOSE=1000
const.COUNT_AREA_LOOP_THRE_LOSE=15
const.AREA_THRE_START=2500
const.COUNT_AREA_LOOP_THRE_START=5
const.COG_THRE_START=10000
const.MAX_CAMERA_ANGLE=62.2
const.CAMERA_GAIN=1
const.REFOLLOW_THRE=2#再探索の際のモーターへの指令数
const.BLACKLIGHT_SD_UP=60#以下3つはガンマ補正に関する閾値
const.BLACKLIGHT_SD_DOWN=40
const.GAMMA=1.8
