from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from parse import parsePageSource
import time
import config

ORIGIN = "ORD"
DEST = [
  "hnl", "slc", "dfw", "lax", "sea", "atl",
  "mia", "mco", "sfo", "jfk", "ewr", "lga", "dca", "iad"
]
DEP_DATE = "03/01/23"
RET_DATE = "03/10/23"

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

for DEST in DEST:

    elem = driver.find_element(
      By.ID, "bookFlightOriginInput")
    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(ORIGIN)
    elem.send_keys(Keys.TAB)

    elem = driver.find_element(By.ID, "bookFlightDestinationInput")
    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(DEST)
    elem.send_keys(Keys.TAB)

    elemList = driver.find_elements(
      By.XPATH, '//div[@class="DateInput DateInput_1"]/input')

    elem = elemList[0]
    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(DEP_DATE)

    elem = elemList[1]
    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(RET_DATE)

    elem = driver.find_element(
      By.XPATH, '//*[@id="bookFlightForm"]/div[1]/div[1]/label')
    elem.click()

    elem = driver.find_element(
      By.CSS_SELECTOR,
      "button."
      "app-components-BookFlightForm-bookFlightForm__findFlightBtn--1lbFe")
    elem.submit()

    time.sleep(15)

    # scrape fare data
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    flight_elements = parsePageSource(soup)

    # write to file
    print(DEST + " ********************************************************\n")
    for i in range(len(flight_elements)):
        for j in range(len(flight_elements[i])):
            print(*flight_elements[i][j])
        print()

    # return to home page
    elem = driver.find_element(By.ID, "unitedLogo")
    elem.click()

    time.sleep(10)

driver.close()
