# -*- coding: utf-8 -*-

import sys, os
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
        img = file.filename
        file.save('static/temp/' + img)
        img = 'static/temp/' + img
    else:
        return render_template('error.html', message='文件格式错误，请上传[jpg|png|jepg|gif]格式的文件')


@app.route('/lagrange', methods=['GET'])
def Lagrange():
    res1 = lagrange.test(10)
    res2 = lagrange.test(20)
    return render_template('lagrange.html', result1=res1[0], right1=res1[1],
        error1=res1[2], result2=res2[0],  right2=res2[1], error2=res2[2])

@app.route('/run', methods=['GET'])
def run():
    global img
    if not img:
        return render_template('error.html', message='请上传文件')
    new = fix_image.run_fix(ld = 2, u = 8, Q1 = 0.05, Q2 = 0.1, img = img)
    extension = img.rsplit('.', 1)[1]
    new += '.' + extension
    old = img
    return render_template('result.html', old=old, new=new)



if __name__ == '__main__':
    app.debug = True
    app.run()
