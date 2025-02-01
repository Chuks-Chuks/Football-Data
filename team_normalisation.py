import time

from selenium.webdriver.common.by import By

from fetch_data import FetchData

class TeamNormalisation(FetchData):
    def __init__(self):
        super().__init__(url='https://www.premierleague.com/clubs')

        # self.driver.get(self.url)
        # self.season_text()



f = TeamNormalisation()
for season_count in range(len(f.season_text().split())):
    pass

f.pinpoint_dropdown()[0].click()
elements = f.driver.find_elements(By.CSS_SELECTOR, 'li.club-card-wrapper a')
for e in elements:
    time.sleep(3)
    print(e.text)
    print(e.get_attribute('href'))
    time.sleep(3)
    f.driver.execute_script("arguments[0].setAttribute('target', '_blank');", e)
    # time.sleep(3)
    e.click()
    time.sleep(3)
    f.driver.switch_to.window(f.driver.window_handles[1])
    time.sleep(3)
    f.driver.close()
    # Switch back to the original window
    f.driver.switch_to.window(f.driver.window_handles[0])

