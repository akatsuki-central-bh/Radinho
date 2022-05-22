import sqlite3
import secrets

connection = sqlite3.connect('database.db', check_same_thread=False)

cursor = connection.cursor()

def create_database():
  cursor.execute("CREATE TABLE IF NOT EXISTS users (username text, password text, token text)")
  connection.commit()

def create_user(username, password):
  cursor.execute("INSERT INTO users VALUES (?, ?, NULL)", (username, password))
  connection.commit()

def get_username(token):
  cursor.execute("SELECT username FROM users WHERE token = :token LIMIT 1", {"token": token})
  return cursor.fetchone()[0]

def login(username, password):
  token = generate_token()
  cursor.execute(
    "UPDATE users SET token = ? WHERE username = ? AND password = ?", (token, username, password)
  )
  connection.commit()

  return token

def logout(token):
  cursor.execute("UPDATE users SET token = NULL WHERE token = ?", (token))
  connection.commit()

def generate_token():
  return secrets.token_hex(8)

def disconnect():
  connection.close()
