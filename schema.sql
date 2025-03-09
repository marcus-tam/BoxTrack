CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE box (
    box_id SERIAL PRIMARY KEY,
    user_id SERIAL,
    box_creator SERIAL,
    box_type VARCHAR(50) NOT NULL,
    qr_code VARCHAR(255) NOT NULL,
    box_name VARCHAR(50) NOT NULL,
    box_description VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)

CREATE TABLE item (
    item_id SERIAL PRIMARY KEY,
    user_id SERIAL,
    box_id SERIAL,
    item_creator SERIAL,
    item_name VARCHAR(50) NOT NULL,
    item_category VARCHAR(50) NOT NULL,
    item_description VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vox_id) REFERENCES box(box_id)
)