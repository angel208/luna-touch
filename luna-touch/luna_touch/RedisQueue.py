import redis
import json

class RedisQueue(object):

    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.db= redis.Redis(**redis_kwargs)
        self.key = name
        print(self.key)

    def qsize(self):
        return self.db.llen(self.key)

    def empty(self):
        if self.qsize() == 0 :
            return True
        else:
            return False

    def put(self, item):
        #json_item = json.dumps(item)
        self.db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        
        if block:
            item = self.db.blpop(self.key, timeout=timeout)
        else:
            item = self.db.lpop(self.key)

        if item:
            item = item[1]

        return item

    def get_nowait(self):
        
        return self.get(False)