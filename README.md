# Wolve'Z CANSAT2020
Mission code in Python for Keio Wolve'Z CaSat project 2020

## Description: About our CanSat
  CanSat is a small satellite sized approximately as small as soda can.
  Our ultimate goal is to develop an autonomous tracking rover which is able to recognize a moving object such as humans or the other rover and chase it until it stops. This rover would be beneficial when it comes to space exploration, especially when building a base on the other planet, where there would be very few people. We can use it as carrier robot for example, when carring something from one point to another. We are hoping this rover would cooperate with humans and make human space activity more efficiant.
  
  We are assuming a rover which has LRF and optimal camera. Autonomous tracking is accomplished by the combination of image processing and distance and direction recognition by LRF. Considerring the CanSat regulation, we are making a rover which has ultrasonic sensor and camera in order to realize autonomous tracking.

<div align="center">
<img src="https://user-images.githubusercontent.com/57528969/90110593-6fd8ee80-dd88-11ea-88c2-6b1f03e266d6.png" width="45%" title="Our CanSat">
</div>

## Table of Contents
- [Our Mission](#Our-Mission)
  - [Human Following Robot](#Human-Following-Robot)
  - [Mission Sequence](#Mission-Sequence)
  - [Image Processing](#Image-Processing)
- [Hardware Requirements](#Hardware-Requirements)
- [Software Requirements](#Software-Requirements)
- [Usage](#usage)
- [Project Member](#Project-Member)

## Our Mission
### Human Following Robot
### Mission Sequence
### Image Processing

## Hardware Requirements
- Microcomputer
  - Raspberry Pi 3B+
- Sensors
    
    |**Sensor**|**Products**|**image**|
    |:---|:---:|:---:|
    |Camera|[Raspberry Pi Camera Module V2](http://akizukidenshi.com/catalog/g/gM-10518/)|<img src="https://user-images.githubusercontent.com/57528969/90113840-dfe97380-dd8c-11ea-8b1c-cac55b4aa5ee.png" width="20%">|
    |Ultrasonic sensor|[HC-SR04](http://akizukidenshi.com/catalog/g/gM-11009/)|<img src="https://user-images.githubusercontent.com/57528969/90114657-fcd27680-dd8d-11ea-9fe1-95e3e4e484da.png" width="20%">|
    |Communication Module|[ES920LR](https://easel5.com/products/es920lr/)|<img src="https://user-images.githubusercontent.com/57528969/90114355-92b9d180-dd8d-11ea-8565-76540eea0920.png" width="20%">|
    |GPS module|[GYSFDMAXB](http://akizukidenshi.com/catalog/g/gK-09991/)|<img src="https://user-images.githubusercontent.com/57528969/90114335-89c90000-dd8d-11ea-82d3-70ab748fa5f2.png" width="20%">|
    |Accelaration Sensor|[BNO055](https://www.switch-science.com/catalog/5511/)|<img src="https://user-images.githubusercontent.com/57528969/90114534-ce549b80-dd8d-11ea-81fd-3569fe0b1477.png" width="20%">|
    |Motor|comming soon...||
    |Motor Driver|[TA7291P](https://toshiba.semicon-storage.com/jp/semiconductor/product/motor-driver-ics/brushed-dc-motor-driver-ics/detail.TA7291P.html)||

## Software Requirements
Firstly, you need to clone this repository
```
git clone https://github.com/ujtk6014/WolveZ_CANSAT2020.git
```
### Setups
1. **OpenCV**  
  OpenCV is necessary for implimenting image processing in order to recognize following target. Go to `setup` folder and run `inst_opencv.sh` to install opencv
  ```
  bash inst_opencv.sh
  ```
  Check in python wether you successflly installed opencv
  ```Python
  import cv2
  ```

2. **GPS Setup**  
  The proposed robot orients itself by GPS. Type this in terminal.
  ```
  bash setup_gps.sh
  ```

3. **I2C Setup**  
  I2C is one of the ways of serial communication. This is necessary for BNO055 (acceralation sensor)
  ```
  bash setup_i2c.sh
  ```

4. **Access Point Setup (Additional)**  
  if you want to use Raspberry Pi remotely in **No Wi-fi** environment, you may want to use your Rasberry Pi as Wi-fi access point. Then go to `setup/ap` and run `setup_ap.sh`
  ```
  sudo bash setup_ap.sh
  ```
  Once you activate access point, you cannot connect your Raspberry Pi to other Wi-fi networks. So you can turn it off by
  ```
  sudo bash ap_off.sh
  ```
  If you want to re-activate, then
  ```
  sudo bash ap_on.sh
  ```
## Usage
### Algorithm
comming soon... 

## Project Member
- Project manager: 
  Yuki Ko
- Software: 
  Yuji Tanaka, Yuki Ko, Kazuki Oshima, Hikaru Kimura, Miyuki Nakamura
- Hardware: 
  Mina Park, Shinichiro Kaji
