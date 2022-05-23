<?php
//
//pkcs8格式
//通过 e 和m baidu.py 获取pkcs1格式 使用命令行转制pkcs8
//openssl rsa -RSAPublicKey_in -in psk1.pem -pubout
//
$public_key = '-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCzxh67pGWcTONjkofuhx8fSPeT
Dql3mRx6/jzEQv6klkMhLn1XDIU/NoBlzFeiAUZm2orn1JP9R9FxwNiU7uPtf5n2
eYt//XtYcyJwOK0j4xl2MajLZCITufJ9SQGrDZK/onVCrokIVTlu2Sd1JVyXf1ww
Lx5+1LHjacEstrGCLwIDAQAB
-----END PUBLIC KEY-----';
//baidu rsa  加密方式 bdrsa.js ->php 原密码加severtime10（可固定）字符串，用askii 为0的空白字符填充至128位在倒置加密后再转换为16进制
$data = str_pad('password_severtime', 128, chr(0));
//var_dump("$data");
openssl_public_encrypt(strrev($data), $res, $public_key, OPENSSL_NO_PADDING);

$res = bin2hex($res);

echo $res;
?>