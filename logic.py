import os

class Flow:


    def __init__(self):
        self.activity_type = None
        self.pulling_type = None
        self.printing_type  = None
        with open("front_page.txt", "r", encoding="utf-8") as file:
            self.front_page_content = file.read()

        with open("pull_data_conetnt.txt", "r", encoding="utf-8") as file:
            self.pulling_data_content = file.read()

        with open("show_data_content.txt", "r", encoding="utf-8") as file:
            self.printing_data_content = file.read()

        with open("show_exiting_content.txt", "r", encoding="utf-8") as file:
            self.exiting_content = file.read()




    def show_pullingdata_page(self):
        print(self.pulling_data_content)

    def show_printdata_page(self):
        print(self.printing_data_content)

    def show_exiting_page(self):
        print(self.exiting_content)

    def choose_validate(self):
        choose = None
        while True:
            try:
                choose = int(input(""))
                if (choose < 4) and (choose > 0):
                    break
                else:
                    print("Please provide number from 1 to 2 or 3 for exit")
            except ValueError:
                print("Please provide number from 1 to 2 or 3 for exit")

        return choose


    def main_flow(self):

        print(self.front_page_content)
        self.activity_type = self.choose_validate()
        print(self.activity_type)

        match self.activity_type:
            case 1:
                self.show_pullingdata_page()
                self.pulling_type = self.choose_validate()
            case 2:
                self.show_printdata_page()
                self.printing_type = self.choose_validate()
            case 3:
                self.show_exiting_page()



flow = Flow()
flow.main_flow()
