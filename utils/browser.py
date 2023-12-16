from selenium import webdriver


def launch_browser():

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # options.add_argument("--headless=new")

    chrome_webdriver = webdriver.Chrome(options=options)

    return chrome_webdriver
