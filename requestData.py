#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/17
"""
import requests
import readData
import math
import save2File
import threading

KEYS = ['44b62e3b3d95fdc659dbaab04792f1d4', '9b447d25c4a0274224285bb85ebfdd84', '910a60ca33fc399714b9192d7685a41e',
        '9ef483b5926d2fa307f60d6f22c0da36', '942edf2af2fecd2049e4b0aefdb76581', '205cdfbf470bc89835a94505a5ce86aa',
        '4c41262989fdb16bc9598db973ce996d', '9ef8c4be80fcb4bc45bb217bebe48c90', '5e0968d74a8ec3237353af89a6707067',
        '06e65fad0f181aeceacdbfa189e4568d', 'edbdef21659aec87b73277d435d545db']

NEW_KEYS = ['819bc8286a22ac3a18fc27fef81fc6f2','affb440e7998225061cffdea0510ea65','64be9a64c4c4e58eced8f65dbd44a437',
            'd024446bf0f8b88d99dc4254645ccf43']

NEW_KEYS_1 = ['03084aacf754f1514f4f16c579bac8e2','672dec21f70c34d6ea5af0551864571f','87a1fb04f9788c3b8f81cf03d26b932d']
#'672dec21f70c34d6ea5af0551864571f','03084aacf754f1514f4f16c579bac8e2', 87a1fb04f9788c3b8f81cf03d26b932d
shanghai_adcode = ['310101', '310104', '310105', '310106', '310107',
                   '310109', '310110', '310112', '310113', '310114',
                   '310115', '310116', '310117', '310118', '310120', '310151']

BASE_URL = "https://restapi.amap.com/v3/place/text?keywords={keyword}&city={adcode}&output=json&offset={offset}&page={page}&key={key}&extensions=all"
BASE_URL_1 = 'https://restapi.amap.com/v3/place/text?s=rsv3&children=&key={key}&offset={offset}&page={page}&types={keyword}&city={adcode}&extensions=all&language=undefined&platform=JS&logversion=2.0&appname=https%3A%2F%2Flbs.amap.com%2Fapi%2Fjavascript-api%2Fexample%2Fpoi-search%2Fkeywords-search&csid=6C85D721-E99F-4192-AA1B-D98A4A5E11FE&sdkversion=1.4.8&keywords='

class UrlThread(threading.Thread):
    def __init__(self, adcode, keyword, key):
        threading.Thread.__init__(self)
        self.adcode = adcode
        self.keyword = keyword
        self.key = key

    def run(self):
        with thread_max_num:
            concreteGetData(self.adcode, self.keyword, self.key, self.getName())


thread_max_num = threading.Semaphore(1)

offSet = 50


def concreteGetData(adcode, keyword, key, name=''):
    url = assembleUrl(keyword, adcode, offSet, 1, key)
    res = None
    try:
        res = requests.get(url)
    except:
        print("except")
        save2File.saveErrorKeywordsAndCodeInMultiplyThread(adcode, keyword)

    else:
        resJson = res.json()
        #print(resJson)
        count = int(resJson['count'])
        save2File.save2FileMulThread(resJson.get('pois', []))
        pageNumber = math.ceil(count / offSet)
        for i in range(2, pageNumber + 1):
            url = assembleUrl(keyword, adcode, offSet, i, key)
            try:
                res = requests.get(url)
            except:
                print("except")
                save2File.saveErrorKeywordsAndCodeInMultiplyThread(adcode, keyword)
            else:
                resJson = res.json()
                save2File.save2FileMulThread(resJson.get('pois', []))
                print(name + ":" + str(i) + " " + str(len(resJson.get('pois', []))))
                print(adcode)


def assembleUrl(keyword, adcode, offset, page, key):
    res = BASE_URL_1.format(keyword=keyword, adcode=adcode, offset=offset, page=page, key=key)
    # print(res)
    return res


def requestData():
    adCodeData = readData.getAdCode()
    keyWords = readData.getKeyWords()
    adCodeData = adCodeData['adcode'][1:]
    keyWords = keyWords['小类']
    # offSet = 25
    size = len(NEW_KEYS_1)
    i = 0
    for adcode in shanghai_adcode[13:8:-1]:
        for keyword in keyWords:
            pos = i % size
            i += 1
            th = UrlThread(adcode, keyword, NEW_KEYS_1[pos])
            th.start()


if __name__ == '__main__':
    requestData()


# res = requests.get("https://restapi.amap.com/v3/place/text?keywords=北京大学&city=beijing&output=json&offset=20&page=1&key=44b62e3b3d95fdc659dbaab04792f1d4&extensions=all")
# print(res.json())
# assembleUrl('背景','1231231',20,1)
