from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

#Path to file containing database connection and authentication information
confpath = "db.conf"

def connectDb():
    global conn, cursor
    with open(confpath, "r") as dbconffile:
                lines = [line.rstrip('\n') for line in dbconffile]
                print(lines)
    conn = mysql.connector.connect(host=lines[0],
                                        port=lines[1],
                                        database=lines[2],
                                        user=lines[3],
                                        password=lines[4])
    if conn.is_connected():
                        db_Info = conn.get_server_info()
                        print("Connected to MySQL Server version ", db_Info)
                        cursor = conn.cursor()


def disconnectDb():
    global conn, cursor
    cursor.execute("commit;")
    conn.close()
    cursor.close()
    print("DB disconnected")


@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/units')
def drugs():
    if request.args.get('unit'):
        connectDb()
        middle_column = 2
        headings = ("ID", "Nome", "Quantidade")
        unit = request.args.get('unit')
        unit2 = unit.replace("-", "")
        cursor.execute("SELECT * FROM " + str(unit2))
        records = cursor.fetchall()
        disconnectDb()
        return render_template('drugsDisplay.html', headings=headings, data=records, title=unit, middle_column=middle_column)
    else:
        connectDb()
        cursor.execute("show tables;")
        unidades = cursor.fetchall()
        disconnectDb()
        return render_template('drugs.html', unidades=unidades)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
