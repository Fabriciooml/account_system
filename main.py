import mysql.connector
from mysql.connector import Error
from use_key import encrypt, decrypt

def connect_database():
  try:
    global connection
    global cursor
    connection = mysql.connector.connect(host='localhost',
                                        database='passwords',
                                        user='root')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

  except Error as e:
      print("Error while connecting to MySQL", e)

def user_interface():
  user_answer = input('''\nHello, welcome to your new account control system!\n
                      What you want to do?\n
                      (1) Insert a new account.\n
                      (2) Delete an existing account.\n
                      (3) Display an account already registered.\n
                      (4) Display all registered accounts.\n
                      (0) exit.\n''')
  if(user_answer=='1'):
    insert_data()
  elif(user_answer=='2'):
    delete_data()
  elif(user_answer=='3'):
    select_data()
  elif(user_answer=='4'):
    display_all()
  else:
    print('Okay, goodbye :)')
    exit()

def insert_data():
  site = input("Insert here where are your account from: (ex.: Amazon)\n")
  login = input("Insert here your login:\n")
  password = input("Insert here your password:\n")
  print("From: {}\nLogin: {}\nPassword: {}".format(site, login, password))
  validation = input("Correct? (y/n)\n")
  password = encrypt(password)
  if(validation == "y"):
    if(existing_validation(site = site)):
      print("Already exists a account on this site!\n")
    else:
      sql_insert = "INSERT INTO password_control_system (site, login, password) VALUES (%s, %s, %s);"
      val_insert = (site, login, password)
      cursor.execute(sql_insert, val_insert)
      connection.commit()
      print("Account succesfully saved!\n")
    user_interface()

def delete_data():
  site = input("Insert here where are your account from: (ex.: Amazon)\n")
  if(existing_validation(site = site)):
    sql_delete = "DELETE FROM password_control_system WHERE site=%s"
    val_delete = (site, )
    cursor.execute(sql_delete, val_delete)
    connection.commit()
    print("Account successfully deleted!\n")
  else:
    print("Don't have a account on this site yet!\n")
  user_interface()

def existing_validation(site = None): 
  sql_select = "SELECT * FROM password_control_system WHERE site=%s;"
  val_select = (site, )
  cursor.execute(sql_select, val_select)
  result_select = cursor.fetchone()
  if(result_select):
    return True
  return False

def select_data():
  site = input("Insert here where are your account from: (ex.: Amazon)\n")
  if(existing_validation(site = site)):
    sql_select = "SELECT * FROM password_control_system WHERE site=%s;"
    val_select = (site, )
    cursor.execute(sql_select, val_select)
    result_select = cursor.fetchone()
    password = decrypt(result_select[2])
    print("Site: {}\nLogin: {}\nPassword: {}".format(result_select[0], result_select[1], password))
  else:
    print("Don't have a account on this site yet!\n")
  user_interface()

def display_all():
  sql_select = "SELECT * FROM password_control_system"
  cursor.execute(sql_select)
  result_select = cursor.fetchall()
  nrow = len(result_select)
  if(nrow > 0):
    for i in range(nrow):
      print("|Site: {} | Login: {} | Password: {}|".format(result_select[i][0], result_select[i][1], decrypt(result_select[i][2])))
  else:
    print("No registered accounts!\n")
  user_interface()


def desconnect_database():
  if (connection.is_connected()):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

connect_database()
user_interface()
desconnect_database()