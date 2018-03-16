# coding:utf-8
# from spider.JobpageWordCloud.MakeWordCloud import outputCiyun
# from spider.JobpageWordCloud.SmtpExample import sendEmail
# from spider.JobpageWordCloud.mwordCloud import getworkinfo, geturl
# import AI.AIandSpider.JobpageWordCloud.mwordCloud
#
# import AI.AIandSpider.JobpageWordCloud.MakeWordCloud
#
# import AI.AIandSpider.JobpageWordCloud.SmtpExample

from MakeWordCloud import *
from SmtpExample import *
from mwordCloud import *
from worknum import *
if __name__ == '__main__':
    # 1.绘制北京，上海，深圳,python岗位数量的图  51job
    sumwork1()

    # 北京，上海，深圳的  python ,运维，测试，爬虫，数据,web等等岗位分布图
    sumwork2()

    # 3.绘制北京，上海，深圳的最低平均工资，最高平均工资对比图
    sumwork3()

    # 上海 url 抓取到的url 存储在url.txt 文件中
    geturl("html","上海")

    # 读取url.txt文件取出url 抓取 工作要求
    rfile = open("url.txt", "r")
    rurllist = rfile.readlines()
    infofile = open("info.txt", "w")
    for rurl in rurllist:
        if rurl != "\n":
            workinfo = getworkinfo(rurl.rstrip())
            try:
                if workinfo != "":
                    infofile.write((workinfo + "\r\n").encode('utf-8'))
            except Exception as e:
                print  "ERROR@", e

    infofile.close()

    outputCiyun()

    sendEmail()


