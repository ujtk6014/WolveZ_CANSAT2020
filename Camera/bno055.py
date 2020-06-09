import logging
import sys
import time

import BNO055

bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

class Bno055(object):
    
    def __init__(self):
        self.Ax=0.0
        self.Ay=0.0
        self.Az=0.0
        self.gx=0.0
        self.gy=0.0
        self.gz=0.0
        
        
    def setupBno(self):
        # Enable verbose debug logging if -v is passed as a parameter.
        if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
            logging.basicConfig(level=logging.DEBUG)

        # Initialize the BNO055 and stop if something went wrong.
        if not bno.begin():
            raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

        # Print system status and self test result.
        status, self_test, error = bno.get_system_status()
        print('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # Print out an error if system status is in error mode.
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')

        # Print BNO055 software revision and other diagnostic data.
        sw, bl, accel, mag, gyro = bno.get_revision()
        print('Software version:   {0}'.format(sw))
        print('Bootloader version: {0}'.format(bl))
        print('Accelerometer ID:   0x{0:02X}'.format(accel))
        print('Magnetometer ID:    0x{0:02X}'.format(mag))
        print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
    
    def readlinearaccel(self):
        #global Ax,Ay,Az
        self.Ax,self.Ay,self.Az = bno.read_linear_acceleration()
        #print('Ax=',ax,',Ay=',ay,',Az=',az)
    
    def readgravity(self):
        #global gx,gy,gz
        self.gx,self.gy,self.gz = bno.read_gravity()
        #print('Gx=',gx,',Gy=',gy,',Gz=',gz)
        
