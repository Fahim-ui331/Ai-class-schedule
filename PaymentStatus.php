<?php
class PaymentStatus {
    private $conn;

    public function __construct($db_conn) {
        $this->conn = $db_conn;
    }

    // Get students who have cleared their payment
    public function getClearedPayments() {
        $query = "SELECT * FROM students WHERE payment_status = 'cleared'";
        $result = $this->conn->query($query);
        $students = [];
        while ($row = $result->fetch_assoc()) {
            $students[] = $row;
        }
        return $students;
    }

    // Get students who have pending payments
    public function getPendingPayments() {
        $query = "SELECT * FROM students WHERE payment_status = 'pending'";
        $result = $this->conn->query($query);
        $students = [];
        while ($row = $result->fetch_assoc()) {
            $students[] = $row;
        }
        return $students;
    }
}
?>
