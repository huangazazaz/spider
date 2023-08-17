import os.path
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
start_time = "2021-01-01"
end_time = "2022-07-01"
# start_time = 1577808000
# end_time = 1672588800
# user = 2803301701

# chrome_options = webdriver.EdgeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)

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
            "https://s.weibo.com/weibo?q=%E7%96%AB%E6%83%85&xsort=hot&suball=1&timescope=custom%3A{}%3A{}&Refer=g".format(
                start_time, end_time))
        time.sleep(2)
        page = 1
        filepath = "D:\\大创\\原始数据\\data.csv"
        with open(filepath, "w+", encoding="gb2312") as f:
            f.write("发帖时间,发帖账户,帖子内容,评论\n")
            while True:
                cntt = driver.find_elements(by=By.CLASS_NAME, value="card-wrap")
                for ind in range(1, len(cntt)):
                    # 开始获取帖子信息
                    ite = driver.find_elements(by=By.CSS_SELECTOR,
                                               value="#pl_feedlist_index > div:nth-child(2) > div:nth-child({}) > div > div.card-feed > div.content > div.info > div:nth-child(2) > a".format(
                                                   ind))
                    title = ite[0].text
                    ite = driver.find_elements(by=By.CSS_SELECTOR,
                                               value="#pl_feedlist_index > div:nth-child(2) > div:nth-child(2) > div > div.card-feed > div.content > p:nth-child(3)".format(
                                                   ind))
                    content = ite[0].text
                    ite = driver.find_elements(by=By.CSS_SELECTOR,
                                               value="#pl_feedlist_index > div:nth-child(2) > div:nth-child({}) > div > div.card-feed > div.content > div.from > a:nth-child(1)".format(
                                                   ind))
                    uptime = ite[0].text
                    driver.get(ite[0].get_attribute(
                        'href'))  # pl_feedlist_index > div:nth-child(2) > div:nth-child(2) > div > div.card-feed > div.content > div.from > a:nth-child(1)
                    time.sleep(2)
                    if len(driver.find_elements(by=By.CSS_SELECTOR,
                                                value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ > div:nth-child(2) > main > div.Main_full_1dfQX > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div > div.wbpro-tab3 > div > div:nth-child(2)")) == 0:
                        driver.get(
                            "https://s.weibo.com/weibo?q=%E7%96%AB%E6%83%85&xsort=hot&suball=1&timescope=custom%3A{}%3A{}&Refer=g&page={}".format(
                                start_time, end_time, page))
                        time.sleep(2)
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
                                texts.add(text)
                                print(text)
                                try:
                                    f.write("{},{},{},{}\n".format(uptime, title, content, text))
                                except:
                                    continue
                        if len(driver.find_elements(by=By.CSS_SELECTOR,
                                                    value="#app > div.woo-box-flex.woo-box-column.Frame_wrap_3g67Q > div.woo-box-flex.Frame_content_3XrxZ > div:nth-child(2) > main > div.Main_full_1dfQX > div > div.woo-panel-main.woo-panel-top.woo-panel-right.woo-panel-bottom.woo-panel-left.Card_wrap_2ibWe.Card_bottomGap_2Xjqi.Detail_detail_3typT > div.Detail_box_3Jeom > div:nth-child(3) > div > div.RepostCommentList_mar1_3VHkS > div > div > div.woo-box-flex.woo-box-alignCenter.Bottom_box_1riM3 > div.Bottom_text_1kFLe")) > 0\
                        or len(driver.find_elements(by=By.CSS_SELECTOR,
                                                    value="#scroller > div.vue-recycle-scroller__slot > div > div > div > span")) > 0\
                                :
                            driver.get(
                                "https://s.weibo.com/weibo?q=%E7%96%AB%E6%83%85&xsort=hot&suball=1&timescope=custom%3A{}%3A{}&Refer=g&page={}".format(
                                    start_time, end_time, page))
                            time.sleep(2)
                            break
                if len(driver.find_elements(by=By.CSS_SELECTOR,
                                            value="#pl_feedlist_index > div.m-page > div > a.next")) > 0:
                    page += 1
                    driver.get(
                        "https://s.weibo.com/weibo?q=%E7%96%AB%E6%83%85&xsort=hot&suball=1&timescope=custom%3A{}%3A{}&Refer=g&page={}".format(
                            start_time, end_time, page))
                    time.sleep(2)
                else:
                    break
                    # time.sleep(10)
                    # get_img()
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
