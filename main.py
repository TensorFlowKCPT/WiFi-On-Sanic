from sanic import Sanic, response, HTTPResponse, json, redirect, html, file
from sanic.response import text, html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from Database import Database, PromoDatabase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from sanic_session import Session
import subprocess
from threading import Thread
import pytz
import random
import string



app = Sanic("Wifi-On")

local_link = "localhost:3000"
env = Environment(
    loader=FileSystemLoader('templates'),  # Папка с шаблонами
    autoescape=select_autoescape(['html', 'xml'])
)
app.static("/static/", "./st/")

cacheAdr = {}
cacheCities = {}

Session(app)

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

#region /index
@app.route("/")
async def index(request):
    data = {}
    data['City'] = {'Name':'Москва', 'NameEng': 'moskva','id':416}
    
    data['Cities'] = Database.GetAllCities()
    host = request.headers.get('host')
    subdomain = host.split('.')[0].removeprefix('https://')
    if host!=local_link and subdomain!="on-wifi" and subdomain!="www" :
        data['City'] = Database.GetCityBySubdomain(subdomain)
    data['Providers'] = Database.GetInfoByCity(data['City'])['providers']
    data['RandTariffs'] = []
    for i in range(10):
        data['RandTariffs'].append(Database.GetRandomTariffByCity(data['City']['id']))
    data['host'] = host
    
    template = env.get_template('main.html')
    rendered_html = template.render(data=data)
    return html(rendered_html)
#endregion

#region /promo
@app.post("/login")
async def login(request):
    loggedin = PromoDatabase.LoginUser(request.json.get('login'),request.json.get('password'))
    if loggedin:
        request.ctx.session['login'] = loggedin
        request.ctx.session['timeZone'] = request.json.get('timeZone')
    return json({'status':loggedin})

@app.post("/pay_one")
async def pay_one(request):
    login = request.ctx.session.get('login')
    DealId = request.json.get('DealId')
    res = PromoDatabase.CreateOnePartnerPayout(DealId, login)
    return json(res)

@app.post("/pay_all")
async def pay_all(request):
    login = request.ctx.session.get('login')
    res = PromoDatabase.CreateAllPartnerPayout(login)
    return json(res)

@app.get("/auth")
async def auth(request):
    request.ctx.session['login'] = None
    data = {}
    template = env.get_template('auth.html')
    rendered_html = template.render(data=data)
    return html(rendered_html)

@app.get("/recovery")
async def recovery(request):
    data = {}
    template = env.get_template('recovery.html')
    rendered_html = template.render(data=data)
    return html(rendered_html)


@app.post("/updateProfile")
async def updateProfile(request):
    login = request.ctx.session.get('login')
    Mail = request.json.get('Mail')
    Fio = request.json.get('FIO')
    Card = request.json.get('Card')
    Password = request.json.get('Password')
    if login and Mail and Fio and Card and Password:
        result = PromoDatabase.UpdateUserProfile(login, Mail, Fio, Card,Password)
    else:
        return json({'result': 'error'},status=403)
    return json({'result': 'ok'},status=200)

@app.post("/send_partner_lead")
async def send_partner_lead(request):
    login = request.ctx.session.get('login')
    Name = request.json.get('Name')
    Phone = request.json.get('Phone')
    Address = request.json.get('Address')
    if login and Name and Phone and Address:
        result = PromoDatabase.CreatePartnerLead(login, Name, Phone, Address)
    else:
        return json({'result': 'error'},status=403)
    return json({'result': result[0]},status=result[1])

recoverydict = {}

