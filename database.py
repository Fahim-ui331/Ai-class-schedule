import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Your MySQL username
            password="password",  # Your MySQL password
            database="class_scheduler"  # Your database name
        )
        self.cursor = self.conn.cursor()

    def save_student_preferences(self, student_id, preferred_time, preferred_section, cgpa, payment_status):
        query = "INSERT INTO students (student_id, preferred_time, preferred_section, cgpa, payment_status) VALUES (%s, %s, %s, %s, %s)"
        data = (student_id, preferred_time, preferred_section, cgpa, payment_status)
        self.cursor.execute(query, data)
        self.conn.commit()

    def get_student_preferences(self):
        query = "SELECT * FROM students"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return [{'student_id': row[0], 'preferred_time': row[1], 'preferred_section': row[2], 'cgpa': row[3], 'payment_status': row[4]} for row in result]
