from flask import Flask, render_template, request
from models.scheduler import ClassScheduler
from utils.database import Database

app = Flask(__name__)

@app.route('/')
def home():
    # Load home page or student preferences form
    return render_template("index.html")

@app.route('/submit_preferences', methods=['POST'])
def submit_preferences():
    # Get preferences from form and run scheduling algorithm
    student_id = request.form['student_id']
    preferred_time = request.form['preferred_time']
    preferred_section = request.form['preferred_section']
    cgpa = float(request.form['cgpa'])
    payment_status = request.form['payment_status']

    # Connect to Database (you'll implement this part)
    db = Database()
    db.save_student_preferences(student_id, preferred_time, preferred_section, cgpa, payment_status)

    # Run scheduling algorithm (you'll implement this part)
    scheduler = ClassScheduler(db)
    schedule = scheduler.generate_schedule()

    # Return the result (You can render a schedule result page)
    return render_template("schedule_result.html", schedule=schedule)

if __name__ == '__main__':
    app.run(debug=True)
