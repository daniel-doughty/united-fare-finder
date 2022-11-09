from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

mileage_plus_number = ""
password = ""

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://www.united.com")

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

time.sleep(60)
# answer security questions here 

cookies = driver.get_cookies()

print cookies

driver.close()
