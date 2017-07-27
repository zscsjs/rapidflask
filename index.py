from flask import Flask
from flask import render_template
import os
import json
import time
import urllib

app = Flask(__name__)

@app.route("/")
def index():
    return "hello, World";

@app.route("/goodbye")
def goodbye():
    return "Goodbye, World!"

@app.route("/hello/<name>")
def hello_name(name):
    return "Hello, {}".format(name)

def get_weather():
    url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=London&cnt=10&mode=json&units=metric&APPID=f9a69fdec39e6f457cae563a7d39d1da"
    response = urllib.request.urlopen(url).read()
    return response

@app.route("/weather")
def weather():
    data = json.loads(get_weather())
    page = "<html><head><title>My Weather</title></head><body>"
    page += "<h1>Weather for {}, {}</h1>".format(data.get('city').get('name'), data.get('city').get('country'))
    for day in data.get("list"):
        page += "<b>date:</b> {} <b>min:</b> {} <b>max:</b> {} <b>description:</b> {} <br/> ".format(
										 time.strftime('%d %B', time.localtime(day.get('dt'))),
                                                                                 (day.get("temp").get("min")),
                                                                                  day.get("temp").get("max"),
                                                                                  day.get("weather")[0].get("description"))
    page += "</body></html>"
    return page

@app.route("/altweather")
def altweather():
    data = json.loads(get_weather())
    day = time.strftime('%d %B', time.localtime(data.get('list')[0].get('dt')))
    mini = data.get("list")[0].get("temp").get("min")
    maxi = data.get("list")[0].get("temp").get("max")
    description = data.get("list")[0].get("weather")[0].get("description")
    return render_template("index.html", day=day, mini=mini, maxi=maxi, description=description)

@app.route("/altweather2")
def altweather2():
    data = json.loads(get_weather())
    forecast_list = []
    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get('dt')))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day,mini,maxi,description))
    return render_template("altweather2.html", forecast_list=forecast_list)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
