import logging

import redis


class RedisUtil:
    def __init__(self):
        redis_host = '118.195.242.175'
        redis_port = '30001'
        redis_password = '@Tj20170524'
        redis_db = 0

        # 创建Redis连接
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)

    def set_with_expire(self, key, value, ex):
        try:
            self.redis_client.set(key, value, ex=ex)
            logging.info(f"Success inserted value '{value}' with key '{key}' into Redis.")
        except redis.RedisError as e:
            logging.error(f"Fail to insert key= '{key}': value='{value}' into redis")

    def set(self, key, value):
        try:
            self.redis_client.set(key, value)
            logging.info(f"Success inserted value '{value}' with key '{key}' into Redis.")
        except redis.RedisError as e:
            logging.error(f"Fail to insert key= '{key}': value='{value}' into redis")

    def delete(self, key):
        try:
            self.redis_client.delete(key)
            logging.info(f"Success deleted value with key '{key}' from Redis.")
        except redis.RedisError as e:
            logging.error(f"Fail to delete key '{key}' from redis")

    def get(self, key):
        try:
            value = self.redis_client.get(key)
            if value is not None:
                return value.decode("utf-8")
        except redis.RedisError as e:
            logging.error(f"Fail to get value from '{key}'")

    def h_get(self, key, hashValue):
        try:
            value = self.redis_client.hget(key, hashValue)
            if value is not None:
                return value.decode("utf-8")
        except redis.RedisError as e:
            logging.error(f"Fail to get value from '{key}'")

    def h_set(self, key, h_key, value):
        try:
            self.redis_client.hset(key, h_key, value)
        except redis.RedisError as e:
            logging.error(f"Fail to set value for '{key}': {e}")
