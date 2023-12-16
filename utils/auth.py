import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def auth_login(chrome_webdriver: webdriver.Chrome, singpass_id: str, singpass_pwd: str):

    try:
        # simulate href click - activesg site will redirect to another URL before navigating to the actual singpass auth page
        chrome_webdriver.execute_script(
            'document.location.href = \'https://www.onepa.gov.sg/login\'')

        singpass_login_button = WebDriverWait(chrome_webdriver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#SpQrToggle-1FATab')))

        singpass_login_button.click()

        singpass_form = chrome_webdriver.find_element(
            By.CSS_SELECTOR, 'input#SpLoginIdPw-singpass-id')

        singpass_form.send_keys(singpass_id)

        singpass_form = chrome_webdriver.find_element(
            By.CSS_SELECTOR, 'input#SpLoginIdPw-password')

        singpass_form.send_keys(singpass_pwd)

        singpass_form.submit()

    except NoSuchElementException as e:
        # handle pause and allow user to manually navigate
        print(e)
