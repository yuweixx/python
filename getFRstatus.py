#coding=utf-8
##用于监控帆软报表服务器状态
import os
import time

import smtplib
import email.mime.multipart
import email.mime.text

## 发送邮件函数
def send_email(SMTP_host, from_addr, password, to_addrs, subject='', content=''):
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = from_addr
    msg['to'] = to_addrs
    msg['subject'] = subject
    content = content
    txt = email.mime.text.MIMEText(content)
    msg.attach(txt)

    smtp = smtplib.SMTP()
    smtp.connect(SMTP_host, '25')
    smtp.login(from_addr, password)
    smtp.sendmail(from_addr, to_addrs, str(msg))
    smtp.quit()
# 获取帆软报表服务器状态
def frstatus():
#print(csvreader.line_num("D:\\webtest\\apache-jmeter-3.2\\bin\\FR8500.csv"))
    # 执行jmeter脚本
    os.system("D:\\webtest\\apache-jmeter-3.2\\bin\\jmeter -n -t D:\\webtest\\apache-jmeter-3.2\\bin\\FR8500.jmx")
    with open("D:\\webtest\\apache-jmeter-3.2\\bin\\FR8500.csv","r",encoding="utf-8") as csvfile:
        readers = csvfile.readlines()
        countlines = len(readers)
        print(countlines)
        relusttype = readers[-1].split(',')[7]
        print('relusttype=',relusttype)
        if relusttype == 'true':
            print("registerSuccess")
            send_email('smtp.126.com', '*****@126.com', '******', '****@szewec.com', 'FR8500StatusOK', 'registerSuccess')
        else:
            print("registerFail")
            send_email('smtp.126.com', '*****@126.com', '******', '****@szewec.com', 'FR8500StatusFail', 'registerFail')
    return relusttype

def frfailstatus():
    os.system("D:\\webtest\\apache-jmeter-3.2\\bin\\jmeter -n -t D:\\webtest\\apache-jmeter-3.2\\bin\\FR8500.jmx")
    with open("D:\\webtest\\apache-jmeter-3.2\\bin\\FR8500.csv","r",encoding="utf-8") as csvfile:
        readers = csvfile.readlines()
        countlines = len(readers)
        print(countlines)
        relusttype = readers[-1].split(',')[7]
        print('relusttype=',relusttype)
        if relusttype == 'true':
            print("registerSuccess")
        else:
            print("registerFail")
            send_email('smtp.126.com', '*****@126.com', '*****', '*****@szewec.com', 'FR8500StatusFail', 'registerFail')
    return relusttype

## 监控循环，没100秒执行一次，失败跳出并发送邮件；没4小时发送一次正常的邮件
while 1>0:
    i = 0
    typeB = frstatus()
    print('tpyeB=', typeB)
    if typeB == 'true':
        pass
    else:
        break
    time.sleep(100)
    while i<144:
        typeA = frfailstatus()
        print('tpyeA=', typeA)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        if typeA == 'true':
            pass
        else:
            break
        time.sleep(100)
        i = i+1
