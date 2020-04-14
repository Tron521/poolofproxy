from random import choice
import redis
max_score = 100
min_score = 0
initial_score = 10
redis_key = "proxies"


class redisclient(object):
    def __init__(self):
        self.db = redis.StrictRedis(host="127.0.0.1", port=6379, password=None)

    def add(self, proxy, score=initial_score):
        if not self.db.zscore(redis_key, proxy):
            print("添加代理  ", proxy)
            self.db.zadd(redis_key, {proxy: score})

    def random(self):
        res = self.db.zrangebyscore(redis_key, max_score, min_score)
        if len(res):
            return choice(res)
        else:
            res = self.db.zrevrangebyscore(redis_key, max_score, min_score)
            if len(res):
                return choice(res)
            else:
                raise "pool empty error"

    def decrease(self, proxy):
        score = self.db.zscore(redis_key, proxy)
        if score and score > min_score:
            print("代理", proxy, "当前有效分数", score, "减一")
            return self.db.zincrby(redis_key, -1, proxy)
        else:
            print("代理", proxy, "当前有效分数", score, "移除")
            return self.db.zrem(redis_key, proxy)

    def exists(self, proxy):
        return not self.db.zscore(redis_key, proxy) == None

    def max(self, proxy):
        proxy("代理", proxy, "有效  设置为", max_score)
        return self.db.zadd(redis_key, proxy, max_score)

    def count(self):
        return self.db.zcard(redis_key)

    def all(self):
        return self.db.zrangebyscore(redis_key, min_score, max_score)
