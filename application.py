import sqlite3, os, json, weather, llm
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, session
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash


application = Flask(__name__)
application.config['SECRET_KEY'] = 'G7kL9qX2vR8mT4zP1c'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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

@application.route('/summary', methods=["POST"])
def summary():
    data = request.get_json()
    periods = data["periods"]
    summary = llm.gen_forecast_summary(periods)
    return jsonify({"summary": summary})

@application.route('/login', methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        usrEmail = request.form['usrEmail']
        usrPass  = request.form['usrPass']

        if (not usrEmail) or (not usrPass):
            pass

        else:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (usrEmail,)).fetchone()
            conn.close()
            if user is None:
                return render_template('login.html', emailError='Email not found.')

            if not check_password_hash(user['password'], usrPass):
                return render_template('login.html', passError='Incorrect password.')
            
            session['user_id'] = user['id']
            return redirect(url_for('index'))

    return render_template('login.html')

@application.route('/signup', methods=("GET", "POST"))
def signup():
    if request.method == 'POST':
        usrEmail = request.form['usrEmail']
        usrPhone = request.form['usrPhone']
        usrPass  = request.form['usrPass']

    
        if (not usrEmail) or (not usrPhone) or (not usrPass):
            # flash('Title is required!')
            pass 
        
        else:
            conn = get_db_connection()
            cursor = conn.execute('INSERT INTO users (email, phone_number, password) VALUES (?, ?, ?)',
                         (usrEmail, usrPhone, generate_password_hash(usrPass)))
            session['user_id'] = cursor.lastrowid  
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('signup.html')

if __name__ == "__main__":
    application.debug = True
    application.run()
