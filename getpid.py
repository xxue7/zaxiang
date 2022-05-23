import requests
import threading
import pymysql


def getPid(i):
    for index in range(i,END+1,Wcount):
        try:
            print(threading.currentThread().name+'--'+str(index))
            url = "https://tieba.baidu.com/mo/q/postreport?pid=" + str(index)
            html = requests.get(url).text
            portriat = jq('/sys/portrait/item/', '.jpg', html)
            name = jq('<span class="name">', '</span>', html)
            word = jq('<span class="word">', '吧</span>', html)
            content = jq('<p class="thread_abstract">', '</p>', html)
            sql = 'insert into tieba_content(pid,author_name,content,portrait,word)values'
            sql += "(%d,'%s','%s','%s','%s')" % (index, name, content, portriat, word)
            if mutex.acquire():
                cursor.execute(sql)
                db.commit()

        except Exception as e:
            print(e)
            db.rollback()
        mutex.release()

def jq(l,r,strs):
    lindex=strs.find(l)
    if lindex>-1:
        lindex = lindex + len(l)
        rindex=strs.find(r,lindex)
        if rindex>-1:
            return strs[lindex:rindex]
    return ''

mutex = threading.Lock()

# 打开数据库连接 #localhost 本地主机 可以用其他 ip 如 虚拟机的ifconfig 命令 所得到 的 ip 来 连接虚拟机的 数据库
db = pymysql.connect('','','.','test',charset='utf8',port=)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

ths=[]

START=1050100
END=1060000
Wcount=5

for i in range(0,Wcount):
    ths.append(threading.Thread(target=getPid,args=(i+START,)))
    ths[i].start()

for i in range(0,Wcount):
    ths[i].join()
print('ok')