from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import config
# can use embed() to launch Ipython terminal for debugging
from IPython import embed
import re
from datetime import datetime

HOME_PAGE_URL = "https://www.united.com"
ORIGIN = "ORD"
DEST = [
  "hnl", "slc", "dfw", "lax", "sea", "atl",
  "mia", "mco", "sfo", "jfk", "ewr", "lga", "dca", "iad"
]
DEP_DATE = "03/01/23"

mileage_plus_number = config.mileage_plus_number
password = config.password
cookies = config.cookies

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(HOME_PAGE_URL)

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

#write CSV headers to file
print("origin, destination, date, miles, dollars, error")

#iterate through each destination
for DEST in DEST:
  try:
    elem = driver.find_element(
      By.ID, "bookFlightOriginInput")
    # on macbook, ctrl+a doesn't work, so also adding clear()
    elem.clear()
    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(Keys.COMMAND + "a")
    elem.send_keys(ORIGIN)
    elem.send_keys(Keys.TAB)

    elem = driver.find_element(By.ID, "bookFlightDestinationInput")
    elem.clear()
    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(Keys.COMMAND + "a")
    elem.send_keys(DEST)
    elem.send_keys(Keys.TAB)

    elemList = driver.find_elements(
      By.XPATH, '//div[@class="DateInput DateInput_1"]/input')

    elem = elemList[0]
    elem.clear()
    elem.send_keys(Keys.CONTROL + "a")
    elem.send_keys(Keys.COMMAND + "a")
    elem.send_keys(DEP_DATE)

    # 'Book with miles' checkbox, can't click checkbox directly
    elem = driver.find_element(
      By.XPATH, '//*[@id="bookFlightForm"]/div[1]/div[1]/label')
    checkbox = driver.find_element(
      By.ID, 'award')
    # Dont click if checkbox is already checked
    if checkbox.is_selected() != True:
      elem.click()

    # 'One-way radio button'
    elem = driver.find_element(By.ID, 'oneway')
    elem.click()

    # 'Find flights' button
    elem = driver.find_element(
      By.CSS_SELECTOR,
      "button."
      "app-components-BookFlightForm-bookFlightForm__findFlightBtn--1lbFe")
    elem.submit()
    
    elem = driver.find_element(
      By.CSS_SELECTOR,
      "button."
      "app-components-Shopping-Calendar-styles__calendarIcon--2nO38")
    elem.click()

    # Waits for calendar to load on page
    elem = driver.find_element(
      By.CSS_SELECTOR,
      "div."
      "app-components-Shopping-FlexibleCalendar-styles__content--11v1q")

    # scrape fare data
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    price_elements = soup.find_all(
        "div",
        class_="app-components-Shopping-FlexibleCalendar-styles__content--11v1q")
   

    # parse rows and write to file
    for element in price_elements:
      s = element.text
      
      # parse date
      try:
        date = re.search("\, (.*?)starting",s).group(1)
        formatted_date = datetime.strptime(date, "%B %d, %Y").strftime("%m-%d-%Y")  
      except:
        date = ""

      # parse miles
      try:  
        miles = re.search("from(.*?)\+",s).group(1)
      except: 
        miles = ""

      # parse dollars
      try:  
        dollars = re.search("\+(.*?)$",s).group(1)
      except: 
        dollars = ""

      print(ORIGIN+",", DEST+",",formatted_date+",",miles+",",dollars)
  except Exception as e:
    print(ORIGIN+",", DEST+",",",",",",",",f'{type(e)}: {e.message}')
  finally:
    # return to home page
    driver.get(HOME_PAGE_URL)

driver.close()
