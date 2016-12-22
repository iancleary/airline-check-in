
# coding: utf-8

# In[2]:

import time # sleep
from selenium import webdriver # Browswer Automation

# Site Information
URL = 'https://www.aa.com/reservation/flightCheckInViewReservationsAccess.do'
# ---- American Airlines Check In Policy ----
# Check in online beginning 24 hours and up to 
# 45 minutes before your flight 
#(90 minutes for international).


# Login list (confirmationNumber, firstName, lastName, AAdvantage #)
# append as many users as desired
passengerList = []
passengerList.append(['CONFNUM', 'Ian', 'Cleary', 'AADVANTAGE#'])

#Site specific xpaths
recordLocator_xpath = '//*[@id="findReservationForm.recordLocator"]'
firstName_xpath = '//*[@id="findReservationForm.firstName"]'
lastName_xpath = '//*[@id="findReservationForm.lastName"]'
checkIn_xpath = '//*[@id="findReservationForm.submit"]' #Check In button

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
        text_autofill(driver, recordLocator_xpath, passenger[0])
        text_autofill(driver, firstName_xpath, passenger[1])
        text_autofill(driver, lastName_xpath, passenger[2])
        #time.sleep(1)
        click(driver, checkIn_xpath)
        #time.sleep(1)
    #driver.quit()
    
    # I am not sure what the check in process is after the login screen

# Main Code Block
login(passengerList)

