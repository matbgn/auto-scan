import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv


def send_email(subject: str, emails: str, filename: str, ts: str) -> str:
    load_dotenv()

    smtp_user = os.environ['SMTPSERVER_EMAIL']
    smtp_password = os.environ['SMTPSERVER_PASS']
    smtp_host = os.environ['SMTPSERVER_HOST']

    sent_from = smtp_user

    message_subject = subject

    message = MIMEMultipart('mixed')
    message['From'] = 'BGN Scanner <{sender}>'.format(sender=sent_from)
    message['To'] = emails
    message['CC'] = ''
    message['Subject'] = 'Scan ' + message_subject + " " + ts

    msg_content = '<h4>Hi There,<br> This is an automatic HP scanner message.</h4>\n'
    body = MIMEText(msg_content, 'html')
    message.attach(body)

    attachmentPath = "./" + filename

    try:
        with open(attachmentPath, "rb") as attachment:
            p = MIMEApplication(attachment.read(), _subtype="pdf")
            p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.split("/")[-1])
            message.attach(p)
    except Exception as e:
        print(str(e))

    msg_full = message.as_string()

    try:
        server = smtplib.SMTP_SSL(smtp_host, 465)
        server.ehlo()
        server.login(smtp_user, smtp_password)
        server.sendmail(sent_from,
                        message['To'].split(";") + (message['CC'].split(";") if message['CC'] else []),
                        msg_full)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')
