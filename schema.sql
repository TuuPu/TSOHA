CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT, admin INTEGER
);

CREATE TABLE userinfo (
    id SERIAL PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users
);


CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    visible BOOLEAN,
    address TEXT UNIQUE
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants,
    sent_at TIMESTAMP
);

CREATE TABLE restaurant_info (
    id SERIAL PRIMARY KEY,
    type TEXT,
    grade INTEGER,
    restaurant_id INTEGER REFERENCES restaurants
);

CREATE TABLE restaurant_tags (
    id SERIAL PRIMARY KEY,
    tag TEXT,
    restaurant_id INTEGER REFERENCES restaurants
);

