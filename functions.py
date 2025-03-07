from operator import concat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_website_content(url, con_type, _class, find_type):

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

def get_matches_links(content):

    '''  returns all matches links from given html content   '''

    matches_links = []
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

    keys = input[0].keys()
    header = ""
    for key in keys:
        header += concat(key, ";")

    # encoding="utf-8" required for properly write file
    with open("hltv.txt", "w", encoding="utf-8") as file:
        file.write(concat(header, "\n"))
        for match in input:
            row = ""
            for elem in match.values():
                row += concat(str(elem), ";")
            file.write(concat(row, "\n"))



def get_maps_scores(match_url):

    '''  returns each maps scores for each team   '''

    content_overall = get_website_content(match_url, "div", "results played", "multi")
    match_id = match_url.split("/")[4]
    result_set = []

    for no, content in enumerate(content_overall):
        conetnt_scores = content.find_all("div", class_="results-team-score")
        conetnt_teams = content.find_all("div", class_="results-teamname text-ellipsis")

        result_set.append(
            {
                "match_id" : match_id,
                "map_no" : no+1,
                "team_1" : conetnt_teams[0].get_text(),
                "score_t1" : conetnt_scores[0].get_text(),
                "team_2" : conetnt_teams[1].get_text(),
                "score_t2" : conetnt_scores[1].get_text()
            }
        )

    return result_set


def get_players_played(match_url):

    '''  gets player nick, kd, adr for each player played given match   '''

    # gets table stats
    content_overall = get_website_content(match_url, "div", "stats-content", "single")
    # finds each player content
    content_player = content_overall.find_all("tr", class_="")

    match_id = match_url.split("/")[4]

    # players team 1 - filters duplicates
    content_player_t1 = content_player[:5]
    # players team 2 - filters duplicates
    content_player_t2 = content_player[15:20]
    # merge both teams content
    content_players = content_player_t1 + content_player_t2

    result_set = []

    for player in content_players:

        player_nick = player.find("span", class_="player-nick").get_text()
        player_kd = player.find("td", class_="kd text-center").get_text()
        player_adr = player.find("td", class_="adr text-center").get_text()

        result_set.append({

            "match_id" : match_id,
            "player_nick" : player_nick,
            "player_kd" : player_kd,
            "player_adr" : player_adr
        })

    return result_set


# FINE match type bo3 bo1 #  match_type = get_website_content(url, "div","padding preformatted-text", "single").get_text()
