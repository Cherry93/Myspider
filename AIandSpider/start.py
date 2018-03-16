#coding:utf-8
'''
语音登录淘宝领金币
'''



# 录音
import re

import mp3play
import pymongo as pymongo
from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave

import  os
from aip import AipSpeech
import  time


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

""" 我的的 APPID AK SK """
APP_ID = '10254547'
API_KEY = 'KN3hFlvWrHykUD8iN12Ah8Q1'
SECRET_KEY = 'pPhhSxEnuKa30nUIj2elReioqLMsHolw '
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


class recoder:
    NUM_SAMPLES = 2000      #pyaudio内置缓冲大小
    SAMPLING_RATE = 8000    #取样频率
    LEVEL = 500         #声音保存的阈值
    COUNT_NUM = 20      #NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 8         #声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
    TIME_COUNT = 60     #录音时间，单位s

    Voice_String = []

    def savewav(self,filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes(np.array(self.Voice_String).tostring())
        # wf.writeframes(self.Voice_String.decode())
        wf.close()

    def recoder(self):
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE, input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []
        time_count = self.TIME_COUNT

        while True:
            time_count -= 1
            # print time_count
            # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            large_sample_count = np.sum( audio_data > self.LEVEL )
            print(np.max(audio_data))
            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH
            else:
                save_count -= 1

            if save_count < 0:
                save_count = 0

            if save_count > 0 :
            # 将要保存的数据存放到save_buffer中
                #print  save_count > 0 and time_count >0
                save_buffer.append( string_audio_data )
            else:
            #print save_buffer
            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                #print "debug"
                if len(save_buffer) > 0 :
                    self.Voice_String = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
            if time_count==0:
                if len(save_buffer)>0:
                    self.Voice_String = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 录音
def LuYin(filepath):
    res = recoder()
    res.recoder()
    res.savewav(filepath)

# 识别录音
def Identify(mfile):
    result = aipSpeech.asr(get_file_content(mfile), 'wav', 8000, {
        'lan': 'zh',
    })

    print result["result"][0]
    return result["result"][0]

# 智能提示
def SmartTips(mstr):
    mstresult = aipSpeech.synthesis(mstr, 'zh', 1, {
        'vol': 5, 'spd': 5, 'per': 1
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(mstresult, dict):
        with open('files/auido.mp3', 'wb') as f:
            f.write(mstresult)

    filetext = "files/auido.mp3"
    player = mp3play.load(filetext)
    player.play()
    time.sleep(4)


def userLogin(musername):
    # 连接远程的mongodb 数据库
    client = pymongo.MongoClient('120.78.177.150', 27017)
    db = client['myAccount']
    myconn = db['myAccount']

    # 从数据库查找用户名对应的密码
    pwdresult = myconn.find_one({"username": musername})

    if (pwdresult):  # 如果找到了用户名对应的密码，
        os.system('python2  D:\mPython2\AI\AIandSpider\getGold.py ' + musername +" " + pwdresult['password'])
        #     # 提示确认用户，输入提示口令
    # mstr = "谨防他人假冒,请输入中文登录口令"
    # SmartTips(mstr)
    # time.sleep(0.2)
    # # 开始录音
    # LuYin("files/tips")
    # # 识别录音
    # tipsPawwword = Identify("files/tips")
    # count = 0
    # while count < 2:
    #     if (tipsPawwword == pwdresult['tippwd']):
    #         # 对号成功，启动浏览器进行登录
    #         os.system('python2  D:\mPython2\spider\TaoBao\getGold.py ' + musername + pwdresult['password'])
    #         break
    #
    #     else:  # 对号失败，提示用户进行第二次对号
    #         count += 1
    #         if (count == 2):
    #             mstr = "对号失败，芝麻不开门，系统即将退出"
    #             SmartTips(mstr)
    #             break
    #         else:
    #             mstr = "亲，口令不正确，你还有一次机会哟，"
    #             SmartTips(mstr)
    #             time.sleep(0.2)
    #             LuYin("files/tips")  # 录音
    #             # 识别录音
    #             tipsPawwword = Identify("files/tips")


    else:  # 如果没有找到用户名对应的密码，则表示用户第一次使用本系统，需要对用户名和密码进行入库
        tipWord = "您的用户名未入库,请入库您的密码"
        SmartTips(tipWord)
        resultpassword =  raw_input(u"please input your password ")


        # # 提示用户输入登录口令
        # mstr = "谨防他人假冒,请输入中文登录口令"
        # SmartTips(mstr)
        # time.sleep(0.2)
        # # 开始录音
        # LuYin("files/tips")
        # # 识别录音
        # tipsPassord = "每日领金币"
        # tipsPassord = Identify("files/tips")

        # 在数据库中存储用户名和密码，登录口令
        myconn.insert({"username": musername, "password": resultpassword})
        # myconn.insert({"username": musername, "password": resultpassword, 'tippwd': tipsPassord})

        resultWord = "入库成功，开始登录，请稍后"
        os.system('python2  D:\mPython2\AI\AIandSpider\getGold.py  ' + musername + " "+ resultpassword)

        # 启动浏览器进行淘宝登录

if __name__ == "__main__":
    while True:
        # 录音，保存为
        LuYin("files/luyin.wav")

        #  调用百度接口,识别语音
        # 识别刚录好的本地文件
        theWord = Identify("files/luyin1.wav")

        if theWord.find(u'金币') != -1 :
                mstr = "请输入用户名"
                SmartTips(mstr)
                username = raw_input(u"please input the username ")
                userLogin(username)
        elif theWord.find(u'记事本') != -1:
            os.system("notepad")
        elif theWord.find(u'计算器')  != -1:
            os.system("calc")
        elif theWord .find(u'关机')!= -1 and theWord.find(u'取消')!= -1 :
            os.system("shutdown -s -t 300")
        elif theWord.find(u'关机') != -1:
            os.system("shutdown -a")
        elif theWord.find(u'识别')!=-1:
            imgpath  = raw_input(u"please input the path of image ")
            os.system(u'python2  D:\mPython2\AI\AIandSpider/facialFeatures.py '+imgpath)
            time.sleep(10)
        elif theWord.find(u'岗位信息')!=-1:
            os.system(u'python2  D:\mPython2\AI\AIandSpider\JobpageWordCloud\mSalaryMain.py ')

        else:
            os.system(u"python2 D:\mPython2\AI\AIandSpider\Baidusearch.py " + theWord)





