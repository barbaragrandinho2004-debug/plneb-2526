from selenium import webdriver
import time
from selenium.webdriver.common.by import By

#começar sessão
driver = webdriver.Chrome()

#navegar para a pagina
driver.get("http://www.saucedemo.com/")
time.sleep(3)

#procurar elementos para interagir
username = driver.find_element(By.ID, "user-name")
password = driver.find_element(By.NAME, "password")
login_button = driver.find_element(By.ID, "login-button")

#interagir com os elementos
username.send_keys("standard_user")
password.send_keys("secret_sauce")
login_button.click()

time.sleep(3)

produtos = driver.find_element(By.CLASS_NAME, "inventory_list")
print(produtos.text)
#desalocar a memoria
driver.quit()