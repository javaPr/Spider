#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/17
"""
import numpy as np
import pandas as pd


def getAdCode(filePath=r'D:\pingan\AMap_adcode_citycode.xlsx\AMap_adcode_citycode.xlsx'):
    # data = np.loadtxt(filePath,skiprows=2,usecols=[1],dtype=bytes).astype(str)
    data = pd.read_excel(filePath)
    # print(data)
    return data


def getKeyWords(filePath=r'D:\pingan\AMap_poicode\高德地图API POI分类编码表.xlsx'):
    data = pd.read_excel(filePath, sheetname='POI分类与编码（中英文）')
    # print(data)
    return data


if __name__ == '__main__':
    getAdCode()
    getKeyWords()
