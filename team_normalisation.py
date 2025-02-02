import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from fetch_data import FetchData

class TeamNormalisation(FetchData):
    def __init__(self):
        super().__init__(url='https://www.premierleague.com/clubs')
        self.pinpoint_dropdown()[0].click()
        self.reserved_titles = ['First Team Manager', 'Head Coach', 'Manager']
        self.current_season = self.pinpoint_dropdown()[0].text
        time.sleep(3)
        self.elements = self.driver.find_elements(By.CSS_SELECTOR, 'td.team a')
        self.stadiums = self.driver.find_elements(By.CSS_SELECTOR, 'td.venue a div.team-index__stadium-name')
        self.past_season = list

    def automate(self, count):
        time.sleep(5)
        e = self.elements[count]
        club_name = e.text
        stadium_name = self.stadiums[count].text
        time.sleep(3)
        self.driver.execute_script("arguments[0].setAttribute('target', '_blank');",e)  # Sets the element to be placed in a new tab
        e.click()  # Clicks on the element
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1]) # Switches to the new tab
        time.sleep(5)
        club_details = self.fetch_club_details() # Contains a tuple with the team_id as the first item, est_year as the second
        time.sleep(5)
        coach_list = self.fetch_manager()
        coach_name = self.__break_down_titles(coach_list)
        time.sleep(5)
        capacity = self.fetch_capacity()
        time.sleep(5)
        time.sleep(5)
        self.driver.close()
        # Switch back to the original window
        self.driver.switch_to.window(self.driver.window_handles[0])
        return club_name, stadium_name, club_details, coach_name, capacity

    def fetch_club_details(self):
        # Fetch club name, year
        try:
            name = self.driver.find_element(By.CSS_SELECTOR, 'h2.club-header__team-name').text # This retrieves the name of the club
            est_year = self.driver.find_element(By.CSS_SELECTOR, 'span.club-header__founded-date').text.split()[1] #
            team_id = name[:3] + est_year
            print(name, team_id, est_year)
            return team_id, int(est_year)
        except NoSuchElementException:
            pass

    def fetch_manager(self):
        directory_list = self.driver.find_element(By.CSS_SELECTOR, '.tab [data-link-index="8"]')
        directory_list.click()
        time.sleep(5)
        title = self.driver.find_elements(By.CLASS_NAME, 'card')
        title_name = [name.text.split('\n') for name in title]
        return title_name

    def __break_down_titles(self, title_name_array: list):
        for a in title_name_array:
            for i, k in enumerate(a):
                if '-' in k:
                    new_word = k.split('-')
                    new_word = ' '.join(new_word)  # Joining the words in a list to form a single sentence
                    if new_word.title().strip() in self.reserved_titles:
                        return a[i + 1]
                elif k.title().strip() in self.reserved_titles:
                    return a[i + 1]

    def fetch_capacity(self):
        stadium = self.driver.find_element(By.CSS_SELECTOR, '.tab [data-link-index="6"]')
        stadium.click()
        time.sleep(3)
        stadium_information = self.driver.find_element(By.CSS_SELECTOR, '.tablist [data-tab-index="1"]')
        stadium_information.click()
        time.sleep(3)
        capacity = self.driver.find_element(By.CSS_SELECTOR, '.tabbedContent [data-ui-tab="Stadium Information"]').text
        capacity = int(capacity.split('\n')[0].split(':')[1].strip().replace(',', ''))
        return capacity




f = TeamNormalisation()
print(f.current_season)
for j in range(len(f.elements)):
    print(f.automate(j))

# for season_count in range(len(f.season_text().split())):
#     pass
