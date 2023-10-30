import sqlite3

conn = sqlite3.connect("bd.sql")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS state(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS city(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        id_state INTEGER,
        FOREIGN KEY (id_state) REFERENCES state (id)
    )
""")

conn.commit()
conn.close()
