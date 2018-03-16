# -*- coding: utf-8 -*-
'''
伪装请求头 1.绘制北京，上海，深圳,python岗位数量的图  51job
'''
import re
import urllib
import urllib2

import matplotlib
import  matplotlib.pyplot as plt #数据可视化
import time
import matplotlib as mpl
import numpy as np

matplotlib.rcParams["font.sans-serif"]=["simhei"] #配置字体
matplotlib.rcParams["font.family"]="sans-serif"


# 各城市工资列表
sumworklist = []

# 各城市名称列表
placelist = [u"北京", u"上海", u"深圳"]


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

# 获得岗位数量
def  getnumberbyname(searchname,place):
    if (place == u"北京"):
        placeNum = '010000'
    elif (place == u"深圳"):
        placeNum = '040000'
    elif place == u"上海":
        placeNum = "020000"

    url = "http://search.51job.com/jobsearch/search_result.php?"
    word = {"jobarea": placeNum, "keyword": searchname}
    word = urllib.urlencode(word)  # 编码成字符串
    url = url + word
    request = urllib2.Request(url, headers=header)  # 发起请求，
    # 也可以通过调⽤Request.add_header() 添加/修改⼀个特定的 header
    request.add_header("Connection", "keep-alive")  # 一直活着
    response = urllib2.urlopen(request)
    pagesource = response.read()  # 打开请求，抓取数据

    restr = "<div class=\"rt\">[\s\S]*?</div>"
    swork = []
    swork = re.compile(restr,re.I).findall(pagesource)
    sumwork = []
    sumwork = re.compile("(\\d+)").findall(swork[0])
    print sumwork
    print  place,searchname,sumwork[0]

    sumworklist.append(sumwork[0])
    return  sumwork[0]

def getAverageSalary(searchname,place):
    if (place == u"北京"):
        placeNum = '010000'
    elif (place == u"深圳"):
        placeNum = '040000'
    elif place == u"上海":
        placeNum = "020000"

    bottomlist = []
    toplist = []

    url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=" + placeNum + "&keyword=" + searchname + "&keywordtype=2&lang=c&stype=2&curr_page=69&postchannel=0000&fromType=1&confirmdate=9"

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
        restr = """<span class="t4">(.*)</span>"""  # 正则表达式，（）只要括号内的数据,如果正则抓取失败，空白字符
        regex = re.compile(restr, re.I)
        mylist = regex.findall(pagesource)
        print(len(mylist))
        for list in mylist:
            list = list.decode('gbk')
            if (list.find('-') != -1 and list.find('/') != -1):
                indexBarsH = list.find('-')
                indexBarsO = list.find('/')
                bottomMoney = list[0:indexBarsH]
                topMoney = list[indexBarsH + 1:indexBarsO - 1]

                if (list.find(u'月') != -1 and list.find(u'万') != -1):
                    bottomlist.append(bottomMoney)
                    toplist.append(topMoney)
                if (list.find(u'月') != -1 and list.find(u'千') != -1):
                    bottomlist.append(str(round(float(bottomMoney) / 10, 1)))
                    toplist.append(str(round(float(topMoney) / 10, 1)))

                if (list.find(u'年') != -1):
                    bottomlist.append(str(round(float(bottomMoney) / 12, 1)))
                    toplist.append(str(round(float(topMoney) / 12, 1)))



    print  "*********", place, "     ", searchname, "***********"
    return  bottomlist, toplist


baveragelist = []
aaveragelist = []


def averageSalary(bottomlist, toplist):
    bsum = 0
    for b in bottomlist:
        bsum += float(b)
    baverage = round(bsum / len(bottomlist), 2)

    tsum = 0
    for t in toplist:
        tsum += float(t)
    taverage = round(tsum / len(toplist), 2)
    ave = round((taverage + baverage) / 2, 2)
    baveragelist.append(baverage)
    aaveragelist.append(taverage)
    print("低平均薪资:%f" % baverage)
    print("高平均薪资:%f" % taverage)
    print('平均薪资:%f' % ave)
    # draw()



#1.绘制北京，上海，深圳,python岗位数量的图  51job
def sumwork1():
    for place in placelist:
        getnumberbyname("python", place)

     # 绘图
    draw()

# 北京，上海，深圳的  python ,运维，测试，爬虫，数据,web等等岗位分布图
def sumwork2 ():
    for place in placelist:
        if place == "北京":
            imgplace = "beijin"
        if place == "深圳":
            imgplace = "shenzhen"
        if place == "上海":
            imgplace = "shanghai"


        pythonlist = ["python","python 运维" ,"python 测试", "python 数据", "python web"]
        num = 0
        for pystr in pythonlist:
            num += 1
            rects1 = plt.bar([num], eval(getnumberbyname(pystr,place)), label=pystr.decode('utf-8'))
            add_labels(rects1)
        plt.legend()  # 绘制
        plt.xlabel(place)
        plt.title(u'互联网薪资对比')
        plt.ylabel(u'薪资')
        plt.savefig(imgplace+'.jpg')
        plt.close()


# 添加数据标签
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        # 柱形图边缘用白色填充，纯粹为了美观
        rect.set_edgecolor('white')





def sumwork3():
    for place in placelist:
        bottomlist, toplist=  getAverageSalary('html',place)
        averageSalary(bottomlist, toplist)
    draw2()



# 绘图
def draw():
    num = 0
    for sum in sumworklist:
        num += 1
        print placelist[num-1],sum
        rects1 = plt.bar([num], eval(sum), label=placelist[num-1])
        add_labels(rects1)
    # 指定标题和坐标注释
    plt.legend()  # 绘制
    plt.xlabel(u"区域")
    plt.title(u'互联网薪资对比')
    plt.ylabel(u'薪资')
    plt.savefig(u'BSS.jpg')
    plt.close()



# 绘图
def draw2():
    bar_width = 0.35
    names = [u"低平均薪资",u"高平均薪资"]
    index = np.arange(len(baveragelist))

    # 绘制最低的薪资
    rects1 = plt.bar(index, baveragelist, bar_width, color='#0072BC', label=names[0])
    # 绘制最高的薪资
    rects2 = plt.bar(index + bar_width, aaveragelist, bar_width, color='#ED1C24', label=names[1])

    add_labels(rects1)
    add_labels(rects2)

    # X轴标题
    plt.xticks(index + bar_width, placelist )
    plt.title(u'互联网薪资对比')
    # 图例显示在图表下方
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, ncol=5)

    # 图表输出到本地
    plt.savefig('average.jpg')
    plt.close()



if __name__ == '__main__':
    # 1.绘制北京，上海，深圳,python岗位数量的图  51job
    # sumwork1()

    # 北京，上海，深圳的  python ,运维，测试，爬虫，数据,web等等岗位分布图
    # sumwork2()

    # 3.绘制北京，上海，深圳的最低平均工资，最高平均工资对比图
    sumwork3()





