import ssl
import os
import socket
from datetime import datetime
from urllib.parse import urlparse

import smtplib
from email.message import EmailMessage

import traceback
import sys

# config
hostname = os.getenv("website_url")
port = 443
threshold_days = 30  # Alert if cert expires in less than this many days
email_address = str(os.getenv("protonmail_email_address"))
protonmail_bridge_pass = str(os.getenv("protonmail_bridge_pass"))

# function to email error code using ProtonMail Bridge
def send_error_email(error_message):
    # create message object
    msg = EmailMessage()
    msg.set_content(f"Error occurred:\n\n{error_message}")
    msg['Subject'] = "Cert Checker - Error Occurred"
    msg['From'] = email_address
    msg['To'] = email_address

    with smtplib.SMTP('127.0.0.1', 1025) as smtp:  # Port 1025 is default for Bridge
        smtp.login(email_address, protonmail_bridge_pass)
        smtp.send_message(msg)

    sys.exit(1)  # Exit script if error occurs (will show in task scheduler that error occurred)

# function to send email using ProtonMail Bridge
def send_email_proton(subject):
    # create message object
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
            expire_date = datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z')
            return expire_date  # ← return the datetime object


# main logic
try:
    expiry = get_cert_expiry(hostname, port)
    days_left = (expiry - datetime.utcnow()).days

    if days_left < threshold_days:
        # only send email if less than the threshold days left
        send_email_proton(f"Certificate for {hostname} expires on {expiry.strftime('%d/%m/%Y %H:%M:%S')} ({days_left} days left)")

except Exception as e:
    send_error_email(traceback.format_exc())




'''
MIT License

Copyright (c) 2025 newKio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Original creator: newKio - https://github.com/newKio/cert_checker
'''