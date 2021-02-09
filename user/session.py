from user import RedisSession
from flask import session, render_template, g
from log import logging
import uuid

error_page = 'login.html'


# 세션이 존재하지는 체크하는 데코레이터
# 세션 만료되었으면 로그인 페이지로 이동
def check_session(original_function):
    def wrapper(*args, **kwargs):
        try:
            access_token = session['access_token']
        except KeyError :
            logging.error('세션키를 찾을 수 없습니다.')
            return render_template(error_page), 403

        # 레디스에 세션 존재하는지 확인
        user_data = RedisSession.RedisSession().open_session(access_token)
        if user_data is None:
            logging.error("레디스 세션 에러")
            return render_template(error_page), 403

        logging.info(session)
        g.user_data = user_data
        logging.info(f"유저아이디: {g.user_data}")
        result = original_function(*args, **kwargs)
        return result
    wrapper.__name__ = original_function.__name__
    return wrapper


def save_session(data):
    try:
        redis_session = RedisSession.RedisSession()
        access_token = str(uuid.uuid4())
        redis_session.save_session(access_token, data)
        session['access_token'] = access_token
        logging.info(session)
    except Exception as e:
        logging.error(e)
        return False

    return True


def logout():
    logging.info(session)
    if 'access_token' in session:
        del session['access_token']
    return True
