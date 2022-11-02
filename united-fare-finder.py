from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

mileage_plus_number = ""
password = ""
cookies = [{}]

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

elem = driver.find_element(By.ID, "bookFlightOriginInput")
elem.clear()
elem.send_keys("ORD")
elem.send_keys(Keys.TAB)

elem = driver.find_element(By.ID, "bookFlightDestinationInput")
elem.clear()
elem.send_keys("HNL")
elem.send_keys(Keys.TAB)

elem = driver.find_element(By.ID, "DepartDate")
elem.clear()
elem.send_keys("03/03/23")
elem.send_keys(Keys.TAB)


elem = driver.find_element(By.ID, "ReturnDate")
elem.clear()
elem.send_keys("03/10/23")
elem.send_keys(Keys.TAB)

elem = driver.find_element(By.XPATH, '//*[@id="bookFlightForm"]/div[1]/div[1]/label')
elem.click()

elem = driver.find_element(By.CSS_SELECTOR, "button.app-components-BookFlightForm-bookFlightForm__findFlightBtn--1lbFe")
elem.submit()

time.sleep(10)

driver.close()
