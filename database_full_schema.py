import mysql.connector
import csv

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="password",  # Replace with your MySQL password
            database="class_scheduler"  # Your database name
        )
        self.cursor = self.conn.cursor()

    def create_students_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id VARCHAR(50),
                    name VARCHAR(100),
                    course VARCHAR(50),
                    preferred_section VARCHAR(50),
                    assigned_section VARCHAR(50),
                    department VARCHAR(50),
                    semester VARCHAR(50),
                    course_load INT,
                    cgpa FLOAT,
                    preferred_time VARCHAR(50),
                    payment_status VARCHAR(20)
                )
            """)
            self.conn.commit()
            print("Students table created or verified successfully")
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")

    def save_student_preferences(self, student_id, name, course, preferred_section, assigned_section, 
                                department, semester, course_load, cgpa, preferred_time=None, payment_status='pending'):
        query = """
            INSERT INTO students (student_id, name, course, preferred_section, assigned_section, 
                                department, semester, course_load, cgpa, preferred_time, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (student_id, name, course, preferred_section, assigned_section, 
                department, semester, int(course_load) if course_load else 0, 
                float(cgpa) if cgpa else 0.0, preferred_time, payment_status)
        try:
            self.cursor.execute(query, data)
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")

    def get_student_preferences(self):
        query = "SELECT * FROM students"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return [{
                'student_id': row[0], 'name': row[1], 'course': row[2], 
                'preferred_section': row[3], 'assigned_section': row[4], 
                'department': row[5], 'semester': row[6], 'course_load': row[7], 
                'cgpa': row[8], 'preferred_time': row[9], 'payment_status': row[10]
            } for row in result]
        except mysql.connector.Error as err:
            print(f"Error fetching data: {err}")
            return []

    def import_from_csv(self, csv_file):
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.save_student_preferences(
                        student_id=row['Student_ID'],
                        name=row['Name'],
                        course=row['Course'],
                        preferred_section=row['Preferred_Sections'],
                        assigned_section=row['Assigned_Section'],
                        department=row['Department'],
                        semester=row['Semester'],
                        course_load=row['Course_Load'],
                        cgpa=row['GPA'],
                        preferred_time=None,  # Default, adjust as needed
                        payment_status='pending'  # Default, adjust as needed
                    )
                print(f"Successfully imported data from {csv_file}")
        except FileNotFoundError:
            print(f"Error: File {csv_file} not found")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except Exception as e:
            print(f"Error processing CSV: {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    db.create_students_table()
    db.import_from_csv('assigned_sections.csv')
    preferences = db.get_student_preferences()
    for pref in preferences:
        print(pref)
    db.close()