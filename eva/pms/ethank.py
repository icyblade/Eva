import datetime
from functools import wraps

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar
import numpy as np


def need_login(func):
    """Decorator for functions which need authentication."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].is_login:
            return func(*args, **kwargs)
        else:
            raise Exception('Please login first.')

    return wrapper


def allclose(x, y, atol=1):
    return np.allclose(x, y, atol=atol)


class Ethank(object):
    """智云 PMS 管理系统.

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

    References
    --------
    http://pms.ethank.com.cn
    """

    host = 'http://pms.ethank.com.cn'

    def __init__(self, hotel_id=None, hotel_name=None, authentication=None, start_dt=None, end_dt=None):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.shop_id = authentication['shop_id']
        self.username = authentication['username']
        self.password = authentication['password']
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
        response = self.session.post(
            f'{self.host}/service/staff/login',
            data={
                'shopID': self.shop_id,
                'username': self.username,
                'password': self.password,
            },
        )
        json_data = response.json()

        if json_data['ret_code']:
            raise Exception(json_data['ret_msg'])

        self.is_login = True

    def update_data(self):
        # 酒店业绩日报
        day_report = pd.DataFrame(self._parse_day_report()).set_index('live_dt')
        day_report.index = pd.to_datetime(day_report.index)
        assert allclose(day_report['occ'] * day_report['adr'] / 100, day_report['revpar'])
        assert allclose(day_report['revenue'], day_report['tosell'] * day_report['revpar'])

        self.data['day_report'] = day_report

    @property
    def budget(self):
        return self.data['budget']

    @budget.setter
    def budget(self, value):
        self.data['budget'] = value

    @need_login
    def _parse_day_report(self):
        """爬取酒店业绩日报."""
        for delta in range((self.end_dt - self.start_dt).days + 1):
            dt = self.start_dt + datetime.timedelta(delta)
            response = self.session.post(
                url=f'{self.host}/reportServlet?action=dayReport&aTime={dt}&bTime={dt}',
                data={
                    'power_parent_id': 10000000041201,
                    'atime': dt,
                    'btime': dt,
                },
            )
            soup = BeautifulSoup(response.text, 'html.parser')

            def extract_number(label):
                number = soup.find_all(text=label)[0].parent.nextSibling.nextSibling.text
                if number.find('%') != -1:
                    return float(number[:-1])
                else:
                    return float(number)

            yield {
                'live_dt': dt,
                'occ': extract_number('出租率'),
                'roomnights': extract_number('出租间数'),
                'adr': extract_number('平均房价'),
                'revpar': extract_number('RevPar'),
                'revenue': extract_number('当日房费收入'),
                'day_roomnight': extract_number('日租房'),
                'ooo': extract_number('维修房'),
                'free_roomnight': extract_number('免单房') + extract_number('自用房'),
                'tosell': extract_number('可用房数'),
            }
