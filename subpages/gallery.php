<head>
    <title>Gallery</title>
</head>

<div id="container">

    <!-- include header from separate file -->
    <?php include("../includes/header.html");?>


    <!-- include navigation from separate file -->
    <?php include("../includes/navigation.html");?>

    <!-- Animations -->
    <br><br>
    <?php

        print "<form action=\"/tabswebsite/subpages/gallery.php\" method=\"get\">\n";

        $gallery = $_GET["gallery"];  // get gallery variable
        $res = $_GET["res"];  // get resolution

        if (! $res) {$res = "high";}  # high resolution by default

        $base = "http://pong.tamu.edu/movies/";
        $years = range(1993, 2017);

        // for individual variable pages
        if ($gallery) {

            foreach ($years as $year) {

                $imagedate = $year."-07-01T00";
                if ($gallery == "oxygen") {
                    $image = $base.$gallery."/".$year."/".$imagedate.".png";
                    $movie = $base.$gallery."/".$year."/".$year."_".$res.".mp4";
                }
                else {
                    $image = $base.$gallery."/".$imagedate.".png";
                    $movie = $base.$gallery."/".$year."_".$res.".mp4";
                }

                print "<div class=\"responsive\"><div class=\"gallery\">";
                print "<a target=\"_blank\" href=$movie width=\"300\" height=\"200\"><img src=$image alt=$year></a>";
                print "<div class=\"desc\">$year</div>";
                print "</div></div>";
            }
        }

        // Index page showing all variables
        if (! $gallery) {
            $base = "http://pong.tamu.edu/movies/";
            $year = 1993;
            $vars = array("salt", "speed", "ssh", "temp", "u", "v", "vort",
                          "dye_miss", "dye_atch", "dye_brazos", "oxygen");
            $varnames = array("Salinity", "Speed", "Sea surface height",
                                "Temperature", "Along-shore velocity",
                                "Across-shore velocity", "Vertical vorticity",
                                "Mississippi river dye", "Atchafalaya river dye",
                                "Brazos river dye", "Bottom oxygen");
            $imagedate = $year."-07-01T00";

            // check box for resolution
           print "<select id=\"res_id\" name=\"res\"  onchange=\"this.form.submit();\">";
           print "<option type=radio value=\"$res\">selected resolution: $res</option> ";
           print "<option type=radio value=\"high\">High resolution animations (70-400MB)</option> ";
           print "<option type=radio value=\"low\">Low resolution animations (20-130MB)</option> ";
           print "</select><br><br>";

            // this syntax for looping over 2 arrays at once
            $array = array_combine($vars, $varnames);
            foreach ($array as $var => $varname) {
                if ($var == "oxygen") {
                    $image = $base.$var."/".$year."/".$imagedate.".png";
                }
                else {
                    $image = $base.$var."/".$imagedate.".png";
                }
                $newpage = "gallery.php?gallery=".$var."&res=".$res;
                $gallery = $var;  # set gallery variable

                print "<div class=\"responsive\"><div class=\"gallery\">";
                print "<a href=$newpage width=\"300\" height=\"200\"><img src=$image alt=$varname></a>";
                print "<div class=\"desc\">$varname</div>";
                print "</div></div>";
            }
        }


    ?>


</div>
