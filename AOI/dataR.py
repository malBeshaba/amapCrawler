import os
import pandas as pd

furl = 'E:\\华南\\国土测绘院功能区项目\\宝安高德'
ref = 'amap_poicode.xlsx'


def getFiles(path):
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    fileNames = [file.split('.')[0] for file in files]
    files = [path + '\\' + file for file in files]
    return fileNames, files


fn, files = getFiles(furl)
refDf = pd.read_excel(ref)
dic = {}
codeType = {}
for index, row in refDf.iterrows():
    dic[row['小类']] = row['NEW_TYPE']
    codeType[row['NEW_TYPE']] = row['大类'] + ';' + row['中类'] + ';' + row['小类']

codeDic = {}
idL = []
for file in files:
    csvF = open(file, encoding='utf-8')
    df = pd.read_csv(csvF)
    # print('reading ', file)
    for index, row in df.iterrows():
        if row['id'] in idL:
            continue
        else:
            if type(row['type']) == type('a'):
                idL.append(row['id'])
                c = row['type'].split(';')[-1]
                if dic[c] in codeDic:
                    codeDic[dic[c]] += 1
                else:
                    codeDic[dic[c]] = 1

# print(list(codeDic.keys()))
codes = list(codeDic.keys())
nums = [codeDic[code] for code in codes]
types = [codeType[code] for code in codes]
outdf = pd.DataFrame({'code': codes, 'num': nums, 'type': types})
print(outdf)
outdf.to_csv('code.csv', index=False)