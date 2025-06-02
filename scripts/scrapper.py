from abc import abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dataclasses import dataclass

from scripts import links_manager


@dataclass
class UrlManager:
    links_dict = {"main" : "https://www.hltv.org",
                 "results" : "https://www.hltv.org/results",
                 "ranking" : "https://www.hltv.org/ranking/teams/",
                 "players" : "https://www.hltv.org/stats/players",
                 "team" : "https://www.hltv.org/team/"}

class MenuManager:

    def __init__(self):
        self.menu_tabs = {1 : self.show_results_tab,
                          2 : self.show_players_tab,
                          3 : self.show_teams_tab}


    @staticmethod
    def show_results_tab():
        print("results tab")

    @staticmethod
    def show_players_tab():
        print("players tab")

    @staticmethod
    def show_teams_tab():
        print("teams tab")


    @staticmethod
    def show_menu() -> None:
        print("1. Scratch results")
        print("2. Scratch players stats")
        print("3. Scratch ranked teams")
        print("4. Exit")

    def __call__(self):
        self.show_menu()

        while True:
            choice = int(input("Your choice... "))
            if choice == 4:
                break
            self.menu_tabs.get(choice)()


class Scrapper:
    find_type = ""
    find_types = ("single", "multi")
    con_class = ""
    con_type = ""
    soup = None
    driver = None
    url_manager = UrlManager()
    menu_manager = MenuManager()

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def execute(cls):
        cls.menu_manager()

    @classmethod
    def get_content(cls, url : str):

        cls.driver = webdriver.Chrome(options=Options())
        cls.driver.get(url)

        # waits for page to fully load
        cls.driver.implicitly_wait(2)
        page_content = cls.driver.page_source

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


class Results(Scrapper):

    def __init__(self):
        super().__init__()
        self.con_type = "div"
        self.con_class = "result-con"
        self.soup = None
        self._content = None
        self.url_manager = UrlManager()

    def scratch(self) -> None:
        self.soup = Scrapper.get_content(self.url_manager.links_dict["results"])
        self._content = self.soup.find_all(self.con_type, class_= self.con_class)
        Scrapper.driver.quit()

    @property
    def content(self):
        return self._content


def main():

    scrapper = Scrapper()
    scrapper.execute()

if __name__ == "__main__":
    main()
