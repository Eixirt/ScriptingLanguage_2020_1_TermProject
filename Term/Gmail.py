import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

def SendGmail(Address, Message):
    # global value
    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = "587"
    htmlFileName = "logo.html"

    senderAddr = "kje980827@gmail.com" # 보내는 사람 email 주소.
    recipientAddr = Address  # 받는 사람 email 주소.

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "Kuide"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    # MIME 문서를 생성합니다.
    HtmlPart = MIMEText(Message, _charset='UTF-8')

    # 만들었던 mime을 MIMEBase에 첨부 시킨다.
    msg.attach(HtmlPart)

    # 메일을 발송한다.
    s = mysmtplib.MySMTP(host, port)
    # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("kje980827@gmail.com", "qwer!@#$980827")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()