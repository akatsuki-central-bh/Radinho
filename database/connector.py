import sqlite3
import secrets

connection = sqlite3.connect('database/database.db')

cursor = connection.cursor()

def create_database():
  cursor.execute("CREATE TABLE users (login text, password text, token text)")
  connection.commit()

def create_user(login, password):
  cursor.execute("INSERT INTO users VALUES (?, ?, NULL)", (login, password))
  connection.commit()

def select_user(token):
  cursor.execute("SELECT login, password FROM users WHERE token = ?", (token))
  connection.commit()

def alter_password(token, password):
  cursor.execute("UPDATE users SET password = ? WHERE token = ?", (token, password))
  connection.commit()

def login(login, password):
  token = generate_token()
  cursor.execute(
    "UPDATE users SET token = ? WHERE login = ? AND password = ?", (token, login, password)
  )
  connection.commit()

  return token

def logout(token):
  cursor.execute("UPDATE users SET token = NULL WHERE token = ?", (token))
  connection.commit()

def generate_token():
  return secrets.token_bytes(16)

def disconnect():
  connection.close()

