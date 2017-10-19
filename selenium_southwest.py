# Ian Cleary
# https://github.com/iancleary
# https://github.com/iancleary/airline-check-in
# clearyia@gmail.com
import os
import time # sleep
from selenium import webdriver # Browswer Automation
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import threading # multi thread browsers to log in all passengers at the same time

#from exceptions import Exception

##############################################################################
##############################################################################
####################### Only Edit Below Passenger List #######################
##############################################################################
##############################################################################

# Login list (confirmationNumber, firstName, lastName, 'email' or 'text', area code, phone prefix, phone number, email address)
# append as many users as desired
passengerList = []
passengerList.append(['M48GBP', 'Ian', 'Cleary', 'text', '4805551234', 'myemail@gmail.com'])

##############################################################################
##############################################################################
####################### Only Edit Above Passenger List #######################
##############################################################################
##############################################################################

# Site Information
URL = 'https://www.southwest.com/flight/retrieveCheckinDoc.html?clk=GSUBNAV-CHCKIN&forceNewSession=yes'

DEBUG_XPATH = True
DEBUG_CHROMEDRIVER_PATH = True

HEADLESS = False

FIRST_SCREEN_ATTEMPTS = 0
SECOND_SCREEN_ATTEMPTS = 0
THIRD_SCREEN_ATTEMPTS = 0

#############################################################################

import os
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# functions to enter username, password, and click login
def text_autofill(driver, text_xpath, text):
    text_box = driver.find_element_by_xpath(text_xpath)
    text_box.send_keys(text)
    return

def text_clear(driver, text_xpath):
    text_box = driver.find_element_by_xpath(text_xpath).clear()
    return

def click(driver, webElement_xpath):    
    driver.find_element_by_xpath(webElement_xpath).click()
    return

#############################################################################

# Functions to script each log in screen
def firstScreen(driver, passenger):
    global FIRST_SCREEN_ATTEMPTS

    confirmationNumber_xpath = '//*[@id="confirmationNumber"]'
    firstName_xpath = '//*[@id="passengerFirstName"]'
    lastName_xpath = '//*[@id="passengerLastName"]'
    checkIn_xpath = '//*[@id="form-mixin--submit-button"]' #Check In button

    text_autofill(driver, confirmationNumber_xpath, passenger[0])
    text_autofill(driver, firstName_xpath, passenger[1])
    text_autofill(driver, lastName_xpath, passenger[2])
    time.sleep(1)
    click(driver, checkIn_xpath)
    
    if DEBUG_XPATH:
        clear()
        print("1st screen: %s %s: Attempt %i" % (passenger[1], passenger[2], FIRST_SCREEN_ATTEMPTS))
        FIRST_SCREEN_ATTEMPTS = FIRST_SCREEN_ATTEMPTS + 1  
    return

def secondScreen(driver, passenger):
    global SECOND_SCREEN_ATTEMPTS
    
    
    #checkIn_2nd_Screen_xpath = '//*[@id="printDocumentsButton"]'
    checkIn_2nd_Screen_xpath = '//*[@id="swa-content"]/div/div[2]/div/section/div/div/div[3]/button'
    click(driver, checkIn_2nd_Screen_xpath)

    time.sleep(1)
    if DEBUG_XPATH:
        clear()
        print("2nd screen: %s %s: Attempt %i" % (passenger[1], passenger[2], SECOND_SCREEN_ATTEMPTS))
        SECOND_SCREEN_ATTEMPTS = SECOND_SCREEN_ATTEMPTS + 1
    return

def thirdScreen(driver, passenger):
    print_button_xpath = '//*[@id="swa-content"]/div/div[2]/div/section/div/div/section/table/tbody/tr/td[1]/button'


    email_button_xpath = '//*[@id="swa-content"]/div/div[2]/div/section/div/div/section/table/tbody/tr/td[2]/button'
    email_textBox_xpath = '//*[@id="emailBoardingPass"]'
    email_send_xpath = '//*[@id="form-mixin--submit-button"]'

    text_button_xpath = '//*[@id="swa-content"]/div/div[2]/div/section/div/div/section/table/tbody/tr/td[3]/button'
    text_phone_number_xpath = '//*[@id="textBoardingPass"]'
    text_phone_number_send_xpath = '//*[@id="form-mixin--submit-button"]'
    
    if(passenger[3] == 'text'):
        click(driver, text_button_xpath)
        time.sleep(1)
        text_autofill(driver, text_phone_number_xpath, passenger[4])
        click(driver, text_phone_number_send_xpath)
        
    elif(passenger[3] == 'email'):
        click(driver, email_button_xpath)
        time.sleep(1)
        text_autofill(driver, email_textBox_xpath, passenger[5])
        click(driver, email_send_xpath)
        
    return

#############################################################################

def loginSinglePassenger(passenger):
    cwd = os.getcwd()
    path_to_chromedriver = '%s/chromedriver' % (cwd)
    
    chrome_options = Options()  
    chrome_options.add_argument("--headless")

    if DEBUG_CHROMEDRIVER_PATH:
        print(path_to_chromedriver)

    if HEADLESS:
        driver = webdriver.Chrome(path_to_chromedriver, chrome_options=chrome_options) # faster with one driver for entire list
    else:
        driver = webdriver.Chrome(path_to_chromedriver) # faster with one driver for entire list
    
    driver.get(URL)
    #time.sleep(1)
    firstScreen(driver, passenger)
    time.sleep(2)

    #loop first screen until second screen appears (will only go through exactly 24 hours before flight)
    passFirstScreen = False
    while (passFirstScreen == False):
        try:
            secondScreen(driver, passenger)
            passFirstScreen = True
        except NoSuchElementException:
            driver.get(URL)
            firstScreen(driver, passenger)
            
    # now third screen
    #time.sleep(1)
    thirdScreen(driver, passenger)
    
    time.sleep(10)
    driver.quit()
    return

#############################################################################

# Threading class
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, passenger):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.passenger = passenger
    def run(self):
        print("Starting " + self.name + "\n")
        loginSinglePassenger(self.passenger)
        print("Exiting " + self.name + "\n")

#############################################################################
        
# Main Login with MultiThreading
def login(passengerList):
    threads = []
    for passengerIndex,passenger in enumerate(passengerList):
        thread = myThread(passengerIndex, "Thread-" + str(passengerIndex), passengerIndex, passenger)
        threads.append(thread)

    for passengerIndex,passenger in enumerate(passengerList):
        threads[passengerIndex].start()

    print("Exiting Main Thread")
    return

# Main Code Block
login(passengerList)
