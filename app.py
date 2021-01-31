from flask import Flask, render_template, g, jsonify, request
from db import db_connect
from post import post_list, post, image
from log import logging

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post/<category>', methods=['GET'])
def text_editor(category):
    return render_template('textEditor.html', category=category)


@app.route('/post/<category>', methods=['POST'])
def make_post(category):
    # subject: str, category_code: int, user_code: int, contents: str
    subject = request.form['subject']
    contents = request.form['contents']

    post_data = {
        'subject': subject,
        'category_code': category,
        'user_code': 1,
        'contents': contents
    }
    result = 'OK' if post.create_post(get_db(), **post_data) else 'Fail'

    return jsonify({
        'result': result
    })


@app.route('/upload/image', methods=['POST'])
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


@app.route('/post/<category>/<post_id>')
def view_post(category, post_id):
    post_data = post.get_post(db_connect(), post_id)
    # post_data['contents'] = Template(post_data['contents'])
    return render_template('post.html', post_data=post_data)


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


def get_blob_storage():
    if not hasattr(g, 'blob_storage'):
        g.blob_storage = image.blob_connect()
    return g.blob_storage


@app.teardown_appcontext
def close_all(error):
    if hasattr(g, 'mariadb'):
        g.mariadb.close()
        logging.info("DB Connection closed")


if __name__ == '__main__':
    app.run(port=5000, host='192.168.1.27')
