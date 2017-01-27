import time # sleep
from selenium import webdriver # Browswer Automation

# Site Information
URL = 'https://www.southwest.com/flight/retrieveCheckinDoc.html?clk=GSUBNAV-CHCKIN&forceNewSession=yes'

# Login list (confirmationNumber, firstName, lastName)
# append as many users as desired
# Friday, January 27, Flight 4333 4:55PM
passengerList = []
passengerList.append(['BT6TU9', 'Ian', 'Cleary', 'email', '480', '555', '1234', 'iansemail@gmail.com'])
passengerList.append(['BGH4KT', 'Bob', 'Bobson', 'email', '317', '555', '2345', 'bobsemail@gmail.com'])

#Site specific xpaths
confirmationNumber_xpath = '//*[@id="confirmationNumber"]'
firstName_xpath = '//*[@id="firstName"]'
lastName_xpath = '//*[@id="lastName"]'
checkIn_xpath = '//*[@id="submitButton"]' #Check In button
checkIn_2nd_Screen_xpath = '//*[@id="printDocumentsButton"]'

checkIn_3rd_screen_print_radio_xpath = '//*[@id="optionPrint"]'

checkIn_3rd_screen_email_radio_xpath = '//*[@id="optionEmail"]'
checkIn_3rd_screen_email_textBox_xpath = '//*[@id="emailAddress"]'

checkIn_3rd_screen_text_radio_xpath = '//*[@id="optionText"]'
checkIn_3rd_screen_text_area_code_xpath = '//*[@id="phoneArea"]'
checkIn_3rd_screen_text_phone_prefix_xpath = '//*[@id="phonePrefix"]'
checkIn_3rd_screen_text_phone_number_xpath = '//*[@id="phoneNumber"]'

checkIn_3rd_screen_check_in_button_xpath = '//*[@id="checkin_button"]'


# functions to enter username, password, and click login
def text_autofill(driver, text_xpath, text):
    text_box = driver.find_element_by_xpath(text_xpath)
    text_box.send_keys(text)
def text_clear(driver, text_xpath):
    text_box = driver.find_element_by_xpath(text_xpath).clear()

def click(driver, webElement_xpath):    
    driver.find_element_by_xpath(webElement_xpath).click()

def login(passengerList):
    driver = webdriver.Chrome() # faster with one driver for entire list
    for passenger in passengerList:
        driver.get(URL)
        #time.sleep(1)
        text_autofill(driver, confirmationNumber_xpath, passenger[0])
        text_autofill(driver, firstName_xpath, passenger[1])
        text_autofill(driver, lastName_xpath, passenger[2])
        #time.sleep(1)
        click(driver, checkIn_xpath)
        time.sleep(1)
        click(driver, checkIn_2nd_Screen_xpath)
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
        driver.get(URL) # goes back to main screen to ensure that the next passenger works
    driver.quit()

# Main Code Block
login(passengerList)
