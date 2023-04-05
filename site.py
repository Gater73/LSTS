from flask import Flask, render_template, request, flash, session, url_for, redirect, g
import mysql.connector, bios, hashlib
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "SomeReallySecureSecretKey"
pathToConfig = "admin/config.yml"


@app.before_request
def before_request():
    g.name = None
    if 'name' in session:
        g.name = session['name']
        g.is_admin = session['is_admin']

#Path to file containing database connection and authentication information
confpath = "db.conf"


with open("admin.cred", "r") as admin:
    lines = admin.readlines()
    admin_username = lines[0]
    admin_pass = lines[1]
    if "\n" in admin_username:
        admin_username = admin_username.replace("\n","")
    if "\n" in admin_pass:
        admin_pass = admin_pass.replace("\n","")

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    global admin_username, admin_pass
    if request.method == 'POST':
        session.pop('is_admin', None)
        session.pop('name', None)

        username = request.form['username']
        password = request.form['password']
        unit = request.form['unit']
        print_records = []

        if unit != "":
            userNameHash = hashlib.sha256(username.encode())
            passwordHash = hashlib.sha256(password.encode())
            configData = bios.read(pathToConfig)
            userNameHashed = configData[unit]["username"]
            passwordHashed = configData[unit]["password"]
            try:
                connectDb()
                cursor.execute("SELECT * FROM " + unit)
                records = cursor.fetchall()
                disconnectDb()
                for record in records:
                    print_records.append(str(record[2]) + " - " + str(record[1]) + " - ID:" + str(record[0]))
            except:
                flash("Unidade não identificada")
                return redirect(url_for('login'))
        
        try:
            if username == admin_username and password == admin_pass:
                session['is_admin'] = "yes"
                session['name'] = "Administrator"

                return redirect(url_for('adminpanel'))
            elif userNameHash.hexdigest() == userNameHashed and passwordHash.hexdigest() == passwordHashed:
                session['is_admin'] = "no"
                session['name'] = username
                session['print_records'] = print_records

                return redirect(url_for('userpanel'))
        except:
            flash("Unidade não identificada")
            return redirect(url_for('login'))
    flash('Incorrect username or password')
    return render_template('login.html')


@app.route('/delunit')
def delunit():
    print(session)
    try:
        if session['is_admin'] == 'yes':
            unit = str(request.args.get('unit'))
            data = bios.read(pathToConfig)
            del data[unit]
            bios.write(pathToConfig, data)
            connectDb()
            cursor.execute(f"DROP TABLE {unit};")
            disconnectDb()
            flash(f"Unidade {unit} Deletada com sucesso!")
            return redirect(url_for('adminpanel'))
        else:
            return "You are not allowed to delete units"
    except:
        return "You are not allowed to delete units"


@app.route('/add_unit', methods=['GET', 'POST'])
def addunit():
    try:
        if session['is_admin'] == 'yes':
            if request.method == "POST":
                name = request.form['name']
                login = request.form['login']
                password = request.form['password']
                connectDb()
                cursor.execute(f"CREATE TABLE `{name}` (`id` MEDIUMINT(255) NOT NULL AUTO_INCREMENT,`remedio` VARCHAR(1024) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,`quantidade` INT NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB;")
                disconnectDb()
                #LOgin
                with open(pathToConfig, "a") as configFile:
                    configFile.write("\n" + name + ":")
                    loginHash = hashlib.sha256(login.encode())
                    configFile.write("\n    username: " + loginHash.hexdigest() + "\n")
                    passHash = hashlib.sha256(password.encode())
                    configFile.write("    password: " + passHash.hexdigest())
                flash("Adicionado com successo!")
                return redirect(url_for('adminpanel'))
            else:
                return "You are not allowed to add units"
    except:
        return "You are not allowed to add units"
    

@app.route('/admin-panel')
def adminpanel():
    if not g.name:
        flash("You are not logged in!")
        return redirect(url_for('login'))
    connectDb()
    cursor.execute("show tables;")
    unidades = cursor.fetchall()
    disconnectDb()
    g.unidades = unidades
    return render_template('admin-panel.html')

@app.route('/user-panel')
def userpanel():
    if not g.name:
        flash("You are not logged in!")
        return redirect(url_for('login'))

    return render_template('user-panel.html')


@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    session.pop('name', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
