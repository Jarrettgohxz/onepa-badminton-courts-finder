import requests
import urllib.parse
import json
import re


class OnePA():
    # get_courts_availability_url = "https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=canberracc_BADMINTONCOURTS&selectedDate=20/10/2023"

    #   "https://www.onepa.gov.sg/facilities/availability?facilityId=siglapcc_BADMINTONCOURTS&date=18/11/2023&time=all",

    def __init__(self):
        self.s = requests.session()

        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Host": "www.onepa.gov.sg",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Referer": "https://www.onepa.gov.sg/facilities"
        })

    def set_cookies(self):
        self.s.get("https://www.onepa.gov.sg")

    def get_venues_list(self):
        # 1 to 10
        page = 1

        # r = self.s.get(
        #     f'https://www.onepa.gov.sg/pacesapi/facilitysearch/searchjson?facility=BADMINTON%20COURTS&outlet=&date=&time=&page={page}&division=')

        r = self.s.get(
            'https://www.onepa.gov.sg/pacesapi/catalogs/outlets',
            # 'https://www.onepa.gov.sg/pacesapi/FacilitySearch/GetFacilityOutlets',
            headers={
                'Content-Type': 'application/json;charset=utf-8',
                "Accept": "application/json, text/plain, */*",

                # else won't work - empty response
                'Referer': 'https://www.onepa.gov.sg/facilities/search?facility=BADMINTON%20COURTS'
            })

        # outlets = json.loads(r.text)['data']['data']['outlets']

        # index = 0

        # for outlet in outlets:
        #     for i in outlet['ccList']:
        #         label = i['label']

        #         if 'rc' in label.lower() or 'rn' in label.lower():
        #             continue

        #         print(i['label'])

        #         index += 1
        #         print(index)

        outlets = json.loads(r.text)['data']['outlets']

        index = 0

        for outlet in outlets:
            title = outlet['title']

            if outlet['type'] != 'CC':
                continue

            if re.search('cc$', title.lower(), re.IGNORECASE) == None:
                continue

            if 'defunct' in title.lower():
                continue

            print(outlet['title'])
            index += 1
            print(index)

        with open('venues2.json', 'w', encoding='utf-8') as v:
            v.write(r.text)

    def get_courts_availability(self):

        facility = urllib.parse.quote('BADMINTON COURTS')
        date = '23/11/2023'
        outlet = urllib.parse.quote(
            'CANBERRA CC,YEW TEE CC,YUHUA CC, BIDADARI CC, ZHENGHUA CC')

        get_courts_list_api = f'https://www.onepa.gov.sg/pacesapi/facilitysearch/searchjson?facility={
            facility}&outlet={outlet}&date={date}&time=all&page=1&division='

        res = self.s.get(
            get_courts_list_api,
            headers={
                "Accept": "application/json, text/plain, */*",
                # "Referer": "https://www.onepa.gov.sg/facilities",
            }
        )

        with open("data.json", "w", encoding="utf-8") as test:
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
    onepa = OnePA()

    # onepa.set_cookies()
    # onepa.test_algo()
    onepa.get_venues_list()
    # onepa.get_courts_availability()
