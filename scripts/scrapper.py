from unittest import result

from matches import MatchesResults
from players import Players
from teams import Teams
from menu_manager import Menu

class Scrapper:
    def __init__(self):
            # subScrappers objects
        self.matches_results = MatchesResults()
        self.teams = Teams()
        self.players = Players()
            # menu object for printing menu content and executing Scrapper methods
        self.menu = Menu()
            # collector for funcs
        self.funcs = None
        self.collect_funcs()

    def collect_funcs(self):
        self.funcs = {1 : {1 : self.matches_results.scrap, 2 : self.matches_results.describe,
                           3 : self.matches_results.write_to_csv_file, 4 : self.matches_results.write_to_json_file},
                      2 : {1 : self.teams.scrap, 2 : self.teams.describe,
                           3 : self.teams.write_to_csv_file, 4 : self.teams.write_to_json_file},
                      3 : {1 : self.players.scrap, 2 : self.players.describe,
                           3 : self.players.write_to_csv_file, 4 : self.players.write_to_json_file}
                      }

    def execute(self) -> None:
        self.menu.show_main_menu()
        tab = int(input("Your choice... "))
        while True:
            self.menu.show(tab)
            operation = int(input("Your choice... "))
            self.funcs[tab][operation]()
