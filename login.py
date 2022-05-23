# -*- coding:UTF-8 -*-

import weilogin
import json

with open('un.txt') as f:

    listun=f.readlines()

countindex=0

print '开始登陆：'

for unpw in listun:

    countindex+=1

    if unpw.find('----')>-1:

        weilogin.usname,weilogin.password=unpw.strip().split('----')

    elif unpw.find('"cookie":')>-1:

        unpwjson=json.loads(unpw.strip())

        weilogin.password=unpwjson['psd']

        weilogin.usname=unpwjson['emailphone']

    else:
        print '未读取到账号--'+unpw
        continue

    res=weilogin.login()

    print str(countindex)+'--'+weilogin.usname+'--'+res

print '完成'