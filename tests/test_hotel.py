import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../'))


def test_init():
    from eva.hotel import Hotel

    Hotel(None)


def test_pms():
    from eva.hotel import Hotel

    hotel = Hotel(None)
    hotel.pms = 'pms'
    assert hotel.pms == 'pms'


def test_init_pms():
    from eva.hotel import Hotel

    hotel = Hotel(None)
    hotel.init_pms()
