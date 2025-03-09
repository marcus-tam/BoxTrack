CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    location_creator SERIAL,
    location_name VARCHAR(50) NOT NULL,
    location_category VARCHAR(50) NOT NULL, --ie. Attic, Storage Unit, House, etc.
    location_address VARCHAR(50) NOT NULL,
    location_city VARCHAR(50) NOT NULL,
    location_province VARCHAR(50) NOT NULL,
    location_lon VARCHAR(50) NOT NULL,
    location_lat VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
)

CREATE TABLE box (
    user_id SERIAL,
    box_id SERIAL PRIMARY KEY,
    location_id SERIAL,
    box_creator SERIAL,
    box_type VARCHAR(50) NOT NULL,
    qr_code VARCHAR(255) NOT NULL,
    box_name VARCHAR(50) NOT NULL,
    box_description VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
)

CREATE TABLE item (
    item_id SERIAL PRIMARY KEY,
    box_id SERIAL,
    item_creator SERIAL,
    item_name VARCHAR(50) NOT NULL,
    item_image_ref VARCHAR(50) NOT NULL,
    item_category VARCHAR(50) NOT NULL,
    item_description VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vox_id) REFERENCES box(box_id)
)