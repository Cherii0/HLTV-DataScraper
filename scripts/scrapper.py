from matches import MatchesResults
from players import Players
from teams import Teams

class Menu:

    @staticmethod
    def show_menu():
        print("1. Scratch results")
        print("2. Describe results")
        print("3. Save matches results into txt")
        print("4. Scratch players database")
        print("5. Describe players")
        print("6. Scratch ranked teams")
        print("7. Describe teams")


class ScrapperManager:
    def __init__(self):
        self.matches_results = MatchesResults()
        self.players = Players()
        self.teams = Teams()
        self.menu = Menu()
        self.funcs = self.make_funcs()
        self.menu_options_num = len(self.funcs)

    def make_funcs(self) -> dict:
        return {
            1. : self.matches_results.scratch,
            2. : self.matches_results.describe,
            3  : self.matches_results.write_to_txt_file,
            4. : self.players.scratch,
            5. : self.players.describe,
            6. : self.teams.scratch,
            7. : self.teams.describe
        }

    def execute(self) -> None:
        self.menu.show_menu()
        while True:
            choice = int(input("Your choice... "))
            if not 0 < choice <= self.menu_options_num:
                break
            self.funcs.get(choice)()
