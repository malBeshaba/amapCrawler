import osgeo.osr as osr
import shapefile  # 使用pyshp
import pandas as pd
import coor_trans as cToT
from tqdm import tqdm


def initShp(url):
    data_address = url  # 新建数据存放位置
    file = shapefile.Writer(data_address)
    file.field('ID')
    file.field('NAME', 'C', '40')  # 'SECOND_FLD'为字段名称，C代表数据类型为字符串，长度为 40
    # file.field('THIRD_FLD', 'C', '40')
    return file


# # 创建两个字段
# csvF = open('小学.csv', encoding='utf-8')  # 读取对应的csv文件
# df = pd.read_csv(csvF, engine='python')


def setShp(file, S, poi, name):
    file.poly([S])  # 输入id信息
    file.record(poi, name)


def getShape(file, url):
    # 创建两个字段
    csvF = open(url, encoding='utf-8')  # 读取对应的csv文件
    df = pd.read_csv(csvF, engine='python')
    for i in range(len(df)):
        # 逐行读取
        L = df['shape'][i]
        pid = df['id'][i]
        name = df['name'][i]
        if isinstance(L, str):
            # 非字符串为空值（非独立用地）
            shapeL = [cToT.gcj02_to_wgs84(list(map(float, e))[0], list(map(float, e))[1])
                      for e in [s.split('-') for s in L.split('|')]]
            setShp(file, shapeL, pid, name)


# 关闭文件操作流
def over(file, url):
    file.close()
    # 定义投影
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(4326)  # 4326-GCS_WGS_1984; 4490- GCS_China_Geodetic_Coordinate_System_2000
    wkt = proj.ExportToWkt()
    # 写入投影
    f = open(url.replace(".shp", ".prj"), 'w')
    f.write(wkt)
    f.close()
    print(url, 'over')
    

def transfer(ipL, op):
    f = initShp(op)
    with tqdm(total=len(ipL), desc='shapeTrans', leave=True, ncols=100, unit_scale=True) as pbar:
        for i in ipL:
            getShape(f, i)
            pbar.update(1)
    over(f, op)


def transferFile(ip, op):
    f = initShp(op)
    getShape(f, ip)
    over(f, op)


def transferFiles(ipL, opL):
    for ip in ipL:
        op = opL + '\\' + ip.split('\\')[-1].split('.')[0] + '.shp'
        transferFile(ip, op)
