<?php
class CGPAStatus {
    private $conn;

    public function __construct($db_conn) {
        $this->conn = $db_conn;
    }

    // Get all students with CGPA >= 3.50 (priority)
    public function getPriorityStudents() {
        $query = "SELECT * FROM students WHERE eligibility_status = 'priority'";
        $result = $this->conn->query($query);
        $students = [];
        while ($row = $result->fetch_assoc()) {
            $students[] = $row;
        }
        return $students;
    }

    // Get all students with CGPA < 3.50 (normal)
    public function getNormalStudents() {
        $query = "SELECT * FROM students WHERE eligibility_status = 'normal'";
        $result = $this->conn->query($query);
        $students = [];
        while ($row = $result->fetch_assoc()) {
            $students[] = $row;
        }
        return $students;
    }
}
?>
