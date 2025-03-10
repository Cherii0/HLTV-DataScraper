from operator import concat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_website_content(url, con_type = "None", _class = "None", find_type = "None"):

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


def get_match(url):

    '''  pull all data needed for single row
     in table matches from provided match    '''

    result = []

    content_overall = get_website_content(url, "None", "None", "None")

    id = url.split("/")[4]

    try:
        date = content_overall.find_all("div", class_="date")[1].get_text()
    except IndexError:
        date = None

    type_ = content_overall.find("div", class_ = "padding preformatted-text").get_text().split("*")[0]
    type_ = type_.replace("\n\n", "")
    tournament_id = content_overall.find("div", class_="event text-ellipsis").find("a").get("href").split("/")[2]

    teamA_area = content_overall.find("div", class_ = "team1-gradient")
    teamB_area = content_overall.find("div", class_ = "team2-gradient")

    teamA_id = teamA_area.find("a").get("href").split("/")[2]
    teamB_id = teamB_area.find("a").get("href").split("/")[2]

    for type in ["won", "lost"]:
        temp = teamA_area.find("div", class_=type)
        if temp is None:
            continue
        else:
            score_teamA = temp.get_text()

    for type in ["won", "lost"]:
        temp = teamB_area.find("div", class_=type)
        if temp is None:
            continue
        else:
            score_teamB = temp.get_text()

    try:
        bans_area = content_overall.find_all("div", class_="standard-box veto-box")[1].find("div", class_="padding")
    except IndexError:
        bans_area = None

    bans_both = [ban.get_text().split(".")[1].lstrip() for ban in bans_area.find_all("div")]
    bans_teamA = []
    bans_teamB = []

    for no, ban in enumerate(bans_both):
        if no % 2 == 0:
            bans_teamB.append(ban)
        else:
            bans_teamA.append(ban)

    bans_teamB.pop() # removes left map

    bans_teamB = ",".join([ban.split(" ")[-1] for ban in bans_teamB])
    bans_teamA = ",".join([ban.split(" ")[-1] for ban in bans_teamA])

    mvp = content_overall.find("div", class_ = "highlighted-player potm-container").find("span", class_="player-nick").get_text()

    result.append(
        {
            "id" : id,
            "date" : date,
            "type" : type_,
            "tournament_id" : tournament_id,
            "teamA_id" : teamA_id,
            "teamB_id" : teamB_id,
            "score_teamA" : score_teamA,
            "score_teamB" : score_teamB,
            "bans_teamA" : bans_teamA,
            "bans_teamB" : bans_teamB,
            "mvp" : mvp
        }
    )

    return result


def get_players_details():

    '''     '''

    all_players_link = "https://www.hltv.org/stats/players?startDate=2025-02-10&endDate=2025-03-10&maps=de_dust2&rankingFilter=Top5"
    content = get_website_content(all_players_link)
    
    players_table = content.find("table", class_ = "stats-table player-ratings-table")
    players_box = players_table.find_all("tr")

    players_links = []

    for player_box in players_box[2:3]:
        href = player_box.find("a").get("href")
        player_id = concat(href.split("/")[3], "/")
        player_name = href.split("/")[4].split("?")[0]
        player_link = "https://www.hltv.org/player/" + concat(player_id, player_name)



def get_players_links():

    main_page = "https://www.hltv.org/stats/players?startDate=2024-09-10&endDate=2025-03-10"
    content = get_website_content(main_page)

    '''
    from main page that contains all
    players basic stats we catch link to each player hltv profile
    '''

    players_table = content.find("table", class_ = "stats-table player-ratings-table")
    players_box = players_table.find_all("tr")

    players_links = []

    for player_box in players_box[1:]:
        href = player_box.find("a").get("href")
        player_id = concat(href.split("/")[3], "/")
        player_name = href.split("/")[4].split("?")[0]
        player_link = "https://www.hltv.org/player/" + concat(player_id, player_name)
        players_links.append(player_link)

    return players_links


def get_players_details(link):

    ''' returns list of dictionaries for all significant players stats '''

    players_details = []

    player_box = get_website_content(link)
    age = player_box.find("div", class_="playerInfoRow playerAge").find("span", class_= "listRight").find("span").get_text().split(" ")[0]

    try:
        team = player_box.find("div", class_ = "playerInfoRow playerTeam").find("img").get("title")
    except AttributeError:
        team = "NoTeam"

    attributes = player_box.find("div", class_ = "playerpage-container playerpage-container-attributes").find_all("div", "player-stat")
    attr_val = []
    attr_name = []
    for attribute in attributes:
        attribute_name = attribute.find("b").get_text()
        attr_name.append(attribute_name)
        attribute_value = attribute.find("span", class_ = "statsVal").find("p")

        if attribute_value.find("b"):
            attribute_value =  attribute_value.find("b").get_text()
            attr_val.append(attribute_value)
        else:
            attribute_value = attribute_value.get_text().split("/")[0]
            attr_val.append(attribute_value)


    player_names = player_box.find("div", class_ = "playerName")
    nick = player_names.find("h1").get_text()
    real_name = player_names.find("div", class_ = "playerRealname").get_text()
    id = link.split("/")[4]

    players_details.append(
        {
            "id" : id,
            "nick" : nick,
            "realName" : real_name,
            "age" : age,
            "team" : team,
            attr_name[0]: attr_val[0],
            attr_name[1]: attr_val[1],
            attr_name[2]: attr_val[2],
            attr_name[3]: attr_val[3],
            attr_name[4]: attr_val[4],
            attr_name[5]: attr_val[5],
            attr_name[6]: attr_val[6],
            attr_name[7]: attr_val[7]
        }
    )

    return players_details


