#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/25
"""

from queue import Queue
import re
import urllib
import time
from bs4 import BeautifulSoup
import socket
import sys
import math
import json
import gzip
import codecs
from io import BytesIO

timeout = 15
socket.setdefaulttimeout(timeout)
inputq = Queue(maxsize=0)
outputq = Queue(maxsize=0)

regexp = r"ubp = ({.*?})"
regexp1 = r'px:"(.*?)"'
regexp2 = r'py:"(.*?)"'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}


def downloadhtml(url, headers, RepeatCount=5):
    try:
        time.sleep(5)
        req = urllib.request.Request(url, headers)
        response = urllib.request.urlopen(req)
        if response.info().get('Content-Type') == 'gzip':
            buf = BytesIO(response.read())
            content = gzip.GzipFile(fileobj=buf).read()
        else:
            content = response.read()
    except urllib.error.HTTPError as e:
        content = None
        if RepeatCount > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:  # 服务器错误
                return downloadhtml(url, headers, RepeatCount - 1)
    except socket.error:
        content = None
        errno, errstr = sys.exc_info()[:2]
        if errno == socket.timeout:
            print("error:Timeout")
        else:
            print("other error")
        time.sleep(2)
        if RepeatCount > 0:
            return downloadhtml(url, headers, RepeatCount - 1)
    except:
        content = None
        if RepeatCount > 0:
            return downloadhtml(url, headers, RepeatCount - 1)
    try:
        content = content.decode("GBK")
    except:
        pass
    return content


def get_pages(url, ReC=2):
    content = downloadhtml(url, headers)
    if content is not None:
        soup = BeautifulSoup(content, "html.parser")
        Num = soup.findAll("b", {"class": "findplotNum"})
        xiaoqu_count = Num[0].get_text()
        if xiaoqu_count == str(0) and ReC > 0:
            return get_pages(url, ReC - 1)
        print("70:" + xiaoqu_count)
        return int(math.ceil(int(xiaoqu_count) / 20.0))
    return 0


def WriteToFile(xiaoqu_info_list):
    print("start:write")
    f1 = codecs.open(filename, 'w', 'utf8')
    for xiaoqu_info in xiaoqu_info_list:
        f1.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n"
                 % (xiaoqu_info[0], xiaoqu_info[1], xiaoqu_info[2], xiaoqu_info[3], xiaoqu_info[4],
                    xiaoqu_info[5], xiaoqu_info[6], xiaoqu_info[7], xiaoqu_info[8]))
        f1.close()


#线程执行的任务
def task():
    while not inputq.empty():
        xiaoqu_info = inputq.get()
        id = xiaoqu_info[0]
        url = qianzhui_url + "/newsecond/map/newhouse/ShequMap.aspx?newcode={}".format(id)
        content = downloadhtml(url,headers)
        if content is None:
            print("93:"+url)
            inputq.put(xiaoqu_info)
            continue

        try:
            latitude = re.findall(regexp2,content)[0]
            longtitude = re.findall(regexp1,content)[0]
        except Exception as e:
            inputq.put(xiaoqu_info)
            print("102:"+url)
            continue
        xiaoqu_info.append("")
        xiaoqu_info.append("")
        xiaoqu_info.append("")

        if xiaoqu_info[2] == "":
            xiaoqu_info[2] = u"未知"
        xiaoqu_info[0], xiaoqu_info[1], xiaoqu_info[2], xiaoqu_info[3], xiaoqu_info[4],
        xiaoqu_info[5], xiaoqu_info[6], xiaoqu_info[7], xiaoqu_info[8] = \
            xiaoqu_info[1],xiaoqu_info[3],xiaoqu_info[6], xiaoqu_info[7], xiaoqu_info[4],latitude,
        longtitude, xiaoqu_info[2],  xiaoqu_info[5]
        outputq.put(xiaoqu_info)




all_url_list = []
temp_infp = []
f = codecs.open("city.dat", 'r', 'utf8')
for each0 in f:
    list_temp = each0.strip().split("\t")
    qianzhui_url = list_temp[0]
    cityname = list_temp[0].split(".")[1]
    filename = "./temp/{}_xioaqu.dat".format(cityname)
    province = list_temp[1]
    print("124:"+province)
    city = list_temp[2]
    print("126:"+city)
    url = qianzhui_url + "/housing/__0_0_1_0_1_0_0_0/"
    pg = get_pages(url)
    if pg == 0:
        continue
    elif pg > 100:
        content = downloadhtml(url, headers)
        soup = BeautifulSoup(content, 'html.parser')
        list_div = soup.find_all("div", class_="sq-info mt10")
        list1 = []
        for eachx in list_div:
            list1 += eachx.find_all("a")
        print(list1)

        all_url_list = []
        temp_infp = []
        for each in list1:  # 每个小地区
            url = qianzhui_url + each['href']
            pages = get_pages(url)
            if pages == 0:
                continue
            url_list = [url[:-14] + "0_1_0" + "{}_0_0_0/".format(str(i)) for i in range(1, pages + 1)]
            for ul in url_list:
                inputq.put(ul)
            while not inputq.empty():
                name_list = []
                xiaoqu_url_list = []
                addr_list = []
                avg_list = []
                useway_list = []
                each1 = inputq.get()
                content = downloadhtml(each1, headers)
                if content is None:
                    inputq.put(each1)
                    continue
                content1 = content
                find = re.findall(regexp, content)[0]
                find = json.load(find)
                try:
                    find = find['vwx.showhouseid'].split['.']
                except:
                    inputq.put(each1)
                    continue
                soup = BeautifulSoup(content1, 'html.parser', from_encoding='gb18030')
                temp_xiaoqu_info = soup.select(".plotListwrap")
                avg_list_info = soup.select(".priceAverage")
                for k in temp_xiaoqu_info:
                    xiaoqu_info = k.dd.find_add("p")
                    name_list.append(xiaoqu_info[0].a.get_text().strip())
                    useway_list.append(xiaoqu_info[0].span.get_text().strip())
                    xiaoqu_url_list.append(xiaoqu_info[0].a['href'])
                    addr_list.append(xiaoqu_info[1].get_text().strip())

                for ap in avg_list_info:
                    avg_list.append(ap.get_text().strip())

                for each2,name,addr,url,avg,useway in zip(find,name_list,addr_list,xiaoqu_url_list,avg_list,
                                                          useway_list):
                    if each2 not in all_url_list:
                        all_url_list.append(each2)
                        temp_infp.append([each2,name,addr,url,avg,useway,province,city])
                for xiaoqu_info in temp_infp:
                    inputq.put(xiaoqu_info)




    else:
        pass
