import requests
from f_api import Land


URL = 'http://127.0.0.1:8000'

LÄNDER = []

######################################################################################

def nytt_land(): 

        print("Lägg till nytt land")
        land, fertilitetsgrad = input("Land & fertilitetsgrad: ").split()
        nytt_land = Land(land = land.capitalize(), fertilitetsgrad = float(fertilitetsgrad))

        return requests.post(f'{URL}/nytt_land', json=nytt_land.dict())


def ny_favorit(): 

        print("Lägg till favorit")
        
        land = input("Vilket land ska bli ny favorit? ").capitalize()
   
        for l in LÄNDER:
            if l.land == land:
                ny_favorit = Land(land = l.land, fertilitetsgrad = l.fertilitetsgrad )
        
        requests.post(f'{URL}/favorit', json=ny_favorit.dict())


##########################################################


def visa_topp():

    res = requests.get(f'{URL}/land')
    
    top = res.json()
    top = Land(**top)
    
    print(f"""
{top.land} har högst fertilitet i databasen: {top.fertilitetsgrad} barn/kvinna
    """)


def visa_länder(): 
    
    print("ALLA LÄNDER")
    for l in LÄNDER:
        print(f"--------")
        print(f"{l.land}: {l.fertilitetsgrad} barn/kvinna")
    

def visa_favoriter():

    res_f = requests.get(f'{URL}/favoriter')
  
    favos = res_f.json()
    print("\nFAVORITER!")

    for f in favos:
        f = Land(**f)
        print(f"--------")
        print(f"{f.land}: {f.fertilitetsgrad} barn/kvinna")
    


##########################################################

def radera_land(): 

    radera = input("Vilket land ska bort?").capitalize()
  

    return requests.delete(f'{URL}/radera_land/{radera}')


def redigera_land():

    print("Uppdatera land")
    land = input("Vilket land ska uppdateras?").capitalize()
    fert = input("Ny fertilitet: ")
    nytt_land = input("Döpa om landet: ").capitalize()
       
    for l in LÄNDER:
        
        if l.land == land and not fert:
            uppdaterad = Land(land = nytt_land, fertilitetsgrad = l.fertilitetsgrad)

        elif l.land == land and not nytt_land:
            uppdaterad = Land(land = land, fertilitetsgrad = float(fert))

        elif l.land == land:
            uppdaterad = Land(land = nytt_land, fertilitetsgrad = float(fert) )
    

    return requests.put(f'{URL}/uppdatera_land/{land}', json=uppdaterad.dict())


##########################################################


def main():

    global LÄNDER
    LÄNDER = [ Land(**l) for l in requests.get(f'{URL}/länder').json() ]


    print("""
[1]Ny data [2]Visa data [3]Radera data [4]Redigera data [5]Avsluta
""")

    val = int(input("Välj 1-5\n"))
 
    match int(val):
        case 1:
            val_data = int(input("[1]Nytt land & fertilitet [2]Ny favorit"))
            nytt_land() if val_data == 1 else ny_favorit()
     
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
