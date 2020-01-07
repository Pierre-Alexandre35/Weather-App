<?php 
require("db.php");

if(isset($_GET["query"])){

    $search = $_GET["query"];

    $results = $conn->prepare("SELECT * FROM cities WHERE city LIKE '{$search}%' 
    ORDER BY population DESC LIMIT 5");
} 

$results->execute();

foreach ($results as $row) {
    echo $row["city"] . "-" . $row["population"] ."<br/>";
}
?>