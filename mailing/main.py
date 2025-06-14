import smtplib

server = smtplib.SMTP('smtp.gmail.com', 25)
server.ehlo()
server.login('code.nischal.tech@gmail.com', )