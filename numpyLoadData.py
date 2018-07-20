#!/usr/bin/env python
"""
Author wangdechang
Time 2018/7/18
"""
import numpy as np
import pandas as pd

import codecs

filePath = r'D:\PythonWorkSpace\AMap\data\scale_hotel.csv'
filePath1 = r'D:\PythonWorkSpace\AMap\data\test.csv'

# ndata = np.loadtxt(open(filePath1,encoding='utf-8'))
with open(filePath) as f:
    d = np.loadtxt(f, delimiter=',', encoding='latin-1', dtype=str)
    print(d)
# d = np.loadtxt(open(filePath1, encoding='latin-1'), delimiter=',', dtype=bytes).astype(str)

# npData = np.genfromtxt(filePath, comments=str, dtype=np.str, delimiter='\s')
cfile = codecs.open(filePath, encoding='cp1252')

pData = pd.read_csv(open(filePath))
# pdata = pd.read_excel(filePath1)
# pdata = pd.read_csv(filePath1,sep=',')
data = np.loadtxt(cfile, delimiter=',', dtype=str)
print(data)
