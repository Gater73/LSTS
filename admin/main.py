from tkinter import *
from tkinter import ttk, messagebox
from threading import Thread
from time import sleep
from datetime import date
import bios, hashlib, sqlite3, os


pathToConfig = "config.yml"

def creditSpawn():
    messagebox.showinfo("Credits", "Authors:\n  -Cadu Santana\n  -Gabriel Martins Nascimento\n  -Lucas Daniel\n  -Natanael Ferreira\n  -Vitória Sousa\n\nEspecial Thanks to the open source community!")


def licenseSpawn():
    os.system("start https://www.gnu.org/licenses/gpl-3.0.html" if os.name == "nt" else "xdg-open https://www.gnu.org/licenses/gpl-3.0.html")


def deleteDb(remedioIdDel, tableStringDel):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE from " + tableStringDel + " WHERE oid=" + str(remedioIdDel))
    messagebox.showinfo("Delete record", f"Deleted item with id {str(remedioIdDel)}")
    comboBox2.set("")
    cursor.execute("SELECT *, oid FROM " + str(comboBox1.get()).replace("-", ""))
    records = cursor.fetchall()
    print_records = []
    for record in records:
            print_records.append(str(record[0]) + " - " + str(record[1]) + " - ID:" + str(record[2]))
    comboBox2.configure(values=print_records)
    conn.commit()
    conn.close()


def saveDb(idRemedio, tableString, remedioNome, remedioQuant):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE " + tableString + " SET remedio = '" + str(remedioNome) + "', quantidade = " + str(remedioQuant) + " WHERE oid = "+ str(idRemedio))
    messagebox.showinfo("Edit record", f"Record for {str(remedioNome)} changed to {str(remedioQuant)}")
    comboBox2.set("")
    cursor.execute("SELECT *, oid FROM " + str(comboBox1.get()).replace("-", ""))
    records = cursor.fetchall()
    print_records = []
    for record in records:
            print_records.append(str(record[0]) + " - " + str(record[1]) + " - ID:" + str(record[2]))
    comboBox2.configure(values=print_records)
    conn.commit()
    conn.close()
    editWindow.withdraw()


def saveDbAdd(tableStringAdd, remedioNomeAdd, remedioQuantAdd):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO " + tableStringAdd + "(remedio,quantidade) VALUES('"+ str(remedioNomeAdd) + "', " + str(remedioQuantAdd) + ")")
    messagebox.showinfo("Add record", f"Added for {str(remedioNomeAdd)} with the value {str(remedioQuantAdd)}")
    comboBox2.set("")
    cursor.execute("SELECT *, oid FROM " + str(comboBox1.get()).replace("-", ""))
    records = cursor.fetchall()
    print_records = []
    for record in records:
            print_records.append(str(record[0]) + " - " + str(record[1]) + " - ID:" + str(record[2]))
    comboBox2.configure(values=print_records)
    conn.commit()
    conn.close()
    addWindow.withdraw()


def editWindowOpen(comboBox2String, tableString):
    editWindow = Tk()
    editWindow.title("Edit - LSTS-Admin")
    editWindow.eval('tk::PlaceWindow . center')
    comboBox2String = str(comboBox2String.replace("ID:",""))
    remedioList = comboBox2String.split(" - ")
    remedioName = Label(editWindow, text="Remédio:")
    remedioName.pack()
    remedioNameEntry = Entry(editWindow)
    remedioNameEntry.pack()
    remedioQuant = Label(editWindow, text="Quantidade:")
    remedioQuant.pack()
    remedioQuantEntry = Entry(editWindow)
    remedioQuantEntry.pack()
    remedioNameEntry.delete(0, END)
    remedioNameEntry.insert(0, str(remedioList[0]))
    remedioQuantEntry.delete(0, END)
    remedioQuantEntry.insert(0, str(remedioList[1]))
    saveBtn = Button(editWindow, text="Save", command= lambda: saveDb(remedioList[2], tableString, remedioNameEntry.get(), remedioQuantEntry.get()))
    saveBtn.pack()
    return


def addWindowOpen(comboBox2StringAdd, tableStringAdd):
    addWindow = Tk()
    addWindow.title("Add - LSTS-Admin")
    addWindow.eval('tk::PlaceWindow . center')
    comboBox2StringAdd = str(comboBox2StringAdd.replace("ID:",""))
    remedioListAdd = comboBox2StringAdd.split(" - ")
    remedioNameAdd = Label(addWindow, text="Remédio:")
    remedioNameAdd.pack()
    remedioNameEntryAdd = Entry(addWindow)
    remedioNameEntryAdd.pack()
    remedioQuantAdd = Label(addWindow, text="Quantidade:")
    remedioQuantAdd.pack()
    remedioQuantEntryAdd = Entry(addWindow)
    remedioQuantEntryAdd.pack()
    remedioNameEntryAdd.delete(0, END)
    remedioQuantEntryAdd.delete(0, END)
    saveBtnAdd = Button(addWindow, text="Add records", command= lambda: saveDbAdd(tableStringAdd, remedioNameEntryAdd.get(), remedioQuantEntryAdd.get()))
    saveBtnAdd.pack()
    return


