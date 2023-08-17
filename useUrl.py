import csv
import os.path
import random
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

driver = webdriver.Edge()
# print(dir(driver))
driver.maximize_window()
# start_time = "2021-01-01"
# end_time = "2022-07-01"
start_time = 1577808000
end_time = 1672588800
user = 2028810631
path = "C:\\Users\\26227\\Desktop\\大创\\原始数据\\"

filename = "{}{}-url.csv".format(path, user)
titles = []
uptimes = []
contents = []
data = []

with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    # header = next(csv_reader)        # 读取第一行每一列的标题
    for row in csv_reader:  # 将csv 文件中的数据保存到data中
        titles.append(row[1])  # 选择某一列加入到data数组中
        uptimes.append(row[0])  # 选择某一列加入到data数组中
        contents.append(row[2])  # 选择某一列加入到data数组中
        data.append(row[3])  # 选择某一列加入到data数组中
    csvfile.close()

data = data[1:]
titles = titles[1:]
uptimes = uptimes[1:]
contents = contents[1:]
filepath = "{}{}-commont.csv".format(path, user)
driver.get("https://weibo.com/login.php")

html1 = driver.page_source
doc1 = pq(html1, parser='html')
# 切换到扫码登录
btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#pl_login_form > div > div.info_header > div > a:nth-child(2)"))
)
btn.click()
key = input("任意输入以继续：")

with open(filepath, "a+", encoding="gb2312") as f:
    # f.write("发帖时间,发帖账户,帖子内容,链接\n")
    cntcom = 0
    starttime = time.time()
    for url in range(428, len(data)):
        driver.get(data[url])
        time.sleep(2)
        html1 = driver.page_source
        doc1 = pq(html1, parser='html')

        # 检查是否无评论
        hhh = doc1(".item").items()
        cnnnt = 0
        for cnnt in hhh:
            cnnnt += 1
        if cnnnt == 0:
            continue
        # # 切换到按时间排序
        # btn = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                                 "#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ > div:nth-child(2) > main > div.Main_full_1dfQX > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div > div.wbpro-tab3 > div > div:nth-child(2)"))
        # )  # app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ > div:nth-child(2) > main > div.Main_full_1dfQX > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div > div.wbpro-tab3 > div > div:nth-child(2)
        # btn.click()
        # time.sleep(1)

        texts = set()
        now = 0

        while True:
            pa = random.randint(1, 3)
            driver.execute_script('window.scrollTo({},{});'.format(now, now + pa * 100));
            delay = random.randint(10, 30) / 10
            time.sleep(delay)
            # print(delay)
            now = now + pa * 100
            html1 = driver.page_source
            doc1 = pq(html1, parser='html')
            items = doc1('.vue-recycle-scroller__item-view').items()
            ccc = 0
            for li in items:
                text = str(li.find('div.text > span'))
                if len(text) > 200:
                    continue
                while text.__contains__('<img'):
                    rar = text.index('<img')
                    head = text.index('/>') + 2
                    text = str(text[:rar]) + str(text[head:])
                while text.__contains__('<a h'):
                    rar = text.index('<a h')
                    head = text.index('/a>') + 3
                    text = str(text[:rar]) + str(text[head:])
                ind2 = text.index('</span>')
                text = text[6:ind2]
                # print(text)
                # print("enter")
                if not texts.__contains__(text):
                    # print("enter2")
                    ccc += 1
                    texts.add(text)
                    # print(text)
                    # print(uptimes[url])
                    # print(title[url])
                    # print(content[url])
                    try:
                        cntcom += 1
                        f.write("{},{},{},{}\n".format(uptimes[url], titles[url], contents[url], text))
                        nowtime = time.time()
                        print("正在爬取第{}篇帖子，共完成{}条评论,每条评论平均花费时间为{}秒".format(url + 1, cntcom,
                                                                                                    (
                                                                                                            nowtime - starttime) / cntcom))

                        # print("write")
                    except:
                        # print("con")
                        continue
            # if ccc == 0:
            #     now -= 200
            # app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ.Frame_noside1_3M1rh.Frame_noside2_1lBwY > div:nth-child(2) > main > div > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div.RepostCommentList_tip_2O5W- > div > span
            if len(driver.find_elements(by=By.CSS_SELECTOR,
                                        value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ.Frame_noside1_3M1rh.Frame_noside2_1lBwY > div:nth-child(2) > main > div > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div > div.RepostCommentList_mar1_3VHkS > div > div > div.woo-box-flex.woo-box-alignCenter.Bottom_box_1riM3 > div.Bottom_text_1kFLe")) > 0 \
                    or len(driver.find_elements(by=By.CSS_SELECTOR,
                                                value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ.Frame_noside1_3M1rh.Frame_noside2_1lBwY > div:nth-child(2) > main > div > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div.RepostCommentList_tip_2O5W- > div > span")) > 0 \
                    or len(driver.find_elements(by=By.CSS_SELECTOR,
                                                value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ > div:nth-child(2) > main > div.Main_full_1dfQX > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div.RepostCommentList_tip_2O5W- > div > span")) > 0 \
                    or len(driver.find_elements(by=By.CSS_SELECTOR,
                                                value="#scroller > div.vue-recycle-scroller__slot > div > div > div > span")) > 0 \
                    or len(driver.find_elements(by=By.CSS_SELECTOR,
                                                value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ > div:nth-child(2) > main > div.Main_full_1dfQX > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div > div.RepostCommentList_mar1_3VHkS > div > div > div.woo-box-flex.woo-box-alignCenter.Bottom_box_1riM3 > div.Bottom_text_1kFLe")) > 0:
                break
    f.close()
