from sqlalchemy import create_engine
from config import user, password, ip, port, dbname

engine = create_engine("postgresql://postgres@{ip}:{port}/postgres"
                       .format(ip=ip, port=port, dbname=dbname))
conn = engine.connect()

conn.execute("commit")
conn.execute("CREATE USER {user} with encrypted password \"{password}\";"
             .format(user=user, password=password))
conn.execute("CREATE DATABASE {dbname};".format(dbname=dbname))
conn.execute("GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {user};".format(dbname=dbname, user=user))

conn.close()
