from flask import Flask, render_template
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

@app.route('/drugs')
def drugs():
    return render_template('drugs.html')

@app.route('/drugs/UPA-SUL')
def drugsUpasul():
    connectDb()
    headings = ("Nome", "Quantidade", "ID")
    cursor.execute("SELECT *, oid FROM UPASUL")
    records = cursor.fetchall()
    disconnectDb()
    return render_template('drugsDisplay.html', headings=headings, data=records, title="UPA-SUL")

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

if __name__ == "__main__":
    app.run(debug=True)
