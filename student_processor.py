import csv

class StudentDataProcessor:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = []

    def load_csv(self):
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                self.data = [row for row in reader]
            print(f"Loaded {len(self.data)} records from {self.csv_file}")
        except FileNotFoundError:
            print(f"Error: File {self.csv_file} not found")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def validate_data(self):
        valid_records = []
        for row in self.data:
            try:
                # Example validation: Ensure GPA is a valid float and not negative
                gpa = float(row['GPA']) if row['GPA'] else 0.0
                if gpa < 0 or gpa > 4.0:
                    print(f"Invalid GPA for student {row['Student_ID']}: {gpa}")
                    continue
                # Add more validation as needed (e.g., check Student_ID format)
                valid_records.append(row)
            except ValueError:
                print(f"Invalid data for student {row['Student_ID']}")
        self.data = valid_records
        print(f"Validated {len(self.data)} records")

    def get_processed_data(self):
        return self.data

if __name__ =="__main__":
    processor = StudentDataProcessor('assigned_sections.csv')
    processor.load_csv()
    processor.validate_data()
    for record in processor.get_processed_data():
        print(record)