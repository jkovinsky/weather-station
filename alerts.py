import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def save_user_alert(userId, is_email, is_phone_number, latitude, longitude, location, operator, threshold):
    # operator or threshold is optional 
    if not all([userId, (is_email or is_phone_number), latitude, longitude, location]):
        return False
    
    else:
        conn = get_db_connection()
        data = (userId, is_email, is_phone_number, latitude, longitude, location, operator, threshold)
        print(data)
        cursor = conn.execute("""
            INSERT INTO alerts (user_id, is_email, is_phone_number, latitude, longitude, location, operator, threshold) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        # session['user_id'] = cursor.lastrowid  
        conn.commit()
        conn.close()
    
    return True
        # return redirect(url_for('index'))

save_user_alert(userId=3, is_email=False, is_phone_number=True, latitude=37.8057618, longitude=-122.4121934, location="North Beach, CA", operator=">=", threshold="85")