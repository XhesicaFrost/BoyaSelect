from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import getpass
from login import login
from BoyaSelect import BoyaSelect

login_url="https://d.buaa.edu.cn/https/77726476706e69737468656265737421f2ee4a9f69327d517f468ca88d1b203b/login"

if __name__=='__main__':
    print("博雅自动选课准备中")
    username = input("请输入学号")
    password = getpass.getpass("请输入密码（输入时不会显示）：")

    driver = login(username, password, login_url)
    if driver is None:
        print("登录失败，程序结束")
        exit(1)
    print("登录成功，准备选课")
    BoyaSelect(driver)
    input("请观察结果")


