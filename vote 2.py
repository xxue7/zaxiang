import requests
import time
import common


config={
        'stime':15,
        'rurl':'https://vote.weibo.com/h5/index/index?vote_id=2019_319889_-_150174',
        'index':0

        }

header={
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer':config['rurl'],
    #'Referer': 'https://service.account.weibo.com/reportspam?rid='+rid+'&type=1&from=30000',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',

}


listcookie=common.getListCk()
count=len(listcookie)

for i in range(config['index'],count):
    res=''
    try:
        ck=listcookie[i]
        uid,dictcookie = common.getUidCookie(ck)
        re=requests.get(config['rurl'],cookies=dictcookie).text;
        index=re.find('"sk": "')
        sk=re[index+7:index+49]
        data='vote_id=2019_319889_-_150174&vote_optionids=1107354&sk='+sk
        res=requests.post('https://vote.weibo.com/vote/h5/aj/vote/index',data,headers=header,cookies=dictcookie).text.encode("utf-8").decode("'unicode_escape'")
        #print res
    except Exception as e:
        res=e.message
    print str(i+1)+res
    time.sleep(config['stime'])