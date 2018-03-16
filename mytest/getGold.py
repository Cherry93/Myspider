#coding:utf-8
'''
模拟淘宝领金币
'''

#coding:utf-8
import lxml.etree
import requests
import selenium
import sys
from bs4 import BeautifulSoup
from  selenium import webdriver
import time

#设置
from selenium.webdriver import ActionChains

# import mp3play
# from aip import AipSpeech
# """ 你的 APPID AK SK """
# APP_ID = '10254547'
# API_KEY = 'KN3hFlvWrHykUD8iN12Ah8Q1'
# SECRET_KEY = 'pPhhSxEnuKa30nUIj2elReioqLMsHolw '
# aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 打开火狐浏览器
driver= selenium.webdriver.Chrome()
driver.get("https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F")
time.sleep(2)

try:
    elem = driver.find_element_by_link_text('密码登录')
    elem.click()
    time.sleep(2)
except Exception as e :
    print (e)
    pass

# 模拟输入账号密码
username=driver.find_element_by_id("TPL_username_1")
password=driver.find_element_by_id("TPL_password_1")
username.send_keys('王湘英00')
time.sleep(2)
password.send_keys('wxy15773978948@')
time.sleep(2)
click=driver.find_element_by_id("J_SubmitStatic")
# 点击登录按钮，登录成功
click.click()
time.sleep(10)

try:
    # 点击我的淘宝
    mytaobao = driver.find_element_by_link_text('我的淘宝')
    ActionChains(driver).move_to_element(mytaobao).perform()
    mytaobao.click()
    time.sleep(6)

    # 点击淘金币
    mybao = driver.find_element_by_link_text('淘金币')
    ActionChains(driver).move_to_element(mybao).perform()
    time.sleep(1)
    mybao.click()
    time.sleep(4)



#     firstwin=driver.current_window_handle #当前的窗体
#     allwindows=driver.window_handles#所有的窗口
#     result = "未找到"
#     #选择注册窗口
#     for  win  in allwindows:
#         if win !=firstwin:
#             driver.switch_to.window(win)
#             print ("切换成功")
#             time.sleep(5)
#             pagesource =  driver.page_source
#
#             try:          # 点击今日领金币
#                 gold = driver.find_element_by_xpath('//a[@class=\'J_GoTodayBtn\']//em/text()')
#                 mygold = driver.find_element_by_class_name('J_GoTodayBtn')
#                 ActionChains(driver).move_to_element(mygold).perform()
#                 time.sleep(1)
#                 mygold.click()
#                 time.sleep(4)
#                 print ("领取成功",str(gold[0]))
#                 result = aipSpeech.synthesis("领取成功,今日领取金币"+ str(gold[0]), 'zh', 1, {
#                     'vol': 5, 'spd': 5, 'per': 3
#                 })
#
#             except :          # 今日金币已领
#                 mytreegold = lxml.etree.HTML(pagesource)
#                 goldlist = mytreegold.xpath("//p[@class=\"take-tips\"]//em//text()")
#                 goldsum = mytreegold.xpath("//p[@class=\"lg-1 info J_Coin\"]/a/text()")
#                 mytipstr = "今日金币已领取，连续领取"+goldlist[0]+"天，明天可领金币"+goldlist[1] + "，现共有金币" + goldsum[0]
#
#                 result = aipSpeech.synthesis(mytipstr, 'zh', 1, {
#                     'vol': 6, 'spd': 5, 'per': 3
#                 })
#
#     # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
#     if not isinstance(result, dict):
#         with open('files/auido.mp3', 'wb') as f:
#             f.write(result)
#
#
#     filename = "files/auido.mp3"
#     player = mp3play.load(filename)
#     player.play()
#     time.sleep(10)
#     driver.close()
except :
    print  ("登录失败")

