import ssl
import os
import socket
from datetime import datetime
from urllib.parse import urlparse

import smtplib
from email.message import EmailMessage

# config
hostname = os.getenv("website_url")
port = 443
threshold_days = 30  # Alert if cert expires in less than this many days
email_address = str(os.getenv("protonmail_email_address"))
protonmail_bridge_pass = str(os.getenv("protonmail_bridge_pass"))


# function to send email using ProtonMail Bridge
def send_email_proton(subject):
    msg = EmailMessage()
    msg.set_content(subject)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = email_address

    with smtplib.SMTP('127.0.0.1', 1025) as smtp:  # Port 1025 is default for Bridge
        smtp.login(email_address, protonmail_bridge_pass)
        smtp.send_message(msg)

# function to check expiry date of the certificate
def get_cert_expiry(hostname, port):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_date_str = cert['notAfter']
            expire_date = datetime.strptime(expire_date_str, "%b %d %H:%M:%S %Y %Z")
            return expire_date

# main logic
expiry = get_cert_expiry(hostname, port)
days_left = (expiry - datetime.utcnow()).days

if days_left < threshold_days:
    send_email_proton(f"Certificate for {hostname} expires on {expiry} ({days_left} days left)")


# upload to github account
# add the function for emailing if an error occurs in the script
# gotta add task sheduler to run every week

# then make the HIBP script to use protonmail bridge to send emails rather than dumbass gmail api
# could make a blog about this tbh on website

# add MIT license and stuff like that