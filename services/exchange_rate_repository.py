from redisworks import Root
import redis
import time


class ExchangeRateRepository:
    def __init__(self, host="127.0.0.1", port=6379):
        self.redis = Root(host, port)
        self.wait_connection()
        self.redis.rates = {"ID": {"ID": 1}}

    def wait_connection(self):
        retries = 10
        while True:
            try:
                self.redis.connected = True
                break
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)

    def merge_rates(self, new_rates, merge=True):
        if (not merge):
            self.redis.rates = {"ID": {"ID": 1}}
        for cfrom in new_rates.keys():
            if cfrom not in self.redis.rates:
                self.redis.rates[cfrom] = {}
            self.redis.rates[cfrom].update(new_rates[cfrom])

    def get_rates_by_base(self, base):
        if (base in self.redis.rates):
            return self.redis.rates[base]
        return None

    def get_rates(self, cfrom, cto):
        if cfrom in self.redis.rates and cto in self.redis.rates[cfrom]:
            return self.redis.rates[cfrom][cto]
        return None
