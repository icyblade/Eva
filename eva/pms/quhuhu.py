import datetime
import warnings

import inflection
import pandas as pd

from . import PMS, need_login


class QuhuhuHotel(PMS):
    """去呼呼酒店版 PMS 管理系统.

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
    http://gj.quhuhu.com/
    """

    _host = 'https://jd.izhonghui.cn'
    _login_host = 'http://wo.izhonghui.cn'

    def __init__(self, hotel_id=None, hotel_name=None, authentication=None, start_dt=None, end_dt=None):
        super(self.__class__, self).__init__(hotel_id, hotel_name, authentication, start_dt, end_dt)

        self.hotel_no = self._authentication['hotel_no']
        self.username = self._authentication['username']
        self.password = self._authentication['password']

        self.data['day_report'] = None

    def login(self):
        super(self.__class__, self).login()

        response = self.session.post(
            f'{self._login_host}/action/login/userLogin',
            data={
                'username': self.username,
                'password': self.password,
                'rememberMe': 'false',
                'bizType': 'pms',
            },
        )
        json_data = response.json()

        if int(json_data['code']):
            raise Exception(json_data['msg'])

        self.is_login = True

    def update_data(self):
        super(self.__class__, self).update_data()

        # 综合营业数据表
        day_report = pd.DataFrame(self._parse_query_comprehensive_by_date())
        if len(day_report):
            if len(day_report) != (self.end_dt - self.start_dt).days + 1:
                warnings.warn('Missing data found, please double check the start_dt and end_dt.')
            day_report = day_report.rename(columns=inflection.underscore)

            day_report['live_dt'] = pd.to_datetime(day_report['live_dt'])
            day_report.drop('hotel_date', axis=1, inplace=True)

            self.data['day_report'] = day_report

    @need_login
    def _parse_query_comprehensive_by_date(self):
        start_dt = self.start_dt

        while start_dt <= self.end_dt:
            end_dt = min(start_dt + datetime.timedelta(180), self.end_dt)
            response = self.session.post(
                f'{self._host}/api/report/queryComprehensiveByDate.do',
                data={
                    'startDate': start_dt,
                    'endDate': end_dt,
                    'hotelNo': self.hotel_no,
                }
            )

            start_dt = end_dt + datetime.timedelta(1)

            json_data = response.json()

            if json_data['code'] != '0000':
                raise Exception(json_data['msg'])

            year = start_dt.year
            for record in json_data['data']['reportList']:
                if record['hotelDate'] != '合计':
                    if record['hotelDate'] == '01-01':
                        record['live_dt'] = f'{year+1}-{record["hotelDate"]}'
                    else:
                        record['live_dt'] = f'{year}-{record["hotelDate"]}'
                    yield record
