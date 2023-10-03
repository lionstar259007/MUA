from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os

email = sys.argv[1]
pwd = 'P@ssw0rd123123'
url = sys.argv[2]

options = webdriver.ChromeOptions()
options.add_extension(os.path.join(os.getcwd(), 'extensions', 'gighmmpiobklfepjocnamgkkbiglidom-5.6.0-Crx4Chrome.com.crx'))
options.add_argument('load-extension=' + os.path.join(os.getcwd(), 'extensions', 'XBlocker 1.0.4 - langpack'))
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://www.upwork.com/ab/account-security/login")
driver.switch_to.window(driver.window_handles[0])

wait = WebDriverWait(driver, 10)

# Wait for email input field to appear and enter email
login_username = wait.until(EC.visibility_of_element_located((By.ID, "login_username")))
login_username.send_keys(email)

# Click on continue button
login_password_continue = wait.until(EC.element_to_be_clickable((By.ID, "login_password_continue")))
login_password_continue.click()

# Wait for password input field to appear and enter password
login_password = wait.until(EC.visibility_of_element_located((By.ID, "login_password")))
login_password.send_keys(pwd)

# Click on continue button
login_control_continue = wait.until(EC.element_to_be_clickable((By.ID, "login_control_continue")))
login_control_continue.click()

if url != 'https://www.upwork.com/ab/proposals/':
    sleep(5)
    driver.get(url)

while True:
    try:
        # Wait for user input
        user_input = input("Type 'quit' to close the browser")

        # If user enters 'quit', close the browser and break the loop
        if user_input.lower() == 'quit':
            driver.quit()
            break

    except NoSuchWindowException:
        # If the browser window is closed manually, exit the loop and quit the driver
        driver.quit()
        print("Browser window closed manually")
        break