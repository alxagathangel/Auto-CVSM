import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.message import EmailMessage
from email.utils import formataddr
import passkeys as pk

def send(sender_mail,receiver_mail,msg):
    
    SERVER = "smtp-mail.outlook.com"
    PORT = 587 #for starttls
    # PORT = 465 #for SSL
    
    sender_pass = pk.epass

    with smtplib.SMTP(SERVER,PORT) as s:
        s.starttls()
        s.login(sender_mail,sender_pass)
        s.sendmail(sender_mail,receiver_mail,msg.as_string())


def mail_txt(file_name, message):

    comp_name = "VisualData Inc."

    sender_mail = pk.email
    receiver_mail = pk.client_emails[f'{os.path.splitext(file_name)[0]}']

    msg = EmailMessage()
    msg["Subject"] = 'Your Data: Visualized.'
    msg["From"] = formataddr((f"{comp_name}",f"{sender_mail}"))
    msg["To"] = receiver_mail

    msg.set_content(message)

    send(sender_mail,receiver_mail,msg)

    
def mail_img(file_name,new_dir_path):

    comp_name = "VisualData Inc."
    sender_mail = pk.email
    receiver_mail = pk.my_emails[f'{os.path.splitext(file_name)[0]}']

    msg = MIMEMultipart("related")
    msg["Subject"] = "Your Data: Visualized."
    msg["From"] = formataddr((f"{comp_name}",f"{sender_mail}"))
    msg["To"] = receiver_mail
    
    msg_txt = MIMEText(
f"""
Dear customer,
The images attatched provide visuals of the {os.path.splitext(file_name)[0]} Data you provided.
We hope they can be insightful for you and your business.
Best regards, 
{comp_name}
"""
    )
    msg.attach(msg_txt)

    pathA = os.path.join(new_dir_path,f'clean_{os.path.splitext(file_name)[0]}_plotArea.png')
    pathBa = os.path.join(new_dir_path,f'clean_{os.path.splitext(file_name)[0]}_plotBar.png')
    pathBo = os.path.join(new_dir_path,f'clean_{os.path.splitext(file_name)[0]}_plotBox.png')

    png_files = [pathA, pathBa, pathBo]

    try:
        for file in png_files:
            with open(file,'rb') as f:
                msg_img = MIMEImage(f.read())
                msg.attach(msg_img)
    except Exception as e:
        print(f">> Error attaching images: {e}")

    try:
        send(sender_mail,receiver_mail,msg)
        print(f"- Message successfully sent to {receiver_mail}.")
    except Exception as e:
        print(f">> Error sending email: {e}")
