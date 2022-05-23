# -*- coding:UTF-8 -*-
import requests,time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open('cookie.txt') as f:
    listc=f.readlines()


header={
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer':'https://m.weibo.cn/p/1059030002_7615',
    #'Referer': 'https://service.account.weibo.com/reportspam?rid='+rid+'&type=1&from=30000',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    #'X-Requested-With': 'XMLHttpRequest'
}

#今天投票次数已满
aindex=0
sindex=0
listc=listc[0:]

while len(listc)>0:
    print len(listc)
    for cc in listc:
        try:
            sindex+=1
            print cc[1:20]
            if cc:
                dictcookie=dict(cookies_are=cc[cc.find(']')+1:].rstrip())
                rd = requests.get('https://m.weibo.cn/api/container/getItem?itemid=231462_2315220f316b17b43ce037574a39fd4ad77d48_-_10012051e9743451d44c9e10ca584546782491_-_1_-_2',cookies=dictcookie).text

                index = rd.find('4145&sig=')
                if index==-1:
                    if '{"ok":0,' not in rd:
                        print 'yichu'
                        listc.remove(cc)
                    print str(sindex)+'-跳过'+rd
                    continue
                sig = rd[index + 9:index + 15]
                url='https://movie.weibo.com/movie/commonvote?theme_id=335&option_id=4145&sig='+sig
                res=requests.get(url,headers=header,cookies=dictcookie).text
                if u'投票成功' in res:
                    aindex = aindex + 1
                    print str(sindex)+'--'+str(aindex) + '-成功'
                elif u'今天投票次数已满' in res:
                    print str(sindex)+'已满'
                    listc.remove(cc)
                    continue
                else:
                    listc.remove(cc)
                    print str(sindex)+res[0:200]
            else:
                listc.remove(cc)
        except requests.RequestException as e:
            print str(sindex)+'-'+str(e)
        time.sleep(55)
print 'ok'