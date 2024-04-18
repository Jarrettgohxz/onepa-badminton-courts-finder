import requests
import time
import sys
import json
import re
import os
import shlex
import subprocess
import webbrowser


class OnePACourtListings():
    date = ''
    time = ''

    start_url = 'https://www.onepa.gov.sg/'

    get_catalog_outlets_url = 'https://www.onepa.gov.sg/pacesapi/catalogs/outlets'

    get_badminton_court_outlets_url = 'https://www.onepa.gov.sg/pacesapi/facilitysearch/searchjson?facility=BADMINTON%20COURTS&outlet=&date={date}&time={time}&page={page}&division='

    get_timeslots_url = 'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility={outlet_id}_badmintoncourts&selectedDate={date}&time=all'

    def __init__(self):
        self.s = requests.session()
        # self.cookiejar = CookieJar()

        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Host": "www.onepa.gov.sg",
            # "Referer": "https://www.onepa.gov.sg/facilities"
        })

    def append_venues_data_json(self, new_outlet: dict = None, new_total_outlets_count_value: int = None):
        #
        # To update `venues_data.json` file
        #

        # SCHEMA:
        # {
        #     "outlets": [],
        #     "total_outlets_count": 0
        # }

        filename = 'venues_data.json'

        with open(filename, 'r') as v:
            data = json.load(v)

            if new_outlet is not None:
                data['outlets'].append(new_outlet)

            if new_total_outlets_count_value is not None:
                data['total_outlets_count'] = new_total_outlets_count_value

        with open(filename, 'w') as v:
            json.dump(data, v)

    def setup_venues_data_json(self, update=False):
        #
        # To update `venues_data.json` file
        #

        if update:

            n = 1

            catalog_outlets = self.get_catalog_outlets()

            while True:

                url = self.get_badminton_court_outlets_url.format(
                    date=self.date, time=self.time, page=n)

                r = self.s.get(url,
                               headers={
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

                time.sleep(2)

        else:
            # to check if there are any new facilities added
            return

    def get_catalog_outlets(self):
        #
        # To retrieve lat, lng information for each facility outlet
        #

        r = self.s.get(self.get_catalog_outlets_url,
                       headers={
                           #    'Cookie': cookie_str,
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
        #
        # Main function to retrieve badminton courts availability
        #

        sleep_timing = 3

        try:

            # to update the cookies in the requests cookies session
            facilities_page_url = f'{self.start_url}/facilities'
            self.s.get(facilities_page_url)

            # original value for "total_outlets_count": 85; as returned from API - some removed due to duplicates
            with open('venues_data.json', 'r') as v:
                data = json.load(v)
                outlets = data['outlets']

            available_courts = []

            for outlet in outlets:
                try:

                    courts_count = outlet['courts_count']

                    label = outlet['label']

                    print('-----------------------------------')
                    print(f'Querying courts at {label}...')

                    if int(courts_count) == 0:
                        print(
                            'Facility currently not available for booking, skipping...')

                        continue

                    outlet_id = outlet['id']

                    url = self.get_timeslots_url.format(
                        outlet_id=outlet_id, date=self.date)

                    r = self.s.get(url,
                                   headers={
                                       'Accept': 'application/json, text/plain, */*',
                                       'Content-Type': 'application/json;charset=utf-8',
                                       'Referer':  'https://www.onepa.gov.sg/facilities/availability?facilityId={outlet_id}_BADMINTONCOURTS&date={self.date}&time=all'

                                   }
                                   )

                    data = json.loads(r.text)
                    response_code = int(data['responseStatusCode'])

                    resource_list = data['response']['resourceList']

                    if resource_list is None or len(resource_list) == 0 or response_code != 200:
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

                            if match is not None:
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

            courts_json_filename = f'courts_{self.date}.json'.replace('/', '_')

            open(courts_json_filename, 'x')

            with open(courts_json_filename, 'w') as courts:
                data = {
                    "date": self.date,
                    "available_courts": available_courts
                }

                print('\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
                print(
                    f'* Writing data to {courts_json_filename}...')

                json.dump(data, courts)

        except KeyboardInterrupt:
            print('\n\n-----------------------------------')
            print('Exiting script...')
            print('courts.json have not been updated.')
            print('-----------------------------------')
            sys.exit()

        except Exception as e:
            print(e)
            sys.exit()

        try:

            map_path = f'file:\\\\{os.getcwd()}\\map\\map.html'
            command = f'flask --app "map/server:create_server(\'{self.date}\')" --debug run'

            print(
                f'* Starting a local HTTP server to retrieve the map data:\n')
            print(f'$ {command}')
            print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++\n')

            args = shlex.split(command)

            proc = subprocess.Popen(args)

            webbrowser.open(
                map_path, new=0, autoraise=True)

            #
            # Waits for flask server to terminate, rather than closing automatically when this script ends
            #
            proc.wait()

        except KeyboardInterrupt:
            print('\n\n-----------------------------------\n')
            print('Exiting script...\n')
            print('-----------------------------------\n')
            sys.exit()


if __name__ == '__main__':

    # print('\n==============================================================================')
    # print('\nNOTE: This script should always be executed from the court_availability folder\n (Eg. on Windows: C:/Users/.../onepa-badminton-courts-finder/court_availability)\n')
    # print('==============================================================================\n')

    onepa_court_listings = OnePACourtListings()

    with open('config.json', 'r') as config:
        data = json.load(config)

        if data['update_venues_data_json']:
            onepa_court_listings.setup_venues_data_json(update=True)

        date_config = data['date']

        try:
            if bool(date_config):
                date_regex = r'\d{2}\/\d{2}\/\d{4}'
                match = re.match(date_regex, date_config)

                if match is None:
                    sys.exit(1)

                onepa_court_listings.date = data['date']

            else:
                sys.exit(1)

        except SystemExit:
            print('\n***********************************************************\n')
            print(
                'Please input a valid date in DD/MM/YYYY format in the config.json file.')
            print('\n***********************************************************\n')

            sys.exit()

    onepa_court_listings.get_timeslots()
