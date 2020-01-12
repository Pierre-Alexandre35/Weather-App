<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link
    rel="stylesheet"
    type="text/css"
    href="//github.com/downloads/lafeber/world-flags-sprite/flags32.css"/>
    <title>Document</title>
</head>
<body>
    
</body>
</html>

<?php 
require("db.php");

if(isset($_GET["query"])){

    $search = $_GET["query"];

    $results = $conn->prepare("SELECT * FROM cities WHERE city LIKE '{$search}%' 
    ORDER BY population DESC LIMIT 5");
} 

$results->execute();

foreach ($results as $row) {
    echo '<li class="cities-select">
     <div id="target-city"> '.$row["city"].' </div>
     <div id="target-country"> '.$row["country"].' </div>
     </li>';
}
?>