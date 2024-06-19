from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
import sqlite3
import uvicorn
import os

app = FastAPI(title="MexiCityNamesApi",
              description="Retrieve cities sorted by their state, Create by: Melchor Ruiz",
              version="1.0.0")

class state(BaseModel):
    id:int
    name:str
    
class city(BaseModel):
    id:int
    name:str
    state:str

@app.get("/states", response_model=list[state], tags=["Cities from Mexico"])
def get_states():
    states = []
    
    conn = sqlite3.connect("bd.sql")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM state')
    data = cursor.fetchall()

    for row in data:
        s = state(id=row[0], name=row[1])
        states.append(s)

    conn.close()
    return states

@app.get("/citys", response_model=list[city], tags=["Cities from Mexico"])
def get_cities(id_state: Union[int, None] = None):
    cities = []
    
    conn = sqlite3.connect("bd.sql")
    cursor = conn.cursor()

    if id_state == None:
        cursor.execute('SELECT c.id, c.name, s.name FROM city AS c INNER JOIN state AS s ON c.id_state = s.id')
    else:
        cursor.execute('SELECT c.id, c.name, s.name, s.id FROM city AS c INNER JOIN state AS s ON c.id_state = s.id WHERE s.id = ?', (id_state,))
    data = cursor.fetchall()

    for row in data:
        s = city(id=row[0], name=row[1], state=row[2])
        cities.append(s)

    conn.close()
    return cities

if (__name__ == "__main__"):
    PORT = os.getenv("PORT", 8000)
    uvicorn.run("main:app", port=PORT, reload=True)
