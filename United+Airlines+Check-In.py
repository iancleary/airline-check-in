
# coding: utf-8

# In[2]:

import time # sleep
from selenium import webdriver # Browswer Automation

# Site Information
URL = 'https://www.united.com/travel/checkin/start.aspx'
# ---- United Airlines Check In Policy ----
# Check-in is available starting 24 hours before your scheduled departure.


# Login list (confirmationNumber, firstName, lastName, MileagePlus #)
# append as many users as desired
passengerList = []
passengerList.append(['CONFNUM', 'Ian', 'Cleary', 'ABCDEFGH'])

#Site specific xpaths
confirmationNumber_xpath = '//*[@id="nbr_id"]'
#firstName_xpath = '//*[@id="findReservationForm.firstName"]'
lastName_xpath = '//*[@id="txtLastName"]'
mileagePlusNumber_xpath = '//*[@id="txtFQTV"]'
password_xpath = '//*[@id="txtPin"]'
continue_xpath = '//*[@id="_ctl0_Main_btnContinue_Button1"]' #Continue button
signIn_xpath = '//*[@id="_ctl0_Main_btnSignin_Button1"]' #Sign In (Secure) button

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
        #text_autofill(driver, firstName_xpath, passenger[1])
        text_autofill(driver, lastName_xpath, passenger[2])
        text_autofill(driver, mileagePlusNumber_xpath, passenger[3])
        #time.sleep(1)
        click(driver, continue_xpath)
        #click(driver, signIn_xpath)
        #time.sleep(1)
    #driver.quit()
    
    # I am not sure what the check in process is after the login screen

# Main Code Block
login(passengerList)

