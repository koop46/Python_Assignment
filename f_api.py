import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel



########### Anropar databas
def db(query, *args):
    conn = sqlite3.connect("fertilitet.db")
    cur = conn.cursor()
    res = cur.execute(query, args)
    datan = res.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return datan


class Land(BaseModel):
    id: int = None
    land: str
    fertilitetsgrad: float


app = FastAPI()


@app.get("/land")
def get_land():

    query = "SELECT Land, MAX(Fertilitetsgrad) FROM Fertilitet"
    land = db(query)
    
    for l in land:
        land, fertilitetsgrad = l
    
    return Land(land=land, fertilitetsgrad=fertilitetsgrad)


@app.get("/länder")
def get_länder():
    query = "SELECT * FROM Fertilitet"
    länder = db(query)

    l_länder = []
    for l in länder:
        id, land, fertilitetsgrad = l
        l_länder.append(Land(id=id, land=land, fertilitetsgrad=fertilitetsgrad))
    
    return l_länder


@app.get("/favoriter")
def get_favoriter():
    f_query = "Select * FROM Favoriter"
    favos = db(f_query)

    f_länder = []
    for f in favos:
        id, land, fertilitetsgrad = f
        f_länder.append(Land(id=id, land=land, fertilitetsgrad=fertilitetsgrad))
   
    return f_länder



@app.post("/nytt_land")
def post_land(land: Land):
    query = """
    INSERT INTO Fertilitet(Land, Fertilitetsgrad)
    VALUES ( ?, ?)
    
    """
    db(query, land.land, land.fertilitetsgrad)
 

@app.post("/favorit")
def post_data(land: Land):
    table_query = """
    CREATE TABLE IF NOT EXISTS Favoriter(
        id INTEGER PRIMARY KEY,
        land TEXT NOT NULL,
        fertilitetsgrad REAL NOT NULL
    );
     """

    value_query = """
    INSERT INTO Favoriter(land, fertilitetsgrad)
    VALUES (?,?)
    
    """
    
    db(table_query)
    db(value_query, land.land, land.fertilitetsgrad)

@app.delete("/radera_land/{land}")
def radera_land(land):
    query = "DELETE FROM Fertilitet where Land = ?"
    db(query, land)


@app.put("/uppdatera_land/{land}")
def uppdatera_land(land, nytt_land: Land):

    query = """
    UPDATE Fertilitet
    SET Land = ?, Fertilitetsgrad = ?
    WHERE Land = ?
    """

    db(query, nytt_land.land, nytt_land.fertilitetsgrad, land)



