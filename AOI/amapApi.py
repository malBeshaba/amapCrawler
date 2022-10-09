import pandas as pd
import requests
import json

key = '73498752e6144a6dffda623f15610e2a'


def getByShapes(shape, types):
    shape_url = 'https://restapi.amap.com/v3/place/polygon'
    L = []

    def getNext(page=1):
        # api中包含count参数，此参数不能作为具体数量标准但翻页过程中如果count变为0则全部获取完成，通过改变page进行翻页，默认一页20项
        # 一般不会超过20项
        params = {'key': key, 'polygon': shape, 'types': types, 'offset': 25,
                  'page': page}
        ret = requests.get(shape_url, params=params)
        arOj = json.loads(ret.text)
        # print(arOj)
        pois = arOj['pois']
        for num in range(len(pois)):
            data = pois[num]
            L.append([data['id'], data['parent'] if len(data['parent']) > 0 else '',
                      data['name'], data['type'], data['address'], data['location']])
        if int(arOj['count']) > 0:
            # count != 0 时代表还未获取完全，递归继续读取
            # print(arOj['count'], page)
            getNext(page + 1)
    getNext()
    return L


def getLocationFromID(poi):
    """
    通过高德POI的id搜索api，获取对应的poi信息
    :param poi:
    :return:
    """
    id_url = 'https://restapi.amap.com/v3/place/detail'
    params = {'key': key, 'id': poi}
    ret = requests.get(id_url, params=params)
    idOj = json.loads(ret.text)['pois'][0]  # id对应的poi信息json对象
    parent = idOj['parent']
    location = idOj['location']
    address = idOj['address']
    return parent, location


def getkeyword(k):
    around_url = 'https://restapi.amap.com/v3/place/text'
    L = []

    def getNext(k, page=1):
        # api中包含count参数，此参数不能作为具体数量标准但翻页过程中如果count变为0则全部获取完成，通过改变page进行翻页，默认一页20项
        # 一般不会超过20项
        params = {'key': key, 'keywords': k, 'city': '440303',
                  'offset': 20, 'page': page, 'children': 0, 'extensions': 'all'}
        ret = requests.get(around_url, params=params)
        arOj = json.loads(ret.text)
        # print(arOj)
        pois = arOj['pois']
        for num in range(len(pois)):
            if pois[num]['adname'] != '罗湖区':
                continue
            data = pois[num]
            L.append(data['name'])
        if int(arOj['count']) > 0:
            # count != 0 时代表还未获取完全，递归继续读取
            getNext(k, page + 1)

    getNext(k)
    return L


def getNearList(local):
    """
    通过 高德搜索周边api 获取周边poi信息
    :param local: 经纬度，string，用','分割
    :return: 方圆100米内的poi信息，参数包含id，parent，name，type，address，location
    """
    around_url = 'https://restapi.amap.com/v3/place/around'
    L = []

    def getNear(location, page=1):
        # api中包含count参数，此参数不能作为具体数量标准但翻页过程中如果count变为0则全部获取完成，通过改变page进行翻页，默认一页20项
        # 一般不会超过20项
        params = {'key': key, 'location': location, 'radius': 100,
                  'offset': 20, 'page': page, 'extensions': 'base'}
        ret = requests.get(around_url, params=params)
        arOj = json.loads(ret.text)
        pois = arOj['pois']
        for num in range(len(pois)):
            data = pois[num]
            L.append([data['id'], data['parent'] if len(data['parent']) > 0 else '',
                      data['name'], data['type'], data['address'], data['location']])
        if int(arOj['count']) > 0:
            # count != 0 时代表还未获取完全，递归继续读取
            getNear(location, page + 1)

    getNear(local)
    return L


def isIndependent(poi):
    parent, location = getLocationFromID(poi)
    if len(parent) > 0:
        return False
    return True


def outFromID(poi):
    id_url = 'https://restapi.amap.com/v3/place/detail'
    params = {'key': key, 'id': poi}
    ret = requests.get(id_url, params=params)
    try:
        idOj = json.loads(ret.text)['pois'][0]  # id对应的poi信息json对象
        name = idOj['name']
        parent = idOj['parent'] if len(idOj['parent']) > 0 else ''
        location = idOj['location']
        ptype = idOj['type']
        address = idOj['address']
        return {'id': [poi], 'name': [name], 'location': [location], 'parent': [parent], 'type': [ptype],
                'address': [address]}
    except:
        print(ret.text)
        return {'id': [poi], 'name': [''], 'location': [''], 'parent': [''], 'type': [''],
                'address': ['']}


def txtToCsv(path, toPath):
    print('read:', path)
    csvF = open(path, encoding='utf-8')  # 读取对应的csv文件
    df = pd.read_csv(csvF, engine='python')
    odf = pd.DataFrame(columns=('id', 'name', 'location', 'parent', 'type', 'address'))
    for i in range(len(df)):
        # 逐行读取
        pid = df['Field1'][i]
        odf = odf.append(pd.DataFrame(outFromID(pid)), ignore_index=True)
        # print(pid, '完成')
    odf.to_csv(toPath, index=False)
    print('out:', toPath)


def xlsxToCsv(path, toPath):
    print('read:', path)
    # xlsx = open(path, encoding='utf-8')  # 读取对应的csv文件
    df = pd.read_excel(path, sheet_name=0)
    odf = pd.DataFrame(columns=('id', 'name', 'location', 'parent', 'type', 'address'))
    for i in range(len(df)):
        # 逐行读取
        pid = df['ID'][i]
        if pid == 'wu':
            continue
        else:
            odf = odf.append(pd.DataFrame(outFromID(pid.replace('\'', '').replace('b', ''))), ignore_index=True)
        print(pid, '完成')
    odf.to_csv(toPath, index=False)
    print('out:', toPath)
