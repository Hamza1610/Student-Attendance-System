
DROP TABLE IF EXISTS attendance;

CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    class_id VARCHAR NOT NULL,
    date DATE NOT NULL,
    student_id VARCHAR UNIQUE NOT NULL,
    status VARCHAR NOT NULL
);

-- Create anextetion to rung the uuid_generate_v4() function 
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    role VARCHAR NOT NULL,
    photo_url VARCHAR(255) DEFAULT 'https://ui-avatars.com/api/?name=John+Doe&background=random'
);

-- Create the 'classes' table
CREATE TABLE IF NOT EXISTS classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    description TEXT,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    status VARCHAR DEFAULT 'active',
    coordinator_id UUID,
    FOREIGN KEY (coordinator_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Create the 'students' table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    student_id VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    class_id VARCHAR,
    face_embedding BYTEA,  -- Use BYTEA for storing BLOB data in PostgreSQL
    registered_by VARCHAR
);
