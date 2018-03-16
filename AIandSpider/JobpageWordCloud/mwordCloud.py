# encoding:utf-8
import urllib2

import selenium  #测试框架
import selenium.webdriver #模拟浏览器
import  re

import matplotlib
import  matplotlib.pyplot as plt #数据可视化

matplotlib.rcParams["font.sans-serif"]=["simhei"] #配置字体
matplotlib.rcParams["font.family"]="sans-serif"


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

def  geturl(searchname,place):
    filePath = "url.txt"
    file = open(filePath, 'w')
    if (place == "北京"):
        placeNum = '010000'
    elif (place == "深圳"):
        placeNum = '040000'
    elif place == "上海":
        placeNum = "020000"



    url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea="+placeNum+"&keyword=" + searchname + "&keywordtype=2&lang=c&stype=2&curr_page=69&postchannel=0000&fromType=1&confirmdate=9"

    request = urllib2.Request(url, headers=header)
    pagesource = urllib2.urlopen(request).read()

    restr = "<span class=\"td\">(.*?)</span>"
    sumpage = re.compile(restr, re.I).findall(pagesource)
    sumpage = re.compile('.*?(\\d+).*').findall(sumpage[0])
    for i in range(1, int(sumpage[0]) + 1):
        url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=" + placeNum + "&keyword=" + searchname + "&keywordtype=2&lang=c&stype=2&curr_page=" + str(
            i) + "&postchannel=0000&fromType=1&confirmdate=9"
        request = urllib2.Request(url, headers=header)
        pagesource = urllib2.urlopen(request).read()
        restr = "<p class=\"t1 \">(.*?)</p>"
        t1list  = re.compile(restr, re.S).findall(pagesource)
        print  len(t1list)
        print  t1list
        restr = "href=\"(.*?)\""
        pattern = re.compile(restr,re.S)
        for t1 in t1list:
            aurl = pattern.findall(t1)
            file.write((aurl[0] + "\r\n").encode("utf-8"))
            print aurl
    file.close()

    print  "*********",place ,"     " ,searchname ,"***********"

def getworkinfo(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);"}
    request = urllib2.Request(url, headers=headers)  # 发起请求，
    # 也可以通过调⽤Request.add_header() 添加/修改⼀个特定的 header
    request.add_header("Connection", "keep-alive")  # 一直活着
    try :
        response = urllib2.urlopen(request)
        data = response.read()  # 打开请求，抓取数据

        restr = "<div class=\"bmsg job_msg inbox\">([\s\S]*?)</div>"  # 正则表达式，（）只要括号内的数据
        regex = re.compile(restr, re.IGNORECASE)
        mylist = regex.findall(data)
        # print mylist
        if len(mylist) > 0:
            print  mylist[0].decode("gbk").strip()
            laststr = mylist[0].decode("gbk").strip().replace("<p", "").replace("</p>", "").replace("<span class=\"label\">", "").replace("</span>", "").replace("class","").replace("fp f2","").replace("mt10","")
            laststr = laststr.replace("=", "").replace("<span", "").replace("<br>","").replace(" ","").replace("\r\n","").replace("<div","").replace(">","").replace("el","").strip()
            return laststr
        else:
            return ""
    except Exception as e:
        print  "ERROR",e



if __name__ == '__main__':

    # 上海 url 抓取到的url 存储在url.txt 文件中
    # geturl("python","上海")

    # 读取url.txt文件取出url 抓取 工作要求
    rfile = open("url.txt","r")
    rurllist = rfile.readlines()
    infofile = open("info.txt", "w")
    for rurl in rurllist:
        if rurl != "\n":
            print rurl.rstrip()
            workinfo = getworkinfo(rurl.rstrip())
            try :
                if workinfo != "" :
                    infofile.write((workinfo +"\r\n" ).encode('utf-8'))
            except Exception as e:
                print  "ERROR@",e

    infofile.close()



