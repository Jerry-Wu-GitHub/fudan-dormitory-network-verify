import json
import requests
from typing import Dict, List, Literal

try:
    from config.constant import TIMEOUT, BASE_URL, IP_API_URL, PRE_LOGIN_API_URL, LOGIN_API_URL, ERROR_FEATURES
except:
    print("./config/constants.py 文件已损坏，请重新下载！")
    input("【按下「回车键」退出】")

from config.user import USERNAME, PASSWORD, CHANNEL



UserOnlineState = Literal["on", "off"]

class ChannelError(Exception):
    pass

class Account:
    """
    Packaged the functions and variables required for logging into Fudan website.
    """

    GET_IP_HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': f'{BASE_URL}/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
    }

    SUBSEQUENT_HEADERS = GET_IP_HEADERS | {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': BASE_URL,
    }


    def __init__(
        self,
        username: str = None, password: str = None, channel: str = None,
        ip:       str = None
    ):
        self.username = username or USERNAME
        self.password = password or PASSWORD
        self.channel  = channel  or CHANNEL
        self.ip       = ip       or Account.get_ip()


    @classmethod
    def get_ip(cls) -> str:
        """
        return: the IP address of the local machine.
        """

        response = requests.get(
            IP_API_URL,
            headers = cls.GET_IP_HEADERS,
            verify = False,
            timeout = TIMEOUT
        )
        return response.json()["data"]


    def get_user_online_data(self) -> Dict[str, str]:
        """
        return: the user's current online data.

        If the user is currently connected to Fudan network, the return value is similar to:

            {
                'useronlinestate': 'on',
                'username': 'your_username',
                'balance': '0',
                'duration': 'online_duration (seconds)',
                'outport': 'your_network_channel',
                'totaltimespan': '0',
                'usripadd': 'your_ip'
            }

        If the user is currently not connected to Fudan network, the return value is similar to:

            {
                'useronlinestate': 'off',
                'option82': '_OPTION82_'
            }
        """

        json_data = {
            'getuseronlinestate': 'on_or_off',
            'user_ipadress': self.ip,
        }
        data = json.dumps(json_data, separators = (',', ':'))  # 去掉多余空格

        response = requests.post(
            PRE_LOGIN_API_URL,
            headers = Account.SUBSEQUENT_HEADERS,
            data = data,
            verify = False,
            timeout = TIMEOUT
        )
        return response.json()["data"]


    @property
    def user_online_state(self) -> UserOnlineState:
        return self.get_user_online_data()["useronlinestate"]


    def _get_channels(self) -> List[{'id': str, 'name': str}]:
        """
        Get options on the "选择网络" panel.

        The return value is similar to:

        [
            {'id': '3', 'name': '校园网'},
            {'id': '2', 'name': '中国移动'},
            {'id': '1', 'name': '中国电信'},
            {'id': '4', 'name': '中国联通'}
        ]
        """

        json_data = {
            'username': self.username,
            'password': self.password,
            'ifautologin': '0',
            'channel': '_GET',
            'pagesign': 'firstauth',
            'usripadd': self.ip,
        }
        data = json.dumps(json_data, separators = (',', ':'))

        response = requests.post(
            LOGIN_API_URL,
            headers = Account.SUBSEQUENT_HEADERS,
            data = data,
            verify = False,
            timeout = TIMEOUT
        )
        response_data = response.json()["data"]

        if "channels" not in response_data:
            for (feature, message) in ERROR_FEATURES.items():
                if feature in response_data["text"]:
                    raise ChannelError(message)
        return response.json()["data"]["channels"]


    @staticmethod
    def _process_channels(channels: List[{'id': str, 'name': str}]) -> Dict[str, str]:
        """
        Convert channels in list form into name/id key value pairs.

        The return value is similar to:

        {
            '校园网': '3',
            '中国移动': '2',
            '中国电信': '1',
            '中国联通': '4'
        }
        """

        return {channel["name"]:channel["id"] for channel in channels}


    def login(self) -> None:
        """
        Log in to Fudan Network.
        """

        json_data = {
            'username': self.username,
            'password': self.password,
            'ifautologin': '0',
            'channel': Account._process_channels(self._get_channels())[CHANNEL],
            'pagesign': 'secondauth',
            'usripadd': self.ip,
        }
        data = json.dumps(json_data, separators = (',', ':'))

        response = requests.post(
            LOGIN_API_URL,
            headers = Account.SUBSEQUENT_HEADERS,
            data = data,
            verify = False,
            timeout = TIMEOUT
        )
        response_data = response.json()["data"]

        if "text" in response_data:
            print("登录失败：" + response_data["text"])
        else:
            print("登录成功！")


    def logout(self) -> None:
        """
        Log out of the current login.

        There will be no error when logging out again after logging out.
        """

        json_data = {
            'username': self.username,
            'password': '123',
            'channel': '0',
            'ifautologin': '1',
            'pagesign': 'thirddauth',
            'usripadd': self.ip,
        }
        data = json.dumps(json_data, separators = (',', ':'))

        response = requests.post(LOGIN_API_URL, headers = Account.SUBSEQUENT_HEADERS, data = data, verify = False, timeout = TIMEOUT)
        print(response.json()["data"]["text"])



if __name__ == "__main__":
    import time

    account = Account()
    print(account.ip)

    account.logout()
    time.sleep(5)
    print(account.get_user_online_data())

    channels = account._get_channels()
    print(channels)
    print(account._process_channels(channels))
    account.login()
    print(account.get_user_online_data())
