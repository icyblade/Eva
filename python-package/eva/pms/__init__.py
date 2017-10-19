class PMS(object):
    def __init__(self, connection_string):
        self._connection_string = connection_string
        self.data = {}
