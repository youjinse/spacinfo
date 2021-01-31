from log import logging
from db import select
import math


def get_post_count(cnx, category_code: int, limit_count=20.0):
    sql = (f"SELECT COUNT(*) AS total_count\n"
           f"from respac.post a\n"
           f"WHERE a.category_code = {category_code}\n")

    logging.info(sql)
    result = select(cnx, sql)
    logging.info(result)

    if result is None:
        logging.error("DB 연결에 실패하였습니다.")
        return []

    return math.ceil(int(result[0]['total_count']) / limit_count)


def get_post_list(cnx, category_code: int, current_seq: int, limit_count=20) -> list:
    sql = (f"    SELECT b.subject, \n"
           f"           a.name AS category_name,\n"
           f"           c.name AS user_name,\n"
           f"           b.create_timestamp AS post_create_time,\n"
           f"           b.seq AS post_id,\n"
           f"           b.category_code\n"
           f"    FROM respac.post_category a\n"
           f"    JOIN respac.post b\n"
           f"    ON (a.code = b.category_code)\n"
           f"    JOIN respac.user c\n"
           f"    ON (b.user_code = c.code)\n"
           f"    WHERE a.code = {category_code}\n"
           f"    AND   b.seq < {current_seq}\n"
           f"    ORDER BY b.category_code, b.seq DESC\n"
           f"    LIMIT {limit_count} \n"
           f"    ")

    logging.info(sql)
    result = select(cnx, sql)
    logging.info(result)

    if result is None:
        logging.error("DB 연결에 실패하였습니다.")
        return []

    return result


if __name__ == '__main__':
    from db import db_connect
    con = db_connect()
    print(get_post_list(con, category_code=1))

