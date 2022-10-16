import os
import AOIGetter as aoiWe

udir = r"D:\POI\分配\王申宇\湛江市"  # 存储poi信息的文件夹


def getFiles(path):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        s.append(path + '\\' + file)
    return s


Files = getFiles(udir)
print(Files)
for f in Files:
    try:
        aoiWe.addAoi(f)
    except aoiWe.pd.errors.EmptyDataError:
        print(f, '空文件跳过')
