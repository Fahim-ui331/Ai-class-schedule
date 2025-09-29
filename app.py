from flask import Flask, request, jsonify, render_template 
import pandas as pd
import os

app = Flask(__name__)

courses_df = pd.read_csv('courses.csv')
courses_map = {
    "Programming": "CS101",
    "Math:": "MATH201",
    "Physics": "PHYS301",
    "English": "ENGL101"
}

@app.route('/')
def index():
    # Load assigned_sections.csv for student dropdown
    df = pd.read_csv('assigned_sections.csv')
    students = df[['Student_ID', 'Name']].to_dict('records')
    return render_template('index.html', students=students)

@app.route('/selected')
def selected():
    student_id = request.args.get('student_id', 'S006')
    df = pd.read_csv('assigned_sections.csv')
    student = df[df['Student_ID'] == student_id].to_dict('records')
    student = student[0] if student else None
    return render_template('selected.html', student=student,
    courses= courses_df.to_dict('records'), course_map=courses_map)

@app.route('/save_schedule', methods=['POST'])
def save_schedule():
    data = request.json
    student_id = data.get('student_id')
    course = data.get('course')
    section = data.get('section')
    day = data.get('day')
    time = data.get('time')

     # Validate input
    if not all([student_id, course, section, day, time]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    # Load and update assigned_sections.csv
    df = pd.read_csv('assigned_sections.csv')
    student = df[df['Student_ID'] == student_id]
    if student.empty:
        return jsonify({"status": "error", "message": "Student not found"}), 404

    # Check eligibility
    gpa = student.iloc[0]['GPA']
    semester = student.iloc[0]['Semester']
    is_eligible = gpa >= 3.50 and (semester != 'Fall2025' or True)  # Assume payment cleared
    if not is_eligible:
        return jsonify({"status": "error", "message": "Student ineligible (GPA < 3.50 or payment issue)"}), 403

    # Validate course and section against courses.csv
    course_id = course_map.get(course, course)
    valid_section = courses_df[
        (courses_df['course_id'] == course_id) &
        (courses_df['section'] == section) &
        (courses_df['day'] == day) &
        (courses_df['start_time'] == time.split('-')[0])
    ]
    if valid_section.empty:
        return jsonify({"status": "error", "message": "Invalid course, section, day, or time"}), 400

    # Update assigned_sections.csv
    df.loc[df['Student_ID'] == student_id, ['Course', 'Assigned_Section']] = [course, section]
    df.to_csv('assigned_sections.csv', index=False)
    return jsonify({"status": "success", "student_id": student_id})

@app.route('/remove_schedule', methods=['POST'])
def remove_schedule():
    data = request.json
    student_id = data.get('student_id')

    # Load and update assigned_sections.csv
    df = pd.read_csv('assigned_sections.csv')
    if student_id not in df['Student_ID'].values:
        return jsonify({"status": "error", "message": "Student not found"}), 404

    df.loc[df['Student_ID'] == student_id, 'Assigned_Section'] = 'Not_Assigned'
    df.to_csv('assigned_sections.csv', index=False)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)