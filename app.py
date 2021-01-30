from flask import Flask, render_template, g, jsonify
from db import db_connect
from post import post_list, post
from log import logging

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post/<category>', methods=['GET'])
def text_editor(category):
    return render_template('textEditor.html')


@app.route('/post/<category>', methods=['POST'])
def make_post(category):
    # subject: str, category_code: int, user_code: int, contents: str
    post_data = {
        'subject': '테스트',
        'category_code': 1,
        'user_code': 1,
        'contents': '테스트입니다.'
    }
    result = 'OK' if post.create_post(get_db(), **post_data) else 'Fail'

    return jsonify({
        'result': result
    })


@app.route('/post/spacinfo/<category>', methods=['GET'])
def view_spacinfo(category):
    post_list_data = post_list.get_post_list(get_db(), category)
    return render_template('spacinfo.html',
                           category=category,
                           post_data=post_list_data)


def get_db():
    if not hasattr(g, 'mariadb'):
        g.mariadb = db_connect()
    return g.mariadb


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'mariadb'):
        g.mariadb.close()
        logging.info("DB Connection closed")


if __name__ == '__main__':
    app.run(port=5000, host='192.168.1.27')
