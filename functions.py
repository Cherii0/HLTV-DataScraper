from operator import concat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_website_content(url, con_type = "None", _class= "None", find_type= "None"):

    '''   from provided url scrapping all content  '''

    driver = webdriver.Chrome(options=Options())
    driver.get(url)

    # waits for page to fully load
    driver.implicitly_wait(2)
    page_content = driver.page_source

    # holds content to scrap
    soup = BeautifulSoup(page_content, "html.parser")

    if find_type == "multi":
        content = soup.find_all(con_type, class_=_class)
    elif find_type == "single":
        content = soup.find(con_type, class_=_class)
    else:
        return soup

    driver.quit()

    return content

def get_matches_links(pages):

    '''  returns all matches links from given number of history results pages  '''

    matches_links = []

    for page in range(pages+1):
        if page == 1:
            content = get_website_content("https://www.hltv.org/results", "div", "result-con", "multi")
        else:
            offset = 100 * page
            content = get_website_content(concat("https://www.hltv.org/results?offset=", str(offset)), "div",
                                          "result-con", "multi")

        for match in content:
            full_link = concat("https://www.hltv.org", match.find("a", class_="a-reset").get("href"))
            matches_links.append(full_link)

    return matches_links


def get_match_overview(content):

    '''  returns list of dictionaries that holds basic match stats   '''

    matches_overview = []
    for match_no, match in enumerate(content):
        full_link = concat("https://www.hltv.org", match.find("a", class_="a-reset").get("href"))
        match_id = full_link.split("/")[4]
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
                "match_id" : match_id,
                "match_no" : match_no,
                "team1" : team1,
                "team2" : team2,
                "score_won" : score_won,
                "score_lost" : score_lost
              }
        matches_overview.append(res)
    return(matches_overview)


def write_to_file(input , file_name, input_type = "listdict"):

    '''  gets list of dictionaries and writes to csv file   '''

    # encoding="utf-8" required for properly write file
    with open(file_name, "a", encoding="utf-8") as file:
        for match in input:
            row = ""
            for elem in match.values():
                row += concat(str(elem), ";")
            file.write(concat(row, "\n"))
