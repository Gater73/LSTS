from datetime import date
import bios, hashlib, os, mysql.connector
from mysql.connector import Error


pathToConfig = "config.yml"
confpath = "../db.conf"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def printTable(table):
       # Connect to MySQL Server
       connectDb()
       # Query database
       cursor.execute("SELECT * FROM " + table)
       records = cursor.fetchall()
       print_records = []
       # Loop and add to Combobox
       for record in records:
           print_records.append(str(record[2]) + " - " + str(record[1]) + " - ID:" + str(record[0]))
       # Print to screen
       print(f"{bcolors.BOLD}======================================================{bcolors.WARNING}{table}{bcolors.ENDC}{bcolors.BOLD}======================================================{bcolors.ENDC}")
       for i in print_records:
              print(i)
       print(f"{bcolors.BOLD}======================================================{'=' * len(table)}======================================================{bcolors.ENDC}")
       # Closes connection with database
       disconnectDb()
       # Waits for input
       input("")


def addEntry(table):
       # Connect to database
       connectDb()
       # Asks user for entry info
       nome = input("Digite o nome do medicamento: ")
       qtd = input("Digite a quantidade do medicamento: ")
       # Query database
       cursor.execute("INSERT INTO " + table + "(remedio,quantidade) VALUES('"+ str(nome) + "', " + str(qtd) + ")")
       print(f"Added for {str(nome)} with the value {str(qtd)}")
       # Closes connection with database
       disconnectDb()
       # Waits for input
       input("")


def editEntry(table):
       # Connect to database
       connectDb()
       # PrintTable without disconnectDb()
       cursor.execute("SELECT * FROM " + table)
       records = cursor.fetchall()
       print_records = []
       # Loop and add to dict
       for record in records:
           print_records.append(str(record[2]) + " - " + str(record[1]) + " - ID:" + str(record[0]))
       # Print to screen
       print(f"{bcolors.BOLD}======================================================{bcolors.WARNING}{table}{bcolors.ENDC}{bcolors.BOLD}======================================================{bcolors.ENDC}")
       for i in print_records:
              print(i)
       print(f"{bcolors.BOLD}======================================================{'=' * len(table)}======================================================{bcolors.ENDC}")
       # Asks user for entry info
       idParaEditar = input("Digite o id que desejas editar: ")
       nome = input("Digite o novo nome do medicamento: ")
       qtd = input("Digite a nova quantidade do medicamento: ")
       # Query database
       cursor.execute("UPDATE " + table + " SET remedio = '" + str(nome) + "', quantidade = " + str(qtd) + " WHERE id = "+ str(idParaEditar))
       print(f"Record for {str(nome)} changed to {str(qtd)}")
       # Closes connection with database
       disconnectDb()
       # Waits for input
       input("")


def removeEntry(table):
       # Connect to database
       connectDb()
       # PrintTable without disconnectDb()
       cursor.execute("SELECT * FROM " + table)
       records = cursor.fetchall()
       print_records = []
       # Loop and add to dict
       for record in records:
           print_records.append(str(record[2]) + " - " + str(record[1]) + " - ID:" + str(record[0]))
       # Print to screen
       print(f"{bcolors.BOLD}======================================================{bcolors.WARNING}{table}{bcolors.ENDC}{bcolors.BOLD}======================================================{bcolors.ENDC}")
       for i in print_records:
              print(i)
       print(f"{bcolors.BOLD}======================================================{'=' * len(table)}======================================================{bcolors.ENDC}")
       # Asks user for entry info
       idParaRem = input("Digite o id que desejas remover: ")
       # Query database
       cursor.execute("DELETE from " + table + " WHERE id=" + str(idParaRem))
       print(f"Deleted item with id {str(idParaRem)}")
       # Closes connection with database
       disconnectDb()
       # Waits for input
       input("")


