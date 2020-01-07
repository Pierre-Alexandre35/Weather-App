<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Weather</title>
</head>
<body>
    <?php require_once("config/db.php")?>
    <h2>Weather</h2>
    <input type="text" name="city-search" class="city-search" id="city-search">
    <ul class="result">
    </ul>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <script src="scripts/app.js"></script>
</body>
</html>