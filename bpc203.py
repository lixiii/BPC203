# BPC203 library

import serial
import math
from bcolours import BC
ser = serial.Serial()

# the following variables are obtained from the communication protocol and applies to the KST101
des = 0x50  # generic USB
source = 0x01  # host

# Initialisation
################
# WARNING
# The serial port is opened by this function. If the port is successfully opened, ensure that the port is closed before termination. 

def init( port = '/dev/serial/by-id/usb-Thorlabs_APT_Piezo_Controller_71837619-if00-port0'):
    ser.baudrate = 115200
    ser.port = port
    ser.open()
    if ser.is_open:
        print(BC.WARNING + "Serial port is open. Please ensure that port is closed before terminating the program." + BC.ENDC)

# Identify the controller and a particular channel by asking it to flash its screen
# Channel 1, 2 or 3
def identify(channel):
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    cmdIdentify = bytearray([ 0x23, 0x02, ] + int2byteArray(channel, 2) + [ des, source ])
    print(BC.OKGREEN + "Sending command 'MGMSG_MOD_IDENTIFY' to controller. " + BC.ENDC)
    ser.write(cmdIdentify)




def closePort():
    ser.close()






#########################
# Helper functions

def int2byteArray(inputInt, byteCount):
    return list( int(inputInt).to_bytes(byteCount, byteorder="little", signed=True) )