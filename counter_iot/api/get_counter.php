<?php
require_once "conn.php";

$sql = "SELECT * FROM status";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    $data=[];
    while ($row = $result->fetch_assoc()) {
        array_push($data, $row);
    }
    echo json_encode($data);
} else {
    echo json_encode([]);
}
$conn->close();
