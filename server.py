# coding=utf-8

import os
from flask import Flask, request, render_template as rt
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upload_file = request.files['file']
        task = request.form.get('task_id')
        chunk = request.form.get('chunk', 0)
        filename = '%s%s' % (task, chunk)
        upload_file.save('upload/%s' % filename)
    return rt('./index.html')


@app.route('/success', methods=['GET'])
def upload_success():
    task = request.args.get('task_id')
    chunk = 0
    with open('./upload/%s' % task, 'w') as target:
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source = open(filename)
                target.write(source.read())
                source.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)
    return rt('./index.html')


if __name__ == '__main__':
    app.run(debug=False)
