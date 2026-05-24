import sqlite3, os, json, weather, llm
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, session
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash


application = Flask(__name__)
application.config['SECRET_KEY'] = 'G7kL9qX2vR8mT4zP1c'

DB_PATH = os.getenv('DATABASE_PATH', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
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

@application.route('/api/session-check')
def check_session():
    # Return true if 'user_id' exists in session
    return jsonify(has_session='user_id' in session)

@application.route('/logout', methods=["POST"])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
    
@application.route('/location', methods=["POST"])
def location():
    data = request.get_json()
    session['lat'] = data.get('lat')
    session['lng'] = data.get('lng')
    return jsonify({"status": "ok"})

@application.route('/alerts', methods=("GET", "POST"))
def alerts():
    alert = {"longitude" : None, "latitude" : None, "alert_type" : None, "operator" : None, "numeric_threshold" : None, "condition" : None, "percentage_threshold" : None}
    if request.method == 'POST':
        alertType           = request.form.get('alert_type')
        if(not alertType):
            return render_template('alerts.html', alertError='Please select an alert type.')
        operator            = request.form.get('operator')
        numericThreshold    = request.form.get('numeric_threshold')
        condition           = request.form.get('condition')
        percentageThreshold = request.form.get('percentageThreshold')

        alert["latitude"]             = session.get('lat')
        alert["longitude"]            = session.get('lng')
        alert["alert_type"]           = alertType
        alert["operator"]             = operator
        alert["numeric_threshold"]    = numericThreshold
        alert["condition"]            = condition
        alert["percentage_threshold"] = percentageThreshold

        if(session['user_id']):
            is_email = False
            is_phone_number = True
            location = f"{alert['latitude']}, {alert['longitude']}"
            alertJSON = json.dumps(alert)
            conn = get_db_connection()
            cursor = conn.execute('INSERT INTO alerts (user_id, is_email, is_phone_number, latitude, longitude, location, alert_type) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (session.get('user_id'), is_email, is_phone_number, alert['latitude'], alert['longitude'], location, alertJSON))
            conn.commit()
            conn.close()
        return redirect(url_for('index'))
    
    google_api_key=os.getenv("GOOGLE_PLACES_API_KEY")
    return render_template('alerts.html', google_api_key=google_api_key)

if __name__ == "__main__":
    application.debug = True
    application.run()
