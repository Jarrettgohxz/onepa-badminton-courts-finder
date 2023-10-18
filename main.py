import requests


class OnePA():
    get_courts_availability_url = "https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=canberracc_BADMINTONCOURTS&selectedDate=20/10/2023"

    def __init__(self):
        self.s = requests.session()

        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            # "Host": "www.onepa.gov.sg",
            # "Accept": "application/json, text/plain, */*",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Referer": "https://www.onepa.gov.sg/facilities"
        })

    def set_cookies(self):
        self.s.get("https://www.onepa.gov.sg")

    def get_courts_availability(self):

        res = self.s.get(
            # self.get_courts_availability_url
            "https://www.onepa.gov.sg/facilities/availability?facilityId=siglapcc_BADMINTONCOURTS&date=19/10/2023&time=all", headers={
                "Referer": "https://www.onepa.gov.sg/facilities",
            }
        )
        print(res.request.headers)

        with open("data.html", "w", encoding="utf-8") as test:
            test.write(res.text)


if __name__ == "__main__":
    onepa = OnePA()

    onepa.set_cookies()
    onepa.get_courts_availability()
