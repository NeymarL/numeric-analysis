# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask
from flask import render_template, request
import lagrange, fix_image

ALLOWED_EXTENSIONS = set(['jpg', 'png', 'gif', 'jepg'])

app = Flask(__name__)
img = ''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/upload_file', methods=['POST'])
def upload_file():
    global img
    file = request.files['upl']
    if file and allowed_file(file.filename):
        img = file.read()
    else:
        return render_template('error.html', message='文件格式错误，请上传[jpg|png|jepg|gif]格式的文件')



@app.route('/run', methods=['GET'])
def run():
    global img
    if not img:
        return render_template('error.html', message='请上传文件')


if __name__ == '__main__':
    app.debug = True
    app.run()
