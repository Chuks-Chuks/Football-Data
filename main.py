from fetch_data import FetchData
import time
from database_connect import WriteToDatabase
from random import randint
import json
from team_normalisation import TeamNormalisation

print('fine')
def seasons_teams_create():
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
            dat.write_to_table(dat.insert_into_seasons_table, data=(season_id, season, list_for_club))
            fetch.pinpoint_dropdown()[0].click()
            time.sleep(3)
        except fetch.exceptions.ElementClickInterceptedException:
            print(f"\n\n We are currently in the error zone. This is the {season_number} iteration\n")
            fetch.scroll_dropdown(season_dropdown, fetch.year[-1])
            time.sleep(3)


def create_teams():
    f = TeamNormalisation()
    dat = WriteToDatabase()
    print(f.current_season)
    dat.create_table(dat.create_teams_query)
    for i in range(len(f.elements)):
        details = f.automate(i)
        club_name = details[0]
        stadium_name = details[1]
        team_id = details[2][0]
        year_created = details[2][1]
        current_manager = details[3]
        capacity = details[4]
        dat.write_to_table(
            insert_query=dat.insert_into_create_teams,
            data=(
                team_id,
                club_name,
                stadium_name,
                capacity,
                year_created,
                current_manager
            )
        )

create_teams()