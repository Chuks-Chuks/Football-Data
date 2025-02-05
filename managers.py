from time import sleep
from selenium.webdriver.common.by import By
from fetch_data import FetchData


class Manager(FetchData):
    def __init__(self):
        super().__init__(url='https://www.premierleague.com/clubs')
        self.pinpoint_dropdown()[0].click()
        self.past_season = list

    def fetch_past_club_details(self):
        sleep(3)
        past_history = self.driver.find_element(By.CSS_SELECTOR, '.tab [data-link-index="7"]')
        past_history.click()
        sleep(5)
        self.past_season = self.driver.find_elements(By.CSS_SELECTOR, 'header.club-archive__header h2')
        past_season_text = [season.text for season in self.past_season]
        print(past_season_text)
        sleep(3)
        manager = self.driver.find_elements(By.CSS_SELECTOR, 'div.club-archive__description-list dl:nth-of-type(2) dd p')
        manager_text = [past_manager.text for past_manager in manager]
        print(manager_text)