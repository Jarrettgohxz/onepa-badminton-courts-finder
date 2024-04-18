# onepa-badminton-courts-finder

A simple automation to find all the available Badminton courts from OnePA CCs in Singapore using Python. (https://www.onepa.gov.sg/ website). I believe that the method used in this project is faster and more efficient compared to the manual method of visiting the website and interacting with the UI elements one by one. It is also more lightweight than other general web crawling/scraping methods used (such as with Selenium, Scrapy or other popular libraries), that interacts with the UI HTML elements. This is because the court availability data are not extracted from the HTML source code, but rather from a rate-limited and non-intrusive direct API call to the relevant URL endpoints.

# Operating system
- This script has only been tested and working on the Windows operating system


# Create a Python virtual environment (In Windows)

```
onepa-badminton-courts-finder$ python -m venv path/to/venv
onepa-badminton-courts-finder$ /path/to/venv/scripts/activate
```

# USAGE

> Edit the config.json

```json
{
  "update_facilities_from_server": false,
  "date": "DD/MM/YYYY"
}
```

- `update_venues_data_json`: boolean to indicate whether to make a call to the function to retrieve venues data and update the existing one (as defined in `venues_data.json`)

> From within the Python virtual environment

Install required packages

```
(venv) onepa-badminton-courts-finder/court_availability$ pip install -r requirements.txt
```

To run the script
> NOTE: This script should always be executed from the `court_availability` folder
> (Eg. on Windows: C:/Users/.../onepa-badminton-courts-finder/court_availability)
```
(venv) onepa-badminton-courts-finder$ cd court_availability
(venv) onepa-badminton-courts-finder/court_availability$ python main.py
```

Output JSON file

- A file named `courts_DD_MM_YYY.json` would be generated with the following format:

```json
{
  "date": null,
  "available_courts": [
    {
      "id": null,
      "resources": [
        {
          "court_number": null,
          "slots": [
            {
              "time_range": null,
              "is_peak": null
            }
          ]
        }
      ]
    }
  ]
}
```

Local HTTP server & map display
> Once the script has complete execution, a local HTTP server would be started with `Flask`. This server is used to serve data for the map display explained below.
> Subsequently, a map display would be opened on the default browser at the address: `C:/Users/.../onepa-badminton-courts-finder/court_availability/map/map.html`


https://github.com/Jarrettgohh/onepa-badminton-courts-finder/assets/54612861/a55952b8-9e28-4f70-a17a-bc20be040b49



# NOTICE

This script is created in a way that it does not disrupt the onepa.gov.sg and related servers/services. It is only used to remove the hassle of manually finding courts from the website, which is really tiresome. Even though this script is significantly faster than the manual method, it is made to be safe and not disrupt the services.
