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
user = 2803301701


chrome_options = webdriver.EdgeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

def load():
    driver.get("https://weibo.com/login.php")
    try:
        driver
        html1 = driver.page_source
        doc1 = pq(html1, parser='html')
        # 切换到扫码登录
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#pl_login_form > div > div.info_header > div > a:nth-child(2)"))
        )
        btn.click()
        key = input("任意输入以继续：")
        # 打开搜索页面
        filepath = "D:\\大创\\原始数据\\{}.csv".format(user)
        with open(filepath, "w+", encoding="gb2312") as f:
            f.write("发帖时间,发帖账户,帖子内容,评论\n")
            postset = set()
            for hei in range(1, 100):
                driver.get(
                    "https://weibo.com/u/{}?key_word=%E7%96%AB%E6%83%85&start_time={}&end_time={}')".format(
                        user, start_time, end_time))
                # print("get")
                time.sleep(2)
                driver.execute_script('window.scrollTo({},{});'.format(0, hei * 600))
                time.sleep(1)
                html1 = driver.page_source
                doc1 = pq(html1, parser='html')
                posts = doc1('.vue-recycle-scroller__item-view').items()
                for post in posts:
                    # print("pp")
                    uptime = post.find(
                        "div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a").text()
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(1) > div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a
                    uptime = str(uptime)
                    if not postset.__contains__(uptime):
                        # print("enter2")
                        postset.add(uptime)
                    else:
                        continue
                    title = post.find(
                        "div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.head_nick_1yix2 > a > span").text()
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(12) > div > article > div > div > div.detail_text_1U10O.detail_ogText_2Z1Q8.wbpro-feed-ogText > div > a
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(12) > div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.head_nick_1yix2 > a > span
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(12) > div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a    # 开始获取帖子信息
                    content = post.find(
                        "div > article > div > div > div.detail_text_1U10O.detail_ogText_2Z1Q8.wbpro-feed-ogText > div > a").text()
                    url = post.find(
                        "div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a").attr(
                        'href')
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(1) > div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a
                    # print(url)
                    driver.get(
                        url)  # pl_feedlist_index > div:nth-child(2) > div:nth-child(2) > div > div.card-feed > div.content > div.from > a:nth-child(1)
                    time.sleep(2)
                    html1 = driver.page_source
                    doc1 = pq(html1, parser='html')
                    # print(doc1)

                    hhh = doc1(".item").items()
                    # print(hhh)
                    cnnnt = 0
                    for cnnt in hhh:
                        cnnnt += 1
                    # print(cnnnt)
                    if cnnnt == 0:
                        # # print(driver.find_elements(by=By.CSS_SELECTOR,value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ.Frame_noside1_3M1rh.Frame_noside2_1lBwY > div:nth-child(2) > main > div > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > article > footer > div > div:nth-child(1) > div > div:nth-child(2) > div > span")[0].text)
                        #
                        # if len(driver.find_elements(by=By.CSS_SELECTOR,
                        #                             value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ.Frame_noside1_3M1rh.Frame_noside2_1lBwY > div:nth-child(2) > main > div > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div > div.wbpro-tab3 > div > div:nth-child(2)")) == 0:
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
                        driver.execute_script('window.scrollTo({},{});'.format(now, now + 600));
                        time.sleep(0.5)
                        now = now + 600
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
                                print(text)
                                try:
                                    f.write("{},{},{},{}\n".format(uptime, title, content, text))
                                    # print("write")
                                except:
                                    # print("con")
                                    continue
                        if ccc == 0:
                            now -= 600
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
                #             time.sleep(2)
                # print("emd")
                # if len(driver.find_elements(by=By.CSS_SELECTOR,
                #                             value="#pl_feedlist_index > div.m-page > div > a.next")) > 0:
                #     page += 1
                #     driver.get(
                #         "https://weibo.com/u/{}?key_word=%E7%96%AB%E6%83%85&start_time={}&end_time={}')".format(
                #             user, start_time, end_time))
                #     time.sleep(2)
                # else:
                #     break
                #     # time.sleep(10)
                #     # get_img()
            f.close()
    except TimeoutError:
        load()
    finally:
        driver.quit()


def get_img():
    time.sleep(2)
    html = driver.page_source
    doc = pq(html, parser='html')
    print(doc)
    items = doc('.card-wrap').items()
    path = mkdir()
    cnt = 1
    for li in items:
        img_addr = li.find('.card-act ul li a').attr('href')
        if save(img_addr, path, cnt):
            print("\rfinish {} page".format(cnt), end="")
            cnt += 1
        else:
            cnt = 1


def save1(data, path, num):
    filepath = path + '//{}.jpg'.format(num)
    try:
        r = requests.get(data)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        return True
    except:
        print("\nfail", end="")
        return False


def mkdir():
    path = 'D://spider_test'
    if not os.path.exists(path):
        os.mkdir(path)
        print("creat file successfully")
    else:
        print('file exited')
    return path


if __name__ == '__main__':
    # pass
    # driver.get("https://weibo.com/login.php")
    # time.sleep(5)
    # # driver.switch_to.new_window()
    # driver.get("https://www.baidu.com/")
    # time.sleep(10)
    load()
