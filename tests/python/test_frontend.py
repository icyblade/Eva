import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/../../python-package/'))

def test_frontend():
    pass


def test_wechat():
    with pytest.raises(NotImplementedError):
        pass
