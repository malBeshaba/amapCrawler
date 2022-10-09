import os
import amapApi as am
# import pandas as pd

udir = "D:\\Project\\amapCrawler\\AOI\\data_class"
odir = "E:\\BaiduNetdiskDownload\\try"
shp = "D:\\\Project\\python\\amapCrawler\\AOI\\classOut"


def getFiles(path, topath):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    o = []
    for file in files:  # 遍历文件夹
        s.append(path + '\\' + file)
        o.append(topath + '\\' + file)
    return s, o


s, o = getFiles(udir, odir)
print(s)

import AOIGetter as aoiWe
for i in s:
    aoiWe.addAoi(i)