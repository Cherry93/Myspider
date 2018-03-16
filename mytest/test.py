from selenium import webdriver
import requests
import time
from selenium.webdriver.support.ui import WebDriverWait
def login_taobao():
    driver = webdriver.Chrome()
    driver.maximize_window() #将浏览器最大化显示
    driver.delete_all_cookies()
    driver.get("https://login.taobao.com/member/login.jhtml")
    #load the switch
    element=WebDriverWait(driver,60).until(lambda driver :
    driver.find_element_by_xpath("//*[@id='J_Quick2Static']"))
    element.click()
    driver.implicitly_wait(20)
    username=driver.find_element_by_name("TPL_username")
    if not username.is_displayed:
        driver.implicitly_wait(20)
        driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
        time.sleep(10)
    driver.implicitly_wait(20)
    username.send_keys("王湘英00")
    driver.find_element_by_name("TPL_password").send_keys("wxy15773978948@")
    time.sleep(10)
    driver.implicitly_wait(20)
    driver.find_element_by_xpath("//*[@id='J_SubmitStatic']").click()
    time.sleep(20)
    print('ok')
    #以下是获得cookie代码
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookiestr = ';'.join(item for item in cookie)
    print(cookiestr)
    return driver
login_taobao()