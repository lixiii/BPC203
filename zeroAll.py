import bpc203 as bpc
bpc.init()
bpc.setMode(1,False)
bpc.setMode(2,False)
bpc.setMode(3,False)
bpc.setOutputVoltage(1,0)
bpc.setOutputVoltage(2,0)
bpc.setOutputVoltage(3,0)
bpc.closePort()