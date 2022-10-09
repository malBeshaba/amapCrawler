import amapApi as am
import pandas as pd
from getRectangle import getShape
from tqdm import tqdm
import os

saveDir = 'D:\\data\\'  # 保存地址

D = {'公园广场': '110100', '公园': '110101', '动物园': '110102', '植物园': '110103', '博物馆': '140100',
     '展览馆': '140200', '美术馆': '140400', '图书馆': '140500', '科技馆': '140600', '档案馆': '140900',
     '纪念馆': '110204', '消防机关': '130504', '城市广场': '110105', '丧葬设施': '071900', '陵园': '071901',
     '公墓': '071902', '高等院校': '141201', '职业技术学校': '141206', '小学': '141203', '中学': '141202',
     '幼儿园': '141204', '综合医院': '090100', '专科医院': '090200', '诊所': '090300', '医疗保健服务场所': '090000',
     '卫生院': '090102', '疗养院': '080402', '邮局': '070400', '停车场相关': '150900', '公共停车场': '150904',
     '路边停车场': '150906', '紧急避难场所': '200400'}  # 更改所需爬取的类别，这里是部分，可能需要添加或删除


for i in range(0, 11):  # 分了100份，0-99，大家自己填自己的范围（开始，结束+1）
     shape = getShape(i)
     if not os.path.exists(saveDir + str(i)):
          os.mkdir(saveDir + str(i))
     for key in tqdm(D.keys()):
          df = pd.DataFrame(am.getByShapes(shape, D[key]),
                            columns=['id', 'parent', 'name', 'type', 'address', 'location'])
          df.to_csv(saveDir + str(i) + '\\' + key + '.csv', index=False)
     df = pd.DataFrame(am.error)
     df.to_csv(saveDir + str(i) + '\\error.csv', index=False)

