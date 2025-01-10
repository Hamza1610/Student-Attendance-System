
DROP TABLE IF EXISTS attendance;

CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    class_name VARCHAR NOT NULL,
    date DATE NOT NULL,
    student_id VARCHAR UNIQUE NOT NULL,
    status VARCHAR NOT NULL
);

-- Create anextetion to rung the uuid_generate_v4() function 
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    role VARCHAR NOT NULL,
    photo_url VARCHAR(255) DEFAULT 'https://ui-avatars.com/api/?name=John+Doe&background=random'
);

-- Create the 'classes' table
CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR DEFAULT 'active',
    teacher_id VARCHAR NOT NULL, -- this can give conflict base on the use of if it's uuid or email
    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE SET NULL --  this is also affected
);

-- Create the 'students' table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    student_id VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    class_name VARCHAR NOT NULL,
    face_embedding BYTEA,  -- Use BYTEA for storing BLOB data in PostgreSQL
    registered_by VARCHAR NOT NULL
);
