import sqlite3

conn = sqlite3.connect('books.sqlite')
print("open database ")
cursor=conn.cursor()
sql_query=""" CREATE TABLE book(
    id interger PRIMARY KEY ,
    topic TEXT NOT NULL,
    title TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL)"""
cursor.execute(sql_query)
conn.close()



