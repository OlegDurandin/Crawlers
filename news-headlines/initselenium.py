from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def selenium_initializer():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome('../chromedriver', chrome_options=options)
    return driver

if __name__ == "__main__":
    pass