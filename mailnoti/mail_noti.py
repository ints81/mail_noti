import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import pickle


class MailNoti:

    def __init__(self):
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp.ehlo()
        self.smtp.starttls()

        self.sender_addr = None

        self.noti_msg = {
            'program_end' : 'program ended.'
        }

    def login(self, sender_addr, pw):
        pw = pickle.load(open('pw.pickle', 'rb'))

        self.sender_addr = sender_addr
        self.smtp.login(sender_addr, pw)

    def _make_msg(self, to_addr, title, contents, attachment=None):
        if attachment:
            msg = MIMEMultipart('mixed')
        else:
            msg = MIMEMultipart('alternative')

        msg['From'] = self.sender_addr
        msg['To'] = to_addr
        msg['Subject'] = title

        text = MIMEText(_text=contents, _charset='utf-8')
        msg.attach(text)

        if attachment:
            from email.mime.base import MIMEBase
            from email import encoders

            file_data = MIMEBase('application', 'octect-stream')
            file_data.set_payload(open(attachment, 'rb').read())
            encoders.encode_base64(file_data)

            filename = os.path.basename(attachment)
            file_data.add_header('Content-Disposition', 'attachment', filename=('UTF-8', '', filename))
            msg.attach(file_data)

        return msg

    def notify_end(self, program_name):
        msg = self._make_msg(to_addr=self.sender_addr,
                             title=f'{program_name} is finished!',
                             contents=f'{program_name} ' + self.noti_msg['program_end'])

        self.smtp.sendmail(self.sender_addr, self.sender_addr, msg.as_string())


if __name__ == '__main__':
    mail_noti = MailNoti()
    mail_noti.login(sender_addr, pw)

    mail_noti.notify_end('MailNoti Test Program')
