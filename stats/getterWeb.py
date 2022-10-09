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
base_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/44"
shapeStr = ''


def initWeb(opt):
    """
    初始化并打开Chrome
    :param opt: option参数
    :return: Chrome对象
    """
    return Chrome(options=opt)


web = initWeb(option)
web.set_page_load_timeout(3)


def isElementFromClass(browser, poi):
    """
    基于find方法在查找失败时会返回异常的原理，通过id判断师范存在某个标签对象
    :param browser: 浏览器
    :param poi: id
    :return: 是否存在
    """
    try:
        browser.find_element_by_class_name(poi)
        return True
    except exceptions.NoSuchElementException:
        return False


L = []
L1 = []
L2 = []
odf = pd.DataFrame(columns=('citycode', 'city', 'countrycode', 'country', 'towncode',
                            'town', 'villagecode', 'villagetypecode', 'PAC', 'village'))


def weberror(turl):
    print('wait 2 minutes')
    time.sleep(120)  # 如果网络异常则2分钟后再次进行
    print('reloading···')
    webVisiter(turl)


def webLoad(url):
    try:
        web.get(url)
    except:
        webLoad(url)


def webVisiter(turl):
    """
    web服务主程序，使用时仅需调用此函数
    :param poi: id
    """
    url = turl + '.html'
    global web, odf
    try:
        web.get(url)
    except:
        weberror(turl)
    time.sleep(random.random() * 5)  # 进入页面后等待随机时间
    if isElementFromClass(web, 'citytr'):
        firstL = [i.text for i in web.find_elements_by_class_name('citytr')]
        for i in firstL:
            city = i.split(' ')
            webLoad(base_url + '/' + city[0][0:4] + '.html')
            secondL = [i.text for i in web.find_elements_by_class_name('countytr')]
            if len(secondL) == 0:
                thridL = [i.text for i in web.find_elements_by_class_name('towntr')]
                # time.sleep(random.random())
                for l in thridL:
                    town = l.split(' ')
                    try:
                        webLoad(base_url + '/' + city[0][2:4] + '/' + town[0][0:9] + '.html')
                    except:
                        # time.sleep(2000)
                        webLoad(base_url + '/' + city[0][2:4] + '/' + town[0][0:9] + '.html')
                    # time.sleep(random.random())
                    forthL = [i.text for i in web.find_elements_by_class_name('villagetr')]
                    for k in forthL:
                        village = k.split(' ')
                        odf = odf.append(
                            pd.DataFrame({'citycode': [city[0]], 'city': [city[1]], 'countrycode': [''],
                                          'country': [''], 'towncode': [town[0]], 'town': [town[1]],
                                          'villagecode': [village[0]], 'villagetypecode': [village[1]],
                                          'PAC': [village[0] + village[1]], 'village': [village[2]]}),
                            ignore_index=True)
            else:
                secondL.pop(0)
                time.sleep(random.random())
                for j in secondL:
                    country = j.split(' ')
                    webLoad(base_url + '/' + city[0][2:4] + '/' + country[0][0:6] + '.html')
                    thridL = [i.text for i in web.find_elements_by_class_name('towntr')]
                    # time.sleep(random.random())
                    for l in thridL:
                        town = l.split(' ')
                        try:
                            webLoad(
                                base_url + '/' + city[0][2:4] + '/' + country[0][4:6] + '/' + town[0][0:9] + '.html')
                        except:
                            # time.sleep(2000)
                            webLoad(
                                base_url + '/' + city[0][2:4] + '/' + country[0][4:6] + '/' + town[0][0:9] + '.html')
                        # time.sleep(random.random())
                        forthL = [i.text for i in web.find_elements_by_class_name('villagetr')]
                        for k in forthL:
                            village = k.split(' ')
                            odf = odf.append(
                                pd.DataFrame({'citycode': [city[0]], 'city': [city[1]], 'countrycode': [country[0]],
                                              'country': [country[1]], 'towncode': [town[0]], 'town': [town[1]],
                                              'villagecode': [village[0]], 'villagetypecode': [village[1]],
                                              'PAC': [village[0] + village[1]], 'village': [village[2]]}),
                                ignore_index=True)


webVisiter(base_url)
odf.to_csv('stats.csv', index=False)
web.quit()
