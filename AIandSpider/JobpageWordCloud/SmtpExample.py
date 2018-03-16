# coding:utf-8

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header



def sendEmail():
    # 收发人
    sender = '1670491921@qq.com'
    receivers = ['1670491921@qq.com','2948117721@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    Password = 'lndtbaoqxrdrdfcc'

    # 构建根对象MIMEMultipart
    msgRoot = MIMEMultipart()
    msgRoot['Subject'] = '开门有惊喜'
    msgRoot['From'] = sender
    msgRoot['To'] = ";".join(receivers)

    # 构建【文本对象】MIMEMultipart
    mail_msg = """
    <h1>换联网薪资水平大对比...</h1>
    
    <p>北京，上海，深圳,python岗位数量的图：</p>
    <p><img src="cid:image1"></p>
    <p>北京  python ,运维，测试，爬虫，数据,web等等岗位分布图：</p>
    <p><img src="cid:image2"></p>
    <p>上海  python ,运维，测试，爬虫，数据,web等等岗位分布图：</p>
    <p><img src="cid:image3"></p>
    <p>深圳  python ,运维，测试，爬虫，数据,web等等岗位分布图：</p>
    <p><img src="cid:image4"></p>
    <p>北京，上海，深圳的最低平均工资，最高平均工资对比图：</p>
    <p><img src="cid:image5"></p>
    <p>北京，上海，深圳的词云图：</p>
    <p><img src="cid:image6"></p>
    """
    msgRoot.attach(MIMEText(mail_msg, 'html', 'utf-8'))


    # 构建【图片对象】MIMEImage
    msgImage = MIMEImage(open('BSS.jpg', 'rb').read())
    msgImage.add_header('Content-ID', '<image1>')# 定义图片 ID，在 HTML 文本中引用
    msgRoot.attach(msgImage)
    msgImage = MIMEImage(open('beijin.jpg', 'rb').read())
    msgImage.add_header('Content-ID', '<image2>')# 定义图片 ID，在 HTML 文本中引用
    msgRoot.attach(msgImage)
    msgImage = MIMEImage(open('shanghai.jpg', 'rb').read())
    msgImage.add_header('Content-ID', '<image3>')# 定义图片 ID，在 HTML 文本中引用
    msgRoot.attach(msgImage)
    msgImage = MIMEImage(open('shenzhen.jpg', 'rb').read())
    msgImage.add_header('Content-ID', '<image4>')# 定义图片 ID，在 HTML 文本中引用
    msgRoot.attach(msgImage)
    msgImage = MIMEImage(open('average.jpg', 'rb').read())
    msgImage.add_header('Content-ID', '<image5>')# 定义图片 ID，在 HTML 文本中引用
    msgRoot.attach(msgImage)
    msgImage = MIMEImage(open('ciyun.jpg', 'rb').read())
    msgImage.add_header('Content-ID', '<image6>')# 定义图片 ID，在 HTML 文本中引用
    msgRoot.attach(msgImage)
    try:
        # 登录邮件服务器
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect('smtp.qq.com', 465)
        smtpObj.login(sender, Password)

        # 发送并退出
        smtpObj.sendmail(sender, receivers, msgRoot.as_string())
        smtpObj.quit()
        print("邮件发送成功")

    # 处理异常
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)

if __name__ == '__main__':
    print("hello")
    sendEmail()