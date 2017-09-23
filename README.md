# upload-demo

Uploading a large file by fragmentation, powered by Flask and WebUploader.  


## 目的

* 前端上传大文件给后端  

* 前端采用分片方式上传，后端接收全部分片后，将其组合成一个文件  

* 支持多用户同时上传，互不干扰  


## 安装

* 通过<code>pip install -r requirements</code>安装所需包  


## 运行

* 命令行键入“./server.py runserver”即可  

* 浏览器访问“http://127.0.0.1:5000/ ”，点击“请选择”按钮，选择文件并上传  


## 效果

![](http://img.my.csdn.net/uploads/201708/27/1503843837_9940.gif)
> 文件上传成功  

![](http://img.my.csdn.net/uploads/201708/27/1503843837_4091.gif)
> 文件上传失败  


## 技术

* Python语言，Flask框架  

* WebUploader分片与上传，Bootstrap渲染上传进度条  


## 备注

* demo中使用了三种开源框架，后续修改应注意遵守BSD与MIT协议，感谢  

