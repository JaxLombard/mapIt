#! python3
# mapit.py
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import webbrowser, sys, pyperclip
from selenium.webdriver.common.keys import Keys
from flask import Flask, render_template
from flask import url_for
import time
from dotenv import load_dotenv
from pathlib import Path
import os
address = (input("What is your desired address?"))
#import modules
def init():
    global driver
    global options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver.Chrome(chrome_options=options)
    
    

init()

def dotenv():
    global api_key
    path = (r'C:\Users\Jax Lombard\Desktop\Code\Python\Web\MapIt\keys.env')
    load_dotenv(dotenv_path=path, verbose=True)
    api_key = os.getenv('api_key')

dotenv()




def searchData():
    #search google for a zipcode of the address
    global zipCode
    driver.get('https://www.unitedstateszipcodes.org/')
    search_box = driver.find_element_by_css_selector('#q')
    search_box.send_keys(address)
    driver.find_element_by_css_selector('#search-forms > div.col-xs-12.col-lg-7 > div > span.input-group-btn > button > i').click()
    time.sleep(2)
    for char in driver.find_elements_by_xpath('//*[@id="map-info"]/table/tbody/tr[4]/td'):
        zipCode = ((char.text)[:5])
    print("The zipcode is " + zipCode)

    #search google for climate of the zipcode
    global climate
    driver.get('https://weatherstreet.com/weather-forecast/weather_lookup.htm')
    search_box = driver.find_element_by_css_selector('body > table:nth-child(5) > tbody > tr:nth-child(3) > td > form > input[type=text]:nth-child(1)')
    search_box.send_keys(zipCode)
    driver.find_element_by_css_selector('body > table:nth-child(5) > tbody > tr:nth-child(3) > td > form > input[type=submit]:nth-child(2)').click()
    time.sleep(2)
    for char in driver.find_elements_by_xpath('/html/body/table/tbody/tr/td/table[6]/tbody/tr/td[1]/table[1]/tbody/tr[4]/td/font[2]'):
        climate = (str(char.text))
        print("The climate is " + climate)
        driver.quit()


        

searchData()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", zipCode=zipCode, climate=climate)

if __name__ == "__main__":
    app.run()
