import sys
import requests
import urllib.parse
import json
import re
import time
import os
import random
import string


# from utils import cookies as cookies_util, webkitformboundary as webkitformboundary_util


from http.cookiejar import CookieJar, Cookie


from dotenv import load_dotenv

from requests_toolbelt import MultipartEncoder


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# issues
# 1. __RequestVerificationToken cookie from selenium not merging properly with those from requests.sessions(); domain not specified correctly - cookies issue
# 2. webkitformboundary data malformed

class OnePA():
    # get_courts_availability_url = "https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=canberracc_BADMINTONCOURTS&selectedDate=20/11/2023"

    #   "https://www.onepa.gov.sg/facilities/availability?facilityId=siglapcc_BADMINTONCOURTS&date=18/11/2023&time=all",

    main_url = 'https://www.onepa.gov.sg/'
    get_facility_info_url = 'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=TeckGheeCC_BADMINTONCOURTS&selectedDate=12/12/2023'

    cart_token_url = 'https://www.onepa.gov.sg/pacesapi/carts/token'
    quick_book_facility_url = 'https://www.onepa.gov.sg/pacesapi/carts/QuickBookFacility'

    cart_summary_url = 'https://www.onepa.gov.sg/cart/summary'

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

    def get_cookie_str(self):
        cookiejar = self.cookiejar

        cookie_str = ''

        for index, c in enumerate(cookiejar):
            cookie_dict = c.__dict__
            cookie_str += f'{cookie_dict['name']}={cookie_dict['value']}' if index == 0 else f';{
                cookie_dict['name']}={cookie_dict['value']}'

        # print(cookie_str)

        return cookie_str

    def set_cookiejar(self):

        try:
            for c in self.chrome_webdriver.get_cookies():
                cookie = Cookie(
                    version=0,
                    name=c['name'],
                    value=c['value'],
                    port=None,
                    port_specified=False,
                    domain=c['domain'],
                    domain_specified=True,
                    domain_initial_dot=False,
                    path=c['path'] if 'path' in c else None,
                    path_specified=True,
                    secure=c['secure'] if 'secure' in c else None,
                    expires=c['expiry'] if 'expiry' in c else None,
                    discard=False,
                    comment=None,
                    comment_url=None,
                    rest=None,
                    rfc2109=False
                )

                self.cookiejar.set_cookie(cookie=cookie)

            # artificially sleep for few seconds to prevent driver.quit() from being invoked too early
            time.sleep(2)

        except Exception as e:
            # TO HANDLE SPECIFIC ERRORS
            print(e)

        finally:
            self.chrome_webdriver.quit()

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

            WebDriverWait(self.chrome_webdriver, 30).until(
                EC.url_contains('https://www.onepa.gov.sg'))

            time.sleep(6)

            # current_cookiejar = self.cookiejar
            # cookies = self.chrome_webdriver.get_cookies()

            # cookies_util.update_cookiejar(
            #     current_cookiejar=current_cookiejar, cookies=cookies)

            # for c in cookies:

            #     cookie = Cookie(
            #         version=0,
            #         name=c['name'],
            #         value=c['value'],
            #         port='443',
            #         port_specified=False,
            #         domain=c['domain'],
            #         domain_specified=True,
            #         domain_initial_dot=False,
            #         path=c['path'] if 'path' in c else None,
            #         path_specified=True,
            #         secure=c['secure'] if 'secure' in c else None,
            #         expires=c['expiry'] if 'expiry' in c else None,
            #         discard=False,
            #         comment=None,
            #         comment_url=None,
            #         rest=None,
            #         rfc2109=False
            #     )
            #     self.s.cookies.update(cookie)
            #     print(c)
            #     print('\n')

        # except TimeoutException:
        #     # input#SpTwoFaSms-otp-fiel not found - no OTP required
        #     return

        except TimeoutException:
            print('timeout')

        except Exception as e:
            print(e)

        # finally:
        #     self.chrome_webdriver.quit()

    def get_cart_token(self):
        time.sleep(6)
        # self.s.cookies.update(self.cookiejar)

        for c in self.cookiejar:
            self.s.cookies.set_cookie(c)

        # self.s.get(
        #     'https://www.onepa.gov.sg/facilities/availability?facilityId=BishanCC_BADMINTONCOURTS&date=18/12/2023&time=all')

        # requests_cookiejar = cookies_util.get_requests_cookiejar(
        #     self.cookiejar)

        # self.s.cookies.update(requests_cookiejar)

        # print(requests_cookiejar)

        print('--------------------------')

        print('before cart token')
        for c in self.s.cookies:
            print(c)
        print('\n')

        r = self.s.get(self.cart_token_url,
                       #    cookies=requests_cookiejar,
                       headers={
                           #    'Cookie': cookie_str,
                           'Accept': 'application/json, text/plain, */*',
                           #    'Referer': ''
                       }
                       )

        cart_token = r.text
        self.cart_token = cart_token

        # cookie_dict = self.s.cookies.get_dict(domain='www.onepa.gov.sg')
        # cookies = [{'name': name, 'value': value, 'domain': 'www.onepa.gov.sg'}
        #            for (name, value) in cookie_dict.items()]

        # print(cookie_dict)
        # print(cookies)

        # cookies_util.update_cookiejar(
        #     current_cookiejar=self.cookiejar, cookies=cookies)

        print('\n')
        print('****')
        print('after cart token')
        for c in self.s.cookies:
            print(c)
        # print(self.s.cookies)
        # print('\n')
        # print(r.headers)
        print('****')

    def get_facility_id(self):

        r = self.s.get(
            'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=BishanCC_BADMINTONCOURTS&selectedDate=16/12/2023')

        print(r.text)

    def quick_book_facility(self):
        time.sleep(6)

        request_verification_token = self.cart_token
        data = {
            "cartId": "",
            "userId": "",
            "facilities": [{"facilityId": "cb0a179e-d355-e911-8120-00155d004f03",
                            "date": "18/12/2023",
                            "slot": "06:00 PM - 07:00 PM",
                            "slotId": "64800"}],
            "isSomeoneElse": False
        }

        fields = {
            'data':  str(data),
            '__RequestVerificationToken': request_verification_token
        }

        boundary = '----WebKitFormBoundary' \
            + ''.join(random.sample(string.ascii_letters + string.digits, 16))

        m = MultipartEncoder(fields=fields, boundary=boundary)

        print(str(m.to_string()))

        # webkitformboundary = webkitformboundary_util.generate_webkitformboundary([

        #     {
        #         'data': data
        #     },
        #     {
        #         '__RequestVerificationToken': request_verification_token
        #     }

        # ])

        # data = webkitformboundary['data']
        # content_type = webkitformboundary['content_type']

        # print(len(data))
        # print(content_type)
        # print(data)

        # print('\n')
        # print('-------------------------')

        # sp = cookie_str.split(';')
        # for s in sp:
        #     print(s)

        # print('\n')
        # print('****')
        # print('requests cookie jar')

        # requests_cookiejar = cookies_util.get_requests_cookiejar(
        #     self.cookiejar)
        # print(requests_cookiejar)

        r = self.s.post(self.quick_book_facility_url,
                        # cookies=requests_cookiejar,
                        headers={
                            # 'Cookie': cookie_str,
                            'Host': 'www.onepa.gov.sg',
                            'Origin': 'https://www.onepa.gov.sg',
                            'Referer': 'https://www.onepa.gov.sg/facilities/availability?facilityId=BishanCC_BADMINTONCOURTS&date=18/12/2023&time=all',
                            'Accept': 'application/json, text/plain, */*',
                            'Content-Length': str(m.len),
                            'Content-Type': m.content_type,
                        },
                        data=str(m.to_string())
                        )

        print('\n')
        print('-------------------------')

        print(r.text)

        # print(r.request.headers['Cookie'])

        for c in self.s.cookies:
            print(c)

        print(r.request.headers)

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

    onepa.launch_browser()
    onepa.auth_login()
    onepa.set_cookiejar()

    onepa.get_cart_token()
    # onepa.get_facility_id()

    onepa.quick_book_facility()

    # onepa.test_algo()
    # onepa.get_venues_list()
    # onepa.get_courts_availability()
