from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
import time
import random
import json
import pandas as pd
from tqdm import tqdm  # 进度条

options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
options.add_argument('disable-blink-features=AutomationControlled')

base_url = "https://ditu.amap.com/detail/get/detail?id="
shapeStr = ''


def initWeb(opt):
    """
    初始化并打开Chrome
    :param opt: option参数
    :return: Chrome对象
    """
    return webdriver.Firefox(
        executable_path="C:\\Program Files\\Mozilla Firefox\\geckodriver.exe",  # 这里必须要是绝对路径
        # windows是.exe文件 xxx/xxx/geckodriver.exe, xxx/xxx/firefox.exe
        # linux直接是xxx/xxx/geckodriver, xxx/xxx/firefox
        firefox_binary="C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        options=opt)



web = initWeb(options)


def isElementFromID(browser, poi):
    """
    基于find方法在查找失败时会返回异常的原理，通过id判断师范存在某个标签对象
    :param browser: 浏览器
    :param poi: id
    :return: 是否存在
    """
    try:
        browser.find_element_by_id(poi)
        return True
    except exceptions.NoSuchElementException:
        return False


def verify_page(browser, poi):
    """
    滑块自动验证方法
    :param browser: 浏览器
    :param poi: id
    """
    while not isElementFromID(browser, 'nc_1_n1z'):  # 由于弱网环境可能出现滑块控件加载不出来的情况，进行几次重新请求直达滑块出现
        url = base_url + poi
        browser.get(url)
        time.sleep(random.random() * 5 + 3)
    try:
        btn = browser.find_element_by_id('nc_1_n1z')  # 根据id定位滑块控件
        action = ActionChains(browser)
        action.click_and_hold(btn).perform()  # 点击并按住滑块
        time.sleep(random.random() * 5)  # 等待随机时间
        for i in range(40):
            action.move_by_offset(10, 0).perform()  # 滑动滑块
            time.sleep(random.random() * 0.01)
    except:
        webVisiter(poi)  # 如果出现异常则重新请求


def get_shape(browser):
    """
    获取shape信息
    :param browser: 浏览器
    :return: shape数据——字符串格式，经纬度以','分割，点与点以';'分割
    """
    try:
        JSON = browser.find_elements_by_tag_name('pre')[0].text
        obj = json.loads(JSON)
        shape = obj['data']['spec']['mining_shape']['shape']
        global shapeStr  # 通过全局变量来读取shape
        shapeStr = shape
        return shape
    except:
        return ''


def webVisiter(poi):
    """
    web服务主程序，使用时仅需调用此函数
    :param poi: id
    """
    url = base_url + poi
    global web
    try:
        web.get(url)
    except:
        print('wait 2 minutes')
        time.sleep(120)  # 如果网络异常则2分钟后再次进行
        print('reloading···')
        webVisiter(poi)
    time.sleep(random.random() * 5 + 2)  # 进入页面后等待随机时间
    if isElementFromID(web, 'tb-beacon-aplus'):  # 进入自动滑块验证环节
        # print('进入自动验证:', poi)
        verify_page(web, poi)
        webVisiter(poi)
    elif isElementFromID(web, 'beacon-aplus'):  # 出现账号密码验证环节通过重新初始化浏览器解决
        # print('出现密码验证')
        web.quit()
        web = initWeb(options)
    else:
        get_shape(web)  # 不存在验证时读取shape


def addAoi(path):
    if path.split('.')[1] == 'csv':
        csvF = open(path, encoding='utf-8')  # 读取对应的csv文件
        df = pd.read_csv(csvF, engine='python')
    else:
        df = pd.read_excel(path)
    if 'shape' in df.columns:
        print(path, 'AOI补充完成')
        return
    L = []
    with tqdm(total=len(df), desc=path.split('\\')[-1].split('.')[0], leave=True, ncols=100, unit_scale=True) as pbar:
        for i in range(len(df)):
            # 逐行读取
            pid = df['id'][i]
            webVisiter(pid)
            L.append(shapeStr.replace(',', '-').replace(';', '|'))  # 为方便在csv中读取转换分割方式
            pbar.update(1)
    df.insert(loc=len(df.columns), column='shape', value=L)  # 输入一列
    df.to_csv(path, index=None)
    print(path, 'AOI补充完成')
