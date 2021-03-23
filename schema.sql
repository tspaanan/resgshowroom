CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT,
	role TEXT
);

CREATE TABLE pages (
	id SERIAL PRIMARY KEY,
	title TEXT,
	introduction TEXT
);