@app.post("/send_recovery_email")
async def send_recovery_email(request):
    user = PromoDatabase.GetUserInfoByMail(request.json.get('email'))
    if not user:
        return json("usernotfound",status=404)
    recoveryPassword = generate_random_string(8)
    request.ctx.session['recovery'] = str(user['id'])+'%'+str(user['Mail'])
    recoverydict[str(datetime.now().hour)+'%'+str(user['id'])+'%'+str(user['Mail'])] = recoveryPassword
    #Вот здесь нужно будет отправить письмо, пока что выводится просто так
    #sendRecoveryEmail(user['Mail'],recoveryPassword) например вот так
    print(recoveryPassword)
    print(recoveryPassword)
    print(recoveryPassword)
    return json('ok',status=200)

@app.post("/recovery_update_password")
async def recovery_update_password(request):
    newpassword = request.json.get('password')
    recovery = request.ctx.session.get('recovery')
    if not str(datetime.now().hour)+'%'+recovery in recoverydict.keys():
        return json('Login Time-out',status=440)
    request.ctx.session['recovery'] = None
    PromoDatabase.UpdateUserPassword(newpassword,str(recovery).split('%')[0])
    return json('ok',status=200)

@app.post("/send_recovery_code")
async def send_recovery_password(request):
    code = request.json.get('code')
    
    if not code:
        return json('nocode',status=400)
    
    recovery = request.ctx.session.get('recovery')
    if not recovery:
        return json('norecovery',status=404)
    
    recoveryPassword = recoverydict[str(datetime.now().hour)+'%'+recovery]
    
    if recoveryPassword == code:
        return json('ok',status=200)
    else: 
        return json('incorrectcode',status=400)

@app.get("/promo")
async def promo(request):
    login = request.ctx.session.get('login')
    userinfo = PromoDatabase.GetUserInfo(login)
    if not login or not userinfo:
        return redirect('/auth')
    data = {}
    data['userinfo'] = userinfo
    data['PartnerLeads'] = []
    leads = PromoDatabase.GetPartnerLeads(login)
    timezone = request.ctx.session.get('timeZone')
    if leads[1] == 200:
        for i in leads[0]:
            date_time = datetime.strptime(i['leadInfo']['DATE_CREATE'],'%Y-%m-%dT%H:%M:%S%z')
            date_time = date_time
            i['leadInfo']['DATE_CREATE'] = date_time.astimezone(pytz.timezone(timezone)).strftime('%d.%m %H:%M')
            data['PartnerLeads'].append(i)
        
    template = env.get_template('promo.html')
    rendered_html = template.render(data=data)
    return html(rendered_html)
