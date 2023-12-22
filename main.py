from sanic import Sanic, response, HTTPResponse, json, redirect, html, file
from sanic.response import text, html
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from Database import Database

app = Sanic("Wifi-On")

env = Environment(
    loader=FileSystemLoader('templates'),  # Папка с шаблонами
    autoescape=select_autoescape(['html', 'xml'])
)

app.static("/static/", "./st/")

#region /index
@app.route("/")
async def index(request):
    template = env.get_template('index.html')
    rendered_html = template.render()

    return html(rendered_html)
#endregion

#region /tariffs
@app.route("/tariffs")
async def tariffs(request):
    address = request.params.get("address")
    template = env.get_template('tariffs.html')
    rendered_html = template.render()
    return html(rendered_html)
#endregion

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
