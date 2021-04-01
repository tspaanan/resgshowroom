CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	role TEXT
);

CREATE TABLE pages (
	id SERIAL PRIMARY KEY,
	title TEXT,
	introduction TEXT
);

CREATE TABLE page_ownership (
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	page_id INTEGER REFERENCES pages
);

CREATE TABLE messages (
	id SERIAL PRIMARY KEY,
	message TEXT,
	time TIMESTAMP,
	archived BOOLEAN,
	user_id INTEGER REFERENCES users,
	page_id INTEGER REFERENCES pages
);
