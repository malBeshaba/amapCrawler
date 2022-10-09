import pandas as pd
import os
import amapApi as am
import requests
import json
from tqdm import tqdm

saveDir = 'D:\\Project\\amapCrawler\\AOI\\image\\'  # 图片存储路径
udir = r'D:\Project\amapCrawler\AOI\data_class'  # poi信息存储路径


def getFiles(path):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        s.append(path + '\\' + file)
    return s


def createDir(path, saveDir):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    D = {}
    for file in files:  # 遍历文件夹
        # s.append(path + '\\' + file)
        # o.append(saveDir+ file.split('.')[0] + '\\')
        D[path + '\\' + file] = saveDir + file.split('.')[0] + '\\'
        if not os.path.exists(saveDir + file.split('.')[0]):
            os.mkdir(saveDir + file.split('.')[0])
    return D


s = getFiles(udir)
Files = []
for i in s:
    Files += getFiles(i)
D = createDir(Files, saveDir)


def downloadImage(sDir, image_name, IMAGE_URL):
    r = requests.get(IMAGE_URL)
    with open(sDir + image_name, 'wb') as f:
        f.write(r.content)


for file in D.keys():
    df = pd.read_csv(file)
    for item in tqdm(df['id']):
        id_url = 'https://restapi.amap.com/v3/place/detail'
        params = {'key': am.key, 'id': item}
        ret = requests.get(id_url, params=params)
        try:
            idOj = json.loads(ret.text)['pois'][0]  # id对应的poi信息json对象
            photos = idOj['photos']
            if len(photos) > 0:
                for i in range(len(photos)):
                    downloadImage(D[file], item + '-' + str(i) + '.png', photos[i]['url'])
        except:
            print(ret.text)
