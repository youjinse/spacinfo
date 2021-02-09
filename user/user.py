from db import select, insert
import hashlib
from log import logging
from user import session as user_session


def check_dup_user_name(con, user_name):
    sql = (f"SELECT 1\n"
           f"FROM respac.user a\n"
           f"WHERE a.name = '{user_name}'")

    return True if len(select(con, sql)) != 0 else False


def check_dup_id(con, user_id):
    sql = (f"SELECT 1\n"
           f"FROM respac.user a\n"
           f"WHERE a.id = '{user_id}'\n")

    return True if len(select(con, sql)) != 0 else False


def create_user(con, user_id: str, password: str, user_name: str, join_channel_code=1):
    if check_dup_user_name(con, user_name):
        logging.info(f"유져명이 중복입니다. [{user_name}]")
        return 1

    if check_dup_id(con, user_id):
        logging.info(f"ID 또는 이메일이 중복입니다. [{user_id}]")
        return 2

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    sql = (f"INSERT INTO respac.user\n"
           f"(id, password, name, join_channel_code)\n"
           f"VALUES	\n"
           f"('{user_id}', '{password_hash}', '{user_name}', {join_channel_code})\n")

    # 리턴 3이면 db 에러
    return 0 if insert(con, sql) == 0 else 3


def get_user_info(con, user_id):
    pass


def login(con, user_id: str, password: str) -> bool:
    if check_dup_id(con, user_id) is False:
        return False

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    sql = (f"SELECT a.code, a.id, a.name\n"
           f"FROM respac.user a\n"
           f"WHERE a.id = '{user_id}'\n"
           f"AND a.password = '{password_hash}'")

    result = select(con, sql)

    if len(result) > 0:
        data = {
            'user_id': user_id,
            'user_code': result[0]['code'],
            'user_name': result[0]['name']
        }
        user_session.save_session(data)
        return True

    return False


def logout():
    return user_session.logout()


if __name__ == '__main__':
    from db import db_connect
    create_user(db_connect(), 'test2@test.com', '1234', '테스트2')
