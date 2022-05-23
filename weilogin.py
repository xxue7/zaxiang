# -*- coding: utf-8 -*-

import requests
import json
import base64
import re
import rsa
import binascii

#sinaSSOController.preloginCallBack({"retcode":0,"servertime":1536326600,"pcid":"gz-b75f5e2c2c4bd805531ea195f09a7992de16","nonce":"6J1KQM","pubkey":"EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443","rsakv":"1330428213","is_openlock":1,"exectime":30})
usname=''

password=''

def login():

    deftext = ''

    infodef=''


    su=base64.encodestring(usname.replace("@","%40")).rstrip()

    header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0' }

    url='https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su='+su+'&rsakt=mod&client=ssologin.js(v1.4.15)&_=1536325253756'

    try:

        rest=requests.get(url,headers=header).text

        restjson=json.loads(re.search(r'\((.*?)\)',rest).group(1))

        pubkey='EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'

        nonce=restjson['nonce']

        servertime=restjson['servertime']

        rsaPublickey = int(pubkey, 16)

        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥


        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password.strip())  # 拼接明文加密文件中得到

        passwd = rsa.encrypt(message, key)  # 加密

        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。

        postdata={
            'entry': 'sso',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'useticket': '0',
            'pagerefer': 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)',
            'vsnf': '1',
            'su': su,
            'service': 'sso',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': '1330428213',
            'sp': passwd,
            'sr': '1440*900',
            'encoding': 'UTF-8',
            'cdult': '3',
            'domain': 'sina.com.cn',
            'prelt': '22',
            'returntype': 'TEXT'
        }
#{"retcode":"0","uid":"6017844516","nick":"豆包子_k","crossDomainUrlList":["https:\/\/passport.weibo.com\/wbsso\/login?ticket=ST-NjAxNzg0NDUxNg%3D%3D-1536344036-gz-710A27FF5345A1CB32DA5340593053FB-1&ssosavestate=1567880036","https:\/\/passport.weibo.cn\/sso\/crossdomain?action=login&savestate=1"]}

        rest2=requests.post('https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=1536329319672',data=postdata,headers=header)

        #rest2= rest2.text.encode('utf-8').decode("'unicode_escape'")

        rest3=json.loads(rest2.text)

        if rest3['retcode']=='0':

            #rurl=re.search(r'(https\:.*?)"',rest2).group(1).replace("\\","")

            rurl=rest3['crossDomainUrlList'][0]

            cookies=requests.get(rurl).cookies.get_dict()

            cookiest={}

            cookiest['cookie']=cookies

            cookiest['emailphone']=usname.strip()

            cookiest['psd']=password.strip()

            cookiest['uid']=rest3['uid']

            cookiest['nick']=rest3['nick']

            strcookie=json.dumps(cookiest).replace('\'','"')

            with open('cookie.txt','a+') as f:

                f.write(strcookie+'\n')

            infodef="ok!!!"
        else:

            deftext=usname+'----'+password+'\n'

            infodef=rest2.text

    except Exception as e:

        infodef =e
        deftext = usname + '----' + password + '\n'

    if deftext.strip():
        with open('det.txt', 'a+') as df:

            df.write(deftext)

    return infodef
#pubkey='EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'



