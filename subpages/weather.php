<head>
    <title>Marine Forecasts</title>
</head>

<div id="container">

    <!-- include header from separate file -->
    <?php include("../includes/header.html");?>


    <!-- include navigation from separate file -->
    <?php include("../includes/navigation.html");?>

    <?php

    $area=$_GET["area"];

    if ($area == "TX") {
        $heading = "Texas Coastal Marine Forecast";
        $urls = array("gmz400","gmz375","gmz355","gmz335","gmz300","gmz270",
                      "gmz250","gmz230","gmz200");
        $base = "http://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/gm/";
    }
    elseif ($area == "LA") {
        $heading = "Louisiana Coastal Marine Forecast";
        $urls = array("gmz570","gmz470");
        $base = "http://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/gm/";
    }
    elseif ($area == "offshore") {
        $heading = "Gulf of Mexico Offshore Marine Forecast";
        $urls = array("gmz011","gmz013","gmz015","gmz017","gmz001");
        $base = "http://tgftp.nws.noaa.gov/data/forecasts/marine/offshore/gm/";
    }

    print "<h2>$heading</h2>";
    foreach ($urls as $url) {
        $str = file_get_contents($base.$url.".txt");
        print "<br><br>";
        echo nl2br( $str );
    }

    ?>

</div>
