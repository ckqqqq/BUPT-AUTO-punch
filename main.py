# -*- coding: utf8 -*-
import json
import time
import requests
import smtplib
import datetime
import re#正则匹配
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
loginURL=
chartURL="https://app.bupt.edu.cn/ncov/wap/default/index"
saveURL=//抓包

# Third-party SMTP service for sending alert emails. 第三方 SMTP 服务，用于
mail_host =       # SMTP server, such as QQ mailbox
mail_user =  # Username 用户名
mail_pass =   # Password, SMTP service password. 
mail_port = # SMTP service port. SMTP服务端口
# The notification list of alert emails. 告警邮件通知列表
email_notify_list = {
    
}


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


def main_handler(event, context):
    WelcomeMail=open("MailContent/Welcome.txt").read()
    Infor = open("UserInform/Inform.txt")

    for line in Infor:
        line=line.strip('\n')
        wordlist=re.split("\s+|\n+|\r+",line)
        try:
            sendEmail(mail_user,wordlist[2],"欢迎使用软院打卡脚本",                     WelcomeMail)
            #欢迎新用户            
        except Exception as e:
            print(e)
    Infor.close()
       
