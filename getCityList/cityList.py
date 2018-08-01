#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/27
"""

import urllib
from bs4 import BeautifulSoup
from io import BytesIO
import gzip
import socket
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', }


def downloadhtml(url, headers, RepeatCount=5):
    print(url)
    try:
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req)
        # print(response)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(response.read())
            content = gzip.GzipFile(fileobj=buf).read()
        else:
            content = response.read()
    except urllib.error.HTTPError as e:
        content = None
        if (RepeatCount > 0):
            if hasattr(e, 'code') and 500 <= e.code < 600:  # 服务器错误
                return downloadhtml(url, headers, RepeatCount - 1)
    except socket.error:
        content = None
        errno, errstr = sys.exc_info()[:2]
        if errno == socket.timeout:
            print("error:Timeout")
        else:
            print("other error")
        if (RepeatCount > 0):
            return downloadhtml(url, headers, RepeatCount - 1)
    except:
        content = None
        if (RepeatCount > 0):
            return downloadhtml(url, headers, RepeatCount - 1)
    try:
        content = content.decode("GBK")
    except:
        pass
    return content


def save2file(link, province, city):
    with open('../data/city.txt', 'a+', encoding='utf-8') as f:
        f.write(link+"\t"+province+"\t"+city+"\n")
        f.close()


url = "http://esf.sh.fang.com/newsecond/esfcities.aspx"

str = ""
with open("city_source.html") as f:
    s = f.readlines()
    for s1 in s:
        str = str+"\t"+s1


#content = downloadhtml(url, headers)
# soup = BeautifulSoup(str, "html.parser", from_encoding='gb2312')
soup = BeautifulSoup(str)
divList = soup.select(".outCont")
liList = divList[0].find_all('li')
for li in liList:
    provice = li.strong.get_text()
    aList = li.find_all('a')
    print(len(aList))
    for a in aList:
        link = a['href']
        city = a.get_text()
        print(link)
        save2file(link, provice, city)
