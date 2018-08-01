#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/23
"""

import csv
import requests
import numpy as np
import threading
import save2File

#BASE_URL = "http://api.map.baidu.com/geocoder/v2/?address={address}&output=json&ak=gQsCAgCrWsuN99ggSIjGn5nO&callback=showLocation0"
BASE_URL = "http://api.map.baidu.com/geocoder/v2/?address={address}&output=json&ak=5ErzLvtGmrkyHVY5HnG9GeMqvgpApGkt&city=上海市"
DISTANTCE = 0.1

class UrlThread(threading.Thread):
    def __init__(self, name, address, row):
        threading.Thread.__init__(self)
        self.name = name
        self.address = address
        self.row = row

    def run(self):
        with thread_max_num:
            try:
                concreteGetData(self.name, self.address, self.row)
            except:
                print("error")


def concreteGetData(name, address, row):
    dist = 1000
    try:
        res = requests.get(assembleURL(name))
        resJson = res.json()
        print(resJson)
        location = resJson['result']['location']
        lng = location['lng']
        lat = location['lat']
        longtitude = row[9]
        latitude = row[10]
        dist = distance(float(lng), float(lat), float(longtitude), float(latitude))
    except:
        print('name - error')
    else:
        if dist <= DISTANTCE:
            save2File.saveFinalPoi(row)
        else:
            res = requests.get(assembleURL(address))
            resJson = res.json()
            # print(resJson)
            location = resJson['result']['location']
            lng = location['lng']
            lat = location['lat']
            longtitude = row[9]
            latitude = row[10]
            dist = distance(float(lng), float(lat), float(longtitude), float(latitude))
            if dist <= DISTANTCE:
                save2File.saveFinalPoi(row)


thread_max_num = threading.Semaphore(10)


def assembleURL(address):
    return BASE_URL.format(address=address)


def distance(longtitude1, latitude1, longtitude2, latitude2):
    # 计算距离
    a = (latitude1 - latitude2) * np.pi / 180.0
    b = (longtitude1 - longtitude2) * np.pi / 180.0
    sin_square_half_a = (np.sin(a / 2)) ** 2
    sin_square_half_b = (np.sin(b / 2)) ** 2
    extract = (sin_square_half_a + np.cos(latitude1 * np.pi / 180.0) * np.cos(
        latitude2 * np.pi / 180.0) * sin_square_half_b)
    extract = np.sqrt(extract)
    r = 6378.137
    s = 2 * np.arcsin(extract) * r
    return s


def openFile(filepath='data\shanghai_whole_MulThread_723_with_geoobj_original.txt'):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='t')
        for row in reader:
            item = row[0].replace('\t', ',').split(',')
            name = item[1]
            if len(item) < 8:
                continue
            address = item[8]
            th = UrlThread(name, address, item)
            th.start()


openFile()
