from matches import MatchesResults
from players import Players
from teams import Teams

class Menu:

    @staticmethod
    def show_menu():
        # matches
        print("1. Scratch matches results")
        print("2. Describe matches results")
        print("3. Save matches results into csv")
        print("4. Save matches results into json")
        # players
        print("5. Scratch players database")
        print("6. Describe players")
        print("7. Save players databases into csv")
        print("8. Save players database into json")
        # teams
        print("9. Scratch ranked teams")
        print("10. Describe teams")
        print("11. Save ranked teams into csv")
        print("12. Save ranked teams into json")



class ScrapperManager:
    def __init__(self):
            # subScrappers objects
        self.matches_results = MatchesResults()
        self.players = Players()
        self.teams = Teams()

            # scrappers functions collector
        self.funcs = self.make_funcs()
        self.menu_options_num = len(self.funcs)
            # menu object for printing menu content
        self.menu = Menu()

    def make_funcs(self) -> dict:
        return {
            1. : self.matches_results.scratch,
            2. : self.matches_results.describe,
            3  : self.matches_results.write_to_csv_file,
            4  : self.matches_results.write_to_json_file,
            5. : self.players.scratch,
            6. : self.players.describe,
            7  : self.players.write_to_csv_file,
            8  : self.players.write_to_json_file,
            9. : self.teams.scratch,
            10. : self.teams.describe,
            11  : self.teams.write_to_csv_file,
            12  : self.teams.write_to_json_file,
        }

    def execute(self) -> None:
        self.menu.show_menu()
        while True:
            choice = int(input("Your choice... "))
            if not 0 < choice <= self.menu_options_num:
                break
            self.funcs.get(choice)()
