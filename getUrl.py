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
end_time = 1579536000
user = 2028810631

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
        driver.get(
            "https://weibo.com/u/{}?key_word=%E7%96%AB%E6%83%85&start_time={}&end_time={}')".format(
                user, start_time, end_time))
        filepath = "C:\\Users\\26227\\Desktop\\大创\\原始数据\\{}-url.csv".format(user)
        with open(filepath, "a+", encoding="gb2312") as f:
            # f.write("发帖时间,发帖账户,帖子内容,链接\n")
            postset = set()
            for hei in range(0, 10000):
                delay = random.randint(5, 20) / 10
                time.sleep(delay)
                driver.execute_script('window.scrollTo({},{});'.format(hei * 600, (1 + hei) * 600))
                print(delay)
                # print("hh")
                html1 = driver.page_source
                doc1 = pq(html1, parser='html')
                posts = doc1('.vue-recycle-scroller__item-view').items()
                for post in posts:
                    # print("pp")
                    url = post.find(
                        "div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a").attr(
                        'href')
                    url = str(url)
                    if not postset.__contains__(url):
                        # print("enter2")
                        postset.add(url)
                    else:
                        continue
                    uptime = post.find(
                        "div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a").text()
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(1) > div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a
                    title = post.find(
                        "div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.head_nick_1yix2 > a > span").text()
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(12) > div > article > div > div > div.detail_text_1U10O.detail_ogText_2Z1Q8.wbpro-feed-ogText > div > a
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(12) > div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.head_nick_1yix2 > a > span
                    # scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(12) > div > article > div > header > div.woo-box-item-flex.head_main_3DRDm > div > div.woo-box-flex.woo-box-alignCenter.woo-box-justifyCenter.head-info_info_2AspQ > a    # 开始获取帖子信息
                    content = post.find(
                        "div > article > div > div > div.detail_text_1U10O.detail_ogText_2Z1Q8.wbpro-feed-ogText > div > a").text()
                    print("用户：{}，时间：{}，内容：{}，url：{}".format(title, uptime, content, url))
                    f.write("{},{},{},{}\n".format(uptime, title, content, url))
                if len(driver.find_elements(by=By.CSS_SELECTOR,
                                            value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ > div:nth-child(2) > main > div.Main_full_1dfQX > div > div:nth-child(2) > div.container > div:nth-child(3) > div > div > div.woo-box-flex.woo-box-alignCenter.Bottom_box_1riM3 > div.Bottom_text_1kFLe")) > 0:
                    break
    except:
        pass


if __name__ == '__main__':
    # pass
    # driver.get("https://weibo.com/login.php")
    # time.sleep(5)
    # # driver.switch_to.new_window()
    # driver.get("https://www.baidu.com/")
    # time.sleep(10)
    load()
