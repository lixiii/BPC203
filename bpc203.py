# BPC203 library

import serial
import math
from bcolours import BC
ser = serial.Serial()

verbose = False

# the following variables are obtained from the communication protocol and applies to the KST101
des = 0x50  # generic USB
source = 0x01  # host


def init( port = '/dev/serial/by-id/usb-Thorlabs_APT_Piezo_Controller_71837619-if00-port0', Verbose = False):
    """
        Initialisation
        ################
        WARNING
        The serial port is opened by this function. If the port is successfully opened, ensure that the port is closed before termination. 
    """
    verbose = Verbose
    ser.baudrate = 115200
    ser.port = port
    ser.open()
    if ser.is_open:
        print(BC.WARNING + "Serial port is open. Please ensure that port is closed before terminating the program." + BC.ENDC)

def identify(channel):
    """
        Identify the controller and a particular channel by asking it to flash its screen
        Parameter:  Channel 1, 2 or 3
    """
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    cmdIdentify = bytearray([ 0x23, 0x02, ] + int2byteArray(channel, 2) + [ des, source ])
    print(BC.OKGREEN + "Sending command 'MGMSG_MOD_IDENTIFY' to controller. " + BC.ENDC)
    ser.write(cmdIdentify)

def setMode(channel, closedLoop = True):
    """
        This function sets the particular channel to a closed loop mode (0x04: closed loop smooth, a smooth transition to closed loop mode to minimise voltage peaks)
    """
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    mode = 0x01 # open loop smooth
    if closedLoop:
        mode = 0x02 # closed loop smooth
    cmd = bytearray([ 0x40, 0x06 ] + int2byteArray(channel, 1) + [ mode, des, source ])
    if verbose: 
        print(cmd.hex())
    print(BC.OKGREEN + "Sending command 'MGMSG_PZ_SET_POSCONTROLMODE' to controller for channel " + str(channel) + BC.ENDC)
    ser.write(cmd)

def getMode(channel):
    """
        Requests the current mode from the controller
    """
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    cmd = bytearray([ 0x41, 0x06] + int2byteArray(channel, 1) + [ 0x00, des, source ])
    if verbose: 
        print(cmd.hex())
    print(BC.OKGREEN + "Sending command 'MGMSG_PZ_SET_ZERO' to controller for channel " + str(channel) + BC.ENDC)
    ser.write(cmd)
    resp = ser.read(6)
    if verbose: 
        print(resp.hex())
    print("Mode = " + str(resp[3]) )


def zero(channel):
    """
        This function zeros the piezo actuator associated with the channel
        At the end of the routine, the mode will be in closed loop. Call getMode to check that the mode is closed loop. 
    """
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    cmd = bytearray([ 0x58, 0x06, ] + int2byteArray(channel, 1) + [ 0x00, des, source ])
    if verbose: 
        print(cmd.hex())
    print(BC.OKGREEN + "Sending command 'MGMSG_PZ_SET_ZERO' to controller for channel " + str(channel) + BC.ENDC)
    ser.write(cmd)


def closePort():
    ser.close()






#########################
# Helper functions

def int2byteArray(inputInt, byteCount):
    return list( int(inputInt).to_bytes(byteCount, byteorder="little", signed=True) )