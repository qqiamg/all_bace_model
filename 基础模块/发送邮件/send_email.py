import smtplib
from email.header import Header
from email.mime.text import MIMEText
import time
import base64

def send_exmail_qq(sender_email, send_key, receiver_email, title, text):
    '''
    使用腾讯企业邮箱发送文本邮件
    :param sender_email: 发送邮箱
    :param send_key: 发送邮箱的stampkey
    :param receiver_emali(list): 接受邮箱列表
    :param title: 邮件标题
    :param text: 邮件正文
    :return: 
    '''
    flag = True
    retime = 0
    while flag == True:
        try:
            tete = text  # 正文
            sender = sender_email  # 发送邮件的
            recevers = receiver_email  # 接受邮件的
            username = sender_email
            password = send_key
            msg = MIMEText(tete, 'plain', 'utf-8')
            msg['From'] = Header(u'信息 <%s>' % sender)
            msg['To'] = Header(u'用户<%s>' % recevers)
            msg['Subject'] = Header(title, 'utf-8')  # 标题
            mail_host = "smtp.exmail.qq.com"
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            smtpObj.login(username, password)
            smtpObj.sendmail(sender, recevers, msg.as_string())
            flag = False
            print('Successfully')
        except smtplib.SMTPException:
            if retime > 3:
                break
            # self.str_out.emit('网址 {} 发送邮件失败，重试发送'.format(url))
            time.sleep(3)
            print('失败')
            flag = True


def send_qq_email(sender_email, send_key, receiver_email, title, text):
    '''
    使用qq邮箱发送文本邮件
    :param sender_email: 发送邮箱
    :param send_key: 发送邮箱的stampkey
    :param receiver_emali(list): 接受邮箱列表
    :param title: 邮件标题
    :param text: 邮件正文
    :return: 
    '''
    flag = True
    retime = 0
    while flag == True:
        try:
            tete = text  # 正文
            sender = sender_email  # 发送邮件的
            recevers = receiver_email  # 接受邮件的
            username = sender_email
            password = send_key
            msg = MIMEText(tete, 'plain', 'utf-8')
            msg['From'] = Header(u'信息 <%s>' % sender)
            msg['To'] = Header(u'用户<%s>' % recevers)
            msg['Subject'] = Header(title, 'utf-8')  # 标题
            mail_host = "smtp.qq.com"
            smtpObj = smtplib.SMTP_SSL(mail_host)

            smtpObj.login(username, password)
            smtpObj.sendmail(sender, recevers, msg.as_string())
            flag = False
            print('Successfully')
        except smtplib.SMTPException:
            if retime > 3:
                break
            # self.str_out.emit('网址 {} 发送邮件失败，重试发送'.format(url))
            time.sleep(3)
            print('失败')
            flag = True

def send_163_email(sender_email, send_key, receiver_email, title, text):
    '''
    使用qq邮箱发送文本邮件
    :param sender_email: 发送邮箱
    :param send_key: 发送邮箱的stampkey
    :param receiver_emali(list): 接受邮箱列表
    :param title: 邮件标题
    :param text: 邮件正文
    :return:
    '''
    flag = True
    retime = 0
    while flag == True:
        try:
            tete = text  # 正文
            sender = sender_email  # 发送邮件的
            recevers = receiver_email  # 接受邮件的
            username = sender_email
            password = send_key
            # msg = MIMEText(tete, 'plain', 'utf-8')
            # msg['From'] = Header(u'信息 <%s>' % sender)
            # msg['To'] = Header(u'用户<%s>' % recevers)
            # msg['Subject'] = Header(title, 'utf-8')  # 标题
            mail_host = "smtp.163.com"
            # smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            # smtpObj.login(username, password)
            # smtpObj.sendmail(sender, recevers, msg.as_string())
            svr = smtplib.SMTP(mail_host)
            # 设置为调试模式，就是在会话过程中会有输出信息
            svr.set_debuglevel(1)
            # ehlo命令，docmd方法包括了获取对方服务器返回信息
            svr.docmd("EHLO server")
            # auth login 命令
            svr.docmd("AUTH LOGIN")
            # 发送用户名，是base64编码过的，用send发送的，所以要用getreply获取返回信息
            svr.send(base64.encodestring(username))
            svr.getreply()
            # 发送密码
            svr.send(base64.encodestring(password))
            svr.getreply()
            # mail from, 发送邮件发送者
            svr.docmd("MAIL FROM: <%s>" % sender)
            # rcpt to, 邮件接收者
            svr.docmd("RCPT TO: <%s>" % recevers)
            # data命令，开始发送数据
            svr.docmd("DATA")
            # 发送正文数据
            svr.send(msg)
            # 比如以 . 作为正文发送结束的标记
            svr.send(" . ")
            svr.getreply()
            # 发送结束，退出
            svr.quit()
            flag = False
            print('Successfully')
        except Exception as e:
        # except smtplib.SMTPException:
            if retime > 3:
                break
            print(e)
            # self.str_out.emit('网址 {} 发送邮件失败，重试发送'.format(url))
            time.sleep(3)
            print('失败')
            flag = True


if __name__ == '__main__':
    ###使用例子###
    # 腾讯企业邮箱
    # sender_email = 'assistant2@yisurvey.com'
    # receiver_email = ['1245013121@qq.com', '212142290@qq.com']
    # password = 'YFSHAJMJSiWxAhLq'
    # send_exmail_qq(sender_email, password, receiver_email, '测试', '发送邮件')
    # qq邮箱
    sender_email = '1245013121@qq.com'
    receiver_email = ['1245013121@qq.com', '212142290@qq.com']
    password = 'mqviyxearcvlhhgj'
    send_qq_email(sender_email, password, receiver_email, '测试', '发送邮件')
    # 163邮箱()
#     sender_email = '15218090298@163.com'
#     receiver_email = ['1245013121@qq.com', '212142290@qq.com','15218090298@163.com']
#     password = 'jizhu4560'
#     text = '''
# 文字，是一个汉语词汇，拼音为wén zì，基本意思是记录思想、交流思想或承载语言的图像或符号。该词出自《史记·秦始皇本纪》：“一法度衡石丈尺，车同轨，书同文字。”'''
#     send_163_email(sender_email, password, receiver_email,'文字介绍',text)

