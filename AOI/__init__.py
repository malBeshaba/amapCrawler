import os
import AOIGetter as aoiWe

udir = "D:\\Project\\amapCrawler\\AOI\\data_class"  # 存储poi信息的文件夹


def getFiles(path, topath):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    # o = []
    for file in files:  # 遍历文件夹
        s.append(path + '\\' + file)
    return s


s = getFiles(udir)


for i in s:
    aoiWe.addAoi(i)
