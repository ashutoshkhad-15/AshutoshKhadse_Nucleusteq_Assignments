CREATE TABLE app_users (
    id BIGSERIAL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone_number VARCHAR(15),
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'USER',
	drivers_license_number VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT pk_app_users PRIMARY KEY (id),
    CONSTRAINT uq_app_users_email UNIQUE (email),
    CONSTRAINT uq_app_users_phone UNIQUE (phone_number),
	CONSTRAINT uq_app_users_license UNIQUE (drivers_license_number),
    CONSTRAINT chk_app_users_role CHECK (role IN ('USER', 'ADMIN'))
);

CREATE TABLE vehicles (
    id BIGSERIAL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    license_plate VARCHAR(20) NOT NULL,
    vehicle_type VARCHAR(10) NOT NULL,
    fuel_type VARCHAR(15),
    transmission VARCHAR(15),
    seating_capacity INT DEFAULT 4,
    daily_rate NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'AVAILABLE',
    image_url TEXT,
    version INT DEFAULT 0, -- Optimistic locking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT pk_vehicles PRIMARY KEY (id),
    CONSTRAINT uq_vehicles_license_plate UNIQUE (license_plate),
    CONSTRAINT chk_vehicles_type CHECK (vehicle_type IN ('CAR', 'BIKE')),
    CONSTRAINT chk_vehicles_status CHECK (status IN ('AVAILABLE', 'BOOKED', 'MAINTENANCE', 'RETIRED'))
);

CREATE TABLE bookings (
    id BIGSERIAL,
    user_id BIGINT NOT NULL,
    vehicle_id BIGINT NOT NULL,
    start_date DATE NOT NULL, 
    end_date DATE NOT NULL,   
    price_per_day NUMERIC(10,2) NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    version INT DEFAULT 0, -- Optimistic locking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT pk_bookings PRIMARY KEY (id),
    CONSTRAINT fk_bookings_users FOREIGN KEY (user_id) REFERENCES app_users(id),
    CONSTRAINT fk_bookings_vehicles FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    CONSTRAINT chk_bookings_dates CHECK (end_date > start_date),
    CONSTRAINT chk_bookings_status CHECK (status IN ('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED'))
);

CREATE TABLE reviews (
    id BIGSERIAL,
    booking_id BIGINT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT pk_reviews PRIMARY KEY (id),
    CONSTRAINT uq_reviews_booking UNIQUE (booking_id),
    CONSTRAINT fk_reviews_bookings FOREIGN KEY (booking_id) REFERENCES bookings(id),
    CONSTRAINT chk_reviews_rating CHECK (rating BETWEEN 1 AND 5)
);

-- Indexes for performance optimization (Naming: idx_[table]_[column])
CREATE INDEX idx_app_users_email ON app_users(email);
CREATE INDEX idx_vehicles_search ON vehicles(make, model, vehicle_type, status);
CREATE INDEX idx_bookings_dates ON bookings(start_date, end_date);