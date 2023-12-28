from sanic import Sanic, response, HTTPResponse, json, redirect, html, file
from sanic.response import text, html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from Database import Database
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Sanic("Wifi-On")
local_link = "http://localhost:3000/"
env = Environment(
    loader=FileSystemLoader('templates'),  # Папка с шаблонами
    autoescape=select_autoescape(['html', 'xml'])
)

app.static("/static/", "./st/")
#Получение адреса пользователя из ip не очень работает, надо будет уже с ssh и серваком это делать, без них не понять
#region /index
@app.route("/")
async def index(request):
    data = {}
    data['City'] = {'Name':'Москва', 'NameEng': 'unknown'}
    subdomain = request.headers.get('host').split('.')[0].removeprefix('https://')
    if subdomain!="on-wifi":
        data['City'] = Database.GetCityBySubdomain(subdomain)
    template = env.get_template('main.html')
    rendered_html = template.render(data=data)
    return html(rendered_html)
#endregion

#region /tariffs
@app.route("/tariffs")
async def tariffs(request):
    address = request.args.get("address")
    city = request.args.get("city")
    template = env.get_template('tariffs.html')
    if address:
        data = Database.GetInfoByAddress(address)
    elif city:
        data = Database.GetInfoByCityName(city)
    rendered_html = template.render(data = data)
    return html(rendered_html)
#endregion

#region /aboutUs
@app.route("/aboutUs")
async def aboutUs(request):
    template = env.get_template('aboutUs.html')
    return html(template.render())
#endregion

#region /question
@app.route("/questions")
async def questions(request):
    template = env.get_template('questions.html')
    return html(template.render())
#endregion

#region /reviews
@app.route("/reviews")
async def reviews(request):
    template = env.get_template('reviews.html')
    return html(template.render())
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
    app.run(host="0.0.0.0", port=3000, debug=True)
