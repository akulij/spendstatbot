CREATE TABLE costs(
	id SERIAL PRIMARY KEY,
	user_id integer,
	cost integer,
	type varchar(100),
	description varchar(255),
	data timestamp
);

CREATE TABLE families(
	id SERIAL PRIMARY KEY,
	creator_id integer unique,
	name varchar(100)
);

CREATE TABLE users(
	id SERIAL PRIMARY KEY,
	user_id integer unique,
	nickname varchar(100),
	family_id integer
);

CREATE TABLE links(
	id SERIAL PRIMARY KEY,
	family_id integer,
	ref_part varchar(256)
);