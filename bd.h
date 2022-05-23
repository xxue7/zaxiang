#ifndef BD_H
#define BD_H

#include <QObject>

class BD : public QObject
{
    Q_OBJECT
public:
    explicit BD(QObject *parent = 0);
    enum ENCODE{GBK,UTF8};Q_ENUM(ENCODE);
    enum METHOD{POST,GET};Q_ENUM(METHOD);
    static QByteArray fetch(const QString &url,ENCODE en=UTF8,METHOD mod=GET,const QByteArray &data="",const QByteArray &cookie="");
    static QString md5(const QByteArray &str);
    static QString fid(const QString &kw);
    static QString midstr(const QString &left,const QString &right,const QString &str);
    static QString tbs(const QByteArray &cookie);
    static QString login(const QString &un,const QByteArray &psd,const QString &vcode="",const QString &pic="");
    static QString unicodeTozn(const QString &);
    static bool ReadAllText(const QString &fileName, QString &text,const char *codec=NULL);
    static bool WriteAllText(const QString &fileName, const QString &text, const bool mode=true,const char *codec=NULL);
    static QString random(const int &len,const bool num=true);
    static QString reply(const QString &tid,const QString &name,const QString &fid,const QString &tbs,const QString &cookie,const QString &content);
signals:

public slots:
};

#endif // BD_H
