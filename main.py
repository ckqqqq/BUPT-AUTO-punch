# -*- coding: utf8 -*-
import json
import time
import requests
import smtplib
import datetime
import re#正则匹配,自闭机23333
import os
import sys

import logging
from email.mime.text import MIMEText
from email.header import Header
session = requests.Session()
#session = requests.Session()
#服务端的记录
oldKeys = [
    "ismoved",    "jhfjrq", "jhfjjtgj", "jhfjhbcc", "sfxk", "xkqq", "szgj", "szcs", "zgfxdq", "mjry", "csmjry", "uid",  "tw", "sfcxtz", "sfyyjc", "jcjgqr", "jcjg", "sfjcbh", "sfcxzysx", "qksm", "remark", "address", "area", "province", "city", "geo_api_info",  "sfzx", "sfjcwhry", "sfcyglq", "gllx",
    "glksrq", "jcbhlx", "jcbhrq", "sftjwh", "sftjhb", "fxyy", "bztcyy", "fjsj", "sfjchbry", "sfjcqz", "jcqzrq", "jcwhryfs", "jchbryfs", "xjzd", "sfsfbh", "jhfjsftjwh", "jhfjsftjhb", "szsqsfybl", "sfygtjzzfj", "gtjzzfjsj", "sfsqhzjkk", "sqhzjkkys", "created_uid", "gwszdd", "sfyqjzgc", "jrsfqzys", "jrsfqzfy"
]
defaultKeys = [
    "date", "created", "id",
]
loginURL="打卡登陆地址"
chartURL="打卡表格地址"#/default/index
saveURL="打卡地址存储"

SuccessMail = open("MailContent/Success.txt").read()
FailMail=open("MailContent/Fail.txt").read()
# Third-party SMTP service for sending alert emails. 第三方 SMTP 服务，用于多用户自动发邮件
mail_host = ""   # SMTP server, such as QQ mailbox
mail_user = ""  # Username 
mail_pass = ""  # Password, SMTP service password. 
mail_port =465   # SMTP service port. SMTP服务端口
# The notification list of alert emails. 告警邮件通知列表



def sendEmail(fromAddr, toAddr, subject, content):
    sender = fromAddr
    receivers = [toAddr]
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(fromAddr, 'utf-8')
    message['To'] = Header(toAddr, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("send email success")
        return True
    except smtplib.SMTPException as e:
        print(e)
        print("Error: send email fail")
        return False
        #没有问题
def login(username: str, password: str):
    #发送密码,返回json包 https://www.runoob.com/python3/python3-json.html
    response = session.post(loginURL, data={
        "username": username,
        "password": password,
    })

    if response.json()["e"] == 0:
        return True
    else:
        print(response.text)
        return False


def check(username: str, password: str,mailReceiver: str):

    if login(username, password):
        print(username, "登录成功")
    else:
        sendEmail(mail_user,mailReceiver,"登录失败提醒",FailMail)
        print(username, "登录失败")
        return
    #获取默认信息
    response = session.get(chartURL)
    #print("response.text\n", response.text,"\n")
    #!!!之前忘记加原生 r "\n" gg
    #返回string中所有与pattern匹配的全部字符串,返回形式为数组。zz
    #
    matchDefault = re.findall(r'var def = (.*);\n', response.text)

    if (len(matchDefault) == 0):
        print("获取默认信息失败")
        sendEmail(mail_user,mailReceiver,"获取默认信息失败",FailMail)
        return
    default = json.loads(matchDefault[0])
    #上次信息

    matchOld = re.findall(r'oldInfo: (.*),\n', response.text)
    #注 完全匹配不加问好
    if (len(matchOld) == 0):
        print("获取上次信息失败")
        sendEmail(mail_user,mailReceiver,"获取上次信息失败",FailMail)
        return
    #载入Oldinfo 对齐
    oldInfo = json.loads(matchOld[0])

    #通过r=request.get（url）构造一个向服务器请求资源的url对象。

    data = {}#类似map智能
    yesterdayAddress=""
    for k in oldInfo:
        data[k] = oldInfo.get(k, "")#查找键k,返回默认值
        if re.match(k,"address"):
            yesterdayAddress=k+":"+data[k]
            print(yesterdayAddress)
    for k in defaultKeys:
        data[k] = default.get(k, "")
       
    #构造返回包
    response = session.post(saveURL, data=data)
    j = response.json()

    if j.get("e", 1) == 0:
        print("填报成功",mailReceiver)
        sendEmail(mail_user,mailReceiver,"打卡成功提醒",re.sub("Address",yesterdayAddress,username+SuccessMail))
    else:
        FailReason=j.get("m", "") 
        print("填报失败原因:(测试)", FailReason,"(测试)填报失败原因"+FailReason,
        re.sub("Address",yesterdayAddress,username+FailMail))#返回m信
        sendEmail(mail_user,"接受失败信息的邮箱,注意区分覆盖信息!",
        "(测试)填报失败原因"+FailReason,re.sub("Address",yesterdayAddress,username+FailMail))


def main_handler(event, context):
    #WelcomeMail=open("MailContent/Welcome.txt")
    Infor = open("UserInform/Inform.txt")
    i=0
    for line in Infor:
        line=line.strip('\n')
        wordlist=re.split("\s+|\n+|\r+",line)
        try:
            #打卡检测发邮件
            i+=1
            print(i,"\n")
            check(wordlist[0],wordlist[1],wordlist[2])#u p mail           
            #欢迎新用户            
        except Exception as e:
            print(e)
    Infor.close()
       
