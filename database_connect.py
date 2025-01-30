import psycopg2 # importing this to enable me to connect to my PostgreSQL database
connection = psycopg2.connect(
    user='postgres',
    password='Nkemdebe@2024',
    host='localhost',
    port='5432',
    database='postgres'
)

cursor = connection.cursor()