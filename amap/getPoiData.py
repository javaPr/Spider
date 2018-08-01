#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/17
"""

import threading
import time

import requests
from utils import save2File

import readData

shanghai_adcode = ['310000', '310100', '310101', '310104', '310105', '310106', '310107',
                   '310109', '310110', '310112', '310113', '310114',
                   '310115', '310116', '310117', '310118', '310120', '310151']
motorcycle_key_words = ['摩托车服务相关', '摩托车销售', '宝马摩托车销售', '摩托车维修', '宝马摩托车维修']
hotel_key_words = ['住宿服务相关', '宾馆酒店', '奢华酒店', '五星级宾馆', '四星级宾馆',
                   '三星级宾馆', '经济型连锁酒店', '旅馆招待所', '青年旅舍']
hotel_key_words_scale = ['住宿服务']

BASE_URL = 'https://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=30&pagenum={page}&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=false&zoom=10&city={adcode}&keywords={keyword}'


class UrlThread(threading.Thread):
    def __init__(self, adcode, keyword):
        threading.Thread.__init__(self)
        self.adcode = adcode
        self.keyword = keyword

    def run(self):
        with thread_max_num:
            concreteGetData(self.adcode, self.keyword,self.getName())


thread_max_num = threading.Semaphore(20)


def assembleURL(keyword, adcode, page=1):
    return BASE_URL.format(page=page, adcode=adcode, keyword=keyword)


def concreteGetData(adcode, keyword,name=""):
    page = 1
    i = 0
    res = None
    try:
        res = requests.get(assembleURL(keyword, adcode))
    except:
        save2File.saveErrorKeywordsAndCodeInMultiplyThread(adcode, keyword)
    else:
        resJson = res.json()
        if 'data' in resJson and 'poi_list' in resJson['data']:
            save2File.savePoiInMultiplyThread(resJson['data']['poi_list'])
            # save2File.saveKeywordsAndCode(adcode, keyword)
            i += 1
            print(name+":"+str(i) + " " + str(len(resJson['data']['poi_list'])))
            isLoop = len(resJson['data']['poi_list']) >= 20
            index = 0
            while isLoop:
                page += 1
                index += 1
                resJson = None
                try:
                    res = requests.get(assembleURL(keyword, adcode, page))
                except:
                    save2File.saveErrorKeywordsAndCodeInMultiplyThread(adcode, keyword)
                else:
                    resJson = res.json()
                    if 'poi_list' in resJson['data']:
                        save2File.savePoiInMultiplyThread(resJson['data']['poi_list'])
                        # save2File.saveKeywordsAndCode(adcode, keyword)
                        time.sleep(1)
                        i += 1
                        print(name+":"+str(i) + " " + str(len(resJson['data']['poi_list'])))
                        print(adcode)
                        if 'poi_list' in resJson['data']:
                            isLoop = len(resJson['data']['poi_list']) >= 20
                        else:
                            isLoop = False
                            break
                    if index >= 50:
                        break


def requestData():
    keyWords = readData.getKeyWords()
    keyWords = keyWords['小类']
    i = 0
    a = ['310113', '310114','310115', '310116', '310117', '310151']
    for adcode in a:
        for keyword in keyWords:
            th = UrlThread(adcode,keyword)
            th.start()
            # concreteGetData(adcode, keyword)


if __name__ == '__main__':
    requestData()
