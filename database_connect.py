import psycopg2 # importing this to enable me to connect to my PostgreSQL database


class WriteToDatabase:
    create_seasons_query = """
    CREATE TABLE IF NOT EXISTS seasons_teams (
        season_id TEXT PRIMARY KEY,
        season TEXT,
        teams JSONB
    )
    """
    insert_into_seasons_table = """
    INSERT INTO seasons_teams (season_id, season, teams) VALUES (%s, %s, %s)
    """

    create_teams_query = """
    CREATE TABLE IF NOT EXISTS teams (
        team_id TEXT PRIMARY KEY,
        team TEXT,
        stadium TEXT,
        capacity INTEGER,
        year_created INTEGER,
        current_manager TEXT
    )
    """

    insert_into_create_teams = """
        INSERT INTO teams (team_id, team, stadium, capacity, year_created, current_manager) VALUES (%s, %s, %s, %s, %s, %s)
        """

    create_managers_query = """
    CREATE TABLE IF NOT EXISTS managers (
        manager_id TEXT PRIMARY KEY,
        manager_name TEXT,
        season TEXT REFERENCES season_teams(season) ON UPDATE CASCADE
    )
    """
    def __init__(self):
        self.connection = psycopg2.connect(
                user='postgres',
                password='Nkemdebe@2024',
                host='localhost',
                port='5432',
                database='football'
            )
        self.cursor = self.connection.cursor()

    def create_table(self, create_table_sq):
        # try:
        self.cursor.execute(create_table_sq)
        self.connection.commit()
        print('table created successfully')

    def write_to_table(self, insert_query, data):
        self.cursor.execute(insert_query, data)
        self.connection.commit()

    def drop_table(self, table_name):
        drop_table_query = f"""
            DROP TABLE IF EXIST {table_name} 
            """
        self.cursor.execute(drop_table_query)
        self.connection.commit()

