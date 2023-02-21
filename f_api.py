import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel



########### Anropar databas
def call_db(query, *args):
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
    data = call_db(query)
    
    for d in data:
        land, fertilitetsgrad = d
    
    return Land(land=land, fertilitetsgrad=fertilitetsgrad)


@app.get("/länder")
def get_länder():
    query = "SELECT * FROM Fertilitet"
    data = call_db(query)

    l_länder = []
    for d in data:
        id, land, fertilitetsgrad = d
        l_länder.append(Land(id=id, land=land, fertilitetsgrad=fertilitetsgrad))
    
    return l_länder


@app.get("/favoriter")
def get_favoriter():
    f_query = "Select * FROM Favoriter"
    data1 = call_db(f_query)

    f_länder = []
    for l in data1:
        id, land, fertilitetsgrad = l
        f_länder.append(Land(id=id, land=land, fertilitetsgrad=fertilitetsgrad))
    return f_länder



@app.post("/nytt_land")
def post_land(land: Land):
    query = """
    INSERT INTO Fertilitet(Land, Fertilitetsgrad)
    VALUES ( ?, ?)
    
    """
    call_db(query, land.land, land.fertilitetsgrad)
    return f"""
Ny data
    {land.land}: {land.fertilitetsgrad}
    """


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
    
    call_db(table_query)
    call_db(value_query, land.land, land.fertilitetsgrad)
    return f"{land.land} ny favorit"

@app.delete("/radera_land/{land}")
def radera_land(land):
    query = "DELETE FROM Fertilitet where Land = ?"
    call_db(query, land)
    return f"Bort med {land}"


@app.put("/uppdatera_land/{land}")
def uppdatera_land(land, nytt_land: Land):

    query = """
    UPDATE Fertilitet
    SET Land = ?, Fertilitetsgrad = ?
    WHERE Land = ?
    """

    call_db(query, nytt_land.land, nytt_land.fertilitetsgrad, land)

    return f"Uppdaterat {land}"


