项目管理及接管细节
=====

目标
---
* 18年9月20日前：***移交项目工作准备***
* 需添加: 蜂鸣器提示已经识别到人脸
* 需查阅: python调用蜂鸣器

进度
---
* 提前编码完成，编码卡顿已植入多进程
* UI设计完成
* 数据库已经可以正常访问
* 邮箱完成，等待组合
* 结果统计，导出txt完成
* 数据库移植完成

问题
---
* 如何继续优化openface程序？**尝试多进程，蜂鸣器**
* 如何编写结果统计程序？**prettytable输出表格**
* 如何解决过拟合问题？ **投票机制给下限**

资源
---
* face-recognition树莓派环境搭建
* 树莓派初始化
* 人脸识别立项答辩

项目程序简要介绍
---
* [authorreference.py](https://github.com/purity77/facerecognition/blob/master/PycharmProjects/facedebug/authorreference.py) 文件为官方程序参考文件
* [encodingdir.py](https://github.com/purity77/facerecognition/blob/master/PycharmProjects/facedebug/encodingdir.py) 给对以名字作为文件名的需要预编码的图片 
  * 输出格式为 encodings.pkl 存储了名为data{names： encodings:}的字典数据
* [pfasterpool.py](https://github.com/purity77/facerecognition/blob/master/PycharmProjects/facedebug/fasterpool.py) 使用多进程的主识别程序
* [fastermysql.py](https://github.com/purity77/facerecognition/blob/master/PycharmProjects/facedebug/fastermysql.py) 使用多进程以及包含数据库连接的程序
* [opcvtest.py](https://github.com/purity77/facerecognition/blob/master/PycharmProjects/facedebug/opcvtest.py) 为opcv控制摄像头测试程序
* [send_mail_add_more.py](https://github.com/purity77/facerecognition/blob/master/PycharmProjects/facedebug/send_mail_add_more.py) 邮箱发送程序
* [testconnect.py](https://github.com/purity77/facerecognition/blob/master/PycharmProjects/facedebug/testconnect.py) pycharm远程开发程序
* [UI_3.py](https://github.com/purity77/facerecognition/blob/master/PycharmProjects/facedebug/UI_3.py) UI设计程序
