from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from dotenv import load_dotenv
import os
import time 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def get_token():
    load_dotenv()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Remote("http://chrome:4444/wd/hub", DesiredCapabilities.CHROME, options=chrome_options)
    # driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://developer.spotify.com/console/get-several-shows/")
    print("Headless Firefox Initialized")
    driver.find_elements_by_xpath("//*[contains(text(), 'Get Token')]")[0].click()
    button = driver.find_elements_by_xpath("//input[@id='scope-user-read-recently-played']/following-sibling::span")[0]
    time.sleep(1)
    ActionChains(driver).move_to_element(button).click(button).perform()

    button = driver.find_element_by_id('oauthRequestToken').click()
    time.sleep(2)

    button = driver.find_element_by_id('login-username')
    button.send_keys(os.environ['SPOTIFY_USER'])
    button = driver.find_element_by_id('login-password')
    button.send_keys(os.environ['SPOTIFY_PWD'])
    button = driver.find_element_by_id('login-button').click() 
    time.sleep(1)
    button = driver.find_element_by_id('oauth-input')
    token = button.get_attribute("value")
    driver.quit()
    return token