# -*- coding:UTF-8 -*-
import time,requests,json,random

def getCkUid():
    ckdict = dict(cookies_are=config['ck'])
    strjson=requests.get('https://m.weibo.cn/api/config',cookies=ckdict,timeout=5).text
    print strjson
    if '"data":{"login":true' in strjson:
        strjson=json.loads(strjson)
        if 'uid' in strjson['data']:
            return strjson['data']['uid'],ckdict
    return '',''


config={
    'ck':'',
    'time':4,
    'uid':'3159135863',
    'index':1
}
header={
    'Content-Type': 'application/x-www-form-urlencoded',
    #'Referer':'https://service.account.weibo.com/reportspam?rid=HzPQj2exj&from=10106&type=1&url=%2Fu%2F6159334641&bottomnav=1&wvr=5',
    #'Referer': 'https://service.account.weibo.com/reportspam?rid='+rid+'&type=1&from=30000',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
with open('ip.txt') as k:
    listip=k.readlines()

uid,cookies=getCkUid()

if uid:
    while True:
        try:
          print '第%d页:'%config['index']
          url='https://m.weibo.cn/api/container/getIndex?containerid=230413'+config['uid']+'_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page='+str(config['index'])
          res=requests.get(url,timeout=5).text
          if '{"card_type":9' in res:
              resjson=json.loads(res)
              wb=resjson['data']['cards']
              if config['index']==1:
                  wb=wb[1:]
              i = 0
              for w in wb:
                  i = i + 1
                  try:
                      ip=random.choice(listip).strip()
                      time_=str(int(time.time() * 1000))
                      header['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.'+str(random.randint(1000,10000))+'.106 Safari/537.36'
                      header['X-Real-IP']=ip
                      header['X-Forwarded-For'] = ip
                      data = 'category=8&tag_id=804&url=%2Fu%2F' + config[
                          'uid'] + '&type=1&rid=' + w['mblog']['id'] + '&uid=' + uid + '&r_uid=' + config[
                                 'uid'] + '&from=10106&getrid=' + w['mblog'][
                                 'id'] + '&appGet=0&weiboGet=0&blackUser=0&_t=0'
                      header['Referer'] = 'https://service.account.weibo.com/reportspam?rid=' + w['mblog'][
                          'bid'] + '&from=10106&type=1&url=%2Fu%2F' + config['uid'] + '&bottomnav=1&wvr=5'
                      wres = requests.post('https://service.account.weibo.com/aj/reportspam?__rnd='+time_, data,
                                           cookies=cookies, headers=header, timeout=5).text.encode("utf-8").decode(
                          "'unicode_escape'")
                      if 'raw_text' in w['mblog']:
                          title = w['mblog']['raw_text']
                      else:
                          title = w['mblog']['text']
                      print '%d:%s' % (i, title)
                      print wres
                  except Exception as ee:
                      print str(i) + ':no-3:' + str(ee)
                  time.sleep(config['time'])

          else:
              print 'no-2'
              break
        except Exception as e:
            print 'no-4:'+str(e)
        config['index'] = config['index'] + 1

    print 'ok'
else:
    print 'no-1'
