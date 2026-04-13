import sqlite3, os, json, weather, llm
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort

application = Flask(__name__)
application.config['SECRET_KEY'] = 'G7kL9qX2vR8mT4zP1c'

@application.route('/')
def index():
    return render_template("index.html", google_api_key=os.getenv("GOOGLE_PLACES_API_KEY"))

@application.route('/forecast', methods=["POST"])
def forecast():
    data = request.get_json()
    lat = data["lat"]
    lng = data["lng"]

    forecast = weather.get_forecast(lat, lng)
    periods  = weather.get_periods(forecast)
    summary = llm.gen_forecast_summary(periods)

    return jsonify({"data": {"periods": periods, "summary" : summary}})

if __name__ == "__main__":
    application.debug = True
    application.run()