from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/editor')
def text_editor():
    return render_template('textEditor.html')


if __name__ == '__main__':
    app.run(port=5000, host='192.168.1.27')
