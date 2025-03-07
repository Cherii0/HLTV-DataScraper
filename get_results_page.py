from operator import concat

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome(options=Options())
url = "https://www.hltv.org/results"
driver.get(url)

# waits for page to fully load
driver.implicitly_wait(2)
page_content = driver.page_source

soup = BeautifulSoup(page_content, "html.parser")
soup.prettify()

# holds content to scrap
matches_content = soup.find_all("div", class_="result-con")

def get_matches_links(matches_content):
    matches_links = []
    for match in matches_content:
        full_link = concat("https://www.hltv.org", match.find("a", class_="a-reset").get("href"))
        matches_links.append(full_link)
    return matches_links

def get_match_overview(matches_content):
    matches_overview = []
    for match_no, match in enumerate(matches_content):
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
        res = {
                "match_no" : match_no,
                "team1" : team1,
                "team2" : team2,
                "score_won" : score_won,
                "score_lost" : score_lost
              }
        matches_overview.append(res)
    return(matches_overview)


def write_to_file(match_overview, file_name):
    # encoding="utf-8" required for properly write file
    with open(file_name, "w", encoding="utf-8") as file:
        for match in match_overview:
            file.write(concat(str(match), "\n"))


write_to_file(get_match_overview(matches_content), "hltv.txt")

driver.quit()
