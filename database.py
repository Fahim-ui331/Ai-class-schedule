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

    def save_student_preferences(self, student_id, preferred_time, preferred_section, cgpa, payment_status):
        query = "INSERT INTO students (student_id, preferred_time, preferred_section, cgpa, payment_status) VALUES (%s, %s, %s, %s, %s)"
        data = (student_id, preferred_time, preferred_section, cgpa, payment_status)
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
            return [{'student_id': row[0], 'preferred_time': row[1], 'preferred_section': row[2], 
                     'cgpa': row[3], 'payment_status': row[4]} for row in result]
        except mysql.connector.Error as err:
            print(f"Error fetching data: {err}")
            return []

    def import_from_csv(self, csv_file):
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student_id = row['Student_ID']
                    preferred_section = row['Preferred_Sections']
                    cgpa = float(row['GPA']) if row['GPA'] else 0.0
                    preferred_time = None  # Default, as CSV doesn't provide this
                    payment_status = 'pending'  # Default, adjust as needed
                    self.save_student_preferences(
                        student_id, preferred_time, preferred_section, cgpa, payment_status
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
    db.import_from_csv('assigned_sections.csv')
    preferences = db.get_student_preferences()
    for pref in preferences:
        print(pref)
    db.close()