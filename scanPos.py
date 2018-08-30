# This example script scans the actuaros from zero position to maximum position sequentially from channel 1 to 3
import bpc203 as bpc
import time

########################################################################################################
# NOTE THAT CHANNEL THREE OF THE CONTROLLER AT THE LAB IS BROKEN AS IT DOES NOT SUPPORT CLOSED LOOP MODE 
########################################################################################################

bpc.init()
bpc.zero(1)
bpc.zero(2)

# now check for zeroing completion
while bpc.zeroFinished(1) != True and bpc.zeroFinished(2) != True:
    # resend status check every 0.5s
    time.sleep(0.5)

print("Scanning channel 1 actuator from 0 um to 30um")
for i in range(31):
    bpc.position(1, i)
    time.sleep(0.1)

print("Scanning channel 2 actuator from 0 um to 30um")
for i in range(31):
    bpc.position(2, i)
    time.sleep(0.1)

print("Scanning channel 3 actuator from 0 um to 30um")
for i in range(100):
    bpc.setOutputVoltage(3, i)
    time.sleep(0.1)

print("Returning channel 1 actuator back to origin")
for i in range(30, 0, -1):
    bpc.position(1, i)
    time.sleep(0.1)

print("Returning channel 2 actuator back to origin")
for i in range(30, 0, -1):
    bpc.position(2, i)
    time.sleep(0.1)

print("Returning channel 3 actuator back to origin")
for i in range(100, 0, -1):
    bpc.setOutputVoltage(3, i)
    time.sleep(0.1)

print("Task complete. Closing connection")
bpc.close()