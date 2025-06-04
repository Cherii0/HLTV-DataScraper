
class Menu:

    def __init__(self):
        self.tabs = None
        self.prepare_tabs()

    def prepare_tabs(self):
        self.tabs = {1 : self.show_results_tab,
                     2 : self.show_teams_tab,
                     3 :  self.show_players_tab}

    def show(self, choice : int):
        self.tabs[choice]()

    def show_main_menu(self):
        print("1. Scrap matches results")
        print("2. Scrap ranked teams players")
        print("3. Scrap players database")
        print("4. Exit")

    def show_results_tab(self):
        print("1. Scrap matches results")
        print("2. Describe matches results")
        print("3. Save matches results into csv")
        print("4. Save matches results into json")\


    def show_players_tab(self):
        print("1. Scrap players database")
        print("2. Describe players")
        print("3. Save players databases into csv")
        print("4. Save players database into json")

    def show_teams_tab(self):
        print("1. Scrap ranked teams")
        print("2. Describe teams")
        print("3. Save ranked teams into csv")
        print("4. Save ranked teams into json")
