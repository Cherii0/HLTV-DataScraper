import os
from operator import concat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class Flow:


    def __init__(self):
        self.activity_type = None
        self.pulling_type = None
        self.printing_type  = None
        self.ranking = []
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



    def get_website_content(self, url, con_type="None", _class="None", find_type="None"):

        '''   from provided url scrapping all content  '''

        driver = webdriver.Chrome(options=Options())
        driver.get(url)

        # waits for page to fully load
        driver.implicitly_wait(2)
        page_content = driver.page_source

        # holds content to scrap
        soup = BeautifulSoup(page_content, "html.parser")

        if find_type == "multi":
            content = soup.find_all(con_type, class_=_class)
        elif find_type == "single":
            content = soup.find(con_type, class_=_class)
        else:
            return soup

        driver.quit()

        return content



    def pull_ranking(self):

        '''


        return

        '''

        content_overall = self.get_website_content("https://www.hltv.org/ranking/teams/2025/march/24", "None", "None", "None")

        ranking_boxes = content_overall.find_all("div", class_ = "ranking-header")

        for ranking_box in ranking_boxes:
            name = ranking_box.find("span", class_="name").text
            ranking = ranking_box.find("span", class_="position").text.split(sep = "#")[-1]
            points = ranking_box.find("span", class_="points").text[1:].split(sep = " ")[0]
            print(name, ranking, points)

        # self.ranking.append(ranking_boxes[0])


    def show_ranking(self):
        print(self.ranking)

    def main_flow(self):

        print(self.front_page_content)
        self.activity_type = self.choose_validate()
        print(self.activity_type)

        match self.activity_type:
            case 1:
                self.show_pullingdata_page()
                self.pulling_type = self.choose_validate()
                if self.pulling_type == 1:
                    print("pulling ranking....")
                    self.pull_ranking()
            case 2:
                self.show_printdata_page()
                self.printing_type = self.choose_validate()
            case 3:
                self.show_exiting_page()


flow = Flow()
flow.main_flow()
flow.show_ranking()
