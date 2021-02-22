import redis
import json


class RedisSession:
    # host = 'respactest.redis.cache.windows.net'
    # port = '6380'
    # password = 'IGM2PhyxnBhzP0hy4iIpm6uiMEo0yphgQo9X2Eb7e8c='
    host = '192.168.1.41'
    timeout = 3600

    def __init__(self):
        self.db = redis.StrictRedis(host=self.host)
        # self.db = redis.StrictRedis(host=self.host, port=self.port, password=self.password, ssl=True)

    # 세션이 있으면 타임아웃 만큼 다시 연장해주고 없으면 False 있으면 사용자id 리턴
    def open_session(self, session_key):
        self.db.expire(session_key, self.timeout)
        data = self.db.get(session_key)
        return None if data is None else json.loads(data)

    def logout_session(self, session_key):
        self.db.delete(session_key)
        return True

    # 신규 세션 요청 시 세션 값을 만들어서 리턴
    def save_session(self, session_key, data):
        # self.db.setex(session_key, self.timeout, user_id)
        self.db.setex(session_key, self.timeout, json.dumps(data).encode())
        return True

    def keys(self):
        print(self.db.keys())


if __name__ == '__main__':
    s = RedisSession()
    s.save_session('tttt', '1234')
    print(s.open_session('1234'))
