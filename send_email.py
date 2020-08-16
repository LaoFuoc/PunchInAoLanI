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
    # content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
    # message.attach(content)
    # file=open("test.png", "rb")
    # img_data = file.read()
    # file.close()
    # img = MIMEImage(img_data)
    # img.add_header('Content-ID', 'imageid')
    # message.attach(img)

    try:
        server=smtplib.SMTP_SSL("smtp.qq.com",465)
        server.login(sender,"ktqobkcycwvjecfa")
        server.sendmail(sender,receivers,mess.as_string())
        server.quit()
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


# send(['1534372468@qq.com'],'这是一封测试邮件')

