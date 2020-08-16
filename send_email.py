# encoding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send(receivers,message):
    sender = '2168258948@qq.com'
    mess =  MIMEMultipart('related')
    subject = '每日打卡详情'
    mess['Subject'] = subject
    mess['From'] = sender
    mess['To'] = ",".join(receivers)
    mess.attach(MIMEText(message))

    try:
        server=smtplib.SMTP_SSL("smtp.qq.com",465)
#         server.login()中，修改为自己的邮箱授权码
        server.login(sender,"ktqobkcycxxxxxx")
        server.sendmail(sender,receivers,mess.as_string())
        server.quit()
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


# send(['1534372468@qq.com'],'这是一封测试邮件')

