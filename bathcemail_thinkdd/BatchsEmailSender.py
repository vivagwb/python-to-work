
import os
import sys
import csv
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email import encoders
import time
import pandas as pd


# ========================批量发送邮件测试（二）----邮件内容固定，主题和附件变化=================================
#

# --------------------发送服务器配置---------------


# sender_host = 'smtp.163.com:25'  # 默认服务器地址及端口
sender_host = 'smtp.126.com'   # 使用SSL连接，
sender_user = 'gwb1990@126.com'
sender_pwd = 'gwbnetease@think'
sender_name = '测试公司'
# self.attach_type = ".xlsx"

#通讯录及邮件附件所在路径信息

addrpath=r'C:\Users\Administrator\Desktop\邮件发送练习\address.csv'
attachpath=r'C:\Users\Administrator\Desktop\邮件发送练习\文件'

#公司名称和附件对应的字典
comattachdict={}

#分割文件名的关键字符
splitword='10'

#邮件正文中固定内容
fixcontent="吃饭"





# --------------根据输入的CSV文件，获取通讯录人名和相应的邮箱地址-------

def getAddrBook(addrBook):

        #@作用：根据输入的CSV文件，形成相应的通讯录字典,同一个名称可以对应多个邮箱（适用多个收件人场景）

    address=pd.read_csv(addrBook,engine='python',encoding="utf-8")      #注意收件人通讯录需保存为编码格式为utf-8的csv文件
    addrs=address.groupby('name').email.apply(list).to_dict()   #注意收件人通讯录首列应命名为“name”，第二列应命名为“email”

    return addrs


getAddrBook(addrpath)


# -------------------根据附件名称中获得的公司名称，并获取公司名称和附件路径的字典---------------

def getRecvAddr(attachpath):
    filepath=os.listdir(attachpath)
    companylist=[]
    for i in range(len(filepath)):
        companylist.append(filepath[i].split(splitword)[0])
        filepath[i]=attachpath+'\\'+filepath[i]   #获取存储附件绝对路径的列表
    comattachdict=dict(zip(companylist,filepath))  #获取公司名称和对应附件路径的字典
    return comattachdict


getRecvAddr(attachpath)
# --------------------添加附件-----------------------------------

def addAttch(attach_file):
    att = MIMEBase('application','octet-stream')  # 这两个参数不知道啥意思，二进制流文件
    att.set_payload(open(attach_file,'rb').read())
    # 此时的附件名称为****.xlsx，截取文件名
    att.add_header('Content-Disposition', 'attachment')
    encoders.encode_base64(att)
    return att



# ---------------------发送邮件-----------------------
def mailSend(attach_path,bookFile,mail_content):
    smtp = smtplib.SMTP_SSL(sender_host,994)  # 使用SSL连接
    smtp.login(sender_user, sender_pwd)
    for companyname in attach_path:
        mail_msg=MIMEMultipart()
        mail_msg['Subject'] = '吃饭'+companyname #设置邮箱主题
        mail_msg['From'] =  sender_user   #设置发送人
        mail_msg['To']  =';'.join(bookFile[companyname])  #设置收件人

        mail_msg.attach(MIMEText(fixcontent+companyname))
    #------------添加附件---------------------
        attach_file=attach_path[companyname]
        att=addAttch(attach_file)
        mail_msg.attach(att)



        smtp.sendmail(sender_user,bookFile[companyname],mail_msg.as_string())
        print("已发送："+companyname+'\n')








    # for root,dirs,files in os.walk(attach_path):
    # 	for attach_file in files:      # attach_file : ***_2_***.xlsx
    # 		msg = MIMEMultipart('alternative')
    #
    # 		msg['Subject'] = subject   # 设置邮件主题
    # 		person_name = subject.split("_")[-1]
    # 		recv_addr = getRecvAddr(addrs,person_name)
    # 		msg['From'] = formataddr([sender_name,sender_user]) # 设置发件人名称
    # 		# msg['To'] = person_name # 设置收件人名称
    # 		msg['To'] = formataddr([person_name,recv_addr]) # 设置收件人名称
    # 		# mail_content = getMailContent(content_path)
    # 		msg.attach(MIMEText(mail_content))  # 正文  MIMEText(content,'plain','utf-8')
    # 		attach_file = root+"\\"+attach_file
    # 		att = addAttch(attach_file)
    # 		msg.attach(att)  # 附件
     #
    # 		# 增加判断是否到达最大发送限制
    # 		if count >= 10:
    # 			smtp.quit()
    # 			# print("")
    # 			time.sleep(5)  # 让子弹飞一会儿
    # 			count = 1
    # 			smtp = smtplib.SMTP_SSL(sender_host,994)  # 使用SSL连接
    # 			smtp.login(sender_user, sender_pwd)
    # 		smtp.sendmail(sender_user, [recv_addr,], msg.as_string())  # smtp.sendmail(from_addr, to_addrs, msg)
    # 		print("已发送： "+person_name+" <"+recv_addr+">")
    # 		count += 1
    # 		# time.sleep(5)   # 163检测，一次连接状态，最多只能发送10封邮件。故加延时，延时5秒也没用
    # 		time.sleep(1)
    # 	smtp.quit()
    # 	print("请按任意键退出程序：")
    # 	anykey = ord(msvcrt.getch())   # 此刻捕捉键盘，任意键退出
    # 	if anykey in range(0,256):
    # 		print("Have a nice day !")
    # 		time.sleep(1)
    # 		sys.exit()





