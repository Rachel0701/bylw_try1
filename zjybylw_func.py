import json
import os
from selenium import webdriver
import time

# 导入一个新cookie
def Getcookie():
    print("当前cookie已失效，请输入新cookie")
    driver1 = webdriver.Firefox()
    driver1.get('https://weibo.com/login.php')
    title = driver1.title
    while (title != "微博 – 随时随地发现新鲜事"):
        time.sleep(1)
        title = driver1.title
        print(title)
    time.sleep(1)
    dictCookies = driver1.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存

    txt_name = 'cookie/微博_cookies0.txt'
    with open(txt_name, 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')
    driver1.quit()

def read_cookie(driver):
    driver.get('https://weibo.com/login.php')
    print(driver.title)
    time.sleep(5)
    with open("cookie/微博_cookies0.txt", 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        cookie_dict = {
            'domain': '.weibo.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        driver.add_cookie(cookie_dict)
    time.sleep(3)
    driver.refresh()  # 刷新网页,cookies才成功
    time.sleep(3)
    if (driver.title == "微博 – 随时随地发现新鲜事"):
        print("cookie登录成功")
        time.sleep(1)
        return driver

    # 更新cookie
    Getcookie()

    # 再次添加cookies
    with open("cookie/微博_cookies0.txt", 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        cookie_dict = {
            'domain': '.weibo.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        driver.add_cookie(cookie_dict)
    time.sleep(3)
    driver.refresh()  # 刷新网页,cookies才成功
    time.sleep(3)
    if (driver.title == "微博 – 随时随地发现新鲜事"):
        print("cookie登录成功")
        time.sleep(1)
        return driver
    else:
        print("登录失败,请检查")


def get_cookie(driver, txt_name):
    print(txt_name)
    with open("cookie/" + txt_name, 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    # 往browser里添加cookies
    for cookie in listCookies:
        cookie_dict = {
            'domain': '.weibo.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        driver.add_cookie(cookie_dict)
    time.sleep(3)
    driver.refresh()  # 刷新网页,cookies才成功