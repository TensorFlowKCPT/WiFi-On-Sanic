from sanic import Sanic, response, HTTPResponse, json, redirect, html, file
from sanic.response import text, html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from Database import Database
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    MaxTP=request.json.get('MaxTP')
    MinTIS=request.json.get('MinTIS')
    MaxTIS=request.json.get('MaxTIS')
    activeProviders=request.json.get('activeProviders')
    activeOptions=request.json.get('activeOptions')
    page=int(request.json.get('page'))
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
                    if 'mobile' in activeOptions and not ("Mobile" in tariff['Options'].keys()):
                        continue
                    if 'internetspeed' in activeOptions and not ("Internet" in tariff['Options'].keys()):
                        continue
                    if 'channels' in activeOptions and not ("TV" in tariff['Options'].keys()):
                        continue
                    viabletariffs.append(tariff)
    data['tariffs'] = viabletariffs
    
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

@app.route('/send-email', methods=['POST'])
async def send_email_handler(request):
    email = request.form.get('email')
    name = request.form.get('name')
    if email and name:
        send_email(email, name)
        return json({'status': 'все по кайфу'})
    else:
        return json({'status': 'error', 'message': 'Недостающие данные'})


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
