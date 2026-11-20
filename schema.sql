CREATE TABLE IF NOT EXISTS conversation_memory(
message_id integer primary key autoincrement,
user_id integer,
role text,
message text,
timestamp datetime default current_timestamp);

CREATE TABLE IF NOT EXISTS face_memory (
    user_id INTEGER PRIMARY KEY,
    face_file TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS known_facts(
fact_id integer primary key autoincrement,
user_id integer,
category text,
value text,
unique(user_id, category)
);

CREATE TABLE IF NOT EXISTS learning_memory(
id integer primary key autoincrement,
user_id integer,
topic text,
mastery	real default 0,
last_updated datetime default current_timestamp);

CREATE TABLE IF NOT EXISTS profile_memory(
user_id integer primary key,
name text not null,
age integer,
education_level text,
strengths text,
weaknesses text
);
