import requests
import json
import sqlite3
key2gis = "eedd6882-ab52-4127-a367-69e4286b00bf"
class Database:
    def GetProvidersByAdress(address:str):
        houseid = json.loads(requests.get(f"https://catalog.api.2gis.com/3.0/items/geocode?q={address}&key="+key2gis).content)['result']['items'][0]['id']
        resp = json.loads(requests.get(f"https://catalog.api.2gis.com/2.0/catalog/branch/list?building_id={houseid}&servicing=true&servicing_group=internet&key={key2gis}").content)
        providers = []
        try:
            for i in resp['result']['items']:
                providers.append(str(i['name']).lower())
        except KeyError:
            pass
        return providers
        
            
    def GetAllProvidersFromDB():
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT * FROM Providers")
            rows = cursor.fetchall()
            if not rows:
                return None
            rows = [row for row in rows]
            output = []
            for row in rows:
                output.append({
                    "id" : row[0],
                    "Name": row[1],
                    "NameEng" : row[2],
                    "ImageUrl" : row[3]})
            return output
    def GetProviderById(id:int):
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT * FROM Providers WHERE ID = ?",(id,))
            row = cursor.fetchone()
            if not row:
                return None
            output = {
                "id" : row[0],
                "Name": row[1],
                "NameEng" : row[2],
                "ImageUrl" : row[3]}
            return output
    def GetInfoByAddress(address:str):
        providers = Database.GetProvidersByAdress(address)
        allProviders = Database.GetAllProvidersFromDB()
        
        providers = str(providers).lower()
        print(providers)
        validproviders = []
        for i in allProviders:
            
            if str(i["Name"]).lower() in providers:
                validproviders.append(i)
        
        tariffs = []
        maxtariffcost = 0
        mintariffcost = 99999
        maxtariffinternetspeed = 0
        mintariffinternetspeed = 99999
        city = address.split(',')[0].removeprefix("г ")
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT id FROM Cities WHERE Name = ?", (city,)).fetchone()
            if cursor == None:
                return {
                'providers':validproviders,
                'tariffs':tariffs,
                }
            CityId = cursor[0]
            for i in validproviders:
                cursor = conn.execute("SELECT id, Name, NameEng, Description, Price, PriceOld, OptionsJSON FROM Tariffs WHERE idCity = ? AND idProvider = ?", (CityId, i['id'],))
                rows = cursor.fetchall()
                for row in rows:
                    if row[4] > maxtariffcost:
                        maxtariffcost = row[4]
                    if row[4] < mintariffcost:
                        mintariffcost = row[4]
                    options = json.loads(row[6])
                    if "TV" in options.keys() and 'Channels' in options['TV'].keys():
                        try: 
                            int(options['TV']['Channels'])
                            options['TV']['Channels'] = options['TV']['Channels']+" каналов"
                        except:
                            pass
                    try:
                        if options['Internet']['InternetSpeed']:
                                if int(options['Internet']['InternetSpeed'].removeprefix('до '))>maxtariffinternetspeed:
                                    maxtariffinternetspeed = int(options['Internet']['InternetSpeed'])
                                if int(options['Internet']['InternetSpeed'].removeprefix('до '))<mintariffinternetspeed:
                                    mintariffinternetspeed = int(options['Internet']['InternetSpeed'])
                    except:
                        pass
                    tariffs.append({'id':row[0],
                                    'Name':row[1],
                                    'NameEng':row[2],
                                    'Description':row[3],
                                    'Price': row[4],
                                    'PriceOld': row[5],
                                    'Options': options,
                                    'Provider': i
                    })
        output = {
                'providers':validproviders,
                'tariffs':tariffs,
                'maxtariffprice':maxtariffcost,
                'mintariffprice':mintariffcost,
                'maxtariffinternetspeed':maxtariffinternetspeed,
                'mintariffinternetspeed':mintariffinternetspeed
                }
        return output
    
    def GetAllCities():
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT Name, NameEng FROM Cities")
            rows = cursor.fetchall()
            output = []
            if rows != None:
                for city in rows:
                    output.append([city[0],city[1]])
            output = [output[i:i + 10] for i in range(0, len(output), 10)]
            return output
    def GetRandomTariffByCity(cityName:str):
        with sqlite3.connect("sqlite.sqlite3") as conn:
            row = conn.execute("SELECT id, Name, NameEng, Description, Price, PriceOld, OptionsJSON, idProvider FROM Tariffs WHERE idCity = ? ORDER BY RANDOM() LIMIT 1",(cityName,)).fetchone()
            options = json.loads(row[6])
            if "TV" in options.keys() and 'Channels' in options['TV'].keys():
                try: 
                    int(options['TV']['Channels'])
                    options['TV']['Channels'] = options['TV']['Channels']+" каналов"
                except:
                    pass
            return {'id':row[0],
                                    'Name':row[1],
                                    'NameEng':row[2],
                                    'Description':row[3],
                                    'Price': row[4],
                                    'PriceOld': row[5],
                                    'Options': options,
                                    'Provider': Database.GetProviderById(row[7])
                    }
    def GetInfoByCity(city:str):
        with sqlite3.connect("sqlite.sqlite3") as conn:
            CityId = city['id']
            cursor = conn.execute("SELECT id, Name, NameEng, Description, Price, PriceOld, OptionsJSON, idProvider FROM Tariffs WHERE idCity = ?", (CityId,))
            rows = cursor.fetchall()
            tariffs = []
            providers = []
            maxtariffcost = 0
            mintariffcost = 99999
            maxtariffinternetspeed = 0
            mintariffinternetspeed = 99999
            for row in rows:
                Provider = Database.GetProviderById(row[7])
                if not Provider in providers:
                    providers.append(Provider)
                if row[4] > maxtariffcost:
                    maxtariffcost = row[4]
                if row[4] < mintariffcost:
                    mintariffcost = row[4]
                options = json.loads(row[6])
                if "TV" in options.keys() and 'Channels' in options['TV'].keys():
                    try: 
                        int(options['TV']['Channels'])
                        options['TV']['Channels'] = options['TV']['Channels']+" каналов"
                    except:
                        pass
                try:
                    if options['Internet']['InternetSpeed']:
                            if int(options['Internet']['InternetSpeed'].removeprefix('до '))>maxtariffinternetspeed:
                                maxtariffinternetspeed = int(options['Internet']['InternetSpeed'])
                            if int(options['Internet']['InternetSpeed'].removeprefix('до '))<mintariffinternetspeed:
                                mintariffinternetspeed = int(options['Internet']['InternetSpeed'])
                except:
                    pass
                tariffs.append({'id':row[0],
                                'Name':row[1],
                                'NameEng':row[2],
                                'Description':row[3],
                                'Price': row[4],
                                'PriceOld': row[5],
                                'Options': options,
                                'Provider': Provider
                })
            output = {
                'providers':providers,
                'tariffs':tariffs,
                'maxtariffprice':maxtariffcost,
                'mintariffprice':mintariffcost,
                'maxtariffinternetspeed':maxtariffinternetspeed,
                'mintariffinternetspeed':mintariffinternetspeed
                }
            return output
    def GetAllSubdomains():
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT NameEng FROM Cities")
            rows = cursor.fetchall()
            output = []
            for i in rows:
                output.append(i[0])
        return output
    def GetCityByName(Name):
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT * FROM Cities Where Name = ?",(Name,))
            row = cursor.fetchone()
            if row:
                output = {
                    'id' : row[0],
                    'Name' : row[1],
                    'NameEng': row[2]
                }
            else: output = None
        return output
    def GetCityBySubdomain(subdomain):
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT * FROM Cities Where NameEng = ?",(subdomain,))
            row = cursor.fetchone()
            if row:
                output = {
                    'id' : row[0],
                    'Name' : row[1],
                    'NameEng': row[2]
                }
            else: output = None
        return output
    
class PromoDatabase:
    def StartDatabase():
        with sqlite3.connect("promo.db") as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS Users (
                        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        FIO TEXT NOT NULL,
                        Login TEXT NOT NULL,
                        Password TEXT NOT NULL,
                        PhoneNumber TEXT NOT NULL
                    )
                """)
    def LoginUser(Login,Password):
        with sqlite3.connect("promo.db") as conn:
            cursor = conn.execute("SELECT Login FROM Users Where Login = ? AND Password = ?",(Login,Password,))
            row = cursor.fetchone()
            if not row:
                cursor = conn.execute("SELECT Login FROM Users Where PhoneNumber = ? AND Password = ?",(Login,Password,))
                row = cursor.fetchone()
            if row == None:
                return False
            return row[0]
    def GetUserInfo(Login):
        with sqlite3.connect("promo.db") as conn:
            cursor = conn.execute("SELECT * FROM Users Where Login = ?",(Login,))
            row = cursor.fetchone()
            if not row:
                return False
            return {'id':row[0],
                    'FIO': row[1],
                    'Login':row[2],
                    'PhoneNumber':row[4]
                    }
PromoDatabase.StartDatabase()