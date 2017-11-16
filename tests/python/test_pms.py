import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../python-package/'))


def test_init():
    from eva.pms import PMS

    PMS('protocal://host:port')
