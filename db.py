# -*- coding: utf-8 -*-
import pymongo


class DB:
    """存到数据库"""

    def __init__(self):
        self.MONGO_URL = 'localhost'
        self.MONGO_DB = 'youth'
        self.MONGO_COLLECTION = 'post'
        client = pymongo.MongoClient(self.MONGO_URL)
        self.db = client[self.MONGO_DB]

    def save_to_mongo(self, result):
        """
        保存至 MongoDB
        :param result: 结果
        """
        try:
            if self.db[self.MONGO_COLLECTION].insert(result):
                print(' 存储到 MongoDB 成功 ')
        except Exception:
            print(' 存储到 MongoDB 失败 ')