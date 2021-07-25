import string
from sqlalchemy import create_engine
import random
from getpass import getpass

botkey = input("Enter bot token: ")
botname = input("Enter botname (that starts with @, but without @): ")

ip = input("Enter ip of db (default is localhost): ")
ip = ip if ip else "localhost"

port = input("Enter port of db (default is 5432): ")
port = port if port else "5432"

admin_user = input("Enter admin user of your db (default is postgres): ")
admin_user = admin_user if admin_user else "postgres"
admin_password = getpass("Enter admin's password: ")

temp_db = input("Enter your existing database (default is postgres): ")
temp_db = temp_db if temp_db else "postgres"

password = getpass("Enter password for your bot's db: ")
if not password:
    while True:
        print("password can't be blank")
        password = getpass("Enter password for your bot's db: ")
        if password:
            break

blank = f"""
BOT_TOKEN = "{botkey}"
BOTNAME = "{botname}"
SERVER_IP = "{ip}"
SERVER_PORT = "{port}"
DB_USER = "tgbot"
DB_PASSWORD = "{password}"
DB_NAME = "spendbot"
SALT = "{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))}"
"""

config = open("config.py", "w")
config.write(blank)
config.close()

engine = create_engine(f"postgresql://{admin_user}:{admin_password}@{ip}:{port}/{temp_db}")

# engine.execute("commit")
engine.execute(f"CREATE USER tgbot with encrypted password '{password}'")
conn = engine.connect()
conn.execute("commit")
conn.execute("CREATE DATABASE spendbot")
conn.close()
# engine.execute("commit")
engine.execute("GRANT ALL PRIVILEGES ON DATABASE spendbot TO tgbot")
