import random
import time
import functools
import requests
from loguru import logger
from _config import uid, web_sig


def requests_error_catcher(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error("request exception: {}".format(e))
        except Exception as e:
            logger.error("request exception: {}".format(e))
    return wrapper


class Seed:

    def __init__(self):
        self.cookies = {
            "uid": uid,
            "web_sig": web_sig
        }

    @requests_error_catcher
    def culture_room(self):
        url = f"https://seed.futunn.com/main/culture-room?random={self._random()}"
        response = requests.get(url=url, headers=self._header(), cookies=self.cookies)
        if response.status_code == 200:
            if response.json().get("code") == 0:
                return response.json().get("data")
        return dict()

    @requests_error_catcher
    def water(self, seed_id):
        url = "https://seed.futunn.com/main/water"
        response = requests.post(url=url, headers=self._header(), cookies=self.cookies, data={"seed_id": seed_id})
        if response.status_code == 200:
            return response.json()
        return {
                "status": 400,
                "message": "未知错误."
            }

    @requests_error_catcher
    def friends(self, index):
        url = f"https://seed.futunn.com/main/friends?filter_fert=1&index={index}&num=20"
        response = requests.get(url=url, headers=self._header(), cookies=self.cookies)
        friends = list()
        data = response.json().get("data")
        friends.extend(data.get('interactEntry'))
        return friends

    @requests_error_catcher
    def all_friends(self):
        url = f"https://seed.futunn.com/main/friends?filter_fert=1&index=0&num=20"
        response = requests.get(url=url, headers=self._header(), cookies=self.cookies)
        friends = list()
        data = response.json().get("data")
        friends.extend(data.get('interactEntry'))
        while True:
            if data.get('has_more'):
                _friends = self.friends(len(friends))
                if len(_friends) != 0:
                    time.sleep(5)
                    friends.extend(_friends)
                else:
                    break
            else:
                break
        return friends

    @requests_error_catcher
    def fert(self, uid_key):
        url = "https://seed.futunn.com/main/fert"
        response = requests.post(url=url, headers=self._header(), cookies=self.cookies, data={"invite_code": uid_key})
        if response.json().get("code") == 0:
            return True
        return False

    def use(self, seed_id):
        url = "https://seed.futunn.com/main/use"
        response = requests.post(url=url, headers=self._header(), cookies=self.cookies, data={
            "seed_id": seed_id,
            "account_base_type": "2"
        })
        if response.json().get("code") == 0:
            return True
        return False

    @staticmethod
    def _random():
        return random.randint(1, 999)

    @staticmethod
    def _header():
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "priority": "u=1, i",
            "referer": "https://seed.futunn.com",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        return headers

