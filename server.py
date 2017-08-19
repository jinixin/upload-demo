# coding=utf-8

import os
from flask import Flask, request, render_template as rt

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upload_file = request.files['file']
        task = request.form.get('task_id')
        chunk = request.form.get('chunk', 0)
        filename = '%s%s' % (task, chunk)
        upload_file.save('./upload/%s' % filename)
    return rt('./index.html')


@app.route('/success', methods=['GET'])
def upload_success():
    task = request.args.get('task_id')
    ext = request.args.get('ext', '')
    upload_type = request.args.get('type')
    if len(ext) == 0 and upload_type:
        ext = upload_type.split('/')[1]
    ext = '' if len(ext) == 0 else '.%s' % ext
    chunk = 0
    with open('./upload/%s%s' % (task, ext), 'w') as target_file:
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'r')
                target_file.write(source_file.read())
                source_file.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)
    return rt('./index.html')


if __name__ == '__main__':
    app.run(debug=False)
