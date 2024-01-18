from sanic import Sanic, response, HTTPResponse, json, redirect, html, file
from sanic.response import text, html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from Database import Database
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

app = Sanic("Wifi-On")
local_link = "localhost:3000"
env = Environment(
    loader=FileSystemLoader('templates'),  # Папка с шаблонами
    autoescape=select_autoescape(['html', 'xml'])
)

app.static("/static/", "./st/")
#Получение адреса пользователя из ip не очень работает, надо будет уже с ssh и серваком это делать, без них не понять
cacheAdr = {}
cacheCities = {}
#region /index
@app.route("/")
async def index(request):
    data = {}
    data['City'] = {'Name':'Москва', 'NameEng': 'moskva','id':416}
    
    data['Cities'] = Database.GetAllCities()
    host = request.headers.get('host')
    subdomain = host.split('.')[0].removeprefix('https://')
    if host!=local_link and subdomain!="on-wifi" and subdomain!="www"  :
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
    elif city:
        try:
            data = cacheCities[adr].copy()
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
        data = Database.GetInfoByAddress(address)
    else:
        data = Database.GetInfoByCity(city)
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

app.error_handler.add(Exception, handle_500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
