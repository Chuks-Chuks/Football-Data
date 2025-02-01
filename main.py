from fetch_data import FetchData
import time
from database_connect import WriteToDatabase
from random import randint
import json
fetch = FetchData()
dat = WriteToDatabase()
dat.create_table(dat.create_seasons_query)

season_dropdown = fetch.season_text().split()

for season_number in range(0, len(season_dropdown)):
    try:
        print(f"\n\nWe are currently in the error free zone. We are trying the {season_number} path\n")
        season = fetch.get_season(season_number)
        list_for_club = json.dumps(fetch.get_clubs_list())
        print(list_for_club)
        season_id = f'{season.replace("/", "")}{randint(1000, 5000)}'
        # data = (season_id, season , list_for_club)
        dat.write_to_table(dat.insert_into_seasons_table, data=(season_id, season, list_for_club))
        fetch.pinpoint_dropdown()[0].click()
        time.sleep(3)
    except fetch.exceptions.ElementClickInterceptedException:
        print(f"\n\n We are currently in the error zone. This is the {season_number} iteration\n")
        fetch.scroll_dropdown(season_dropdown, fetch.year[-1])
        time.sleep(3)
