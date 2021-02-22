from flask import Flask, render_template, g, jsonify, request, redirect
from db import db_connect
from post import post_list, post, image
from log import logging
from user import RedisSession, user
from user.session import check_session

app = Flask(__name__)
app.secret_key = 'cd48e1c22de0961d5d1bfb14f8a66e006cfb1cfbf3f0c0f3'


@app.route('/')
def index():
    spacinfo_data = post_list.get_post_list(get_db(), 1, limit_count=5)
    stock_wind = post_list.get_post_list(get_db(), 2, limit_count=5)
    stock_discussion = post_list.get_post_list(get_db(), 3, limit_count=5)
    return render_template('index.html',
                           spacinfo_data=spacinfo_data,
                           stock_wind=stock_wind,
                           stock_discussion=stock_discussion)


@app.route('/post/<category>', methods=['GET'])
@check_session
def text_editor(category):
    return render_template('textEditor.html', category=category)


@app.route('/post/<category>', methods=['POST'])
@check_session
def make_post(category):
    # subject: str, category_code: int, user_code: int, contents: str
    subject = request.form['subject']
    contents = request.form['contents']

    post_data = {
        'subject': subject,
        'category_code': category,
        'user_code': g.user_data['user_code'],
        'contents': contents
    }
    result = 'OK' if post.create_post(get_db(), **post_data) else 'Fail'

    return jsonify({
        'result': result
    })


@app.route('/upload/image', methods=['POST'])
@check_session
def upload_image():
    if 'file' not in request.files:
        return jsonify({
            'result': 'Fail'
        })
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'result': 'Fail'
        })

    url = image.upload_image(get_blob_storage(), file.read())

    return jsonify({
        'result': 'OK',
        'fileUrl': url
    })


@app.route('/post/<category>/<post_id>', methods=['GET'])
def view_post(category, post_id):
    post_data = post.get_post(db_connect(), post_id)
    # post_data['contents'] = Template(post_data['contents'])
    return render_template('post.html', post_data=post_data)


@app.route('/post/spacinfo/<category>', methods=['GET'])
def view_spacinfo(category):
    category_name = 'spacinfo'
    data = request.args.to_dict()
    if 'seq' not in data:
        current_page = 1
        last_post_id = 99999999999
    else:
        last_post_id = data['seq']
        current_page = int(data['page']) + 1

    total_pages = post_list.get_post_count(get_db(), category)
    post_list_data = post_list.get_post_list(get_db(), category, last_post_id)
    return render_template('spacinfo.html',
                           category=category,
                           category_name=category_name,
                           current_page=current_page,
                           last_post_id=last_post_id,
                           total_pages=total_pages,
                           post_data=post_list_data)


@app.route('/login', methods=['GET', 'POST'])
def view_login_page():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        if user.login(db_connect(), user_id, password):
            return redirect('/')
        else:
            return redirect('/login')

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    user.logout()
    return redirect('/')


@app.route('/register', methods=['GET'])
def view_register_page():
    return render_template('register.html')


@app.route('/user', methods=['POST'])
def register_user():
    user_id = request.form['user_id']
    password = request.form['password']
    user_name = request.form['user_name']
    join_channel_code = 1 if 'join_channel_code' not in request.form else request.form['join_channel_code']

    user.create_user(get_db(), user_id, password, user_name, join_channel_code)

    return view_login_page()


def get_db():
    if not hasattr(g, 'mariadb'):
        g.mariadb = db_connect()
    return g.mariadb


def get_blob_storage():
    if not hasattr(g, 'blob_storage'):
        g.blob_storage = image.blob_connect()
    return g.blob_storage


def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = RedisSession.RedisSession()
    return g.redis


@app.teardown_appcontext
def close_all(error):
    if hasattr(g, 'mariadb'):
        g.mariadb.close()
        logging.info("DB Connection closed")
    if hasattr(g, 'redis'):
        g.redis.close()
        logging.info("Redis Connection closed")


if __name__ == '__main__':
    app.run(port=5000, host='192.168.1.41')
