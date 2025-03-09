from operator import concat
from funtions import get_website_content

def get_team_details():

    result_set = []

    # creates list of individual team box from ranking page
    ranking_boxed = get_website_content("https://www.hltv.org/ranking/teams/2025/march/3", "div", "ranked-team standard-box", "multi")

    # all links to teams noted in ranking
    team_links = []
    for box in ranking_boxed:
        part_link = box.find("a", class_= "moreLink").get("href")
        team_link = concat("https://www.hltv.org", part_link )
        team_links.append(team_link)


    for link in team_links[:101]:
        team_page = get_website_content(link, "None", "None", "None")

        id = link.split("/")[4]
        name = team_page.find("h1", "profile-team-name text-ellipsis").get_text()
        country = team_page.find("img", class_ = "flag flag").get("title")
        ranking = team_page.find_all("div", class_ = "profile-team-stat")[1].find("a").get_text().split("#")[1]

        # ensures that ties percentage wins/loss are both included
        maps = team_page.find_all("div", class_ = "map-statistics-row")

        best_map = ""
        best_map_percentage_win = int( maps[0].find("div", class_="map-statistics-row-win-percentage").get_text().split(".")[0])
        for map in maps:
            percent = int(map.find("div", class_="map-statistics-row-win-percentage").get_text().split(".")[0])
            if percent == best_map_percentage_win:
                best_map += concat(map.find("div", class_="map-statistics-row-map-mapname").get_text(), "-")

        worst_map = ""
        top_percent_loss = int(maps[len(maps)-1].find("div", class_="map-statistics-row-win-percentage").get_text().split(".")[0])
        for map in reversed(maps):
            percent = int(map.find("div", class_="map-statistics-row-win-percentage").get_text().split(".")[0])
            if percent == top_percent_loss:
                worst_map += concat(map.find("div", class_ = "map-statistics-row-map-mapname").get_text(), "-")


        players_box = team_page.find_all("a", class_ = "col-custom")

        for no, player in enumerate(players_box):
            match no:
                case 0:
                    player_1 = player.find("span", class_ = "text-ellipsis bold").get_text()
                case 1:
                    player_2 = player.find("span", class_ = "text-ellipsis bold").get_text()
                case 2:
                    player_3 = player.find("span", class_ = "text-ellipsis bold").get_text()
                case 3:
                    player_4 = player.find("span", class_ = "text-ellipsis bold").get_text()
                case 4:
                    player_5 = player.find("span", class_ = "text-ellipsis bold").get_text()

        result_set.append({
            "id" : id,
            "name" : name,
            "country": country,
            "ranking" : ranking,
            "best_map" : best_map,
            "worst_map" : worst_map,
            "player1" : player_1,
            "player2" : player_2,
            "player3" : player_3,
            "player4" : player_4,
            "player5" : player_5
        })

    return result_set
