import amapApi as am
import pandas as pd
from getRectangle import getShape
import os

saveDir = 'D:\\data'  # 保存地址

D = {'公园广场': '110100', '公园': '110101', '动物园': '110102', '植物园': '110103', '博物馆': '140100',
     '展览馆': '140200', '美术馆': '140400', '图书馆': '140500', '科技馆': '140600', '档案馆': '140900',
     '纪念馆': '110204', '消防机关': '130504', '城市广场': '110105', '丧葬设施': '071900', '陵园': '071901',
     '公墓': '071902'}  # 更改所需爬取的类别，这里是部分，可能需要添加或删除


for i in range(0, 11):  # 分了100份，0-99，大家自己填自己的范围（开始，结束+1）
     shape = getShape(i)
     if not os.path.exists(saveDir + str(i)):
          os.mkdir(saveDir + str(i))
     for key in D.keys():
          df = pd.DataFrame(am.getByShapes(shape, D[key]),
                            columns=['id', 'parent', 'name', 'type', 'address', 'location'])
          df.to_csv(saveDir + str(i) + '\\' + key + '.csv', index=False)

