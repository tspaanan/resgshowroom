CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT,
	role TEXT
);

CREATE TABLE pages (
	id SERIAL PRIMARY KEY,
	title TEXT,
	introduction TEXT,
	visible BOOLEAN NOT NULL
);

CREATE TABLE page_ownership (
	user_id INTEGER REFERENCES users,
	page_id INTEGER REFERENCES pages
);

CREATE TABLE keywords (
	id SERIAL PRIMARY KEY,
	keyword TEXT,
	visible BOOLEAN NOT NULL
);

CREATE TABLE page_keywords (
	page_id INTEGER REFERENCES pages,
	keyword_id INTEGER REFERENCES keywords
);

CREATE TABLE topics (
	id SERIAL PRIMARY KEY,
	topic TEXT,
	description TEXT,
	responsible_user_id INTEGER REFERENCES users,
	chosen BOOLEAN,
	student_id INTEGER REFERENCES users,
	visible BOOLEAN NOT NULL
);

CREATE TABLE topic_keywords (
	topic_id INTEGER REFERENCES topics,
	keyword_id INTEGER REFERENCES keywords
);

CREATE TABLE publications (
	id SERIAL PRIMARY KEY,
	title TEXT,
	subtitle TEXT,
	journal TEXT,
	volume INTEGER,
	year INTEGER,
	issue TEXT,
	page_no TEXT,
	doi TEXT,
	visible BOOLEAN NOT NULL
);

CREATE TABLE page_publications (
	page_id INTEGER REFERENCES pages,
	publication_id INTEGER REFERENCES publications
);

CREATE TABLE topic_publications (
	topic_id INTEGER REFERENCES topics,
	publication_id INTEGER REFERENCES publications
);

CREATE TABLE images (
	id SERIAL PRIMARY KEY,
	name TEXT,
	b64data TEXT,
	visible BOOLEAN NOT NULL
);

CREATE TABLE documents (
	id SERIAL PRIMARY KEY,
	name TEXT,
	topic_id INTEGER REFERENCES topics,
	uploader_id INTEGER REFERENCES users,
	data BYTEA,
	visible BOOLEAN NOT NULL
);

CREATE TABLE messages (
	id SERIAL PRIMARY KEY,
	message TEXT,
	time TIMESTAMP,
	archived BOOLEAN,
	user_id INTEGER REFERENCES users,
	page_id INTEGER REFERENCES pages,
	topic_id INTEGER REFERENCES topics,
	visible BOOLEAN NOT NULL
);
