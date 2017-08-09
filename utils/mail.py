# coding:utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(subject, content_text, content_html):
    sender = "cedgir+nas@gmail.com"
    receiver = "cedgir+torrents@gmail.com"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    text = content_text
    html = content_html

    part_text = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    part_html = MIMEText(html.encode('utf-8'), 'html', 'UTF-8')

    msg.attach(part_text)
    msg.attach(part_html)

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
