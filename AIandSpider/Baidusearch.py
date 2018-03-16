#coding:utf-8
'''
百度搜索
'''
import selenium.webdriver
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    url = "http://www.baidu.com"
    # 打开火狐浏览器
    driver = selenium.webdriver.Firefox()
    driver.get(url)
    time.sleep(6)  # 等待页面的加载

    elem  = driver.find_element_by_id('kw')
    print sys.argv[1]
    print str(sys.argv[1])[0:-3]
    try:
        elem.send_keys(sys.argv[1][0:-3].decode('utf-8'))
    except Exception as e:
        elem.send_keys(sys.argv[1][0:-3].decode('gbk'))
    elem.send_keys(Keys.RETURN)
    time.sleep(5)  # 等待搜素页面的加载


