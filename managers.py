from time import sleep
from selenium.webdriver.common.by import By
from team_normalisation import TeamNormalisation


class Manager(TeamNormalisation):
    def __init__(self):
        super().__init__()
        # self.pinpoint_dropdown()[0].click()
        self.past_season = list

    def automate(self, count):
        sleep(5)
        e = self.elements[count]
        club_name = e.text
        sleep(3)
        self.driver.execute_script("arguments[0].setAttribute('target', '_blank');",
                                   e)  # Sets the element to be placed in a new tab
        e.click()
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])  # Switches to the new tab
        sleep(5)
        fpcd = self.fetch_past_club_details(club_name=club_name)
        sleep(5)
        self.driver.close()
        sleep(3)
        # Switch back to the original window
        self.driver.switch_to.window(self.driver.window_handles[0])
        return fpcd

    def fetch_past_club_details(self, club_name):
            manager_details_dictionary = {
                f'{club_name}': [
                    {

                    }
                ]
            }
            sleep(3)
            past_history = self.driver.find_element(By.CSS_SELECTOR, '.tab [data-link-index="7"]')
            past_history.click()
            sleep(5)
            self.past_season = self.driver.find_elements(By.CSS_SELECTOR, 'header.club-archive__header h2')
            for season_num in range(len(self.past_season)):
                season = f'/html/body/main/div[2]/section[{season_num + 1}]/header/h2'
                managers = f'/html/body/main/div[2]/section[{season_num + 1}]/div/div[1]/div/dl[2]/dd'
                find_season = self.driver.find_element(By.XPATH, season).text.split('Champions')[0]
                find_managers = self.driver.find_element(By.XPATH, managers).text.split('\n')
                manager_details_dictionary[f'{club_name}'][0][find_season] = find_managers
            return manager_details_dictionary


# Testing the Manager's class

m = Manager()
for i in range(len(m.elements)):
    print(m.automate(i))
