import requests


proxies = {
    'https': 'http://brd-customer-hl_61469640-zone-proxy1:jrukkcrq92tq@brd.superproxy.io:22225'  # datacenter
    # 'https': 'http://brd-customer-hl_61469640-zone-residential:h71mubelhl8a@brd.superproxy.io:22225'  # residential
    # 'https': 'http://brd-customer-hl_61469640-zone-isp:ovmuz8dv1i1r@brd.superproxy.io:22225', # isp

}

r = requests.get(
    # 'https://api.my-ip.io/v2/ip.json',
    'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=woodlandscc_badmintoncourts&selectedDate=18/12/2023&time=all',
    # 'https://www.google.com',
    # 'https://docs.python.org',
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    },
    # proxies=proxies,
    # verify=False
)

print(r.text)
