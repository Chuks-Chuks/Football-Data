for season_number in range(0, len(season_dropdown.text.split())):
    try:
        print(f"\n\nWe are currently in the error free zone. We are trying the {season_number} path\n")
        get_season(season_number)
        get_clubs_list()
        seasons.click()
        time.sleep(3)
    except e.ElementClickInterceptedException:
        print(f"\n\n We are currently in the error zone. This is the {season_number} iteration\n")
        scroll_dropdown(season_dropdown, year[-1])
        time.sleep(3)
