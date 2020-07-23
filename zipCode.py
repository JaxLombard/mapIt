import googlemaps
from datetime import datetime
from mapit import address
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(5)
driver.get('https://www.unitedstateszipcodes.org/')

def searchZip():
    global zipCode
    search_box = driver.find_element_by_css_selector('#q')
    search_box.send_keys(address)
    driver.find_element_by_css_selector('#search-forms > div.col-xs-12.col-lg-7 > div > span.input-group-btn > button > i').click()
    for char in driver.find_elements_by_xpath('//*[@id="map-info"]/table/tbody/tr[4]/td'):
        zipCode = ((char.text)[:5])
    print("The zipcode is " + zipCode)

searchZip()


driver.implicitly_wait(5)
driver.quit()