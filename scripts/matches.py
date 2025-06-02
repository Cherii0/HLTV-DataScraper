from url_manager import UrlManager
from operator import concat
from driver import Driver
from file_manager import FileManager
from functools import reduce

class MatchesResults:

    def __init__(self):
        Driver()
        FileManager()
        self.url_manager = UrlManager()
        self.con_type = "div"
        self.con_class = "result-con"
        self.soup = None
        self.collected_elements = []
        self.matches_links = []
        # main collections for pulled data
        self.matches_details_d = dict()
        self.matches_details_l = list()

        self.matches_num_to_scratch = 5
        self.pages = 1
        self.offset_str = "/?offset="
        self.file_path = "matches_results.txt"

    def convert_matches_details(self):
        record = ""
        for match_id, match_details in self.matches_details_d.items():
            record += concat(match_id, " : ")
            for detail in match_details.values():
                record += concat(detail, ", ")
            self.matches_details_l.append(record)
            record = ""



    def scratch(self) -> None:
        self.update_matches_links() # update matches links before pulling data
        for url in self.matches_links[:self.matches_num_to_scratch]:
            self.append_match_details(url) # iterate through all matches links and pull data into dict
        self.convert_matches_details()

    def update_matches_links(self) -> None:
        """"
        returns all matches links from given number of history results pages 
        """""
        self.matches_links.clear()
        for page in range(1, self.pages+1):
            if page == 1:
                self.soup = Driver.get_content(self.url_manager.links_dict.get("results"))
            else:
                offset = 100 * self.pages
                self.soup = Driver.get_content(self.url_manager.links_dict.get("results") + self.offset_str + str(offset))

            # 100 bins each contains link to extract
            self.collected_elements.extend(self.soup.find_all(self.con_type, class_=self.con_class))
            self.extract_links()

    def extract_links(self):
        for match in self.collected_elements:
            main_part = self.url_manager.links_dict["main"]
            match_part = match.find("a", class_="a-reset").get("href")
            link = concat(main_part, match_part)
            self.matches_links.append(link)

    @staticmethod
    def get_match_id(url) -> str:
        return url.split("/")[4]

    def get_match_date(self) -> str:
        try:
            date = self.soup.find_all("div", class_="date")[1].get_text()
        except IndexError:
            date = None

        return date

    def get_match_type(self) -> str:
        type_ = self.soup.find("div", class_ = "padding preformatted-text").get_text().split("*")[0]
        type_ = type_.replace("\n\n", "")
        return type_

    def get_tournament_id(self) -> str:
        tournament_id = self.soup.find("div", class_="event text-ellipsis").find("a").get("href").split("/")[2]
        return tournament_id

    def get_teams_id(self):
        team_a_area = self.soup.find("div", class_ = "team1-gradient")
        team_b_area = self.soup.find("div", class_ = "team2-gradient")
        team_a_id = team_a_area.find("a").get("href").split("/")[2]
        team_b_id = team_b_area.find("a").get("href").split("/")[2]
        return team_a_id, team_b_id

    def get_teams_scores(self):
        team_a_area = self.soup.find("div", class_ = "team1-gradient")
        team_b_area = self.soup.find("div", class_ = "team2-gradient")
        type_score = ["won", "lost"]
        team_a_score, team_b_score = "", ""

        for type_ in type_score:
            temp = team_a_area.find("div", class_=type_)
            if temp is None:
                continue
            else:
                team_a_score = temp.get_text()

        for type_ in type_score:
            temp = team_b_area.find("div", class_=type_)
            if temp is None:
                continue
            else:
                team_b_score = temp.get_text()

        return team_a_score, team_b_score

    def get_teams_bans(self):
        bans_team_a, bans_team_b = [], []

        try:
            bans_area = self.soup.find_all("div", class_="standard-box veto-box")[1].find("div", class_="padding")
        except IndexError:
            bans_area = None

        try:
            bans_both = [ban.get_text().split(".")[1].lstrip() for ban in bans_area.find_all("div")]
        except AttributeError:
            bans_both = None

        if bans_both is None:
            bans_team_a = "None"
            bans_team_b = "None"
        else:
            for no, ban in enumerate(bans_both):
                if no % 2 == 0:
                    bans_team_b.append(ban)
                else:
                    bans_team_a.append(ban)

            bans_team_b.pop() # removes left map

            bans_team_b = reduce(lambda bans, map_ :  bans.split(" ")[-1] + "," + map_.split(" ")[-1], bans_team_b)
            bans_team_a = reduce(lambda bans, map_ :  bans.split(" ")[-1] + "," + map_.split(" ")[-1], bans_team_a)

        return bans_team_a, bans_team_b

    def get_match_mvp(self):
        try:
            mvp = self.soup.find("div", class_ = "highlighted-player potm-container").find("span", class_="player-nick").get_text()
        except AttributeError:
            mvp = "NoMVP"

        return mvp

    def get_match_maps_links(self):
        links_maps = []
        links_box = self.soup.find_all("a", class_ = "results-stats")
        for link_box in links_box:
            link = link_box.get("href")
            links_maps.append(concat("https://www.hltv.org", link))
        # str(reduce(lambda acc, map_ : acc + map_, links_maps))
        return ""


    def append_match_details(self, url : str):
        """""
        pull all data needed for single row in table matches from provided match 
        """""

        self.soup = Driver.get_content(url)
        match_id = self.get_match_id(url)
        match_date = self.get_match_date()
        match_type = self.get_match_type()
        tournament_id = self.get_tournament_id()
        team_a_id, team_b_id = self.get_teams_id()
        team_a_score, team_b_score = self.get_teams_scores()
        team_a_bans, team_b_bans = self.get_teams_bans()
        match_mvp = self.get_match_mvp()
        match_maps = self.get_match_maps_links()

        self.matches_details_d.update({
            match_id : {
                "date" : match_date,
                "type" : match_type,
                "match_maps_links" : match_maps,
                "tournament_id" : tournament_id,
                "teamA_id" : team_a_id,
                "teamB_id" : team_b_id,
                "score_teamA" : team_a_score,
                "score_teamB" : team_b_score,
                "bans_teamA" : team_a_bans,
                "bans_teamB" : team_b_bans,
                "mvp" : match_mvp
            }})


    def describe(self) -> None:
        print(f"number of matches links pulled : {len(self.matches_links)}")
        print(f"first 5 matches in database : \n {self.matches_links[:5]}")
        print(f"last 5 matches in database : \n {self.matches_links[-5:]}")
        print(f"random match details : \n match id :{self.matches_details_l[-1]}")

    def write_to_txt_file(self) -> None:
        FileManager.write_to_txt_file(file_path=self.file_path, data=self.matches_details_l)