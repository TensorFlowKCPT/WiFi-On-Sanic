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
                providers.append(i['name'])
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
        providers = str(providers)
        validproviders = []
        for i in allProviders:
            if i["Name"] in providers:
                validproviders.append(i)
        
        tariffs = []
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
                    tariffs.append({'id':row[0],
                                    'Name':row[1],
                                    'NameEng':row[2],
                                    'Description':row[3],
                                    'Price': row[4],
                                    'PriceOld': row[5],
                                    'Options': json.loads(row[6]),
                                    'Provider': i
                    })
        output = {
                'providers':validproviders,
                'tariffs':tariffs,
                }
        return output
    
    def GetInfoByCityName(cityName:str):
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT id FROM Cities WHERE Name = ?", (cityName,))
            CityId = cursor.fetchone()[0]
            cursor = conn.execute("SELECT id, Name, NameEng, Description, Price, PriceOld, OptionsJSON, idProvider FROM Tariffs WHERE idCity = ?", (CityId,))
            rows = cursor.fetchall()
            tariffs = []
            providers = []
            for row in rows:
                Provider = Database.GetProviderById(row[7])
                providers.append(Provider)
                tariffs.append({'id':row[0],
                                'Name':row[1],
                                'NameEng':row[2],
                                'Description':row[3],
                                'Price': row[4],
                                'PriceOld': row[5],
                                'Options': json.loads(row[6]),
                                'Provider': Provider
                })
            output = {'tariffs':tariffs, 'providers':providers}
            return output
    def GetAllSubdomains():
        with sqlite3.connect("sqlite.sqlite3") as conn:
            cursor = conn.execute("SELECT NameEng FROM Cities")
            rows = cursor.fetchall()
            output = []
            for i in rows:
                output.append(i[0])
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
#print(Database.GetAllSubdomains())