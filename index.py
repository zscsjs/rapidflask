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
    return get_weather()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
