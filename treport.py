# -*- coding:UTF-8 -*-
import time
import requests
import random
import threading
import common
import re

"""
def getCkUid(cookie):
    index=cookie.find(']')
    ckdict = dict(cookies_are=cookie[index + 1:].rstrip())
    strjson=requests.get('https://m.weibo.cn/api/config',cookies=ckdict,timeout=5).text
    if '"data":{"login":true' in strjson:
        strjson=json.loads(strjson)
        if 'uid' in strjson['data']:
            return strjson['data']['uid'],ckdict
    return '',''

"""
def getItem():
    return random.choice(['category=1&tag_id=108','category=8&tag_id=804','category=2&tag_id=202','category=5&tag_id=503&extra=%23%E5%BE%AE%E5%8D%9A%E8%BE%9F%E8%B0%A3%23%20%E6%96%AD%E7%AB%A0%E5%8F%96%E4%B9%89%EF%BC%8C%E9%80%A0%E8%B0%A3%E8%AF%AF%E5%AF%BC%E4%BB%96%E4%BA%BA'])

def work(index,si):

   tname=threading.currentThread().getName()
   #ss=0
   for i in range(index,workCount,config['threadCount']):
       res=''
       try:
           uid,ck=common.getUidCookie(listcookie[i])
           if uid!='null':
               #postdata=str.replace(config['data'],'%s%',uid)
               postdata=re.sub(r'&uid=[^&]+','&uid='+uid,config['data'])
               if(config['isRitem']):
                   postdata=getItem()+postdata[postdata.find('&url='):]
                   #postdata=re.sub(r'category=\d&tag_id=\d{3}',getItem(),postdata)
               #postdata = 'category=1&tag_id=108&url=%2Fu%2F1391842791&type=3&rid=1391842791&uid='+uid+'&r_uid=1391842791&from=10106&getrid=1391842791&appGet=0&weiboGet=0&blackUser=0&_t=0'
               ip=random.choice(listip).strip()
               time_=str(int(time.time() * 1000))
               header['User-Agent']=common.getheaders()
               header['X-Real-IP']=ip
               header['X-Forwarded-For'] = ip
               print tname+'-'+ip
               res=requests.post(url='https://service.account.weibo.com/aj/reportspam?__rnd='+time_,data=postdata,headers=header,cookies=ck,proxies={'https': 'https://'+ip},timeout=5).text.encode("utf-8").decode("'unicode_escape'")
           else:
               res='cookie失效|uid错误'
       except requests.RequestException as e:
           print tname + '-' + str(e)
           time.sleep(config['stime'])
           #try:

           work(i,si)
           #except requests.RequestException as cc:
               #print str(cc)
           return
       print str(i)+'-'+tname+'-'+res[0:300]
       #ss=ss+1
       tcount[si]=tcount[si]+1
       time.sleep(config['stime'])
   print tname+'-ok-'+str(tcount[si])


#&url=&type=1&rid=4415104063792678&uid=5973027263&r_uid=6348230490&from=10501&getrid=4415104063792678&appGet=0&weiboGet=0&blackUser=0&_t=0
config={
        'index':0,
        'stime':4,
        'threadCount':4,
        'isRitem':0,
        'istxt':False,
        'rurl':'https://service.account.weibo.com/reportspam?rid=55CkED&from=10106&type=3&url=%2Fu%2F5604176016&bottomnav=1&wvr=5',
        'data':'category=8&tag_id=804&url=%2Fu%2F5604176016&type=1&rid=4426303484621563&uid=2150961184&r_uid=5604176016&from=10106&getrid=4426303484621563&appGet=0&weiboGet=0&blackUser=0&_t=0'
        }

header={
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer':config['rurl'],
    #'Referer': 'https://service.account.weibo.com/reportspam?rid='+rid+'&type=1&from=30000',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.'+str(random.randint(1000,10000))+'.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

listip=common.getIp(config['istxt'])

listcookie=common.getListCk()

workCount=len(listcookie)

ths=[]

tcount=[]

for i in range(0,config['threadCount']):
    tcount.append(0)
    ths.append(threading.Thread(target=work,args=(i+config['index'],i,)))
    ths[i].start()

for i in range(0,config['threadCount']):
    #ths[i].start()
    ths[i].join()
acount=0
for i in tcount:
    acount=acount+i
print 'ok-'+str(acount)


