#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/17
"""

import threading


def save2File(dataList):
    with open('resultPOI_1.txt', 'a+', encoding='utf-8') as f:
        for data in dataList:
            f.writelines(str(data['id']) + "\t")
            f.writelines(str(data['name']) + '\t')
            f.writelines(str(data['type']) + '\t')
            f.writelines(str(data['typecode']) + '\t')
            f.writelines(str(data['address']) + '\t')
            f.writelines(str(data['location']) + '\t')
            f.writelines(str(data['tel']) + '\t\n')


def savePoi(dataList,filepath='data\scale_hotel_shanghai_whole_2.txt'):
    with open(filepath, 'a+', encoding='utf-8') as f:
        for data in dataList:
            f.writelines(str(data.get('id','')) + "\t")
            f.writelines(str(data.get('disp_name','')) + '\t')
            f.writelines(str(data.get('name','')) + '\t')
            f.writelines(str(data.get('cityname','')) + '\t')
            f.writelines(str(data.get('rating','')) + '\t')
            f.writelines(str(data.get('newtype','')) + '\t')
            f.writelines(str(data.get('typecode','')) + '\t')
            f.writelines(str(data.get('areacode','')) + '\t')
            f.writelines(str(data.get('address','')) + '\t')
            f.writelines(str(data.get('longitude','')) + '\t')
            f.writelines(str(data.get('latitude','')) + '\t')
            f.writelines(str(data.get('group_flag','') + '\t'))
            f.writelines(str(data.get('tel','')) + '\t\n')


def saveKeywordsAndCode(code,keyword,filePath='data\keyAndCode.txt'):
    with open(filePath,'a+',encoding='utf-8') as f:
        f.writelines(code +":"+keyword+'\n')


def saveErrorKeywordsAndCode(code,keyword,filePath='data\errorKeyAndCode.txt'):
    with open(filePath,'a+',encoding='utf-8') as f:
        f.writelines(code +":"+keyword+'\n')


mu = threading.Lock()
def saveErrorKeywordsAndCodeInMultiplyThread(code,keyword,filePath='data\errorMulThreadKeyAndCode_putuo.txt'):
    if mu.acquire(True):
        with open(filePath,'a+',encoding='utf-8') as f:
            f.writelines(code +":"+keyword+'\n')
        mu.release()

saveThreadLock = threading.Lock()

def savePoiInMultiplyThread(dataList,filepath='data\scale_hotel_shanghai_whole_MulThread_putuo.txt'):
    if saveThreadLock.acquire(True):
        with open(filepath, 'a+', encoding='utf-8') as f:
            for data in dataList:
                f.writelines(str(data.get('id','')) + "\t")
                f.writelines(str(data.get('disp_name','')) + '\t')
                f.writelines(str(data.get('name','')) + '\t')
                f.writelines(str(data.get('cityname','')) + '\t')
                f.writelines(str(data.get('rating','')) + '\t')
                f.writelines(str(data.get('newtype','')) + '\t')
                f.writelines(str(data.get('typecode','')) + '\t')
                f.writelines(str(data.get('areacode','')) + '\t')
                f.writelines(str(data.get('address','')) + '\t')
                f.writelines(str(data.get('longitude','')) + '\t')
                f.writelines(str(data.get('latitude','')) + '\t')
                f.writelines(str(data.get('group_flag','') + '\t'))
                f.writelines(str(data.get('tel','')) + '\t\n')
        saveThreadLock.release()