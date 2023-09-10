import os
import locale
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

istc_id = 'whchanbi@connect.ust.hk'
target = "Washing Machine"

def sendEmail(code_path):
    #Changable Variables
    from_email = "naths.bman@gmail.com"
    to_email = istc_id
    key_email = "vxmpzwdhbcfjvmuy"

    smtp = smtplib.SMTP(host="smtp.gmail.com", port="587")
    smtp.ehlo()
    smtp.starttls()
    smtp.login(from_email, key_email)

    #Send to itself
    content = MIMEMultipart()
    content["from"] = from_email
    content["to"] = to_email
    content['date'] = formatdate(localtime=True)

    #Subject
    content["subject"] = target + " QR Code Record"

    #Contents
    with open(code_path, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename(code_path))
    content.attach(image)
    content.attach(MIMEText(
        "By Naths"
        , 'html'))
    smtp.send_message(content)

    print('Done')

sendEmail("C:\\Users\\Admin\\Documents\\HKUST-Laundry\\1.png")