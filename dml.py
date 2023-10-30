import sqlite3
import pandas as pd

conn = sqlite3.connect("bd.sql")
cursor = conn.cursor()

excel = pd.ExcelFile("CPdescarga.xlsx")

paginas = excel.sheet_names

id_state = 1
for pagina in paginas[1:]:
    state_name = pagina.replace("_", " ")
    cursor.execute("INSERT INTO state (name) VALUES (?)", (state_name,))

    cities = []
    df = excel.parse(pagina)
    for city in df["D_mnpio"]:
        if city not in cities:
            cursor.execute("INSERT INTO city (name, id_state) VALUES (?, ?)", (city, id_state))
            cities.append(city)
    id_state += 1

conn.commit()
conn.close()
