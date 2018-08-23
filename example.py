# Example program to setup the controller and position channel one to 5 um and channel 2 to 6um.
import bpc203 as bpc
import time
bpc.init()
bpc.zero(1)
bpc.zero(2)

# now check for zeroing completion
while bpc.zeroFinished(1) != True and bpc.zeroFinished(2) != True:
    # resend status check every 0.5s
    time.sleep(0.5)

bpc.position(1, 5)
bpc.position(2, 6)

# wait for motion to complete as the controller does not provide a function to achieve that
time.sleep(1)
bpc.getPosition(1)
bpc.getPosition(2)

bpc.closePort()
