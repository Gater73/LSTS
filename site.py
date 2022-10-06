from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def connectDb():
    global conn, cursor
    conn = sqlite3.connect("admin/database.db")
    cursor = conn.cursor()
    print("DB connected")


def disconnectDb():
    global conn, cursor
    conn.commit()
    conn.close()
    print("DB disconnected")


@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/units')
def drugs():
    if request.args.get('unit'):
        connectDb()
        headings = ("Nome", "Quantidade", "ID")
        unit = request.args.get('unit')
        unit2 = unit.replace("-", "")
        cursor.execute("SELECT *, oid FROM " + str(unit2))
        records = cursor.fetchall()
        disconnectDb()
        return render_template('drugsDisplay.html', headings=headings, data=records, title=unit)
    else:
        connectDb()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        unidades = cursor.fetchall()
        disconnectDb()
        return render_template('drugs.html', unidades=unidades)

@app.route('/drugs/UPA-LESTE')
def drugsUpaleste():
    connectDb()
    headings = ("Nome", "Quantidade", "ID")
    cursor.execute("SELECT *, oid FROM UPALESTE")
    records = cursor.fetchall()
    disconnectDb()
    return render_template('drugsDisplay.html', headings=headings, data=records, title="UPA-LESTE")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run(debug=True)
