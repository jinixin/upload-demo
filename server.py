#!/usr/bin/env python
# coding=utf-8

import os

from flask import Flask, request, Response, render_template as rt

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return rt('./index.html')


@app.route('/file/upload', methods=['POST'])
def upload_part():  # 接收前端上传的一个分片
    task = request.form.get('task_id')  # 获取文件的唯一标识符
    chunk = request.form.get('chunk', 0)  # 获取该分片在所有分片中的序号
    filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符

    upload_file = request.files['file']
    upload_file.save('./upload/%s' % filename)  # 保存分片到本地
    return rt('./index.html')


@app.route('/file/merge', methods=['GET'])
def upload_success():  # 按序读出分片内容，并写入新文件
    ext = request.args.get('ext', '')
    upload_type = request.args.get('type')
    if len(ext) == 0 and upload_type:
        ext = upload_type.split('/')[1]
    ext = '' if len(ext) == 0 else '.%s' % ext  # 构造文件后缀名

    task = request.args.get('task_id')  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open('./upload/%s%s' % (task, ext), 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError, msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    return rt('./index.html')


@app.route('/file/list', methods=['GET'])
def file_list():
    files = os.listdir('./upload/')  # 获取文件目录
    return rt('./list.html', files=files)


@app.route('/file/download/<filename>', methods=['GET'])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = './upload/%s' % filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')


if __name__ == '__main__':
    app.run(debug=False, threaded=True)
