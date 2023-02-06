from selenium import webdriver
import config
# can use embed() to launch Ipython terminal for debugging
from IPython import embed
import utils

HOME_PAGE_URL = "https://www.united.com"
ORIGIN = "ORD"
DEST = [
  "hnl", "slc", "dfw", "lax", "sea", "atl",
  "mia", "mco", "sfo", "jfk", "ewr", "lga", "dca", "iad"
]
DEP_DATE = "03/15/23"

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

utils.login(mileage_plus_number, password, driver)

#write CSV headers to file
print("origin,destination,date,miles,dollars,error")

#iterate through each destination
for DEST in DEST:
  # get outbound flights
  try:
    price_elements = utils.get_price_elements(ORIGIN, DEST, DEP_DATE, driver)
    for price_element in price_elements:
      formatted_date, miles, dollars = utils.parse_price_elements(price_element)
      print(f'{ORIGIN},{DEST},{formatted_date},{miles},{dollars}')
  except Exception as e:
    print(f'{ORIGIN},{DEST},,,,{str(e)[:256]}...')  
  finally:
    # return to home page
    driver.get(HOME_PAGE_URL)
  
  # get return flights
  try:
    price_elements = utils.get_price_elements(DEST, ORIGIN, DEP_DATE, driver)
    for price_element in price_elements:
      formatted_date, miles, dollars = utils.parse_price_elements(price_element)
      print(f'{DEST},{ORIGIN},{formatted_date},{miles},{dollars}')
  except Exception as e:
    print(f'{DEST},{ORIGIN},,,,{str(e)[:256]}...')
  finally:
    # return to home page
    driver.get(HOME_PAGE_URL)

driver.close()
