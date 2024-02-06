import json
import sqlite3

import requests
import yoomoney

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
                        Mail TEXT NOT NULL,
                        CardNumber TEXT NOT NULL
                    )
                """)
            conn.execute("""CREATE TABLE IF NOT EXISTS Deals (
                        ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        DealId INT NOT NULL,
                        LeadId INT NOT NULL,
                        OwnerId INT NOT NULL,
                        IsPayed Boolean NOT NULL,
                        PaymentId TEXT,
                        Cache TEXT
                    )
                """)
            conn.execute("""INSERT OR IGNORE INTO Users(ID,FIO,Login,Password,Mail,CardNumber) VALUES ('1','Tester Vladislav Tkachuk','TEST','TEST','72vladvlad72@gmail.com','4100116075156746')""")
            conn.execute("""INSERT OR IGNORE INTO Users(ID,FIO,Login,Password,Mail,CardNumber) VALUES ('2','Tester Vladislav Belan','TEST1','TEST','vladik008481@gmail.com','4100116075156747')""")
        with sqlite3.connect("cache.db") as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS Cache (
                        LeadId INT NOT NULL PRIMARY KEY,
                        DealId INT NOT NULL,
                        CacheJSON TEXT
                    )
                """)
    def CacheAllDeals():
        alldeals = []
        with sqlite3.connect("promo.db") as promo:
            cursor = promo.execute("SELECT * FROM Deals")
            rows = cursor.fetchall()
            for row in rows:
                url = "https://on-wifi.bitrix24.ru/rest/1/6c7x0i0n05ww6zmc/crm.lead.list.json"
                data = {
                    'filter[ID]': row[2]
                }
                response = requests.post(url, data=data)
                if response.json()['result']:
                    leadInfo = response.json()['result'][0]
                    url = "https://on-wifi.bitrix24.ru/rest/1/6c7x0i0n05ww6zmc/crm.contact.get.json"
                    data = {
                        'id': leadInfo['CONTACT_ID']
                    }
                    response = requests.post(url, data=data)
                    if 'PHONE' in response.json()['result'].keys():
                        leadInfo['CONTACT_ID'] = response.json()['result']['PHONE'][0]['VALUE']
                    else:
                        leadInfo['CONTACT_ID'] = 'Нет номера'
                url = "https://on-wifi.bitrix24.ru/rest/1/6c7x0i0n05ww6zmc/crm.deal.list.json"
                data = {
                    'filter[ID]': row[1]
                }
                dealResp = requests.post(url, data=data)
                if len(dealResp.json()['result']):
                    dealInfo = dealResp.json()['result'][0]
                    if dealInfo['STAGE_ID'] in PromoDatabase.deal_stages.keys():
                        dealInfo['STAGE_ID'] = PromoDatabase.deal_stages[dealInfo['STAGE_ID']]
                    else:
                        dealInfo['STAGE_ID'] = 'В работе'
                    newdict = {'leadInfo':leadInfo, "dealInfo":dealInfo}
                    if row[4]:
                        if row[5]:
                            newdict['PaymentInfo'] = yoomoney.GetPayout(row[5])
                        else: newdict['PaymentInfo'] = 'Payed, but no info'
                    
                    alldeals.append([row[2],row[1],newdict])
        with sqlite3.connect('cache.db') as cache:
            for deal in alldeals:
                cachednow = cache.execute('SELECT * FROM Cache WHERE LeadId = ? AND DealId = ?',(deal[0],deal[1],)).fetchone()
                if cachednow:
                    cache.execute('UPDATE Cache SET CacheJSON = ? WHERE LeadId = ? AND DealId = ?',(json.dumps(deal[2]),deal[0],deal[1],))
                else:
                    cache.execute('INSERT INTO Cache(LeadId,DealId,CacheJSON) VALUES (?,?,?)',(deal[0],deal[1],json.dumps(deal[2]),))

    def LoginUser(Login,Password):
        with sqlite3.connect("promo.db") as conn:
            cursor = conn.execute("SELECT Login FROM Users Where Login = ? AND Password = ?",(Login,Password,))
            row = cursor.fetchone()
            if not row:
                cursor = conn.execute("SELECT Login FROM Users Where Mail = ? AND Password = ?",(Login,Password,))
                row = cursor.fetchone()
            if row == None:
                return False
            return row[0]

    def GetUserInfoByMail(Mail:str):
        with sqlite3.connect("promo.db") as conn:
            cursor = conn.execute("SELECT * FROM Users Where Mail = ?",(Mail,))
            row = cursor.fetchone()
            if not row:
                return False
            output = {'id':row[0],
                    'FIO': row[1],
                    'Login':row[2],
                    'Mail':row[4],
                    'CardNumber':row[5]
                    }
            return output
    def UpdateUserPassword(newpassword:str, user_id:str):
        with sqlite3.connect("promo.db") as conn:
            conn.execute("UPDATE Users SET Password = ? Where ID = ?",(newpassword, user_id,))

    def UpdateUserProfile(login, Mail, Fio, Card,Password):
        with sqlite3.connect("promo.db") as conn:
            conn.execute("UPDATE Users SET Mail = ?, FIO = ?, CardNumber = ?, Password = ? Where Login = ?",(Mail, Fio, Card, Password, login,))

    def GetUserInfo(Login):
        with sqlite3.connect("promo.db") as conn:
            cursor = conn.execute("SELECT * FROM Users Where Login = ?",(Login,))
            row = cursor.fetchone()
            if not row:
                return False
            output = {'id':row[0],
                    'FIO': row[1],
                    'Login':row[2],
                    'Password':row[3],
                    'Mail':row[4],
                    'CardNumber':row[5]
                    }
            return output

    def CreatePartnerLead(UserLogin, Name, Phone, Address):
        user = PromoDatabase.GetUserInfo(UserLogin)
        if not user:
            return ["unauthorized",401]
        
        url = "https://on-wifi.bitrix24.ru/rest/11940/pn37z1pw2mxrg7dz/crm.lead.add.json"
        data = {
            "fields[TITLE]": "Лид с сайта on-wifi.ru от партнера "+ user['FIO'],
            "fields[NAME]": Name,
            "fields[PHONE][0][VALUE]": Phone,
            "fields[ADDRESS]": Address,
        }
        response = requests.post(url, data=data)
        lead_id = response.json()['result']
        
        url = "https://on-wifi.bitrix24.ru/rest/1/6c7x0i0n05ww6zmc/crm.deal.list.json"
        data = {
            'filter[LEAD_ID]': lead_id,
            'select[]': 'ID'
        }
        response = requests.post(url, data=data)
        deal_id = response.json()['result'][0]['ID']
        newdeal = (deal_id, lead_id, user['id'],False,)
        with sqlite3.connect("promo.db") as conn:
            conn.execute("INSERT INTO Deals(DealId,LeadID,OwnerId,IsPayed) Values(?,?,?,?)",newdeal)
            
        PromoDatabase.CacheOneDeal(newdeal[0],newdeal[1],newdeal[2],newdeal[3])
        return ['ok',200]
    
    def CacheOneDeal(deal_id,lead_id, user_id, PaymentId):
        alldeals = []
        with sqlite3.connect("promo.db") as promo:
                url = "https://on-wifi.bitrix24.ru/rest/1/6c7x0i0n05ww6zmc/crm.lead.list.json"
                data = {
                    'filter[ID]': lead_id
                }
                response = requests.post(url, data=data)
                if response.json()['result']:
                    leadInfo = response.json()['result'][0]
                url = "https://on-wifi.bitrix24.ru/rest/1/6c7x0i0n05ww6zmc/crm.deal.list.json"
                data = {
                    'filter[ID]': deal_id
                }
                response = requests.post(url, data=data)
                if len(response.json()['result']):
                    dealInfo = response.json()['result'][0]
                    if dealInfo['STAGE_ID'] in PromoDatabase.deal_stages.keys():
                        dealInfo['STAGE_ID'] = PromoDatabase.deal_stages[dealInfo['STAGE_ID']]
                    else:
                        dealInfo['STAGE_ID'] = 'В работе'
                    newdict = {'leadInfo':leadInfo, "dealInfo":dealInfo}
                    
                    if PaymentId:
                        newdict['PaymentInfo'] = yoomoney.GetPayout(PaymentId)
                    alldeals.append([lead_id,deal_id,newdict])
        with sqlite3.connect('cache.db') as cache:
            for deal in alldeals:
                cachednow = cache.execute('SELECT * FROM Cache WHERE LeadId = ? AND DealId = ?',(deal[0],deal[1],)).fetchone()
                if cachednow:
                    cache.execute('UPDATE Cache SET CacheJSON = ? WHERE LeadId = ? AND DealId = ?',(json.dumps(deal[2]),deal[0],deal[1],))
                else:
                    cache.execute('INSERT INTO Cache(LeadId,DealId,CacheJSON) VALUES (?,?,?)',(deal[0],deal[1],json.dumps(deal[2]),))
    
    def CreatePayout(value:int, CardNumber:str, description:str):
        try:return yoomoney.CreatePayout(value, CardNumber, description,'None')
        except Exception as ex:return [ex,500] 
    
    def MarkDealAsPayed(DealId, payout_id):
        with sqlite3.connect("promo.db") as conn:
            res = conn.execute("SELECT PaymentId FROM Deals WHERE DealId = ?",(DealId,)).fetchone()
            if not res:
                return FileNotFoundError
            elif not res[0]:
                return Exception
            conn.execute("UPDATE Deals SET IsPayed = ?, PaymentId = ? WHERE DealId = ?",(True,payout_id, DealId,))
    
    def CreateAllPartnerPayout(UserLogin):
        user = PromoDatabase.GetUserInfo(UserLogin)
        if not user:
            return ["unauthorized",401]
        Deals = list(PromoDatabase.GetPartnerFinishedLeads(UserLogin)[0])
        
        description = "Выплата партнеру " + user['FIO'] + " по сделкам:\n"
        value = 0
        accepedDeals = []
        for deal in Deals:
            description+=str(deal['leadInfo']['ID'])+":"+str(deal['dealInfo']['ID'])
            value += 100 #TODO Тут деньги
            PromoDatabase.MarkDealAsPayed(deal['dealInfo']['ID'], None)
            accepedDeals.append([deal['dealInfo']['ID'],deal['leadInfo']['ID']])
        try:
            if value == 0:
                return ['Cannot pay 0',401]
            res = yoomoney.CreatePayout(value,user['CardNumber'],description,user['Login'])
            if res:
                for i in accepedDeals:
                    PromoDatabase.MarkDealAsPayed(i[0], res['id'])
                    PromoDatabase.CacheOneDeal(i[0], i[1], user['id'], res['id'])
            return [res,200]
        except Exception as ex:return [ex,500] 
    
    #TODO Спросить и сделать количество бабок
    def CreateOnePartnerPayout(DealId,UserLogin):
        user = PromoDatabase.GetUserInfo(UserLogin)
        if not user:
            return ["unauthorized",401]
        Deal = dict(PromoDatabase.GetPartnerDeal(DealId, UserLogin)[0])
        if 'dealInfo' in Deal.keys() and Deal['dealInfo']['STAGE_ID'] != 'Подключен':
            return ["Сделка не завершена или не существует",403]
        PromoDatabase.MarkDealAsPayed(Deal['dealInfo']['ID'], None)
        try:
            with sqlite3.connect("promo.db") as conn:
                res = conn.execute("SELECT IsPayed FROM Deals WHERE DealId = ?",(DealId,)).fetchone()
                if not res:
                    return ['Deal not found',404] 
                elif res[0]:
                    return ['Deal already payed',403] 
            
            res = yoomoney.CreatePayout(100,user['CardNumber'],f'Выплата партнеру {user["FIO"]} по лиду {Deal["leadInfo"]["ID"]}:{Deal["dealInfo"]["ID"]}',user['Login'])
            PromoDatabase.MarkDealAsPayed(Deal['dealInfo']['ID'], res['id'])
            PromoDatabase.CacheOneDeal(Deal['dealInfo']['ID'], Deal['leadInfo']['ID'], user['id'],res['id'])
            return res
        except Exception as ex:return [ex,500] 
    deal_stages = { "NEW" :"Новая",
                    "PREPARATION" : "В работе",
                    "PREPAYMENT_INVOICE": "В работе",
                    "EXECUTING" : "Назначена",
                    "LOSE" : "Отказ",
                    "WON" : "Подключен"}
    
    def GetPartnerDeal(DealId, Login):
        user = PromoDatabase.GetUserInfo(Login)
        if not user:
            return ["unauthorized",401]
        with sqlite3.connect("cache.db") as conn:
            cursor = conn.execute("SELECT CacheJSON FROM Cache WHERE DealId = ?",(DealId,))
            row = cursor.fetchone()
            if not row:
                return ['NotFound',404]
            return [json.loads(row[0]),200]
    
    def GetPartnerFinishedLeads(UserLogin):
        user = PromoDatabase.GetUserInfo(UserLogin)
        if not user:
            return ["unauthorized",401]
        output = []
        with sqlite3.connect("promo.db") as conn:
            rows = conn.execute("SELECT LeadId, DealId FROM Deals Where OwnerId = ? AND IsPayed = ?",(user['id'],False,)).fetchall()
            with sqlite3.connect("cache.db") as cache:
                for row in rows:
                    res = cache.execute("SELECT CacheJSON FROM Cache Where LeadId = ? AND DealId = ?",(row[0],row[1])).fetchone()
                    if res:
                        res = json.loads(res[0])
                        if res['dealInfo']['STAGE_ID'] == 'Подключен':
                            output.append(res)
        return [output, 200]
    
    def GetPartnerLeads(UserLogin):
        user = PromoDatabase.GetUserInfo(UserLogin)
        if not user:
            return ["unauthorized",401]
        output = []
        with sqlite3.connect("promo.db") as conn:
            cursor = conn.execute("SELECT LeadId, DealId, IsPayed, PaymentId FROM Deals Where OwnerId = ?",(user['id'],))
            rows = cursor.fetchall()
            with sqlite3.connect("cache.db") as cache:
                for row in rows:
                    res = cache.execute("SELECT CacheJSON FROM Cache Where LeadId = ? AND DealId = ?",(row[0],row[1])).fetchone()
                    if res:
                        output.append(json.loads(res[0]))
        return [output, 200]

PromoDatabase.StartDatabase()