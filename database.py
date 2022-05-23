import mysql.connector
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
  user=str(os.getenv('user')),
  password=str(os.getenv('password')),
  host=str(os.getenv('host')),
  database=str(os.getenv('database'))
)

cursor = connection.cursor()

def create_database():
  cursor.execute("CREATE TABLE IF NOT EXISTS users (username text, password text, token text)")
  connection.commit()

def create_user(username, password):
  cursor.execute("INSERT INTO users VALUES (%s, %s, NULL)", (username, password))
  connection.commit()

def get_username(token):
  cursor.execute("SELECT username FROM users WHERE token = :token LIMIT 1", {"token": token})
  return cursor.fetchone()[0]

def login(username, password):
  token = generate_token()
  cursor.execute(
    "UPDATE users SET token = %s WHERE username = %s AND password = %s", (token, username, password)
  )
  connection.commit()

  return token

def logout(token):
  cursor.execute("UPDATE users SET token = NULL WHERE token = %s", (token,))
  connection.commit()

def generate_token():
  return secrets.token_hex(8)

def disconnect():
  connection.close()
