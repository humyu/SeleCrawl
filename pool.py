# -*- coding: utf-8 -*-
import random
from fake_useragent import UserAgent


class RandomPool:
    """随机代理池"""

    def __init__(self):
        self.IP_POOL = ['182.99.187.108:55290', '182.84.132.62:7134', '119.114.154.102:39365']

    def get_user_agent(self):
        ua = UserAgent()
        return ua.random

    def get_ip(self):
        ip = random.choice(self.IP_POOL)
        return ip