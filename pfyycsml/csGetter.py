from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
import time
import random
import json
import pandas as pd
from tqdm import tqdm

option = Options()
option.add_argument('disable-blink-features=AutomationControlled')
option.add_argument('headless')
base_url = "https://zwfw.spb.gov.cn"
s_url = '/sj/440000/pfyycsml?currentPage='
odf = pd.DataFrame(columns=('所属省', '所属市', '所属区(县)', '营业场所', '地址',
                            '开办业务', '邮政编码'))
url_L = []


def initWeb(opt):
    """
    初始化并打开Chrome
    :param opt: option参数
    :return: Chrome对象
    """
    return Chrome(options=opt)


web = initWeb(option)


def isElementFromTag(browser, tag):
    try:
        browser.find_elements_by_tag_name(tag)
        return True
    except exceptions.NoSuchElementException:
        return False


def isElementFromID(browser, id):
    try:
        browser.find_element_by_id(id)
        return True
    except exceptions.NoSuchElementException:
        return False


def weberror(turl):
    print('wait 2 minutes')
    time.sleep(120)  # 如果网络异常则2分钟后再次进行
    print('reloading···')
    webVisiter()


def webLoad(url):
    try:
        web.get(url)
    except:
        webLoad(url)


def detailsUrl(page_num):
    url = base_url + s_url + str(page_num)
    global web, url_L
    try:
        web.get(url)
    except:
        weberror(url)
    if isElementFromID(web, 'no'):
        return
    if isElementFromTag(web, 'tbody'):
        tr_list = web.find_elements_by_tag_name('tr')
        for i in range(1, 21):
            try:
                a = tr_list[i].find_elements_by_tag_name('a')[0]
            except:
                return
            child_url = a.get_attribute('href')
            url_L.append(child_url)


def getDetails(url):
    global web, odf
    try:
        web.get(url)
    except:
        weberror(url)
    if isElementFromTag(web, 'tbody'):
        tr_list = web.find_elements_by_tag_name('tr')
        texts = []
        for i in tr_list:
            texts.append(i.find_elements_by_tag_name('td')[1].text)
        odf = odf.append(pd.DataFrame(
            {'所属省': [texts[0]], '所属市': [texts[1]], '所属区(县)': [texts[2]], '营业场所': [texts[3]], '地址': [texts[4]],
             '开办业务': [texts[5]], '邮政编码': [texts[6]]}), ignore_index=True)


def webVisiter():
    for i in tqdm(range(1, 151)):
        detailsUrl(i)
    print(len(url_L))
    for url in tqdm(url_L):
        getDetails(url)
    odf.to_csv('pfyycsml.csv', index=False)


webVisiter()
web.quit()
# detailsUrl(82)