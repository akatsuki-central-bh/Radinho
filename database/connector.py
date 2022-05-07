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

def get_login(token):
  cursor.execute("SELECT login FROM users WHERE token = :token LIMIT 1", {"token": token})
  return cursor.fetchone()[0]

def alter_password(token, password, last_password):
  cursor.execute("UPDATE users SET password = ? WHERE token = ? AND password = ?", (token, password, last_password))
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

