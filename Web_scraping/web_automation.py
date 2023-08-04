from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

driver.get("https://only-testing-blog.blogspot.com/2014/05/form.html?FirstName=&LastName=&EmailID=&MobNo=&Company=")
driver.implicitly_wait(8)

driver.find_element(By.CSS_SELECTOR, 'input[name="FirstName"]').send_keys("Anthony")
driver.find_element(By.CSS_SELECTOR, 'input[name="LastName"]').send_keys("Surya")
driver.find_element(By.CSS_SELECTOR, 'input[name="EmailID"]').send_keys("abc@gmail.com")
driver.find_element(By.CSS_SELECTOR, 'input[name="MobNo"]').send_keys("0812")
driver.find_element(By.CSS_SELECTOR, 'input[name="Company"]').send_keys("Astra")
driver.find_element(By.CSS_SELECTOR, 'input[value="Submit"]').click()