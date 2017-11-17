class Hotel(object):
    def __init__(self, config):
        self._config = config

    @property
    def pms(self):
        return self._pms

    @pms.setter
    def pms(self, pms):
        self._pms = pms

    def init_pms(self):
        pass
