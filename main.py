import random
import os
import requests
from bs4 import BeautifulSoup
users = eval(os.environ['USERS'])

INDEX_API = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0'

LOGIN_API = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login'
LOGIN_FORM = {
    # user form
    'uid': '',
    'upw': '',
    'smbtn': '进入健康状况上报平台',
    # hidden
    'hh28': '753'
}
LOGIN_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://jksb.v.zzu.edu.cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                  ' Mobile/15E148 MicroMessenger/8.0.28(0x18001c2b) NetType/WIFI Language/zh_CN',
    'Referer': INDEX_API,
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
}

SUBMIT_API = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb'
SUBMIT_FORM = {
    # constant values
    'myvs_1': '否',
    'myvs_2': '否',
    'myvs_3': '否',
    'myvs_4': '否',
    'myvs_5': '否',
    'myvs_7': '否',
    'myvs_8': '否',
    'myvs_11': '否',
    'myvs_12': '否',
    'myvs_13': '否',
    'myvs_15': '否',
    'myvs_13a': '41',  # 河南省
    'myvs_13b': '4101',  # 郑州市
    'myvs_13c': '二七区建设东路1号郑州大学第一附属医院',
    'myvs_24': '否',
    'memo22': '成功获取',

    # 获取地理位置，经纬度，开启定位功能会自动获取，使用随机数估计
    'jingdu': '113.',
    'weidu': '34.',

    # 隐藏值 hidden value
    'did': '2',
    'door': '',
    'day6': '',
    'men6': 'a',
    'sheng6': '',
    'shi6': '',
    'fun118': '0904',
    'fun3': '',
    'ptopid': 's2D3CCA9E32C24B7F848EC2122F5356EE',

    # username:
    'sid': ''
}
SUBMIT_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://jksb.v.zzu.edu.cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                  ' Mobile/15E148 MicroMessenger/8.0.28(0x18001c2b) NetType/WIFI Language/zh_CN',
    'Referer': SUBMIT_API,
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
}

session = requests.Session()
# session.verify = False
AUTHOR = 'xlxing@bupt.edu.cn'


class AutoAgent:
    def __init__(self):
        self.login_form = LOGIN_FORM
        self.submit_form = SUBMIT_FORM

    def login_in(self, username, password):
        # get: fill login_form
        try:
            res = session.get(
                url=INDEX_API,
                # verify=False
            )
            res.encoding = 'utf-8'
            result = BeautifulSoup(res.text, 'html.parser')
            # print(result)
            _hh28 = result.find(type='hidden').get('value')
            if _hh28 is None:
                print('出错: 获取隐藏值 hh28为空')
            else:
                self.login_form['uid'] = username
                self.login_form['upw'] = password
                self.login_form['hh28'] = _hh28
        except Exception as e:
            print(e)
            print('获取登陆页面信息时发生错误，请联系{}'.format(AUTHOR))

        # post: login_in
        try:
            res = session.post(
                url=LOGIN_API,
                data={**self.login_form},
                headers={**LOGIN_HEADER}
            )
            result = BeautifulSoup(res.text, 'html.parser')
            s = result.find('script').string
            left = s.find('pid=')
            right = s.find('&sid')

            # assign 'ptopid'
            SUBMIT_FORM['ptopid'] = s[left: right]

            if res.status_code == 200:
                print('成功登陆...')

                return True
            else:
                print('登陆失败，请查看用户名和密码是否正确')
                return False
        except Exception as e:
            print(e)

    def check_submit(self):
        pass

    def submit(self, username, location):
        # fill submit form
        locs = location.split()
        if locs[0] == '河南省':
            self.submit_form['myvs_13a'] = '41'
        if locs[1] == '郑州市':
            self.submit_form['myvs_13b'] = '4101'
        self.submit_form['myvs_13c'] = locs[2]
        self.submit_form['sid'] = username
        a, b = '', ''
        for _ in range(6):
            a += str(random.randint(0, 9))
        for _ in range(6):
            b += str(random.randint(0, 9))
        self.submit_form['jingdu'] += a
        self.submit_form['weidu'] += b

        # post submit
        try:
            res = session.post(
                url=SUBMIT_API,
                headers=SUBMIT_HEADER,
                data=self.submit_form
            )
            if res.status_code != 200:
                print('打卡失败，', res.status_code)
                return False
            return True
        except Exception as e:
            print(e)

    def auto_clock(self, username, password, location):
        self.login_in(username, password)
        if self.submit(username, location):
            print('成功打卡...')


if __name__ == '__main__':
    agent = AutoAgent()
    # agent.auto_clock('202222442027330', '03101523', '河南省 郑州市 二七区建设东路1号郑州大学第一附属医院')

    for person in users:
        uname, passwd, loc = person
        agent.auto_clock(uname, passwd, loc)
        print()
