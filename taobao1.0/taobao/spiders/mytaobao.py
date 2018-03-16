# -*- coding: utf-8 -*-
import scrapy
from  scrapy.http import FormRequest #抓取表单，返回表单数据
from  selenium import webdriver #调用浏览器
from  scrapy.xlib.pydispatch import dispatcher #观察者
from  scrapy import signals #信号


class MytaobaoSpider(scrapy.Spider):
    name = 'mytaobao'
    allowed_domains = ['taobao.com']
    start_urls = ['https://login.m.taobao.com/login.htm',"http://h5.m.taobao.com/mlapp/olist.html?spm=a2141.7756461.2.6"]
    def __init__(self): #初始化
        mobilesetting={"deviceName":"iPhone 6 Plus"}
        options=webdriver.ChromeOptions()#浏览器选项
        options.add_experimental_option("mobileEmulation",mobilesetting)#模拟手机
        self.browser=webdriver.Chrome(chrome_options=options)#创建一个浏览器
        self.browser.set_window_size(400,800)#配置手机大小
        super(MytaobaoSpider,self).__init__() #传递给父类
        dispatcher.connect(self.spider_closed,signals.spider_closed)#爬虫关闭通过信号调用我们自己的函数


    def spider_closed(self,response):#爬虫关闭
        print("爬虫关闭")
        self.browser.close() #关闭浏览器
    def parse(self, response):
        #打印链接，打印网页源代码
        print('源码')
        print(response.url)
        print(response.body.decode("utf-8","ignore"))
