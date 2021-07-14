from config import *
from sqlalchemy import create_engine

engine = create_engine(f"postgresql://{user}:{password}@{ip}:{port}/{dbname}")
conn = engine.connect()

conn.execute("""
CREATE TABLE costs(
	id SERIAL PRIMARY KEY,
	user_id integer,
	cost integer,
	type varchar(100),
	description varchar(255),
	data timestamp
)
""")
conn.execute("""
CREATE TABLE families(
	id SERIAL PRIMARY KEY,
	creator_id integer unique,
	name varchar(100)
)
""")
conn.execute("""
CREATE TABLE users(
	id SERIAL PRIMARY KEY,
	user_id integer unique,
	nickname varchar(100),
	family_id integer
)
""")
conn.execute("""
CREATE TABLE links(
	id SERIAL PRIMARY KEY,
	family_id integer,
	ref_part varchar(256)
)
""")

conn.close()