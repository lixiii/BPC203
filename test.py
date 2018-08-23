# unit test for bpc203 module
import pytest
import bpc203 as bpc

def test_identify():
    bpc.identify(1)
    with pytest.raises(ValueError):
        bpc.identify(0)
    
    with pytest.raises(ValueError):
        bpc.identify(4)

def test_setClosedLoopMode():
    bpc.setMode(1)

def test_zero():
    bpc.zero(1)

def test_position():
    bpc.zero(1)
    if bpc.zeroFinished(1) == False:
        with pytest.raises(RuntimeError):
            bpc.position(1, 10)
            

# function to ensure that the port is initialised before any test is run and that it it closed after all tests are run
@pytest.yield_fixture(scope='session', autouse=True)
def db_conn():
    # Will be executed before the first test
    conn = bpc.init()
    yield conn
    # Will be executed after the last test
    bpc.closePort()