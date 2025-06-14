import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com', 25)
server.ehlo()

with open('password.txt', 'r') as p:
    password = p.read()

server.login('code.nischal.tech@gmail.com', password)

msg = MIMEMultipart()
msg['From'] = 'Nischal Paliwal'
msg['To'] = 'nischalpaliwal@gmail.com'
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
server.sendmail(text, from_addr='code.nischal.tech@gmail.com', to_addrs='nischalpaliwal@gmail.com')