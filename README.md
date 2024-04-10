# onepa-badminton-courts-finder
A simple automation to find all the available Badminton courts from OnePA CCs in Singapore using Python. (https://www.onepa.gov.sg/ website). The speed and efficiency is believed to be faster than other general web crawling/scraping methods used (such as with Selenium, Scrapy or another popular libraries). This is because the court availability data are not extracted from the HTML source code, but rather from a rate-limited and non-intrusive direct API call to the relevant URL endpoints.  



# PACKAGES
Libraries used in this project includes requests & beautiful soup 4.

# USAGE

To run on the shell

```sh
py onepa.py
```

Input date format: DD-MM-YYYY


# WARNING
Using of scripts to book badminton courts in onePA is not allowed. This project is just an experiment to automate finding of courts, but can't be used to book courts; there is no intention to cause any damage to the website. 
