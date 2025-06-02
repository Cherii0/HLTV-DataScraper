from abc import abstractmethod
from operator import concat

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class UrlManager:
    links_dict = {"main" : "https://www.hltv.org",
                 "results" : "https://www.hltv.org/results",
                 "ranking" : "https://www.hltv.org/ranking/teams/",
                 "players" : "https://www.hltv.org/stats/players",
                 "team" : "https://www.hltv.org/team/"}


class Abstract:

    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def scratch(self):
        pass

class Players(Abstract):
    def describe(self) -> None:
        pass

    def scratch(self) -> None:
        pass

class Teams(Abstract):
    def describe(self) -> None:
        pass

    def scratch(self) -> None:
        pass

class MatchesResults(Abstract):

    def __init__(self):
        self.con_type = "div"
        self.con_class = "result-con"
        self.soup = None
        self.collected_elements = []
        self.url_manager = UrlManager()
        self.matches_links = []
        self.pages = 1
        self.offset_str = "/?offset="

    def scratch(self) -> None:
        self.update_matches_links() # update matches links before pulling data


    def update_matches_links(self) -> None:
        """"
        returns all matches links from given number of history results pages 
        """""
        self.matches_links.clear()
        for page in range(1, self.pages+1):
            if page == 1:
                self.soup = Scrapper.get_content(self.url_manager.links_dict.get("results"))
            else:
                offset = 100 * self.pages
                self.soup = Scrapper.get_content(self.url_manager.links_dict.get("results") + self.offset_str + str(offset))

            # 100 bins each contains link to extract
            self.collected_elements.extend(self.soup.find_all(self.con_type, class_=self.con_class))
            self.extract_links()

    def extract_links(self):
        for match in self.collected_elements:
            main_part = self.url_manager.links_dict["main"]
            match_part = match.find("a", class_="a-reset").get("href")
            link = concat(main_part, match_part)
            self.matches_links.append(link)


    def describe(self) -> None:
        print(f"number of matches links pulled : {len(self.matches_links)}")
        print(f"first 5 matches in database : \n {self.matches_links[:5]}")
        print(f"last 5 matches in database : \n {self.matches_links[-5:]}")



class Scrapper:
    find_type = ""
    find_types = ("single", "multi")
    con_class = ""
    con_type = ""
    soup = None
    driver = None

    def __init__(self):
        super().__init__()
        self.url_manager = UrlManager()
        self.results = MatchesResults()
        self.players = Players()
        self.teams = Teams()
        self.menu_tabs = self.make_menu_tabs()
        self.menu_options_num = len(self.menu_tabs)

    def make_menu_tabs(self) -> dict:
        return {
            1. : self.results.scratch,
            2. : self.results.describe,
            3. : self.players.scratch,
            4. : self.players.describe,
            5. : self.teams.scratch,
            6. : self.teams.describe
        }

    @staticmethod
    def show_menu():
        print("1. Scratch results")
        print("2. Describe results")
        print("3. Scratch players database")
        print("4. Describe players")
        print("5. Scratch ranked teams")
        print("6. Describe teams")


    def execute(self) -> None:
        self.show_menu()
        while True:
            choice = int(input("Your choice... "))
            if not 0 < choice <= self.menu_options_num:
                break
            self.menu_tabs.get(choice)()


    @classmethod
    def get_content(cls, url : str):

        cls.driver = webdriver.Chrome(options=Options())
        cls.driver.get(url)

        # waits for page to fully load
        cls.driver.implicitly_wait(2)
        page_content = cls.driver.page_source
        cls.driver.quit()

        # holds content to scrap
        return BeautifulSoup(page_content, "html.parser")


    @classmethod
    def set_search_config(cls, **kwargs : str):
        cls.set_find_type(**kwargs)
        cls.set_container_details(**kwargs)

    @classmethod
    def set_find_type(cls, **kwargs : str) :
        find_type = kwargs.get("find_type")
        if find_type in cls.find_types:
            cls.find_type = find_type


    @classmethod
    def set_container_details(cls,  **kwargs : str):
        cls.con_class = kwargs.get("con_class") if kwargs.get("con_class") else None
        cls.con_class = kwargs.get("con_type") if kwargs.get("con_type") else None


    @abstractmethod
    def scratch(self):
        pass



def main():

    scrapper=Scrapper()
    scrapper.execute()

if __name__ == "__main__":
    main()