#endregion
#region /tariffs
@app.post("/get_tariffs")
async def get_tariffs(request):
    
    MinTP = request.json.get('MinTP')
    if not MinTP:
        MinTP = 0
    MaxTP=request.json.get('MaxTP')
    if not MaxTP:
        MaxTP = 9999
    MinTIS=request.json.get('MinTIS')
    if not MinTIS:
        MinTIS = 0
    MaxTIS=request.json.get('MaxTIS')
    if not MaxTIS:
        MaxTIS = 9999
    activeProviders=request.json.get('activeProviders')
    if not activeProviders:
        activeProviders = []
    activeOptions=request.json.get('activeOptions')
    if not activeOptions:
        activeOptions = []
    page=int(request.json.get('page'))
    if not page:
        page = 1
    adr= request.json.get('adr')
    cityadd = request.json.get('cityadd')
    if cityadd:
        cityadd = cityadd.split(' ')[-1]
    host = request.headers.get('host')
    data = {}
    subdomain = host.split('.')[0].removeprefix('https://')
    if host!=local_link and subdomain!="on-wifi" and subdomain!="www":
        city = Database.GetCityBySubdomain(subdomain)
        data['City']= city
    else:
        city = {'Name':'Москва', 'NameEng': 'moskva','id':416}
        data['City']= city
    if adr:
        try: 
            data = cacheAdr[adr].copy()
        except KeyError:
            data = Database.GetInfoByAddress(adr)
            cacheAdr[adr] = data.copy()
    elif cityadd:
        try:
            data = cacheCities[cityadd].copy()
        except KeyError:
            data = Database.GetInfoByCity(Database.GetCityByName(cityadd))
            cacheCities[cityadd] = data.copy()
    else:
        try:
            data = cacheCities[city['Name']].copy()
        except KeyError:
            data = Database.GetInfoByCity(city)
            cacheCities[city['Name']] = data.copy()
    viabletariffs = []
    for tariff in data['tariffs'].copy():
        if 'Internet' in tariff['Options'].keys():
            if ((tariff['Provider']['Name'] in activeProviders or len(activeProviders) == 0) and MaxTP >= tariff['Price'] and MinTP <= tariff['Price'] and(MaxTIS >= int(tariff['Options']['Internet']['InternetSpeed'].removeprefix('до ')) and MinTIS <= int(tariff['Options']['Internet']['InternetSpeed'].removeprefix('до ')))):
                if (len(activeOptions) == 0):
                    viabletariffs.append(tariff)
                else:
                    if "Internet" in activeOptions and "Internet" in tariff['Options'].keys() or not ("Internet" in activeOptions) and not ("Internet" in tariff['Options'].keys()):
                        if "TV" in activeOptions and "TV" in tariff['Options'].keys() or not ("TV" in activeOptions) and not ("TV" in tariff['Options'].keys()):
                            if "Mobile" in activeOptions and "Mobile" in tariff['Options'].keys() or not ("Mobile" in activeOptions) and not ("Mobile" in tariff['Options'].keys()):
                                viabletariffs.append(tariff)
                    
    data['tariffs'] = viabletariffs.copy()
    data['pages'] = int(len(data["tariffs"])/6)
    if page:
        data['currentpage'] = page
        starttariff = (page-1)*6
        data['tariffs'] = data['tariffs'].copy()[starttariff:starttariff+6]
    else:
        data['currentpage'] = 1
        data['tariffs'] = data['tariffs'].copy()[0:6]
    return json(data)

@app.route("/tariffs")
async def tariffs(request):
    address = request.args.get("address")
    host = request.headers.get('host')
    subdomain = host.split('.')[0].removeprefix('https://')
    cityadd = request.args.get('city')
    if cityadd:
        cityadd = cityadd.split(' ')[-1]
    data = {}
    if host!=local_link and subdomain!="on-wifi"and subdomain!="www":
        city = Database.GetCityBySubdomain(subdomain)
        data['City']= city
    else:
        city = {'Name':'Москва', 'NameEng': 'moskva','id':416}
        data['City']= city
    template = env.get_template('tariffs.html')
    data = {}
    if address:
        try: 
            data = cacheAdr[address].copy()
        except KeyError:
            data = Database.GetInfoByAddress(address)
            cacheAdr[address] = data.copy()
    elif cityadd:
        try:
            data = cacheCities[cityadd].copy()
        except KeyError:
            data = Database.GetInfoByCity(Database.GetCityByName(cityadd))
            cacheCities[cityadd] = data.copy()
    else:
        try:
            data = cacheCities[city['Name']].copy()
        except KeyError:
            data = Database.GetInfoByCity(city)
            cacheCities[city['Name']] = data.copy()
    provider = request.args.get("provider")
    if provider:
        data['provider'] = provider
    options = request.args.get("options")
    if options:
        data['options'] = options.split(' ')
    data['host'] = host
    data['Cities'] = Database.GetAllCities()
    
    rendered_html = template.render(data = data)
    return html(rendered_html)
#endregion

#region /aboutUs
@app.route("/aboutUs")
async def aboutUs(request):
    data = {}
    data['City'] = {'Name':'Москва', 'NameEng': 'moskva','id':416}
    
    data['Cities'] = Database.GetAllCities()
    host = request.headers.get('host')
    subdomain = host.split('.')[0].removeprefix('https://')
    if subdomain!="on-wifi" and host!=local_link:
        data['City'] = Database.GetCityBySubdomain(subdomain)
    template = env.get_template('aboutUs.html')
    return html(template.render(data = data))
