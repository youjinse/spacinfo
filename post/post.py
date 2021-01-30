from log import logging
from db import select, insert


def get_post(cnx, post_id: int) -> list:
    sql = (f"SELECT a.subject,\n"
           f"       a.contents,\n"
           f"       b.name AS category_name,\n"
           f"       c.name AS user_name,\n"
           f"       a.create_timestamp AS post_create_time\n"
           f"FROM respac.post a\n"
           f"JOIN respac.post_category b\n"
           f"ON (a.category_code = b.code)\n"
           f"JOIN respac.user c\n"
           f"ON (a.user_code = c.code)\n"
           f"WHERE a.seq = {post_id}\n")

    logging.info(sql)
    result = select(cnx, sql)
    logging.info(result)

    if result is None or len(result) == 0:
        logging.error("DB 연결에 실패하였습니다.")
        return None

    return result[0]


def create_post(cnx, subject: str, category_code: int, user_code: int, contents: str):
    sql = (f"INSERT INTO respac.post\n"
           f"(subject, category_code, user_code, contents)\n"
           f"VALUES	\n"
           f"('{subject}', {category_code}, {user_code}, '{contents}')\n"
           f"    ")

    return True if insert(cnx, sql) == 0 else False



if __name__ == '__main__':
    from db import db_connect
    con = db_connect()
    get_post(con, post_id=1)
