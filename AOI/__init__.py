import os
import AOIGetter as aoiWe

udir = r"D:\Project\amapCrawler\AOI\data_class"  # 存储poi信息的文件夹


def getFiles(path):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        s.append(path + '\\' + file)
    return s


s = getFiles(udir)
Files = []
for i in s:
    Files += getFiles(i)
print(Files)
for f in Files:
    aoiWe.addAoi(f)
