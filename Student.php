<?php
class Student {
    private $conn;

    public function __construct($db_conn) {
        $this->conn = $db_conn;
    }

    // Save student preferences including payment and cgpa status
    public function saveStudentData($student_id, $preferred_time, $preferred_section, $cgpa, $payment_status) {
        $eligibility_status = ($cgpa >= 3.5) ? 'priority' : 'normal';
        $query = "INSERT INTO students (student_id, preferred_time, preferred_section, cgpa, payment_status, eligibility_status)
                  VALUES (?, ?, ?, ?, ?, ?)";

        $stmt = $this->conn->prepare($query);
        $stmt->bind_param("issdss", $student_id, $preferred_time, $preferred_section, $cgpa, $payment_status, $eligibility_status);

        if ($stmt->execute()) {
            echo "Student data saved successfully!";
        } else {
            echo "Error: " . $stmt->error;
        }
    }

    // Get all student data
    public function getAllStudents() {
        $query = "SELECT * FROM students";
        $result = $this->conn->query($query);
        $students = [];
        while ($row = $result->fetch_assoc()) {
            $students[] = $row;
        }
        return $students;
    }

    // Update student eligibility status based on cgpa
    public function updateEligibilityStatus($student_id, $cgpa) {
        $eligibility_status = ($cgpa >= 3.5) ? 'priority' : 'normal';
        $query = "UPDATE students SET eligibility_status = ? WHERE student_id = ?";
        $stmt = $this->conn->prepare($query);
        $stmt->bind_param("si", $eligibility_status, $student_id);

        if ($stmt->execute()) {
            echo "Eligibility status updated for student {$student_id}.";
        } else {
            echo "Error: " . $stmt->error;
        }
    }
}
?>
