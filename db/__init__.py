from log import logging
import mysql.connector
from mysql.connector import errorcode

password = ''
database = ''

# Obtain connection string information from the portal
config = {
    # 'host': 'respac-test-01.mariadb.database.azure.com',
    # 'user': 'respac@respac-test-01',
    # 'password': 'c3IQbseW1riz',
    'host': 'localhost',
    'user': 'respacadm',
    'password': 'credit123',
    'database': 'respac',
    # 'ssl_verify_cert': True,
}


def db_connect():
    # Construct connection string
    try:
        conn = mysql.connector.connect(**config)
        logging.info("Connection established")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Database does not exist")
        else:
            logging.error(err)
        return None


def select(con: mysql.connector.MySQLConnection, sql: str) -> list:
    """

    :rtype: object
    """

    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
    except Exception as e:
        logging.error(f'DB Select 중 에러가 발생하였습니다. sql: {sql}')
        logging.error(f'{e}')
        return []

    return result


def insert(con: mysql.connector.MySQLConnection, sql: str) -> int:
    try:
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
        cursor.close()
    except mysql.connector.IntegrityError as e:
        logging.error(f'DB insert 데이터가 중복되었습니다. sql: {sql}')
        logging.error(f'{e}')
        # 중복
        return 1
    except Exception as e:
        logging.error(f'DB insert 중 에러가 발생하였습니다. sql: {sql}')
        logging.error(f'{e}')
        # 에러
        return 2

    return 0


if __name__ == '__main__':
    test_conn = db_connect()
    print(select(test_conn, 'select 1 from dual'))
