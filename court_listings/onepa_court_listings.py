import requests
import os
import time
import sys
import json
import re


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from http.cookiejar import CookieJar
from dotenv import load_dotenv


sys.path.append('../')
from utils import browser as browser_utils, cookies as cookies_utils, auth as auth_utils  # NOQA


class OnePACourtListings():

    date = '18/12/2023'
    time = ''

    start_url = 'https://www.onepa.gov.sg/'

    get_catalog_outlets_url = 'https://www.onepa.gov.sg/pacesapi/catalogs/outlets'

    get_badminton_court_outlets_url = 'https://www.onepa.gov.sg/pacesapi/facilitysearch/searchjson?facility=BADMINTON%20COURTS&outlet=&date={date}&time={time}&page={page}&division='

    get_timeslots_url = 'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility={outlet_id}_badmintoncourts&selectedDate={date}&time=all'

    def __init__(self):
        self.chrome_webdriver = None
        self.s = requests.session()
        self.cookiejar = CookieJar()

        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Host": "www.onepa.gov.sg",
            # "Referer": "https://www.onepa.gov.sg/facilities"
        })

    def append_venues_data_json(self, new_outlet: dict = None, new_total_outlets_count_value: int = None):

        # {
        #     "outlets": [],
        #     "total_outlets_count": 0
        # }

        with open('venues_data.json', 'r') as v:
            data = json.load(v)

            if new_outlet != None:
                data['outlets'].append(new_outlet)

            if new_total_outlets_count_value != None:
                data['total_outlets_count'] = new_total_outlets_count_value

        with open('venues_data.json', 'w') as v:
            json.dump(data, v)

    def auth_login(self):
        try:
            self.chrome_webdriver = browser_utils.launch_browser()
            self.chrome_webdriver.get(self.start_url)

            singpass_id = os.getenv('SINGPASS_ID')
            singpass_pwd = os.getenv('SINGPASS_PASSWORD')

            auth_utils.auth_login(chrome_webdriver=self.chrome_webdriver,
                                  singpass_id=singpass_id,
                                  singpass_pwd=singpass_pwd)

            WebDriverWait(self.chrome_webdriver, 30).until(
                EC.url_contains(self.start_url))

            time.sleep(6)

            cookies = self.chrome_webdriver.get_cookies()

            cookies_utils.update_cookiejar(
                current_cookiejar=self.cookiejar, cookies=cookies)

        except:
            print('error')

        finally:
            self.chrome_webdriver.quit()

    def setup_venues_data_json(self, update=False):

        if update:

            cookie_str = cookies_utils.get_cookie_str(cookiejar=self.cookiejar)

            n = 1

            while True:

                url = self.get_badminton_court_outlets_url.format(
                    date=self.date, time=self.time, page=n)

                r = self.s.get(url,
                               headers={
                                   'Cookie': cookie_str,
                                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                                   'Content-Type': 'application/json;charset=utf-8',
                                   'Host': 'www.onepa.gov.sg',
                                   'Referer': 'https://www.onepa.gov.sg',

                               })

                data = json.loads(r.text)
                data = dict(data)

                results = data['data']['results']
                results_len = len(results)

                if results_len == 0:
                    self.append_venues_data_json(
                        new_total_outlets_count_value=data['data']['totalResults'])
                    break

                for result in results:
                    outlet_id = result['outletId']
                    label = result['outlet']
                    courts_count = int(result['count'])

                    catalog_outlets = self.get_catalog_outlets()

                    lat = ''
                    lng = ''

                    for outlet in catalog_outlets:
                        if outlet['id'] == outlet_id:
                            lat = outlet['lat']
                            lng = outlet['lng']

                    print(f'Appending outlet: {label}, with id: {
                          outlet_id} into venues data .json file')

                    data = {
                        "id": outlet_id,
                        "courts_count": courts_count,
                        "label": label,
                        "lat": lat,
                        "lng": lng,
                    }

                    self.append_venues_data_json(new_outlet=data)

                n += 1

                time.sleep(10)

        else:
            # to check if there are any new facilities added
            return

    def get_catalog_outlets(self):

        cookie_str = cookies_utils.get_cookie_str(cookiejar=self.cookiejar)

        r = self.s.get(self.get_catalog_outlets_url,
                       headers={
                           'Cookie': cookie_str,
                           'Accept': 'application/json, text/plain, */*',
                           'Content-Type': 'application/json, text/plain, */*',
                           'Host': 'www.onepa.gov.sg',
                           'Referer': 'https://www.onepa.gov.sg',
                       })

        data = json.loads(r.text)
        data = dict(data)

        outlets = data['data']['outlets']
        return outlets

    def get_timeslots(self):

        # to experiment with proxy switching to reduce pause time - allow for faster requests iterations
        sleep_timing = 6

        proxies = {
            'https': 'http://brd-customer-hl_61469640-zone-isp:ovmuz8dv1i1r@brd.superproxy.io:22225'
        }

        try:
            facilities_page_url = f'{self.start_url}/facilities'
            self.s.get(facilities_page_url)

            # cookie_str = cookies_utils.get_cookie_str(cookiejar=self.cookiejar)

            with open('venues_data.json', 'r') as v:
                data = json.load(v)
                outlets = data['outlets']

            available_courts = []

            for outlet in outlets:
                try:

                    outlet_id = outlet['id']
                    label = outlet['label']

                    url = self.get_timeslots_url.format(
                        outlet_id=outlet_id, date=self.date)

                    print('-----------------------------------')
                    print(f'Querying courts at {label}...')

                    r = self.s.get(url,
                                   headers={
                                       # 'Cookie': cookie_str,
                                       'Accept': 'application/json, text/plain, */*',
                                       'Content-Type': 'application/json;charset=utf-8',
                                       'Host': 'www.onepa.gov.sg',
                                       'Referer':  'https://www.onepa.gov.sg/facilities/availability?facilityId={outlet_id}_BADMINTONCOURTS&date={self.date}&time=all'

                                   }
                                   # , proxies=proxies
                                   )

                    data = json.loads(r.text)
                    response_code = int(data['responseStatusCode'])

                    resource_list = data['response']['resourceList']

                    if resource_list == None or len(resource_list) == 0 or response_code != 200:
                        time.sleep(sleep_timing)
                        continue

                    resources = []

                    for resource in resource_list:

                        slots = []

                        for slot in resource['slotList']:
                            is_available = slot['isAvailable']

                            if is_available:
                                court_number = resource['resourceName']
                                time_range = slot['timeRangeName']
                                is_peak = slot['isPeak']

                                slots_data = {
                                    "time_range": time_range,
                                    "is_peak": is_peak
                                }

                                slots.append(slots_data)

                        if len(slots) > 1:

                            match = re.match(re.compile(
                                r'(?:\w*)(\d)', re.I), court_number.replace(' ', ''))

                            if match != None:
                                court_number = match.group(1)

                            resource_data = {
                                "court_number":  court_number,
                                "slots": slots
                            }

                            resources.append(resource_data)

                    if len(resources) > 1:
                        print(f'Court(s) found at {label}!')

                        id_resource_data = {
                            "id": outlet_id,
                            "resources": resources
                        }
                        available_courts.append(id_resource_data)

                    time.sleep(sleep_timing)

                except Exception as e:
                    time.sleep(sleep_timing)
                    print(f'Error with querying courts at {outlet_id}')
                    print(e)
                    print(r.status_code)
                    print(r.text)
                    continue

            if len(available_courts) == 0:
                return

            with open('courts.json', 'r') as courts:
                courts_data = json.load(courts)

            with open('courts.json', 'w') as courts:
                new_data = {
                    "date": self.date,
                    "available_courts": available_courts
                }

                courts_data['data'].append(new_data)

                print('\n\n++++++++++++++++++++++++++++++++\n')
                print('**** Writing data to courts.json... ****')
                print('\n++++++++++++++++++++++++++++++++\n\n')

                json.dump(courts_data, courts)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    # onepa_court_listings.auth_login()
    load_dotenv()

    onepa_court_listings = OnePACourtListings()

    with open('config.json', 'r') as config:
        data = json.load(config)

        if data['update_facilities_from_server']:
            onepa_court_listings.setup_venues_data_json(update=True)

    onepa_court_listings.get_timeslots()
