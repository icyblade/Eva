class PMS(object):
    def __init__(self, connection_string):
        self._connection_string = connection_string
        self.data = {}
        self._parse_data()

    def _parse_data(self):
        self._protocol, self._path = self._connection_string.split('://')
