CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT, admin INTEGER
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
    grade INTEGER,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants,
    sent_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE restaurant_info (
    id SERIAL PRIMARY KEY,
    type TEXT,
    restaurant_id INTEGER REFERENCES restaurants
);

CREATE TABLE restaurant_tags (
    id SERIAL PRIMARY KEY,
    tag TEXT,
    restaurant_id INTEGER REFERENCES restaurants
);

CREATE TABLE opening_times (
    id SERIAL PRIMARY KEY,
    day TEXT,
    opening_time TEXT,
    closing_time TEXT,
    open TEXT,
    restaurant_id INTEGER REFERENCES restaurants
)

