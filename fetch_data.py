import selenium.common.exceptions as e
from selenium import webdriver # Importing this to enable webscraping of the data
from selenium.webdriver.common.by import By
import tkinter as tk
# from time import sleep
# from selenium.webdriver import ActionChains
import time

root = tk.Tk()
from selenium.webdriver.remote.webelement import WebElement
screen_height = root.winfo_screenheight()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.premierleague.com/players')
driver.maximize_window()
time.sleep(3)

# TODO: I want to be able to pull the players in every club first.
"""# so can have a table that contains the list of clubs -- this is a slow changing dimension as relgations tend to happen

# We will have the table that says: season, teams (this will be an array) -- we should be able to unnest this later on.

# The plan is to be able to connect to a database tool so that I can do this. Postgres maybe? Or would CSV to the database
# make more sense?
"""
# Clicking on the accept button

accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')

accept_button.click()

# Close advert
time.sleep(5)
try:
    close = driver.find_element(By.ID, 'advertClose')
    close.click()
except e.ElementClickInterceptedException:
    pass

# Click on the seasons
time.sleep(3)
dropdown = driver.find_elements(By.CLASS_NAME, 'current') # This is to click on the filter by season dropdown
seasons = dropdown[0]
clubs = dropdown[1]

seasons.click()

# fetch the list of the seasons
season_dropdown = driver.find_element(By.CLASS_NAME, 'dropdownList')
print(len(season_dropdown.text.split()))


# Scroll the dropdown
def scroll_dropdown(web_element: WebElement, origin_point: WebElement):
    """
    This function scrolls the dropdown of the seasons/club dropdown -- AT THE MOMENT

    It takes two arguments:
    web_element: The dropdown element
    origin_point: the last element that was visible

    """
    scroll_distance = 25 # Specifies the distance by which the dropdown will be scrolled

    # I need to find the specified element from which the dropdown will be scrolled. That is the last season.
    if origin_point.is_displayed(): # Checks to see if the last season is presently in view
        print('Element is available')
        driver.execute_script(f"arguments[0].scrollTo(0, {scroll_distance})", web_element)

year = []
def get_season(season: int):
    # season_path = f'//*[@id="mainContent"]/div[2]/div[1]/div/section/div[1]/div[3]/ul/li[{season}]'
    new_path = f'.dropdownList [data-option-index="{season}"]'
    season = driver.find_element(By.CSS_SELECTOR, new_path)
    year.append(season)
    print(season.text)
    season.click()  # This clicks on the season
    time.sleep(5)
    # seasons.click()
    # time.sleep(5)
    return season

# Fetching the Clubs
def get_clubs_list():
    if clubs.is_displayed():
        clubs.click()
        time.sleep(5)
        club_list = driver.find_element(By.CSS_SELECTOR, '.dropdownListContainer [data-dropdown-list="clubs"]').text.split()
        print(return_clubs(club_list))
        time.sleep(3)
        clubs.click()
        time.sleep(3)
        return club_list

def return_clubs(clubs_list: list):
    club_list = clubs_list[2:]
    reserved_words = ['&', 'United', 'City', 'Town', 'Hotspur', 'Ham', 'Wanderers', 'Palace', 'Wednesday', 'Villa', 'Rovers', 'County', 'Forest', 'Athletic', 'Bromwich', 'Albion']
    new_list = []
    for i, j in enumerate(club_list):
        if j in reserved_words and j != '&':
            try:
                if club_list[i - 1] in reserved_words:
                    pass
                elif club_list[i + 1] in reserved_words:
                    new_club_name = f'{club_list[i - 1]} {j} {club_list[i + 1]}'
                    new_list.append(new_club_name)
                else:
                    new_club_name = f'{club_list[i - 1]} {j}'
                    new_list.append(new_club_name)
            except IndexError:
                new_club_name = f'{club_list[i - 1]} {j}'
                new_list.append(new_club_name)

        else:
            try:
                if club_list[i + 1] not in reserved_words:
                    new_list.append(j)
            except IndexError:
                new_list.append(j)
    return new_list

for i in range(0, len(season_dropdown.text.split())):
    try:

        print(f"\n\nWe are currently in the error free zone. We are trying the {i} path\n")
        get_season(i)
        get_clubs_list()
        seasons.click()
        time.sleep(3)
    except e.ElementClickInterceptedException:
        print(f"\n\n We are currently in the error zone. This is the {i} iteration\n")
        scroll_dropdown(season_dropdown, year[-1])
        time.sleep(3)
    # except e.ElementNotInteractableException:
    #     seasons.click()
