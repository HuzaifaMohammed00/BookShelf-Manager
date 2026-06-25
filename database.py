import sqlite3

conn = sqlite3.connect("book.db")
cur = conn.cursor()


cur.execute(
    "create table if not exists author (id integer not null primary key autoincrement ,name text)"
)
cur.execute(
    "create table if not exists Book (id integer not null primary key autoincrement ,title text not null,author_id integer,price integer,amount integer,available text)"
)
conn.commit()
conn.close()
