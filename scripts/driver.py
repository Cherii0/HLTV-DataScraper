from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class Driver:
    @staticmethod
    def get_content(url : str):
        driver = webdriver.Chrome(options=Options())
        driver.get(url)

        # waits for page to fully load
        driver.implicitly_wait(2)
        page_content = driver.page_source
        driver.quit()

        # holds content to scrap
        return BeautifulSoup(page_content, "html.parser")
