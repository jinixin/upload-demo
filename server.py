#!/usr/bin/env python
# coding=utf-8

import os
from flask import Flask, request, render_template as rt

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():  # 一个分片上传后被调用
    if request.method == 'POST':
        upload_file = request.files['file']
        task = request.form.get('task_id')  # 获取文件唯一标识符
        chunk = request.form.get('chunk', 0)  # 获取该分片在所有分片中的序号
        filename = '%s%s' % (task, chunk)  # 构成该分片唯一标识符
        upload_file.save('./upload/%s' % filename)  # 保存分片到本地
    return rt('./index.html')


@app.route('/success', methods=['GET'])
def upload_success():  # 所有分片均上传完后被调用
    task = request.args.get('task_id')
    ext = request.args.get('ext', '')
    upload_type = request.args.get('type')
    if len(ext) == 0 and upload_type:
        ext = upload_type.split('/')[1]
    ext = '' if len(ext) == 0 else '.%s' % ext  # 构建文件后缀名
    chunk = 0
    with open('./upload/%s%s' % (task, ext), 'w') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'r')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    return rt('./index.html')


if __name__ == '__main__':
    app.run(debug=False)
