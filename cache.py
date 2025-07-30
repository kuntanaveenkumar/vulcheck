import time

class SimpleCache:
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self.store = {}

    def get(self, key):
        item = self.store.get(key)
        if not item or (time.time() - item['time']) > self.ttl:
            return None
        return item['value']

    def set(self, key, value):
        self.store[key] = {'value': value, 'time': time.time()}
