#!/home/pray/anaconda2/envs/py3/bin/python3.6
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# from_addr = input('From: ')
# password = input('Password: ')
# to_addr = input('To: ')
# smtp_server = input('SMTP server: ')

#from_addr = 'chentianemail@163.com'

#发送邮箱,要在授权中心打开第三方方服务
from_addr = 'pray771020@163.com'
password = 'pray771020'
#to_addr = '2717965131@qq.com'
#收件邮箱
to_addr = '3161945552@qq.com'
#password = 'ct654321'

smtp_server = 'smtp.163.com'

# 邮件对象:
msg = MIMEMultipart()
msg['From'] = _format_addr('收件人 <%s>' % from_addr)
msg['To'] = _format_addr('发件人 <%s>' % to_addr)
#邮件主题
msg['Subject'] = Header('由Python发送的一封邮件', 'utf-8').encode()

# 邮件正文是MIMEText:
msg.attach(MIMEText('这是一张以图片作为附件的邮件', 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
#with open('''C:/Users/chentian/Desktop/MyProject/MySqlist/123.jpg''', 'rb') as f:
with open('''/home/pray/PycharmProjects/facedebug/images/ljj/ljj.png''', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='android-icon.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='android-icon.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

print("successfuly")