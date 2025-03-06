from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome(options=Options())
url = "https://www.hltv.org/results"
driver.get(url)

# waits for page to fully load
driver.implicitly_wait(5)
page_content = driver.page_source

soup = BeautifulSoup(page_content, "html.parser")
soup.prettify()
matches = soup.find_all("div", class_="result-con")

with open("hltv.txt", "w", encoding="utf-8") as file:
    for match_no, match in enumerate(matches):
        match_link = match.find("a", class_="a-reset").get("href")
        score_won = match.find("span", class_="score-won").get_text()
        score_lost = match.find("span", class_="score-lost").get_text()
        for i in range(1,3):
            team_content =  match.find("div", class_=f'line-align team{i}')
            img_content = team_content.find("img")
            team_name = img_content.get("title")
            if i == 1:
                team1 = team_name
            else:
                team2 = team_name
        res = f"match no : {match_no} {team1}  vs  {team2}  scores :  {score_won} - {score_lost} \n "
        
        # encoding="utf-8" required for properly write file
        file.write(str(res))

driver.quit()
