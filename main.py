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


'''
#Input
print('ISTC ID: ', end='')
istc_id = input()
print('password: ', end='')
password = input()
#password ='Hkust61387159'
print('What are you looking for(0: Washing machine, 1: Dryer): ', end='')
target = input()
if("0" == target):
    target = "Washing Machine"
elif("1" == target):
    target = "Dry Machine"
'''

istc_id = 'whchanbi@connect.ust.hk'
target = "Washing Machine"
password ='Hkust61387159'

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

#Get to website
print('Reaching Website')
locale.setlocale(locale.LC_ALL, '')
driver = webdriver.Chrome()
time.sleep(5)
driver.get("https://laundry.ust.hk/ldr/app/tickets")
time.sleep(5)
driver.find_element(By.NAME, 'loginfmt').send_keys(istc_id)
driver.find_element(By.ID, "idSIButton9").click()
time.sleep(1.5)
driver.find_element(By.NAME, 'passwd').send_keys(password)
driver.find_element(By.ID, "idSIButton9").click()
time.sleep(5)

#Get Tickets
print('Looking for tickets')
tmp = driver.find_elements(By.CLASS_NAME, 'segment')[0].find_elements(By.TAG_NAME, 'div')[1]
tickets = tmp.find_elements(By.TAG_NAME, 'small')
for ticket in tickets:
    if target in ticket.text:
        print('Found Target: ', target)
        tmp = ticket.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
        break
tmp.click()
time.sleep(5)
'''Activite Button'''
tmp = driver.find_element(By.CLASS_NAME, 'ant-btn')
tmp.click()
time.sleep(5)

#Get Target Status
tmp = driver.find_element(By.CLASS_NAME, 'segment').find_elements(By.TAG_NAME, 'div')[1].find_elements(By.TAG_NAME, 'div')[0]
machines = tmp.find_elements(By.TAG_NAME, 'small')
ava_machines = []
for machine in machines:
    if machine.text == "Available":
        print("Found Available: ", tmp.text)
        ava_machines.append(tmp)
    tmp = machine  #As last record

print("Now ", len(ava_machines), " avaiable(s) machine")
for machine in ava_machines:
    print(machine.text)

#Click avaiable
if ava_machines.__len__ > 0:
    #Have avaiable, click first
    ava_machines[0].click()

    #Activite 1 button
    for button in driver.find_elements(By.CLASS_NAME, 'button'):
        for p in button.find_elements(By.TAG_NAME, 'p'):
            if p.text == "Activate Machine":
                button.click()
    time.sleep(0.5)
    
    #Activite 2 button
    for button in driver.find_elements(By.CLASS_NAME, 'button'):
        if button.text == "Proceed":
            button.click()

    #Capture QR Code
    code_path = 1

    for file_path in os.listdir(os.getcwd()):
        if os.path.isfile(file_path):
            if file_path == code_path + ".png":
                code_path += 1
    code_path = os.getcwd() + "\\" + code_path + ".png"
    driver.find_element(By.TAG_NAME, 'body').screenshot(code_path)
    sendEmail(code_path)

    #Delete the QR Code
    os.remove(code_path)
    print('Finish Booking!')
else:
    print('No machine avaiable')