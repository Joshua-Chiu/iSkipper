from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import sys
import time
import random
from environment import *

'''
Mode Selection
0: Random
1: Always Choose A
2: Always Choose B
3: Always Choose C
4: Always Choose D
5: Always Choose E
'''
MODE_SELECTOR = 0
PAGE_CHANGE_TIMEOUT = 30
CLASS_START_TIMEOUT = 7200 # 2 hours
CLASS_LENGTH_TIMEOUT = 7200 # 2 hours

print("Starting selenium: Please ensure you have firefox installed")
print("Remember to define USERNAME and PASSWORD in environment.py")
opts = FirefoxOptions()
if "headless" in sys.argv:
    opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)


# Launch site
driver.get('https://student.iclicker.com/#/login')
print(driver.title)
id_box = driver.find_element(By.ID,'userEmail')
pass_box = driver.find_element(By.ID,'userPassword')
id_box.send_keys(USERNAME)
pass_box.send_keys(PASSWORD)
login_button = driver.find_element(By.ID,'sign-in-button')
login_button.click()

try:
    timeout = PAGE_CHANGE_TIMEOUT
    element_present = expected_conditions.presence_of_element_located((By.CLASS_NAME, 'selectable-item-list-courses'))
    WebDriverWait(driver, timeout).until(element_present)
    print(driver.title)
except TimeoutException:
    print("Timed out waiting for page to load")


# Listed out available courses
print("Press the number next to key to standby for the course")
courselist = driver.find_elements(By.XPATH, "//ul[@class='selectable-item-list-courses']/li/a/label")
for idx, course in enumerate(courselist):
    print(f"{idx}: {course.text}")

selection = int(input("Enter course: "))
courselist[selection].find_element(By.XPATH, "..").click()


# Enter course
try:
    timeout = PAGE_CHANGE_TIMEOUT
    element_present = expected_conditions.presence_of_element_located((By.CLASS_NAME, 'course-navigation-tabs-container'))
    WebDriverWait(driver, timeout).until(element_present)
    print(driver.title)
except TimeoutException:
    print("Timed out waiting for page to load")

print(f"{driver.title}: Waiting for course to start")


# Wait for join
try:
    timeout = CLASS_START_TIMEOUT
    element_present = expected_conditions.visibility_of_element_located((By.ID, 'btnJoin'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for class to load")

print(f"{driver.title}: Class started, now joining")
start_time = time.time()
join_button = driver.find_element(By.ID, 'btnJoin')
join_button.click()


# Enter class
try:
    timeout = PAGE_CHANGE_TIMEOUT
    element_present = expected_conditions.presence_of_element_located((By.CLASS_NAME, 'green-sub-head'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")

print(f"{driver.title}: Joined Class, waiting for Clicker Poll")


# Wait for iclicker poll
while time.time() - start_time < CLASS_LENGTH_TIMEOUT:
    print(f"{driver.title}: Waiting for Poll")
    try:
        timeout = CLASS_LENGTH_TIMEOUT
        element_present = expected_conditions.presence_of_element_located((By.CLASS_NAME, 'multiple-choice-buttons'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print(f"{driver.title}: Timed out waiting for question to load")

    print(f"{driver.title}: Poll Available")
    button_id = "multiple-choice-"

    match MODE_SELECTOR:
        case 1:
            button_id += "a"
        case 2:
            button_id += "b"
        case 3:
            button_id += "c"
        case 4:
            button_id += "d"
        case 5:
            button_id += "e"

        # If an exact match is not confirmed, this last case will be used if provided
        case _:
            button_id += random.choice("abcde")
    
    answer_button = driver.find_element(By.ID, button_id)
    answer_button.click()
    print(f"{driver.title}: Selected {button_id} by MODE_SELECTOR {MODE_SELECTOR} at {time.ctime()}")

    try:
        print(f"{driver.title}: Waiting for end of question")
        element_present = expected_conditions.visibility_of_element_located((By.ID, 'status-text-container-id'))
        WebDriverWait(driver, CLASS_LENGTH_TIMEOUT).until_not(element_present)
    except TimeoutException:
        print(f"{driver.title}: Timed out waiting for end of question")

print(f"{driver.title}: Shutting down")
driver.quit()
print("Clean exit")