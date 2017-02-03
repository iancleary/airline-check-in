# Ian Cleary
# https://github.com/iancleary
# https://github.com/iancleary/airline-check-in
# clearyia@gmail.com

import time # sleep
from selenium import webdriver # Browswer Automation
from selenium.common.exceptions import NoSuchElementException
import threading # multi thread browsers to log in all passengers at the same time

##############################################################################
##############################################################################
####################### Only Edit Below Passenger List #######################
##############################################################################
##############################################################################

# Login list (confirmationNumber, firstName, lastName)
# append as many users as desired
passengerList = []
passengerList.append(['BT6TU9', 'Ian', 'Cleary', 'email', '480', '555', '1234', 'iansemail@gmail.com'])
passengerList.append(['BGH4KT', 'Bob', 'Bobson', 'email', '317', '555', '2345', 'bobsemail@gmail.com'])
passengerList.append(['BGH4KT', 'Jane', 'Doeson', 'email', '203', '555', '3456', 'janesemail@gmail.com'])

##############################################################################
##############################################################################
####################### Only Edit Above Passenger List #######################
##############################################################################
##############################################################################

# Site Information
URL = 'https://www.southwest.com/flight/retrieveCheckinDoc.html?clk=GSUBNAV-CHCKIN&forceNewSession=yes'

#############################################################################

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
    confirmationNumber_xpath = '//*[@id="confirmationNumber"]'
    firstName_xpath = '//*[@id="firstName"]'
    lastName_xpath = '//*[@id="lastName"]'
    checkIn_xpath = '//*[@id="submitButton"]' #Check In button

    text_autofill(driver, confirmationNumber_xpath, passenger[0])
    text_autofill(driver, firstName_xpath, passenger[1])
    text_autofill(driver, lastName_xpath, passenger[2])
    #time.sleep(1)
    click(driver, checkIn_xpath)
    return

def secondScreen(driver):
    checkIn_2nd_Screen_xpath = '//*[@id="printDocumentsButton"]'
    click(driver, checkIn_2nd_Screen_xpath)
    return

def thirdScreen(driver, passenger):
    checkIn_3rd_screen_print_radio_xpath = '//*[@id="optionPrint"]'

    checkIn_3rd_screen_email_radio_xpath = '//*[@id="optionEmail"]'
    checkIn_3rd_screen_email_textBox_xpath = '//*[@id="emailAddress"]'

    checkIn_3rd_screen_text_radio_xpath = '//*[@id="optionText"]'
    checkIn_3rd_screen_text_area_code_xpath = '//*[@id="phoneArea"]'
    checkIn_3rd_screen_text_phone_prefix_xpath = '//*[@id="phonePrefix"]'
    checkIn_3rd_screen_text_phone_number_xpath = '//*[@id="phoneNumber"]'

    checkIn_3rd_screen_check_in_button_xpath = '//*[@id="checkin_button"]'

    if(passenger[3] == 'text'):
        click(driver, checkIn_3rd_screen_text_radio_xpath)
        text_autofill(driver, checkIn_3rd_screen_text_area_code_xpath, passenger[4])
        text_autofill(driver, checkIn_3rd_screen_text_phone_prefix_xpath, passenger[5])
        text_autofill(driver, checkIn_3rd_screen_text_phone_number_xpath, passenger[6])
    elif(passenger[3] == 'email'):
        click(driver, checkIn_3rd_screen_email_radio_xpath)
        text_clear(driver, checkIn_3rd_screen_email_textBox_xpath)
        text_autofill(driver, checkIn_3rd_screen_email_textBox_xpath, passenger[7])
    time.sleep(1)
    click(driver, checkIn_3rd_screen_check_in_button_xpath)
    return

#############################################################################

def loginSinglePassenger(passenger):
    driver = webdriver.Chrome() # faster with one driver for entire list
    driver.get(URL)
    #time.sleep(1)
    firstScreen(driver, passenger)
    #time.sleep(1)

    #loop first screen until second screen appears (will only go through exactly 24 hours before flight)
    passFirstScreen = False
    while (passFirstScreen == False):
        try:
            secondScreen(driver)
            passFirstScreen = True
        except NoSuchElementException:
            driver.get(URL)
            firstScreen(driver, passenger)
            
    # now third screen
    thirdScreen(driver, passenger)
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
