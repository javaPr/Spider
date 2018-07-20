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

KEYS=['44b62e3b3d95fdc659dbaab04792f1d4','9b447d25c4a0274224285bb85ebfdd84','910a60ca33fc399714b9192d7685a41e',
      '9ef483b5926d2fa307f60d6f22c0da36','942edf2af2fecd2049e4b0aefdb76581','205cdfbf470bc89835a94505a5ce86aa',
      '4c41262989fdb16bc9598db973ce996d','9ef8c4be80fcb4bc45bb217bebe48c90','5e0968d74a8ec3237353af89a6707067',
      '06e65fad0f181aeceacdbfa189e4568d','edbdef21659aec87b73277d435d545db','dda813cc9594887a2c07d3b2957680ads']

shanghai_adcode = ['310101', '310104', '310105', '310106', '310107',
                   '310109', '310110', '310112', '310113', '310114',
                   '310115', '310116', '310117', '310118', '310120', '310151']

BASE_URL = "https://restapi.amap.com/v3/place/text?keywords={keyword}&city={adcode}&output=json&offset={offset}&page={page}&key=44b62e3b3d95fdc659dbaab04792f1d4&extensions=all"


def assembleUrl(keyword, adcode, offset, page):
    res = BASE_URL.format(keyword=keyword, adcode=adcode, offset=offset, page=page)
    # print(res)
    return res


def requestData():
    adCodeData = readData.getAdCode()
    keyWords = readData.getKeyWords()
    adCodeData = adCodeData['adcode'][1:]
    keyWords = keyWords['小类']
    offSet = 25
    for adcode in adCodeData:
        for keyword in keyWords:
            url = assembleUrl(keyword, adcode, offSet, 1)
            res = requests.get(url)
            resJson = res.json()
            count = int(resJson['count'])
            save2File.save2File(resJson['pois'])
            pageNumber = math.ceil(count/offSet)
            for i in range(2,pageNumber+1):
                url = assembleUrl(keyword, adcode, offSet, i)
                res = requests.get(url)
                resJson = res.json()
                save2File.save2File(resJson['pois'])



if __name__ == '__main__':
    requestData()


# res = requests.get("https://restapi.amap.com/v3/place/text?keywords=北京大学&city=beijing&output=json&offset=20&page=1&key=44b62e3b3d95fdc659dbaab04792f1d4&extensions=all")
# print(res.json())
# assembleUrl('背景','1231231',20,1)
