#include "bd.h"
#include <QtNetwork>
#include <QtNetwork/QNetworkAccessManager>
#include <QtNetwork/QNetworkReply>
#include <QtNetwork/QNetworkRequest>
#include <QCoreApplication>


BD::BD(QObject *parent) : QObject(parent)
{

}
QString BD::unicodeTozn(const QString &unicode)
{
   QStringList list= unicode.split("\\u");

   QString t1;

   foreach (const QString &t, list) {

       t1.append(t.toUShort(0,16));
   }

   return t1;
}

bool BD::ReadAllText(const QString &fileName, QString &text,const char *codec)
{
       QFile file(fileName);
       if( !file.open(QIODevice::ReadOnly) )
           return false;
       QTextStream in(&file);
       if( codec != NULL )
           in.setCodec(codec);
       text = in.readAll();
       file.close();
       return true;
}
bool BD::WriteAllText(const QString &fileName, const QString &text, const bool mode, const char *codec)
{
    QFile file(fileName);
    if(mode)
    {
        if( !file.open(QIODevice::WriteOnly | QIODevice::Truncate) )
                return false;
    }else
    {
        if( !file.open(QIODevice::WriteOnly | QIODevice::Append) )
                return false;
    }

    QTextStream out(&file);

    if( codec != NULL )
            out.setCodec(codec);
        out << text;
        file.close();
        return true;
}
QByteArray BD::fetch(const QString &url, ENCODE en, METHOD mod, const QByteArray &data,const QByteArray &cookie )
{
    QNetworkRequest req;

    req.setUrl(QUrl(url));

    if(!cookie.isEmpty()) req.setRawHeader("Cookie",cookie);

    req.setRawHeader("Content-Type","application/x-www-form-urlencoded");

    //req.setRawHeader("User-Agent","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)");

    QNetworkAccessManager man;

    QNetworkReply *reply;

    if(mod==POST)
    {
        reply=man.post(req,data);

    }else
    {
        reply=man.get(req);
    }

    QEventLoop loop;

    QTimer timer;

    connect(reply,&QNetworkReply::finished,&loop,&QEventLoop::quit);

    connect(&timer,&QTimer::timeout,&QTimer::stop);

    connect(&timer,&QTimer::timeout,&loop,&QEventLoop::quit);

    connect(reply,SIGNAL(error(QNetworkReply::NetworkError)),&loop,SLOT(quit()));

    timer.start(6000);
    loop.exec();
    if(!timer.isActive())
    {
        reply->abort();
        delete reply;
        return "操作超时";
    }
    QByteArray res;

    if(reply->error()==QNetworkReply::NoError)
    {

        if(en==GBK)
        {
           res.append( QString::fromLocal8Bit(reply->readAll()));
        }else
        {
             res=reply->readAll();
        }
    }else
    {
        res=reply->errorString().toLatin1();
    }

    reply->deleteLater();


    return res;
}

QString BD::md5(const QByteArray &str)
{
   QByteArray res= QCryptographicHash::hash(str,QCryptographicHash::Md5);

   return res.toHex();
}

QString BD::midstr(const QString &left, const QString &right, const QString &str)
{
    QString res("");

    int l=str.indexOf(left);

    int r=str.indexOf(right,l+left.length());

    if(l!=-1&&r!=-1)
    {
        res=str.mid(l+left.length(),r-l-left.length());
    }

    return res;


}

QString BD::fid(const QString &kw)
{
   QString str= fetch("http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname="+kw);

   return midstr("fid\":",",",str);


}

QString BD::tbs(const QByteArray &cookie)
{
    QString str=fetch("http://tieba.baidu.com/dc/common/tbs",UTF8,GET,"",cookie);

    return midstr("tbs\":\"","\",\"is_login\":1",str);

}

QString BD::login(const QString &un, const QByteArray &psd, const QString &vcode, const QString &pic)
{
    QByteArray data;

    data.append("_client_id=&_client_type=2&_client_version=1.0.1&_phone_imei=000000000000000&from=baidu_appstore&isphone=0&net_type=1&passwd=");

    data.append(psd.toBase64()).append(QString("&un=%1&vcode=%2&vcode_md5=%3").arg(un,vcode,pic));

    QByteArray temp=data;

    data.append("&sign=").append(md5(temp.replace("&","").append("tiebaclient!!!")));

    return fetch("http://c.tieba.baidu.com/c/s/login",UTF8,POST,data);
}
QString BD::random(const int &len, const bool num)
{
    QString res;

    for(int i=0;i<len;i++)
    {
        int ce=qrand()%2;
        ce=num==true?0:ce;
        switch(ce)
        {
         case 0:
            res.append(QString::number(qrand()%9));
            break;
        case 1:
           res.append(QChar(65+qrand()%25));
           break;
        case 2:
           res.append(QChar(95+qrand()%25));
           break;
        }

    }
    return res;
}
QString BD::reply(const QString &tid,const QString &name, const QString &fid, const QString &tbs, const QString &cookie, const QString &content)
{
    QByteArray data;

    data.append(cookie+"&_client_id=wappc_136"+random(10)+'_'+random (3)+"&_client_type=1&_client_version=5.0.0&_phone_imei="+md5 ( random ( 16 ).toLatin1() ));
    data.append("&anonymous=0&content="+content+"&fid="+fid+"&kw="+name+"&net_type=3&tbs="+tbs+"&tid="+tid+"&title=");

    QByteArray temp=data;

    data.append("&sign=").append(md5(temp.replace("&","").append("tiebaclient!!!")));

    //qDebug()<<data;

    return fetch("http://c.tieba.baidu.com/c/c/post/add",UTF8,POST,data);



}
