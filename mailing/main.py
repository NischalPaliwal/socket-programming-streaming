import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

sender_mail = 'signuptemp1247@securemail.org'
receiver_mail = 'nbqr6@punkproof.com'

server = smtplib.SMTP('smtp.google.com', 587)
server.ehlo()
server.starttls()

with open('password.txt', 'r') as p:
    password = p.read()

server.login(sender_mail, password)

msg = MIMEMultipart()
msg['From'] = 'Nischal Paliwal'
msg['To'] = receiver_mail
msg['Subject'] = 'Just a testing mail!'

with open('body.txt', 'r') as f:
    message = f.read()

msg.attach(MIMEText(message, 'plain'))

image_filename = '3d-icon-travel-with-airplane.jpg'
attachment = open(image_filename, 'rb')

payload = MIMEBase('application', 'octet-stream')
payload.set_payload(attachment.read())

encoders.encode_base64(payload)
payload.add_header('Content-Disposition', f"attachment; filename={image_filename}")
msg.attach(payload)

text = msg.as_string()
server.sendmail(msg=text, from_addr=sender_mail, to_addrs=receiver_mail)