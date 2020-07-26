#! python3
#mapit.py launches a google map in the browser using an address from the command line or clipboard
import googlemaps
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser, sys, pyperclip

#import modules

def init():
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(5)
    driver.get('https://www.unitedstateszipcodes.org/')

init()

def mapIt():
    global address
    if len(sys.argv) > 1:
        #grab address from cmd line
        address = ' '.join(sys.argv[1:])
    else:
        #get address from clipboard
        address = pyperclip.paste()

mapIt()

def searchZip():
    global zipCode
    search_box = driver.find_element_by_css_selector('#q')
    search_box.send_keys(address)
    driver.find_element_by_css_selector('#search-forms > div.col-xs-12.col-lg-7 > div > span.input-group-btn > button > i').click()
    for char in driver.find_elements_by_xpath('//*[@id="map-info"]/table/tbody/tr[4]/td'):
        zipCode = ((char.text)[:5])
    print("The zipcode is " + zipCode)
    driver.implicitly_wait(5)
    driver.quit()

searchZip()


webbrowser.open('https://www.google.com/maps/place/' + address + zipCode)

def climateSearch():
    global climate
    search_box = driver.find_element_by_css_selector('#inputstring')
    search_box.send_keys(zipCode)
    driver.find_element_by_css_selector('#btnSearch').click()
    for char in driver.find_element_by_xpath('//*[@id="current_conditions-summary"]/p[2]'):
        climate = (char.text)
        print("The climate is " + climate)
    driver.implicitly_wait(5)
    driver.quit()

climateSearch()