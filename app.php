<?php
// Include the database connection and the classes
include 'db_connection.php';
include 'Student.php';
include 'PaymentStatus.php';
include 'CGPAStatus.php';

// Create a new database connection
$db_conn = new mysqli('localhost', 'root', 'password', 'class_scheduler');

// Check if connection was successful
if ($db_conn->connect_error) {
    die("Connection failed: " . $db_conn->connect_error);
}

// Instantiate the classes
$student = new Student($db_conn);
$paymentStatus = new PaymentStatus($db_conn); // Changed from EnrollmentManager to PaymentStatus
$cgpaStatus = new CGPAStatus($db_conn);

// Example usage:

// Save a new student's data
$student->saveStudentData(12345, 'morning', 'A1', 3.8, 'cleared');

// Get all students who have cleared payments
$cleared_students = $paymentStatus->getClearedPayments(); // Restored original method

// Get all students who are eligible (priority based on CGPA)
$priority_students = $cgpaStatus->getPriorityStudents();

// Get all students who are not eligible (normal students)
$normal_students = $cgpaStatus->getNormalStudents();

// Output the students
echo "<pre>";
print_r($cleared_students);
print_r($priority_students);
print_r($normal_students);
echo "</pre>";

?>