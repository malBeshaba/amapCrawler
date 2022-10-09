import pandas as pd
import os
import amapApi as am
import requests
import json
from tqdm import tqdm


key1 = '686615d2c52666778a6d38b59eaea79e'
key = '73498752e6144a6dffda623f15610e2a'

import fox as aoiWeb

aoiWeb.addAoi(r'D:\Project\python\amapCrawler\AOI\data_out\park.xls')
# df = pd.read_excel(r'D:\Project\python\amapCrawler\AOI\data_out\park.xls')
#
#
# def downloadImage(image_name, IMAGE_URL):
#     r = requests.get(IMAGE_URL)
#     with open('D:\\Project\\python\\amapCrawler\\AOI\\image\\' + image_name, 'wb') as f:
#         f.write(r.content)
#
#
# for item in tqdm(df['id']):
#     id_url = 'https://restapi.amap.com/v3/place/detail'
#     params = {'key': key, 'id': item}
#     ret = requests.get(id_url, params=params)
#     try:
#         idOj = json.loads(ret.text)['pois'][0]  # id对应的poi信息json对象
#         photos = idOj['photos']
#         if len(photos) > 0:
#             for i in range(len(photos)):
#                 downloadImage(item+'-'+str(i)+'.png', photos[i]['url'])
#     except:
#         print(ret.text)
