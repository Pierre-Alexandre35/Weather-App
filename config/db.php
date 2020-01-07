<?php 

$servername = "localhost";

$username = "root";

$password = "";


try{
    $conn = new PDO("mysql:host=$servername;dbname=weather-app", $username, $password,[
        PDO::ATTR_EMULATE_PREPARES => false, 
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ]);
} catch (PDOException $e){
    echo "Connection failed: " . $e->getMessage();
}


?>