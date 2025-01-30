from fetch_data import FetchData
import time

fetch = FetchData()

season_dropdown = fetch.season_text().split()

for season_number in range(0, len(season_dropdown)):
    try:
        print(f"\n\nWe are currently in the error free zone. We are trying the {season_number} path\n")
        fetch.get_season(season_number)
        fetch.get_clubs_list()
        fetch.pinpoint_dropdown()[0].click()
        time.sleep(3)
    except fetch.exceptions.ElementClickInterceptedException:
        print(f"\n\n We are currently in the error zone. This is the {season_number} iteration\n")
        fetch.scroll_dropdown(season_dropdown, fetch.year[-1])
        time.sleep(3)
