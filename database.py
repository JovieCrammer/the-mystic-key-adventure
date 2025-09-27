import tkinter as tk
from tkinter import messagebox
import mysql.connector


####################### LOGIN / SQL #############################

window = tk.Tk()
window.geometry('500x300')

COMPLETE = False
USERID = 'default'


def create_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="PlayerVaultDB"
    )

    my_cursor = connection.cursor()

    query1 = "CREATE TABLE users (userID int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(20), password VARCHAR(20))"
    # primary k is foreign k from user table
    # one-to-one relationship
    query2 = ("CREATE TABLE gameData (gameDataID int PRIMARY KEY, FOREIGN KEY(gameDataID) REFERENCES users(userID), "
              "keyFound VARCHAR(20) DEFAULT '')")

    # my_cursor.execute("CREATE DATABASE PlayerVaultDB")
    # my_cursor.execute(query1)
    # my_cursor.execute(query2)


def open_homepage():
    homepage = tk.Frame(window, width=500, height=300, bg='lightsteelblue')
    homepage.place(x=0, y=0)

    title_lbl = tk.Label(homepage, text="Home Page", font=('Arial', 16), bg='lightsteelblue')
    home_btn = tk.Button(homepage, text='Home')
    login_btn = tk.Button(homepage, text='Login', command=open_login)
    signup_btn = tk.Button(homepage, text='Sign Up', command=open_signup)

    title_lbl.place(x=210, y=30)
    home_btn.place(x=50, y=130)
    login_btn.place(x=220, y=130)
    signup_btn.place(x=370, y=130)


def open_login():
    global username_ent, password_ent

    login = tk.Frame(window, width=500, height=300, bg='lightsteelblue')
    login.place(x=0, y=0)

    title_lbl = tk.Label(login, text="Login", font=('Arial', 16), bg='lightsteelblue')
    username_lbl = tk.Label(login, text='Enter Username:', bg='lightsteelblue')
    username_ent = tk.Entry(login)
    password_lbl = tk.Label(login, text='Enter Password:', bg='lightsteelblue')
    password_ent = tk.Entry(login)
    login_btn = tk.Button(login, text='Login', command=login_sql)
    noAcc_lbl = tk.Label(login, text='No Account?', bg='lightsteelblue')
    signup_btn = tk.Button(login, text='Sign Up', command=open_signup)
    home_btn = tk.Button(login, text='Home', command=open_homepage)

    title_lbl.place(x=220, y=10)
    username_lbl.place(x=100, y=60)
    username_ent.place(x=230, y=60)
    password_lbl.place(x=100, y=90)
    password_ent.place(x=230, y=90)
    login_btn.place(x=210, y=140)
    noAcc_lbl.place(x=200, y=200)
    signup_btn.place(x=202, y=240)
    home_btn.place(x=10, y=10)


def open_signup():
    global cre_username_ent, cre_password_ent

    sign_up = tk.Frame(window, width=500, height=300, bg='lightsteelblue')
    sign_up.place(x=0, y=0)

    title_lbl = tk.Label(sign_up, text="Sign Up", font=('Arial', 16), bg='lightsteelblue')
    cre_username_lbl = tk.Label(sign_up, text='Create Username:', bg='lightsteelblue')
    cre_username_ent = tk.Entry(sign_up)
    cre_password_lbl = tk.Label(sign_up, text='Create Password:', bg='lightsteelblue')
    cre_password_ent = tk.Entry(sign_up)
    home_btn = tk.Button(sign_up, text='Home', command=open_homepage)
    login_btn = tk.Button(sign_up, text='Login', command=open_login)
    alr_acc_lbl = tk.Label(sign_up, text='Already have an account?', bg='lightsteelblue')
    signup_btn = tk.Button(sign_up, text='Sign Up', command=signup_sql)

    title_lbl.place(x=210, y=10)
    home_btn.place(x=10, y=10)
    cre_username_lbl.place(x=100, y=60)
    cre_username_ent.place(x=230, y=60)
    cre_password_lbl.place(x=100, y=90)
    cre_password_ent.place(x=230, y=90)
    signup_btn.place(x=202, y=140)
    alr_acc_lbl.place(x=160, y=200)
    login_btn.place(x=210, y=240)
    home_btn.place(x=10, y=10)


def login_sql():
    global COMPLETE
    global USERID
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="PlayerVaultDB"
    )

    my_cursor = connection.cursor()
    usrname = username_ent.get()  # username and password reserved keywords
    pssword = password_ent.get()

    # %s placeholders for variable
    SELECT = "SELECT * FROM `users` WHERE `username` = %s AND `password` = %s"
    my_cursor.execute(SELECT, (usrname, pssword))  # passing arguments
    result = my_cursor.fetchall()

    # if username and password found in db
    if result:
        USERID = result[0][0]  # ID
        SELECT = "SELECT * FROM gameData WHERE gameDataID = %s"
        my_cursor.execute(SELECT, (USERID,))
        gamedata = my_cursor.fetchone()

        if not gamedata:
            # Insert a new row into the gameData table
            INSERT_GAME_DATA = "INSERT INTO gameData (gameDataID, keyFound) VALUES (%s, %s)"
            my_cursor.execute(INSERT_GAME_DATA, (USERID, 'default'))
            connection.commit()

        messagebox.showinfo("", "Login Successful")
        messagebox.showinfo("", "Game Will Begin Shortly")
        messagebox.showinfo("", "Press the cross to exit")
        COMPLETE = True

    else:
        messagebox.showinfo("", "Login Unsuccessful")


def signup_sql():
    global COMPLETE
    global USERID
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="PlayerVaultDB"
    )

    # print(connection)
    usrname = cre_username_ent.get()
    pssword = cre_password_ent.get()
    my_cursor = connection.cursor()

    if len(usrname) < 1 or len(pssword) < 1:  # presence check
        messagebox.showinfo("", "Error: Please Do Not Leave Fields Blank.")

    elif 2 > len(usrname) or 3 > len(pssword):  # length check
        messagebox.showinfo("", "Error: Username And Password Must Be Between 3 and 20 Characters.")

    elif 20 < len(usrname) or 20 < len(pssword):  # length check
        messagebox.showinfo("", "Error: Username And Password Must Be Between 3 and 20 Characters.")

    else:  # insert query
        INSERT = "INSERT INTO users(username, password) values(%s, %s)"
        my_cursor.execute(INSERT, (usrname, pssword))
        connection.commit()
        USERID = my_cursor.lastrowid  # Get ID

        INSERT_GAME_DATA = "INSERT INTO gameData (gameDataID, keyFound) VALUES (%s, %s)"
        my_cursor.execute(INSERT_GAME_DATA, (USERID, 'default'))
        connection.commit()

        messagebox.showinfo("", "Sign Up Successful")
        messagebox.showinfo("", "Game Will Begin Shortly")
        messagebox.showinfo("", "Press the cross to exit")
        COMPLETE = True


def get_game_key():
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="PlayerVaultDB"
    )

    my_cursor = connection.cursor()

    # select query
    SELECT = ("SELECT gameData.keyFound FROM `users` JOIN `gameData` ON `users`.`userID` = `gameData`.`gameDataID` "
              "WHERE `users`.`userID` = %s")

    my_cursor.execute(SELECT, (USERID,))

    # fetch result
    RESULT = my_cursor.fetchone()

    # if gameKey found in db
    if RESULT:
        game_key = RESULT[0]
        return game_key
    else:
        return None


def save_userid():
    return USERID


def login_complete():
    return COMPLETE

