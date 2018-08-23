# BPC203 library

import serial
import math
from bcolours import BC
ser = serial.Serial()

verbose = False

# the following variables are obtained from the communication protocol and applies to the KST101
des = 0x50  # generic USB - addresses the entire controller
# but the BPC203 controller consists of three INDEPENDENT bays with only ONE freaking CHANNEL (ie. the controller has three channels because it has three independent bays and each bay has only one channel, so basically the channel identifier is useless)
bay = [0x21, 0x22, 0x23]

source = 0x01  # host


# from the datasheet
POS_SCALE_FACTOR = 32767
VOL_SCALE_FACTOR = 32767

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
        NOTE: This function currently does not work. 
    """
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    mode = 0x01 # open loop smooth
    if closedLoop:
        mode = 0x02 # closed loop smooth
    cmd = bytearray([ 0x40, 0x06, 0x01,  mode, bay[channel - 1], source ])
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
    cmd = bytearray([ 0x41, 0x06, 0x01, 0x00, bay[channel - 1], source ])
    if verbose: 
        print(cmd.hex())
    ser.write(cmd)
    resp = ser.read(6)
    if verbose: 
        print(resp.hex())
        print("Mode = " + str(resp[3]) )
    return resp[3]


def zero(channel):
    """
        This function zeros the piezo actuator associated with the channel
        At the end of the routine, the mode will be in closed loop. Call getMode to check that the mode is closed loop. 
    """
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")

    # ensure that channel is enabled by enabling it anyway
    enableChannel(channel)
    cmd = bytearray([ 0x58, 0x06, 0x01, 0x00, bay[channel - 1], source ])
    if verbose: 
        print(cmd.hex())
    print(BC.OKGREEN + "Sending command 'MGMSG_PZ_SET_ZERO' to controller for channel " + str(channel) + BC.ENDC)
    ser.write(cmd)

def zeroFinished(channel):
    """
        Checks if the zero routine has finished
        If the routine has finished, the mode will be set to closed loop
    """
    mode = getMode(channel)
    if mode == 0x02: 
        # closed loop mode
        return True
    return False

def position(channel, pos):
    """
        This function positions the DRV517 actuator to a position relative to the zero'ed position. The position parameter is in MICROMETERS
        
        NOTE: pos takes values from 0 to 30 micrometer, which is the maximum piezo travel. 
        NOTE: Also, the channel needs to have finished the zeroing routine. ENSURE that the zeroing routine is finished by checking the mode. Otherwise, this command is ignored by the unit. 
    """
    #error checking
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    if pos > 30 or pos < 0:
        raise ValueError("pos paramter needs to be smaller than 30 and larger than 0")
    if zeroFinished( channel ) == False:
        raise RuntimeError("The zeroing routine has not finished. The position command will be ignored. ")

    posScaled = pos / 30 * POS_SCALE_FACTOR
    cmd = bytearray([ 0x46, 0x06, 0x04, 0x00, 0x80 | bay[channel - 1], source, 0x01, 0x00] + int2byteArray(posScaled, 2))
    if verbose: 
        print(cmd.hex())
    print(BC.OKGREEN + "Sending command 'MGMSG_PZ_SET_OUTPUTPOS' to controller for channel " + str(channel) + BC.ENDC)
    ser.write(cmd)
    
def getPosition(channel):
    """
        This function requests the position of a channel and converts the result into nanometers. It assumes that a DRV517 is used with a maximum trabel of 30 um. 
        
        This function returns the position in integer nanometer.
    """
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    cmd = bytearray([ 0x47, 0x06, 0x01, 0x00, bay[channel - 1], source ])
    if verbose: 
        print(cmd.hex())
    ser.write(cmd)
    resp = ser.read(10)
    # convert into micrometer
    posMSB = list(resp[-2:])[1]
    posLSB = list(resp[-2:])[0]
    pos = int ( ( posMSB * 256 + posLSB ) / POS_SCALE_FACTOR * 30 * 1000 )
    print(BC.OKBLUE + "Position of channel " + str(channel) + " = " + str(pos) + " nanometers " + BC.ENDC )
    return pos



def setOutputVoltage(channel, voltage):
    if channel != 1 and channel != 2 and channel != 3:
        raise ValueError("Channel needs to be 1, 2 or 3")
    if voltage > 100 or voltage < 0:
        raise ValueError("voltage paramter needs to be smaller than 100 percent and larger than 0")

    volScaled = voltage / 100 * VOL_SCALE_FACTOR
    cmd = bytearray([ 0x43, 0x06, 0x04, 0x00, 0x80 | bay[channel - 1], source, 0x01, 0x00] + int2byteArray(volScaled, 2))
    if verbose: 
        print(cmd.hex())
    print(BC.OKGREEN + "Sending command 'MGMSG_PZ_SET_OUTPUTVOLTS' to controller for channel " + str(channel) + BC.ENDC)
    ser.write(cmd)

def getEnableState(channel):
    ser.write( bytearray([ 0x11, 0x02, 0x01, 0x00, bay[channel - 1], source ]) )
    resp = ser.read(6)
    print(" enabled state is " + str(resp[3]))
    # an enable state of 2 is disable
    if verbose:
        print(resp.hex())

def enableChannel(channel):
    ser.write( bytearray([ 0x10, 0x02, 0x01, 0x01, bay[channel - 1], source ]) )

def disableChannel(channel):
    ser.write( bytearray([ 0x10, 0x02, 0x01, 0x02, bay[channel - 1], source ]) )

def closePort():
    ser.close()



#########################
# Helper functions

def int2byteArray(inputInt, byteCount):
    return list( int(inputInt).to_bytes(byteCount, byteorder="little", signed=True) )