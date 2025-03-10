from funtions import get_website_content
from operator import concat


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

    try:
        bans_both = [ban.get_text().split(".")[1].lstrip() for ban in bans_area.find_all("div")]
    except AttributeError:
        bans_both = None

    bans_teamA = []
    bans_teamB = []

    if bans_both is None:
        bans_teamA = "None"
        bans_teamB = "None"
    else:
        for no, ban in enumerate(bans_both):
            if no % 2 == 0:
                bans_teamB.append(ban)
            else:
                bans_teamA.append(ban)

        bans_teamB.pop() # removes left map

        bans_teamB = ",".join([ban.split(" ")[-1] for ban in bans_teamB])
        bans_teamA = ",".join([ban.split(" ")[-1] for ban in bans_teamA])

    try:
        mvp = content_overall.find("div", class_ = "highlighted-player potm-container").find("span", class_="player-nick").get_text()
    except AttributeError:
        mvp = "None"

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

    ''''  pulls links for each map  '''

    links_maps = []

    links_box = content_overall.find_all("a", class_ = "results-stats")
    for link_box in links_box:
        link = link_box.get("href")
        links_maps.append(concat("https://www.hltv.org", link))


    return result, links_maps


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



def get_map_details(match_url):

    '''  returns maps details for given match   '''

    maps_details = []

    ''' overall statistics for map '''
    most_kills = ""
    most_damage = ""
    most_assist = ""
    most_awp_kills = ""
    most_first_kills = ""
    best_rating = ""
    map_name = ""
    teamA = ""
    teamB = ""

    ''' team A'''
    final_score_tA = ""
    fh_score_tA = ""
    sh_score_tA = ""
    first_kills_tA = ""
    clutches_won_tA = ""
    ''' team B'''
    final_score_tB = ""
    fh_score_tB = ""
    sh_score_tB = ""
    first_kills_tB = ""
    clutches_won_tB = ""

    return maps_details

