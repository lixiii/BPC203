# Example programme to interactively controll the actuators
import bpc203 as bpc
import time
bpc.init(Verbose=True)
bpc.zero(1)
bpc.zero(2)

# now check for zeroing completion
while bpc.zeroFinished(1) != True and bpc.zeroFinished(2) != True:
    # resend status check every 0.5s
    time.sleep(0.5)

# As of September 13, Channel 1 = vertical position of fiber, Channel 2 = direction along 1D array, Channel 3 = axis of fiber 
i1 = 1
i2 = 0
while i2 != "c":
    i2 = input("Enter c to close connection and reset controller. Enter cc to select channel. Enter a number to position channel {} (unit nanometer): ".format(i1) )
    if i2 == "cc":
        i1 = int(input("Input channel or use current value: ") or i1)
        i2 = int(input("Enter position of channel {}: ".format(i1)))
    if i2 != "c":
        i2 = int(i2)
        bpc.position(i1, i2)

bpc.close()