def reloadDb():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT *, oid FROM " + str(comboBox1.get()).replace("-", ""))
    records = cursor.fetchall()
    print_records = []
    for record in records:
            print_records.append(str(record[0]) + " - " + str(record[1]) + " - ID:" + str(record[2]))
    conn.close()
    print(print_records)
    comboBox2.set("")
    comboBox2.configure(values=print_records)
    

def focusClear(event):
    event.widget.delete(0, END)

def on_closing():
    loginWindow.destroy()
    mainWindow.destroy()
    editWindow.destroy()

def onClick():
    if comboBox1.get() != "":
        unidade = comboBox1.get()
        configData = bios.read(pathToConfig)
        userName = configData[unidade]["username"]
        password = configData[unidade]["password"]
    else:
        messagebox.showerror(title="Error", message="Must set the unit...")
        return
    userNameHash = hashlib.sha256(userText.get().encode())
    passwordHash = hashlib.sha256(passwordText.get().encode())
    if userNameHash.hexdigest() == userName and passwordHash.hexdigest() == password:
        print(f"Authenticated as {userText.get()} in {date.today()}")
        loginWindow.withdraw()
        mainWindow.deiconify()
        welcomeMessage = Label(mainWindow, text=f"Welcome {userText.get()}")
        welcomeMessage.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 0))

        # TAKES '-' OUT OF UPA-SUL
        tableString = str(comboBox1.get()).replace("-", "")

        # Connect to database
        conn = sqlite3.connect("database.db")
        
        # Creates cursor
        cursor = conn.cursor()

        # Query database
        cursor.execute("SELECT *, oid FROM " + tableString)
        records = cursor.fetchall()
        print_records = []

        # Loop and add to Combobox
        for record in records:
            print_records.append(str(record[0]) + " - " + str(record[1]) + " - ID:" + str(record[2]))

        # Create UI elements
        comboBox2.configure(values=print_records)

        labelEmpty1 = Label(mainWindow, text=" ", pady=5, padx=5)
        labelEmpty1.grid(row=3, column=2, columnspan=1)

        editBtn = Button(mainWindow, text="Edit record", pady=5, padx=5, command= lambda: editWindowOpen(comboBox2.get(), tableString))
        editBtn.grid(row=4, column=0, columnspan=1)

        addBtn = Button(mainWindow, text="Add record", pady=5, padx=5, command= lambda: addWindowOpen(comboBox2.get(), tableString))
        addBtn.grid(row=4, column=1, columnspan=1)

        deleteBtn = Button(mainWindow, text="Delete record", pady=5, padx=5, command= lambda: deleteDb(int(record[2]), tableString))
        deleteBtn.grid(row=4, column=2, columnspan=1)

        labelEmpty = Label(mainWindow, text=" ", pady=5, padx=5)
        labelEmpty.grid(row=5, column=2, columnspan=1)

        conn.close()

    else:
        thread = Thread(target = ErrorThread, args = (10, ))
        thread.start()

def ErrorThread(arg):
    print("Deauth")
    errorMessage = Label(loginWindow, text="Failed to login")
    errorMessage.grid(row=4, column=0, columnspan=2, pady=15, padx=15)
    sleep(1)
    errorMessage.grid_forget()


loginWindow = Tk()
loginWindow.geometry("212x285")
loginWindow.title("Login")
loginWindow.protocol("WM_DELETE_WINDOW", on_closing)
loginWindow.eval('tk::PlaceWindow . center')
loginWindow.iconphoto(True, PhotoImage(file='icon.png'))

mainWindow = Tk()
mainWindow.title("LSTS-Admin")
mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
mainWindow.eval('tk::PlaceWindow . center')
mainWindow.withdraw()

editWindow = Tk()
editWindow.title("Edit - LSTS-Admin")
editWindow.protocol("WM_DELETE_WINDOW", on_closing)
editWindow.eval('tk::PlaceWindow . center')
editWindow.withdraw()


menubar = Menu(mainWindow)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="License", command=licenseSpawn)
helpmenu.add_command(label="Credits", command=creditSpawn)
menubar.add_cascade(label="Information", menu=helpmenu)
mainWindow.config(menu=menubar)


myLabel = Label(loginWindow, text="Login Page")
myLabel.grid(row=0, column=0, columnspan=2, pady=15, padx=15)

comboBox1 = ttk.Combobox(loginWindow, values=["UPA-SUL", "UPA-LESTE"])
comboBox1.grid(row=1, column=0, columnspan=2, pady=15, padx=15)

userText = Entry(loginWindow)
userText.grid(row=2, column=0, columnspan=2, pady=15, padx=15)
userText.insert('end', "User")


passwordText = Entry(loginWindow)
passwordText.grid(row=3, column=0, columnspan=2, pady=15, padx=15)
passwordText.insert('end', "Password")

submitButton = Button(loginWindow, text="Login", command=onClick)
submitButton.grid(row=5, column=0, columnspan=2, pady=15, padx=15)

userText.bind("<FocusIn>", focusClear)
passwordText.bind("<FocusIn>", focusClear)

comboBox2 = ttk.Combobox(mainWindow)
comboBox2.grid(row=2, column=0, columnspan=3, padx=15, pady=5)

loginWindow.mainloop()
