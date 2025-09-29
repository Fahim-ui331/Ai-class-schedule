CREATE DATABASE class_scheduler;


CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    time_slot VARCHAR(50),
    section VARCHAR(10),
    cgpa FLOAT,
    payment_status VARCHAR(20)
);