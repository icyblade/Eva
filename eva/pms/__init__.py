import datetime
from functools import wraps

import requests
from requests.cookies import RequestsCookieJar


class LoginError(Exception):
    pass


def need_login(func):
    """Decorator for functions which need authentication."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].is_login:
            return func(*args, **kwargs)
        else:
            raise LoginError('Please login first.')

    return wrapper


class PMS(object):
    """Abstract class of PMS.

    Parameters
    --------
    hotel_id: int
        酒店 ID. 默认: None.
    hotel_name: str
        酒店名称. 默认: None.
    authenticaiton: dict
        登陆信息字典, key 包含: shop_id, username, password. 默认: None.
    start_dt: datetime.date
        获取数据起始日期. 默认: 365 天前.
    end_dt: datetime.date
        获取数据结束日期. 默认: 1 天前.
    """

    _host = None

    def __init__(self, hotel_id=None, hotel_name=None, authentication=None, start_dt=None, end_dt=None):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self._authentication = authentication
        self.start_dt = datetime.date.today() - datetime.timedelta(365) if start_dt is None else start_dt
        self.end_dt = datetime.date.today() - datetime.timedelta(1) if end_dt is None else end_dt

        # init session
        self.session = requests.Session()
        self.cookie = RequestsCookieJar()
        self.session.cookies = self.cookie
        self._is_login = False

        # init data
        self.data = {}

    @property
    def is_login(self):
        """Is current PMS login.

        TODO
        --------
         - Session expire check.
        """
        return self._is_login

    @is_login.setter
    def is_login(self, value):
        self._is_login = value

    def login(self):
        pass

    def update_data(self):
        pass

    @property
    def budget(self):
        return self.data['budget']

    @budget.setter
    def budget(self, value):
        self.data['budget'] = value
