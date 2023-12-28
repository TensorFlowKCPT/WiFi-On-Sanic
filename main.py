from sanic import Sanic, response, HTTPResponse, json, redirect, html, file
from sanic.response import text, html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from Database import Database

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
    
    print(request.headers.get('Referer'))
    print(request.headers.get('Referer'))
    print(request.headers.get('Referer'))
    print(request.headers.get('Referer'))
    print(request.headers.get('Referer'))
    template = env.get_template('main.html')
    rendered_html = template.render(data=data)

    return html(rendered_html)
#endregion

#region /tariffs
@app.route("/tariffs")
async def tariffs(request):
    address = request.args.get("address")
    template = env.get_template('tariffs.html')
    data = Database.GetInfoByAddress(address)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
