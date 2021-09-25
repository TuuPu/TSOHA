CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT, admin INTEGER
);

CREATE TABLE userinfo (
    id SERIAL PRIMARY KEY,
    title TEXT,
    admin INTEGER,
    user_id INTEGER REFERENCES users
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    address TEXT UNIQUE
);

CREATE TABLE restaurant_info (
    id SERIAL PRIMARY KEY,
    type TEXT,
    grade INTEGER,
    restaurant_id INTEGER REFERENCES restaurants
);

CREATE TABLE restaurant_messages (
    id SERIAL PRIMARY KEY,
    messages_id INTEGER REFERENCES messages,
    restaurants_id INTEGER REFERENCES restaurants
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);