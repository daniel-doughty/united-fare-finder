from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from parse import parsePageSource
import time
import config

mileage_plus_number = config.mileage_plus_number
password = config.password
cookies = config.cookies

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://www.united.com")

driver.delete_all_cookies()
for cookie in cookies:
    driver.add_cookie(cookie)

assert "United Airlines" in driver.title

elem = driver.find_element(By.ID, "loginButton")
elem.click()

elem = driver.find_element(By.NAME, "loginFormPage.mpInput")
elem.clear()
elem.send_keys(mileage_plus_number)

elem = driver.find_element(By.NAME, "loginFormPage.password")
elem.clear()
elem.send_keys(password)
elem.send_keys(Keys.RETURN)

elem = driver.find_element(By.ID, "closeBtn")
elem.click()

origin = "ORD"
dest = [
  "hnl", "slc", "dfw", "lax", "sea", "atl",
  "mia", "mco", "sfo", "jfk", "ewr", "lga", "dca", "iad"
]
depDate = "03/01/2023"
retDate = "03/10/2023"

count = 0
for dest in dest:

    # input flight info in main page
    if (count == 0):
        elem = driver.find_element(By.ID, "bookFlightOriginInput")
        elem.clear()
        elem.send_keys(origin)

        elem = driver.find_element(By.ID, "bookFlightDestinationInput")
        elem.clear()
        elem.send_keys(dest)

        elem = driver.find_element(By.ID, "DepartDate")
        elem.clear()
        elem.send_keys(depDate)

        elem = driver.find_element(By.ID, "ReturnDate")
        elem.clear()
        elem.send_keys(retDate)

        elem = driver.find_element(
          By.XPATH, '//*[@id="bookFlightForm"]/div[1]/div[1]/label')
        elem.click()

        elem = driver.find_element(
          By.CSS_SELECTOR,
          "button."
          "app-components-BookFlightForm-bookFlightForm__findFlightBtn--1lbFe")
        elem.submit()

    # input flight info in subsequent pages
    else:
        elem = driver.find_element(
          By.ID, "airport-autocomplete-.swap0.fromTrip")
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(origin)

        elem = driver.find_element(
          By.XPATH,
          '//li[@id="airport-autocomplete-.swap0.fromTrip-menu-item-0"]//div')
        elem.click()

        elem = driver.find_element(By.ID, "airport-autocomplete-.swap0.toTrip")
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(dest)

        elem = driver.find_element(
          By.XPATH,
          '//li[@id="airport-autocomplete-.swap0.toTrip-menu-item-0"]//div')
        elem.click()

        elemList = driver.find_elements(
          By.XPATH, '//div[@class="DateInput DateInput_1"]/input')

        elem = elemList[0]
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(depDate)

        elem = elemList[1]
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(retDate)

        elem = driver.find_element(
          By.CSS_SELECTOR,
          ".atm-c-btn.atm-c-btn--secondary")
        elem.click()

    time.sleep(15)

    # scrape fare data
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    flight_elements = parsePageSource(soup)

    # write to file
    print(dest + " ********************************************************\n")
    for i in range(len(flight_elements)):
        for j in range(len(flight_elements[i])):
            print(*flight_elements[i][j])
        print()

    count = 1

driver.close()
