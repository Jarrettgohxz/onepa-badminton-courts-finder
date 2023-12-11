import sys
import requests
import urllib.parse
import json
import re
import time
import os


from utils import cookies as cookies_util, webkitformboundary as webkitformboundary_utils


from http.cookiejar import CookieJar


from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class OnePA():
    # get_courts_availability_url = "https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=canberracc_BADMINTONCOURTS&selectedDate=20/11/2023"

    #   "https://www.onepa.gov.sg/facilities/availability?facilityId=siglapcc_BADMINTONCOURTS&date=18/11/2023&time=all",

    main_url = 'https://www.onepa.gov.sg/'
    cart_token_url = 'https://www.onepa.gov.sg/pacesapi/carts/token'
    quick_book_facility_url = 'https://www.onepa.gov.sg/pacesapi/carts/QuickBookFacility'
    get_facility_info_url = 'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=TeckGheeCC_BADMINTONCOURTS&selectedDate=12/12/2023'

    def __init__(self):
        self.chrome_webdriver = None
        self.s = requests.session()
        self.cookiejar = CookieJar()
        self.cart_token = None

        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Host": "www.onepa.gov.sg",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Referer": "https://www.onepa.gov.sg/facilities"
        })

    def set_cookies(self):

        self.s.get(self.main_url)

    def launch_browser(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        # options.add_argument("--headless=new")

        self.chrome_webdriver = webdriver.Chrome(options=options)

        self.chrome_webdriver.get(
            self.main_url)

    def auth_login(self):

        try:
            self.chrome_webdriver.execute_script(
                f"document.location.href = \"{f'{self.main_url}\\login'}\"")

            singpass_login_button = WebDriverWait(self.chrome_webdriver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#SpQrToggle-1FATab')))

            singpass_login_button.click()

            singpass_id = os.getenv('SINGPASS_ID')

            singpass_form = self.chrome_webdriver.find_element(
                By.CSS_SELECTOR, 'input#SpLoginIdPw-singpass-id')

            singpass_form.send_keys(singpass_id)

            singpass_password = os.getenv('SINGPASS_PASSWORD')

            singpass_form = self.chrome_webdriver.find_element(
                By.CSS_SELECTOR, 'input#SpLoginIdPw-password')

            singpass_form.send_keys(singpass_password)

            singpass_form.submit()

            # WebDriverWait(self.chrome_webdriver, 5).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'input#SpTwoFaSms-otp-field')))

            WebDriverWait(self.chrome_webdriver, 20).until(
                EC.url_contains('https://www.onepa.gov.sg'))

            current_cookiejar = self.cookiejar
            cookies = self.chrome_webdriver.get_cookies()

            cookies_util.update_cookiejar(
                current_cookiejar=current_cookiejar, cookies=cookies)

        # except TimeoutException:
        #     # input#SpTwoFaSms-otp-fiel not found - no OTP required
        #     return

        except TimeoutException:
            print('timeout')

        except Exception as e:
            print(e)

        finally:
            self.chrome_webdriver.quit()

    def get_cart_token(self):
        r = self.s.get(self.cart_token_url,
                       headers={
                           'Accept': 'application/json, text/plain, */*',
                           #    'Referer': ''
                       }
                       )

        cart_token = r.text
        self.cart_token = cart_token

    def get_facility_id(self):
        r = self.s.get(
            'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=BishanCC_BADMINTONCOURTS&selectedDate=16/12/2023')

        print(r.text)

    def quick_book_facility(self):
        request_verification_token = self.cart_token

        data = {
            "cartId": "",
            "userId": "",
            "facilities": [{"facilityId": "e18091ad-4968-e611-80d9-00155dad210b",  # found from api call
                            "date": "12/12/2023",
                            "slot": "03:30 PM - 04:30 PM",
                            "slotId": "45000"}],
            "isSomeoneElse": False
        }

        req_body = webkitformboundary_utils.generate_webkitformboundary([
            {
                '__RequestVerificationToken': request_verification_token
            },
            {
                'data': data
            }
        ])
        return

    def get_venues_list(self):
        # 1 to 10
        page = 1
        count = 0

        # while True:

        r = self.s.get(
            f'https://www.onepa.gov.sg/pacesapi/facilitysearch/searchjson?facility=BADMINTON%20COURTS&outlet=&date=&time=&page={page}&division=')

        with open('data.json', 'w') as w:
            w.write(r.text)

            # res_json = json.loads(r.text)
            # outlets = res_json['data']['results']

            # if len(outlets) == 0:
            #     break

            # page += 1

    def get_courts_availability(self):

        self.s.get(
            'https://www.onepa.gov.sg/facilities/search?facility=BADMINTON%20COURT')

        res = self.s.get(
            'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=canberracc_BADMINTONCOURTS&selectedDate=20/11/2023',
            headers={
                'Content-Type': 'application/json;charset=utf-8',
                "Accept": "application/json, text/plain, */*",
                'Referer': 'https://www.onepa.gov.sg/facilities/search?facility=BADMINTON%20COURTS'
            }
        )

        with open("courts.json", "w", encoding="utf-8") as test:
            test.write(res.text)

    def remove_first_few_elements(self, arr, chunk):
        values = arr[:chunk]
        del arr[:chunk]

        return values

    def test_algo(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        chunk = 5

        while len(arr) != 0 and (values := self.remove_first_few_elements(arr, chunk)):
            print(values)


if __name__ == "__main__":

    load_dotenv()

    onepa = OnePA()

    # onepa.set_cookies()

    # onepa.launch_browser()
    # cookies = onepa.auth_login()

    # onepa.get_cart_token()
    onepa.get_facility_id()

    # onepa.quick_book_facility()

    # onepa.test_algo()
    # onepa.get_venues_list()
    # onepa.get_courts_availability()
