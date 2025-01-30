import psycopg2 # importing this to enable me to connect to my PostgreSQL database

class WriteToDatabase:
    def __init__(self):
        self.connection = psycopg2.connect(
                user='postgres',
                password='Nkemdebe@2024',
                host='localhost',
                port='5432',
                database='postgres'
            )
        self.cursor = self.connection.cursor()

