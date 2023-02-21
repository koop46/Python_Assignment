import requests
from f_api import Land


URL = 'http://127.0.0.1:8000'

LÄNDER = []

######################################################################################

def nytt_land(): 

        print("Lägg till nytt land")
        land, fertilitetsgrad = input("Land & fertilitetsgrad: ").split()
        nytt_land = Land(land = land.capitalize(), fertilitetsgrad = float(fertilitetsgrad))

        print(requests.post(f'{URL}/nytt_land', json=nytt_land.dict()))


def favorit(): 

        print("Lägg till favorit")
        
        land = input("Vilket land ska bli ny favorit? ").capitalize()
        for l in LÄNDER:
            if l.land == land:
                ny_favorit = Land(land = l.land, fertilitetsgrad = l.fertilitetsgrad )
        
        print(requests.post(f'{URL}/favorit', json=ny_favorit.dict()))


##########################################################


def visa_topp():

    res = requests.get(f'{URL}/land')
    if res.status_code != 200:
        return
    
    data = res.json()
    data = Land(**data)
    
    print(f"""
{data.land} har högst fertilitet i databasen: {data.fertilitetsgrad} barn/kvinna
    """)


def visa_länder(): 
    
    print("ALLA LÄNDER")
    for l in LÄNDER:
        print(f"--------")
        print(f"{l.land}: {l.fertilitetsgrad} barn/kvinna")

    return LÄNDER
    


def visa_favoriter():

    res_f = requests.get(f'{URL}/favoriter')
    if res_f.status_code != 200:
        return

    favos = res_f.json()
    favoriter = []
    print("\nFAVORITER!")

    for f in favos:
        f = Land(**f)
        print(f"--------")
        print(f"{f.land}: {f.fertilitetsgrad} barn/kvinna")
        favoriter.append(f)
    
    return favoriter


##########################################################

def radera_land(): 

    print("Radera land")
    radera = input("Vilket land ska bort?").capitalize()
    if not isinstance(radera, str):
        print("Måste vara ett land!")
        return


    res = requests.delete(f'{URL}/radera_land/{radera}')
    print(res.json())


def redigera_land():

    print("Uppdatera land")
    land = input("Vilket land ska uppdateras?").capitalize()
    fert = input("Ny fertilitet?")
    
    
    for d in LÄNDER:
        
        if d.land == land and not fert:
            uppdaterad = Land(land = land, fertilitetsgrad = d.fertilitetsgrad)

        elif d.land == land:
            uppdaterad = Land(land = land, fertilitetsgrad = fert)
    

    res = requests.put(f'{URL}/uppdatera_land/{land}', json=uppdaterad.dict())
    print(res.json())


##########################################################

def main():

    global LÄNDER
    LÄNDER = [ Land(**l) for l in requests.get(f'{URL}/länder').json() ]


    print("""
[1]Ny data [2]Visa data [3]Radera data [4]Redigera data [5]Avsluta
""")

    val = input("Välj 1-5\n")
    if not str.isdigit(val):
        print("Måste vara siffra")
        return

    match int(val):
        case 1:
            val_data = int(input("[1]Nytt land & fertilitet [2]Ny favorit"))
            nytt_land() if val_data == 1 else favorit()
        case 2:
            val_data = int(input("[1]Visa alla länder [2]Visa favoriter [3]Visa mest fertil"))            
            visa_länder() if val_data == 1 else visa_favoriter() if val_data == 2 else visa_topp()
        case 3:
            radera_land()
        case 4:
            redigera_land()
        case 5:
            exit()

        case _:
            print("Testa igen")


while __name__ == "__main__":
    main()