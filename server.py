# coding=utf-8

from flask import Flask, request, render_template as rt
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upload_file = request.files['file']
        # print request.form
        task = request.form.get('task_id')
        chunk = request.form.get('chunk', 0)
        filename = secure_filename('%s%s' % (task, chunk))
        upload_file.save('upload/%s' % filename)
    return rt('./index.html')


@app.route('/success', methods=['GET'])
def upload_success():
    return rt('./index.html')


if __name__ == '__main__':
    app.run(debug=False)
