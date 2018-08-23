# unit test for bpc203 module
import pytest
import bpc203 as bpc

def test_identify():
    bpc.identify(1)
    with pytest.raises(ValueError):
        bpc.identify(0)
    
    with pytest.raises(ValueError):
        bpc.identify(4)


@pytest.yield_fixture(scope='session', autouse=True)
def db_conn():
    # Will be executed before the first test
    conn = bpc.init()
    yield conn
    # Will be executed after the last test
    bpc.closePort()