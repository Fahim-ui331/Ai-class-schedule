<?php
class EnrollmentManager {
    private $conn;

    public function __construct($db_conn) {
        $this->conn = $db_conn;
    }

    // Check if payment cleared
    public function isPaymentCleared($student_id) {
        $query = "SELECT payment_status FROM students WHERE id = $student_id";
        $result = $this->conn->query($query);
        if($row = $result->fetch_assoc()) {
            return $row['payment_status'] === 'cleared';
        }
        return false;
    }

    // Check prerequisite
    public function hasCompletedPrerequisite($student_id, $course_id) {
        $query = "
            SELECT prerequisite_course_id 
            FROM courses 
            WHERE id = $course_id
        ";
        $result = $this->conn->query($query);
        if($row = $result->fetch_assoc()) {
            $prereq = $row['prerequisite_course_id'];
            if(!$prereq) return true; // No prerequisite
            // Check if student passed prerequisite
            $check = "SELECT * FROM student_courses 
                      WHERE student_id = $student_id 
                      AND course_id = $prereq 
                      AND grade IN ('A','B','C')"; // Assuming passing grades
            $res = $this->conn->query($check);
            return $res->num_rows > 0;
        }
        return false;
    }

    // Check time conflict
    public function hasTimeConflict($student_id, $section_id) {
        $query = "
            SELECT s.day, s.start_time, s.end_time
            FROM sections s
            JOIN student_courses sc ON sc.section_id = s.id
            WHERE sc.student_id = $student_id
        ";
        $result = $this->conn->query($query);
        // Get target section time
        $secQuery = "SELECT day, start_time, end_time FROM sections WHERE id = $section_id";
        $secRes = $this->conn->query($secQuery);
        $section = $secRes->fetch_assoc();

        while($row = $result->fetch_assoc()) {
            if($row['day'] === $section['day'] &&
               !(strtotime($section['end_time']) <= strtotime($row['start_time']) ||
                 strtotime($section['start_time']) >= strtotime($row['end_time']))) {
                return true; // Conflict exists
            }
        }
        return false;
    }

    // Check if section has seat
    public function hasAvailableSeat($section_id) {
        $query = "SELECT capacity, enrolled FROM sections WHERE id = $section_id";
        $result = $this->conn->query($query);
        $section = $result->fetch_assoc();
        return $section['enrolled'] < $section['capacity'];
    }

    // Attempt enrollment
    public function enroll($student_id, $section_id) {
        if(!$this->isPaymentCleared($student_id)) {
            return "Payment not cleared.";
        }
        if($this->hasTimeConflict($student_id, $section_id)) {
            return "Time conflict with another enrolled section.";
        }
        // Check prerequisite
        $courseQuery = "SELECT course_id FROM sections WHERE id = $section_id";
        $res = $this->conn->query($courseQuery);
        $course = $res->fetch_assoc();
        if(!$this->hasCompletedPrerequisite($student_id, $course['course_id'])) {
            return "Prerequisite not completed.";
        }
        if(!$this->hasAvailableSeat($section_id)) {
            return "Section is full.";
        }
        // All checks passed, enroll student
        $this->conn->query("INSERT INTO student_courses(student_id, section_id) VALUES($student_id, $section_id)");
        $this->conn->query("UPDATE sections SET enrolled = enrolled + 1 WHERE id = $section_id");
        return "Enrollment successful!";
    }
}
?>
