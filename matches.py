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



def get_map(map_url, no):

    '''  returns maps details for given match   '''

    content = get_website_content(map_url)
    maps_details = []

    ''' overall statistics for map '''

    id = map_url.split("/")[6]
    match_id = content.find("a", class_ = "match-page-link button").get("href").split("/")[2]
    names = content.find_all("div", class_="stats-match-map-result-mapname dynamic-map-name-full")
    name = names[no].get_text()
    teamA = content.find("div", class_="team-left").find("a", class_ = "block text-ellipsis").get_text()
    teamB = content.find("div", class_="team-right").find("a", class_ = "block text-ellipsis").get_text()

    ''' team A '''
    final_score_tA = content.find("div", class_="team-left").find("div").get_text()
    fh_score_tA = content.find("div", class_ = "match-info-row").find_all("span")[2].get_text()
    sh_score_tA = content.find("div", class_ = "match-info-row").find_all("span")[4].get_text()

    ''' team B '''
    final_score_tB = content.find("div", class_="team-right").find("div").get_text()
    fh_score_tB = content.find("div", class_ = "match-info-row").find_all("span")[3].get_text()
    sh_score_tB = content.find("div", class_ = "match-info-row").find_all("span")[5].get_text()

    ''' team A B'''

    first_kills_tA, first_kills_tB = content.find_all("div", class_ = "match-info-row")[2].find("div", class_ = "right").get_text().split(":")
    clutches_won_tA, clutches_won_tB = content.find_all("div", class_ = "match-info-row")[3].find("div", class_ = "right").get_text().split(":")

    most_boxes = content.find_all("div", class_ = "most-x-box standard-box")

    for most_box in most_boxes:
        match most_box.find("span", class_ = "most-x-title").get_text():
            case "Most kills":
                most_kills = "-".join([most_box.find("a").get_text(), most_box.find("span", class_ = "valueName").get_text()])
            case "Most damage":
                most_damage = "-".join([most_box.find("a").get_text(), most_box.find("span", class_ = "valueName").get_text()])
            case "Most assists":
                most_assist = "-".join([most_box.find("a").get_text(), most_box.find("span", class_ = "valueName").get_text()])
            case "Most AWP kills":
                most_awp_kills = "-".join([most_box.find("a").get_text(), most_box.find("span", class_ = "valueName").get_text()])
            case "Most first kills":
                most_first_kills = "-".join([most_box.find("a").get_text(), most_box.find("span", class_ = "valueName").get_text()])
            case "Best rating 2.1":
                best_rating = "-".join([most_box.find("a").get_text(), most_box.find("span", class_ = "valueName").get_text()])
            case "_":
                break

    maps_details.append({

        "id" : id,
        "match_id" : match_id,
        "name": name,
        "team A": teamA,
        "team B": teamB,
        "most kills" : most_kills,
        "most damage" : most_damage,
        "most assists" : most_assist,
        "most awp kills" : most_awp_kills,
        "most first kills" : most_awp_kills,
        "best rating" : best_rating,
        "final score team A" : final_score_tA,
        "first half score A" : fh_score_tA,
        "second half score A" : sh_score_tA,
        "first kill team A" : first_kills_tA,
        "clutches won team A" : clutches_won_tA,
        "final score team B": final_score_tB,
        "first half score B": fh_score_tB,
        "second half score B": sh_score_tB,
        "first kill team B": first_kills_tB,
        "clutches won team B": clutches_won_tB
    })

    return maps_details

