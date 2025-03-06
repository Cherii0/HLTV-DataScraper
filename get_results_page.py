from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

driver = webdriver.Chrome(options=Options())
url = "https://www.hltv.org/results"
driver.get(url)

# waits for page to fully load
driver.implicitly_wait(5)
page_content = driver.page_source

soup = BeautifulSoup(page_content, "html.parser")

table = soup.find_all("div", class_="main-content")

# encoding="utf-8" required for properly write file 
with open("hltv.txt", "w", encoding="utf-8") as file:
    file.write(str(soup))

driver.quit()
