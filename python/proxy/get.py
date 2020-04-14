from db import redisclient
from crawler import crawler
pool_strict = 10000


class getter(object):
    def __init__(self):
        self.redis = redisclient()
        self.crawler = crawler()

    def is_over_strict(self):
        if self.redis.count() >= pool_strict:
            return True
        else:
            return False

    def run(self):
        print("获取器开始执行")
        if not self.is_over_strict():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
