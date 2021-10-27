<?php
$servername = "localhost";
$username = "pi";
$password = "raspberry";
$dbname = "counter_iot";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//cek tabel ada atau tidak
$sql = "SHOW TABLES LIKE 'status'";
$result = $conn->query($sql);
if ($result->num_rows == 0) {
    //jika tidak ada tabel status, maka dibuat dan isi
    $sql = "CREATE TABLE status (btn INT PRIMARY KEY, counter INT NOT NULL, last_update TIMESTAMP);";
    $sql .= "INSERT INTO status (btn, counter, last_update) VALUES ('1','0',now()),('2','0',now()),('3','0',now()),('4','0',now()),('5','0',now());";
    if ($conn->multi_query($sql) === FALSE) {
        echo "Error updating record: " . $conn->error;
    }
}
