from webVisiter import webVisiter
from pypinyin import pinyin, NORMAL

url = 'https://www.douban.com/location/'
local = pinyin('佛山', style=NORMAL)[0][0] + pinyin('佛山', style=NORMAL)[1][0]
# print(type(local))
wv = webVisiter(True)
wv.load(url + local)