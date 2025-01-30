import selenium.common.exceptions as e
from selenium import webdriver # Importing this to enable webscraping of the data
from selenium.webdriver.common.by import By
import tkinter as tk
import time
from selenium.webdriver.remote.webelement import WebElement

class FetchData:
    def __init__(self):
        self.root = tk.Tk()
        self.screen_height = self.root.winfo_screenheight()
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.year = []
        self.reserved_words = ['&', 'United', 'City', 'Town', 'Hotspur', 'Ham', 'Wanderers', 'Palace', 'Wednesday', 'Villa',
                          'Rovers', 'County', 'Forest', 'Athletic', 'Bromwich', 'Albion', 'Hove']
        self.driver.get('https://www.premierleague.com/players')
        self.driver.maximize_window()
        self.accept_button()
        self.close_button()
        self.pinpoint_dropdown()[0].click()
        self.exceptions = e

# Clicking on the accept button
    def accept_button(self):
        time.sleep(3)
        accept_button = self.driver.find_element(By.ID, 'onetrust-accept-btn-handler')

        accept_button.click()

    # Close advert
    def close_button(self):
        time.sleep(5)
        try:
            close = self.driver.find_element(By.ID, 'advertClose')
            close.click()
        except self.exceptions.ElementClickInterceptedException:
            pass

    # Click on the seasons
    def pinpoint_dropdown(self):
        """
        This returns a list. The first is the season and the second is the club
        """
        time.sleep(3)
        dropdown = self.driver.find_elements(By.CLASS_NAME, 'current') # This is to click on the filter by season dropdown
        return dropdown

    def season_text(self):
    # fetch the list of the seasons
        season_dropdown = self.driver.find_element(By.CLASS_NAME, 'dropdownList')
        return season_dropdown.text


    # Scroll the dropdown
    def scroll_dropdown(self, web_element: WebElement, origin_point: WebElement):
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
            self.driver.execute_script(f"arguments[0].scrollTo(0, {scroll_distance})", web_element)


    def get_season(self, season: int):
        new_path = f'.dropdownList [data-option-index="{season}"]'
        season = self.driver.find_element(By.CSS_SELECTOR, new_path)
        self.year.append(season)
        print(season.text)
        season.click()  # This clicks on the season
        time.sleep(5)
        return season

    # Fetching the Clubs
    def get_clubs_list(self):
        clubs = self.pinpoint_dropdown()[1]
        if clubs.is_displayed():
            clubs.click()
            time.sleep(5)
            club_list = self.driver.find_element(By.CSS_SELECTOR, '.dropdownListContainer [data-dropdown-list="clubs"]').text.split()
            print(club_list)
            print(self.return_clubs(club_list))
            time.sleep(3)
            clubs.click()
            time.sleep(3)
            return club_list

    def return_clubs(self, clubs_list: list):
        club_list = clubs_list[2:]
        new_list = []
        for i, j in enumerate(club_list):
            if j in self.reserved_words and j != '&': # This checks if the word is a reserved word i.e the complete name of a team
                try:
                    if club_list[i - 1] in self.reserved_words: # this checks if the word before the reserved word is ALSO in the reserved word list
                        pass
                    elif club_list[i + 1] in self.reserved_words: # This checks if the next word is also a reserved word.
                        new_club_name = f'{club_list[i - 1]} {j} {club_list[i + 1]}' # If it is, then combined the word before it, the word itself and also the word after it
                        new_list.append(new_club_name)
                    else: # If it doesn't meet any of the conditions above, trigger this block
                        new_club_name = f'{club_list[i - 1]} {j}' # Add the word before it and call it a day
                        new_list.append(new_club_name)
                except IndexError:
                    new_club_name = f'{club_list[i - 1]} {j}' # if there is an index error simply maintain the else block
                    new_list.append(new_club_name)

            else:
                try:
                    if club_list[i + 1] not in self.reserved_words: # this checks if the next word is in the reserved list
                        # and thus if it is not it simply adds it to the new_list
                        new_list.append(j)
                    else:
                        if club_list[i + 1] == '&' and club_list[i + 2] in self.reserved_words: # This deals specifically with the apersand sign in the name
                            new_club_name = f'{j} {club_list[i + 1]} {club_list[i + 2]} {club_list[i + 3]}' # It adds the word being checked and then also adds the next two words
                            new_list.append(new_club_name)
                except IndexError:
                    new_list.append(j)
        return new_list

