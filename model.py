from flask import Flask
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'a01320622'
app.config['MYSQL_DATABASE_DB'] = 'LaPorra'
app.config['MYSQL_DATABASE_HOST'] = 'ubuntu-512mb-nyc2-01'
mysql.init_app(app)


def create_user(_name,_email,_password): #creates user in the database
    conn = mysql.connect()
    cursor = conn.cursor()
    _hashed_password = generate_password_hash(_password)
    print(_hashed_password)
    cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return True
    else:
        return False

def get_user(_username): #checks that user exists

    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        if len(data) > 0:
            return data
        else:
            return 1

    except Exception as e:
        return -1
    finally:
        cursor.close()
        con.close()
