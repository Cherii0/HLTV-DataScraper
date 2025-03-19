from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from operator import concat

class Driver:
    time_to_load_page = 2

    def get_url_content(self, url, _con = "", _class = "", find_type = None):

        '''

        from provided url scrapping content

        Args : url (string), con_type (string), class_type(string) find_type(string)

        Returns soup (soup)

        '''

        driver = webdriver.Chrome(options=Options())
        driver.get(url)
        driver.implicitly_wait(self.time_to_load_page)
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, "html.parser")
        driver.quit()

        if find_type == "multi":
            return soup.find_all(_con, class_=_class)
        elif find_type == "single":
            return soup.find(_con, class_=_class)
        return soup




class Scrapper(Driver):
    teams_ranking_url = "https://www.hltv.org/ranking/teams/2025/march/17"


    def __init__(self):
        self.teams_urls = []

    def __str__(self):
        return "Scrapper object"


    ''' update attributes'''

    def update_teams_ranking_url(self, url):
        self.teams_ranking_url = url


    ''' adding urls '''

    def add_team_url(self, team_name, url):
        self.teams_urls.append({team_name : url})

    ''' getting urls '''

    def get_team_url(self, team=None):
        if team is None:
            return self.teams_urls
        try:
            url = list(filter(lambda team_dict :  team_dict if team in team_dict else "", self.teams_urls))[0][team]
            return url
        except :
            return f"{team} no found"

    ''' scrapping  '''

    def  retrieve_teams_urls(self):

        teams_boxes = self.get_url_content(self.teams_ranking_url, "div", "lineup-con", "multi")
        for team_box in teams_boxes:
            self.teams_urls.append(concat("https://www.hltv.org", team_box.find("a", class_ = "moreLink")["href"]))

    def get_team_info(self, team_name):

        '''

        returns scrapped data for given team

        Args: team_name (string)

        Returns : result_dict (dictionary)

        '''

        result_dict = {}
        team_link = list(filter(lambda team_dict :  team_dict if team_name in team_dict else "", self.teams_urls))[0][team_name]
        team_page = self.get_url_content(team_link)

        id = team_link.split("/")[4]
        name = team_page.find("h1", "profile-team-name text-ellipsis").get_text()
        country = team_page.find("img", class_ = "flag flag").get("title")
        ranking = team_page.find_all("div", class_ = "profile-team-stat")[1].find("a").get_text().split("#")[1]

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

        result_dict = {
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
        }

        return result_dict




scraper = Scrapper()
scraper.retrieve_teams_urls()
print(scraper.teams_urls)
