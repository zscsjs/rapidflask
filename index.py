from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
import datetime
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

def get_weather(city= "Mars"):
    url = "http://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=10&mode=json&units=metric&APPID=f9a69fdec39e6f457cae563a7d39d1da".format(city)
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
    data = json.loads(get_weather("London"))
    day = time.strftime('%d %B', time.localtime(data.get('list')[0].get('dt')))
    mini = data.get("list")[0].get("temp").get("min")
    maxi = data.get("list")[0].get("temp").get("max")
    description = data.get("list")[0].get("weather")[0].get("description")
    return render_template("index.html", day=day, mini=mini, maxi=maxi, description=description)

@app.route("/altweather2")
def altweather2():
    data = json.loads(get_weather("London"))
    forecast_list = []
    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get('dt')))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day,mini,maxi,description))
    return render_template("altweather2.html", forecast_list=forecast_list)

@app.route("/search")
@app.route("/search/<searchcity>")
def search(searchcity = "Tokyo"):
    data = json.loads(get_weather(searchcity))
    city = data['city']['name']
    country = data['city']['country']
    forecast_list = []
    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get('dt')))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day,mini,maxi,description))
    return render_template("search.html", forecast_list=forecast_list, city=city, country=country)

@app.route("/get")
def get():
    getcity= request.args.get("city")
    if not getcity:
        getcity=request.cookies.get("last_city")
    if not getcity:
        getcity="Portland"
    try:
        data = json.loads(get_weather(getcity))
        city = data['city']['name']
    except:
        return render_template('invalid_city.html',user_input=getcity)
    country = data['city']['country']
    forecast_list = []
    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get('dt')))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day,mini,maxi,description))
        response = make_response(render_template("get.html", forecast_list=forecast_list, city=city, country=country))
        response.set_cookie("last_city","{},{}".format(city,country), expires=datetime.datetime.today() + datetime.timedelta(days=365))
        return response

@app.route("/post", methods=["POST","GET"])
def post():
    getcity= request.form.get("city")
    if not getcity:
        getcity="Madrid"

    try:
        data = json.loads(get_weather(getcity))
        city = data['city']['name']
    except:
        return render_template('invalid_city.html',user_input=getcity)
    country = data['city']['country']
    forecast_list = []
    for d in data.get("list"):
        day = time.strftime('%d %B', time.localtime(d.get('dt')))
        mini = d.get("temp").get("min")
        maxi = d.get("temp").get("max")
        description = d.get("weather")[0].get("description")
        forecast_list.append((day,mini,maxi,description))
    return render_template("post.html", forecast_list=forecast_list, city=city, country=country)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
