import locale
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
'''

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
        print("Found Available: ", tmp)
        ava_machines.append(tmp)
    tmp = machine.text  #As last record

print("Now ", len(ava_machines), " avaiable(s) machine")
for machine in ava_machines:
    print(machine)

#Capture QR Code
driver.find_element(By.CLASS_NAME, 'segment').screenshot('foo.png')