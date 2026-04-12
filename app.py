import sqlite3, os, json, weather
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'G7kL9qX2vR8mT4zP1c'

@app.route('/')
def index():
    # conn = get_db_connection()
    # posts = conn.execute('SELECT * FROM posts').fetchall()
    # conn.close()
    return render_template("index.html", google_api_key=os.getenv("GOOGLE_PLACES_API_KEY"))



@app.route('/forecast', methods=["POST"])
def forecast():
    data = request.get_json()
    lat = data["lat"]
    lng = data["lng"]


    forecast = weather.get_forecast(lat, lng) # to-do
    periods = weather.get_periods(forecast)


    return jsonify({"data": {"periods" : periods}})


'''
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')
'''