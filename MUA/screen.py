from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from time import sleep
import sqlite3
import os

# def waitInfinite(callback, debug = False):
#     sleep(0.5)
#     yet = True
#     while yet:
#         try:
#             callback()
#             yet = False
#         except NoSuchElementException as e:
#             print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
#             sleep(0.5)
#             pass
#         except JavascriptException as e:
#             print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
#             sleep(0.5)
#             pass
#         except StaleElementReferenceException as e:
#             print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
#             sleep(0.5)
#             pass
#         except ElementClickInterceptedException as e:
#             print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
#             sleep(0.5)
#             pass
#         except ElementNotInteractableException as e:
#             print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
#             sleep(0.5)
#             pass
#         except Exception as e:
#             print("{} on line {}".format(str(e).split('\n')[0], sys.exc_info()[-1].tb_lineno))
#             # sleep(0.5)
#             # pass
#             driver.quit()
#             exit()

def getScreen(driver, email, pwd, index, flag):
    driver.get("https://www.upwork.com/ab/proposals/")
    # if flag:
    #     sleep(1)
    #     driver.switch_to.window(driver.window_handles[0])
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

    sleep(8)
    # waitInfinite(lambda: driver.find_element(By.ID, "onetrust-close-btn-container").click())
    
    driver.save_screenshot('static/' + "{:02d}".format(index) + email + '.png')
    driver.execute_script('document.querySelector(".link-logout.nav-menu-item").click()')

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
# options.add_extension(os.path.join(os.getcwd(), 'extensions', 'gighmmpiobklfepjocnamgkkbiglidom-5.6.0-Crx4Chrome.com.crx'))
options.add_argument('load-extension=' + os.path.join(os.getcwd(), 'extensions', 'XBlocker 1.0.4 - langpack'))

i = 0
driver = False

while 1:
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute('SELECT email from accounts WHERE status="sent"')
    emails = cur.fetchall()
    emails = [email[0] for email in emails]
    emails = emails[::-1]
    conn.commit()
    conn.close()

    for index, email in enumerate(emails):
        print(email)
        try:
            if email.count("@") > 0:
                if i % 5 == 0:
                    i = 0
                    if driver: driver.quit()
                    driver = webdriver.Chrome(options=options)
                email = email.split(".org")[0]
                if i == 0:
                    getScreen(driver, email + ".org", "P@ssw0rd123123", index, True)
                else:
                    getScreen(driver, email + ".org", "P@ssw0rd123123", index, False)
                i += 1
        except Exception as e:
            print("error:", str(e))
            continue

    break
