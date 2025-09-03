from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from login import login

def auto_select_course(driver):
    import datetime

    # 获取结果第一条课程的选课开始时间
    first_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[contains(@ng-repeat,'course in vm.data.coursePageList')]"))
    )
    start_time_str = first_row.find_element(By.XPATH, ".//div[contains(text(),'选课开始：')]").text.replace("选课开始：", "").strip()
    print(f"[日志] 选课开始时间：{start_time_str}")

    # 转换为时间对象
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    now = datetime.datetime.now()
    wait_seconds = (start_time - now).total_seconds()
    if wait_seconds > 0:
        print(f"[日志] 距离选课开始还有 {wait_seconds:.2f} 秒，等待中...")
        time.sleep(wait_seconds)
    else:
        print("[日志] 已到选课时间，准备选课...")

    while True:
        # 点击刷新列表
        refresh_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'btn-warning') and contains(.,'刷新列表')]"))
        )
        refresh_btn.click()
        print("[日志] 已点击刷新列表")
        time.sleep(1)

        # 检查“报名课程”按钮是否出现
        try:
            signup_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'text-success') and contains(.,'报名课程')]"))
            )
            signup_btn.click()
            print("[日志] 已点击报名课程按钮")
            time.sleep(1)

            # 等待弹窗出现并点击“确定”
            confirm_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-dialog ']//button[contains(@class,'btn-primary') and contains(text(),'确定')]"))
            )
            confirm_btn.click()
            print("[日志] 已点击弹窗确定按钮")
            time.sleep(1)

            # 检查是否变为“退选”
            try:
                cancel_btn = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'退选')]"))
                )
                print("[日志] 选课成功，已变为退选")
                break
            except:
                print("[日志] 选课未成功，继续刷新列表")
                continue
        except:
            print("[日志] 未检测到报名课程按钮，继续刷新列表")
            continue

def BoyaSelect(driver):
    # 等待“我的课程”菜单出现并点击展开
    my_course = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='我的课程']"))
    )
    my_course.click()
    time.sleep(1)  # 等待子菜单展开

    # 等待“选择课程”子菜单出现并点击
    select_course = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='选择课程']"))
    )
    select_course.click()

    # 等待课程名称检索框出现
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@st-search='courseName']"))
    )
    course_name = input("请输入要检索的课程名称：")
    search_box.clear()
    search_box.send_keys(course_name)
    search_box.send_keys(u'\ue007')  # 发送回车键

    # 点击刷新列表，确保数据最新
    refresh_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'btn-warning') and contains(.,'刷新列表')]"))
    )
    refresh_btn.click()
    print("[日志] 已点击刷新列表")
    time.sleep(1)

    # 自动选课流程
    auto_select_course(driver)