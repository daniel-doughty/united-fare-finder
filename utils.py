from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# can use embed() to launch Ipython terminal for debugging
from IPython import embed
import re
from datetime import datetime

def login(mileage_plus_number, password, driver):
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

def get_price_elements(origin, destination, departure_date, driver):
  elem = driver.find_element(
      By.ID, "bookFlightOriginInput")
  # on macbook, ctrl+a doesn't work, so also adding clear()
  elem.clear()
  elem.send_keys(Keys.CONTROL + "a")
  elem.send_keys(Keys.COMMAND + "a")
  elem.send_keys(origin)
  elem.send_keys(Keys.TAB)

  elem = driver.find_element(By.ID, "bookFlightDestinationInput")
  elem.clear()
  elem.send_keys(Keys.CONTROL + "a")
  elem.send_keys(Keys.COMMAND + "a")
  elem.send_keys(destination)
  elem.send_keys(Keys.TAB)

  elemList = driver.find_elements(
      By.XPATH, '//div[@class="DateInput DateInput_1"]/input')

  elem = elemList[0]
  elem.clear()
  elem.send_keys(Keys.CONTROL + "a")
  elem.send_keys(Keys.COMMAND + "a")
  elem.send_keys(departure_date)

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
  return price_elements

def parse_price_elements(price_element):
  # parse rows and write to file
  s = price_element.text

  # parse date
  try:
    date = re.search("\, (.*?)starting", s).group(1)
    formatted_date = datetime.strptime(
        date, "%B %d, %Y").strftime("%m-%d-%Y")
  except:
    formatted_date = ""
  
  # parse miles
  try:
    miles = str(float(re.search("from(.*?)k", s).group(1)) * 1000)
  except:
    miles = ""
  
  # parse dollars
  try:
    dollars = re.search(
        "\$(.*?)$", s).group(1).replace("Lowestprice", "").replace("selected", "")
  except:
    dollars = ""
  return formatted_date, miles, dollars
