#coding:utf-8
'''
识别人脸特征
'''

#coding:utf-8
import sys


import time
from aip import AipFace

import mp3play
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '10254547'
API_KEY = 'KN3hFlvWrHykUD8iN12Ah8Q1'
SECRET_KEY = 'pPhhSxEnuKa30nUIj2elReioqLMsHolw '
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 调用人脸属性检测接口

# 定义参数变量
options = {
    'max_face_num': 1,
    'face_fields': "age,beauty,expression,faceshape",
}

# 调用人脸属性识别接口
result = aipFace.detect(get_file_content(sys.argv[1]), options)
print result
beauty =int(result['result'][0]['beauty'])
age = int(result['result'][0]['age'])
print beauty
print age
mstr = "颜值为" + str(beauty) + ",年龄为" +str(age)
print mstr

result  = aipSpeech.synthesis(mstr, 'zh', 1,                      {
    'vol': 5,'spd': 5,'per':3
})
print result
# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    print "write"
    with open('auido.mp3', 'wb') as f:
        f.write(result)



filetext = "auido.mp3"
player = mp3play.load(filetext)
player.play()
time.sleep(5)