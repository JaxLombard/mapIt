#! python3
#mapit.py launches a google map in the browser using an address from the command line or clipboard
import googlemaps
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser, sys, pyperclip
from selenium.webdriver.common.keys import Keys
from flask import Flask, render_template

#import modules

def init():
    global driver
    global options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(chrome_options=options)
    

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

def searchData():
    #search google for a zipcode of the address
    global zipCode
    driver.get('https://www.unitedstateszipcodes.org/')
    search_box = driver.find_element_by_css_selector('#q')
    search_box.send_keys(address)
    driver.find_element_by_css_selector('#search-forms > div.col-xs-12.col-lg-7 > div > span.input-group-btn > button > i').click()
    for char in driver.find_elements_by_xpath('//*[@id="map-info"]/table/tbody/tr[4]/td'):
        zipCode = ((char.text)[:5])
    print("The zipcode is " + zipCode)

    #search google for climate of the zipcode
    global climate
    driver.get('https://weatherstreet.com/weather-forecast/weather_lookup.htm')
    search_box = driver.find_element_by_css_selector('body > table:nth-child(5) > tbody > tr:nth-child(3) > td > form > input[type=text]:nth-child(1)')
    search_box.send_keys(zipCode)
    driver.find_element_by_css_selector('body > table:nth-child(5) > tbody > tr:nth-child(3) > td > form > input[type=submit]:nth-child(2)').click()
    for char in driver.find_elements_by_xpath('/html/body/table/tbody/tr/td/table[6]/tbody/tr/td[1]/table[1]/tbody/tr[4]/td/font[2]'):
        climate = (str(char.text))
        print("The climate is " + climate)
    #grab an embeded map of the address
    driver.get('https://www.maps.ie/create-google-map/')
    search_box = driver.find_element_by_css_selector('#address')
    search_box.send_keys(address + Keys.RETURN)
    for char in driver.find_element_by_css_selector('#code > textarea'):
        global iframe
        iframe = (str(char.text))
        

        

searchData()

webbrowser.open('https://www.google.com/maps/place/' + address + ' ' + zipCode)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", zipCode=zipCode, climate=climate, iframe=iframe)

if __name__ == "__main__":
    app.run()