#endregion

#region /question
@app.route("/questions")
async def questions(request):
    data = {}
    data['City'] = {'Name':'Москва', 'NameEng': 'moskva','id':416}
    
    data['Cities'] = Database.GetAllCities()
    host = request.headers.get('host')
    subdomain = host.split('.')[0].removeprefix('https://')
    if subdomain!="on-wifi"and subdomain!="www" and host!=local_link:
        data['City'] = Database.GetCityBySubdomain(subdomain)
    template = env.get_template('questions.html')
    return html(template.render(data = data))
#endregion

#region /reviews
@app.route("/reviews")
async def reviews(request):
    data = {}
    data['City'] = {'Name':'Москва', 'NameEng': 'moskva','id':416}
    
    data['Cities'] = Database.GetAllCities()
    host = request.headers.get('host')
    subdomain = host.split('.')[0].removeprefix('https://')
    if subdomain!="on-wifi"and subdomain!="www" and host!=local_link:
        data['City'] = Database.GetCityBySubdomain(subdomain)
    template = env.get_template('reviews.html')
    return html(template.render(data = data))
#endregion

def send_email(email, name):
    
    # Настройки почтового сервера
    smtp_server = 'sm4.hosting.reg.ru'  # Замените на адрес вашего SMTP-сервера
    smtp_port = 587  # Порт SMTP-сервера (обычно 587 для TLS)

    # Ваши учетные данные
    sender_email = 'user@on-wifi.ru'  # Ваш адрес электронной почты
    sender_password = 'pochtaUser'  # Ваш пароль

    # Получатель и тема письма
    recipient_email = 'info@on-wifi.ru'  # Адрес получателя
    subject = 'Сообщение о сотрудничестве с сайта on-wifi.ru'

    # Текст и формат письма
    body = f'Имя: {name} \n Почта: {email}'

    # Создание объекта MIMEMultipart
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Добавление текста в письмо
    message.attach(MIMEText(body, 'plain'))

    # Подключение к почтовому серверу
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Установка соединения с сервером
            server.starttls()

            # Вход в учетную запись отправителя
            server.login(sender_email, sender_password)

            # Отправка письма
            server.send_message(message)

        return 'Письмо успешно отправлено!'
    except Exception as e:
        return f'Ошибка при отправке письма: {e}'

def send_lead(name, phone, address, room):
    url = "https://on-wifi.bitrix24.ru/rest/11940/pn37z1pw2mxrg7dz/crm.lead.add.json"

    data = {
        "fields[TITLE]": "С сайта on-wifi.ru",
        "fields[NAME]": name,
        "fields[PHONE][0][VALUE]": phone,
        "fields[ADDRESS]": f"{address}[{room}]",
    }

    response = requests.post(url, data=data)

    return response.text

@app.route('/send-lead', methods=['POST'])
async def send_lead_handler(request):
    name = request.json.get('name')
    phone = request.json.get('phone')
    address = request.json.get('address')
    room = request.json.get('room')
    
    lead = send_lead(name=name, phone=phone, address=address, room=room)

    return response.json({"data": lead}, status=200)
@app.route('/send-email', methods=['POST'])
async def send_email_handler(request):
    email = request.form.get('email')
    name = request.form.get('name')
    if email and name:
        send_email(email, name)
        return json({'status': 'все по кайфу'})
    else:
        return json({'status': 'error', 'message': 'Недостающие данные'})

async def handle_500(request, exception):
    return redirect('https://on-wifi.ru/')

#app.error_handler.add(Exception, handle_500)

def runCaching():
    subprocess.Popen(['python', 'Cacher.py'], shell=True)

if __name__ == "__main__":
    cachingThread = Thread(target=runCaching)
    cachingThread.start()
    app.run(host="0.0.0.0", port=3000, debug=False)

