
# coding: utf-8

# In[3]:

import time # sleep
from selenium import webdriver # Browswer Automation

# Site Information
URL = 'https://www.southwest.com/flight/retrieveCheckinDoc.html?clk=GSUBNAV-CHCKIN&forceNewSession=yes'

# Login list (confirmationNumber, firstName, lastName)
# append as many users as desired
passengerList = []
passengerList.append(['ZZZZZZ', 'Ian', 'Cleary'])
passengerList.append(['YYYYYY', 'Johannes', 'Keplar'])
passengerList.append(['XXXXXX', 'John', 'Glenn'])

#Site specific xpaths
confirmationNumber_xpath = '//*[@id="confirmationNumber"]'
firstName_xpath = '//*[@id="firstName"]'
lastName_xpath = '//*[@id="lastName"]'
checkIn_xpath = '//*[@id="submitButton"]' #Check In button

# functions to enter username, password, and click login
def text_autofill(driver, text_xpath, text):
    text_box = driver.find_element_by_xpath(text_xpath)
    text_box.send_keys(text)

def click(driver, webElement_xpath):
    driver.find_element_by_xpath(webElement_xpath).click()

def login(passengerList):
    driver = webdriver.Chrome() # faster with one driver for entire list
    for passenger in passengerList:
        driver.get(URL);
        #time.sleep(1)
        text_autofill(driver, confirmationNumber_xpath, passenger[0])
        text_autofill(driver, firstName_xpath, passenger[1])
        text_autofill(driver, lastName_xpath, passenger[2])
        #time.sleep(1)
        click(driver, checkIn_xpath)
        #time.sleep(1)
    driver.quit()

# Main Code Block
login(passengerList)
