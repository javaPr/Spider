#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author wangdechang
Time 2018/7/31
"""

import re
import os

regex = r'[\w]*?_xioaqu.dat'

fileList = os.listdir('../temp/')

for f in fileList:
    m = re.match(regex,f)
    if m is None:
        fileList.remove(f)
        continue

with open('../result/result_xiaoqu_info_20180731.dat','w',encoding='utf-8') as f:
    for fileName in fileList:
        for line in open('../temp/'+fileName,encoding='utf8'):
            f.writelines(line.replace('元/㎡',''))