def loggedIn(username, unidade):
       tableString = str(unidade).replace("-", "")
       print(bcolors.FAIL +" /$$        /$$$$$$  /$$$$$$$$ /$$$$$$") 
       print("| $$       /$$__  $$|__  $$__//$$__  $$")
       print("| $$      | $$  \__/   | $$  | $$  \__/")
       print("| $$      |  $$$$$$    | $$  |  $$$$$$ ")
       print("| $$       \____  $$   | $$   \____  $$")
       print("| $$       /$$  \ $$   | $$   /$$  \ $$")
       print("| $$$$$$$$|  $$$$$$/   | $$  |  $$$$$$/")
       print("|________/ \______/    |__/   \______/ ")
       print("" + bcolors.ENDC)
       print(f"Unidade: {bcolors.BOLD}{unidade}{bcolors.ENDC}")
       print(f"Authenticated as {bcolors.BOLD}{username}{bcolors.ENDC} in {bcolors.BOLD}{date.today()}{bcolors.ENDC}")
       print("")
       print("Options:")
       print(bcolors.BOLD +"print  - Imprimir tabela")
       print(bcolors.BOLD + bcolors.OKGREEN + "add    - Adicionar" + bcolors.ENDC)
       print(bcolors.BOLD + bcolors.OKBLUE + "edit   - Editar" + bcolors.ENDC)
       print(bcolors.BOLD + bcolors.FAIL + "rem    - Remover" + bcolors.ENDC)
       print(bcolors.BOLD + "exit - Sair/Deslogar" + bcolors.ENDC)
       print("")
       escolha = input(">")
       if escolha == "print":
              printTable(tableString)
              loggedIn(username, unidade)
       elif escolha == "add":
              addEntry(tableString)
              loggedIn(username, unidade)
       elif escolha == "edit":
              editEntry(tableString)
              loggedIn(username, unidade)
       elif escolha == "rem":
              removeEntry(tableString)
              loggedIn(username, unidade)



def askLogin():
        while True:
              os.system("cls" if os.name == "nt" else "clear")
              print(bcolors.FAIL +".......................................")
              print(".......................................")
              print(".......................................")
              print("..............&&&&&&...................")
              print("..........&&&&&&&&&&&&&&...............")
              print("......&&&&&&&&&&&&&&&&&&&&&&...........")
              print("......&&&&&&&&&&&&&&&&&&&&&&...........")
              print("......&&&&&&&&&&&&&&&&&&&&&&&&&&@@@@...")
              print("......&&&&&&&&&&&&&&&............@@....")
              print("......&&&&&&&&&&&&&&&&.........&@,.....")
              print(".......&&&&&&&&&&&&&&&&&......&&.......")
              print("...........&&&&&&&&&&&&&&...&&&........")
              print("................&&......&&/&&..........")
              print("..........................&&...........")
              print(".......................................")
              print("......................................." + bcolors.ENDC)
              print("")
              print("Digite a unidade...")
              print(f"{bcolors.BOLD}'exit'{bcolors.ENDC} para sair - {bcolors.BOLD}'credits'{bcolors.ENDC} para ver créditos - {bcolors.BOLD}'license'{bcolors.ENDC} para abrir a licença")
              unidade = input("> ")
              if unidade == "exit":
                     exit(0)
              elif unidade == "credits":
                     print("Credits", "Authors:\n  -Cadu Santana\n  -Gabriel Martins Nascimento\n  -Lucas Daniel\n  -Natanael Ferreira\n  -Vitória Sousa\n\nEspecial Thanks to the open source community!")
                     input()
                     askLogin()
              elif unidade == "license":
                     os.system("start https://www.gnu.org/licenses/gpl-3.0.html" if os.name == "nt" else "xdg-open https://www.gnu.org/licenses/gpl-3.0.html > /dev/null")
                     askLogin()
              print("Username")
              user = input("> ")
              print("Password")
              password = input("> ")
              userNameHash = hashlib.sha256(user.encode())
              passwordHash = hashlib.sha256(password.encode())
              configData = bios.read(pathToConfig)
              userNameHashed = configData[unidade]["username"]
              passwordHashed = configData[unidade]["password"]
              if userNameHash.hexdigest() == userNameHashed and passwordHash.hexdigest() == passwordHashed:
                     os.system("cls" if os.name == "nt" else "clear")
                     loggedIn(user, unidade)

              else:
                     print("Usuário ou Senha incorretos!")
                     input("Pressione qualquer tecla para continuar...")
                     askLogin()

askLogin()
