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

        $gallery = $_GET["gallery"];  // get gallery variable

        $base = "http://pong.tamu.edu/~kthyng/movies/txla_plots/";
        $years = range(2004, 2014);
        $imagedate = "2004-07-30T00";

        // for individual variable pages
        if ($gallery) {

            $image = $base.$gallery."/".$imagedate.".png";

            foreach ($years as $year) {

                $movie = $base.$gallery."/".$year.".mp4";

                print "<div class=\"responsive\"><div class=\"gallery\">";
                print "<a target=\"_blank\" href=$movie width=\"300\" height=\"200\"><img src=$image alt=$year></a>";
                print "<div class=\"desc\">$year</div>";
                print "</div></div>";
            }
        }

        // Index page showing all variables
        if (! $gallery) {
            $base = "http://pong.tamu.edu/~kthyng/movies/txla_plots/";
            $year = 2004;
            $vars = array("salt", "speed", "ssh", "temp", "u", "v", "vort");
            $varnames = array("Salinity", "Speed", "Sea surface height",
                                "Temperature", "Along-shore velocity",
                                "Across-shore velocity", "Vertical Vorticity");
            $imagedate = "2004-07-30T00";

            // this syntax for looping over 2 arrays at once
            $array = array_combine($vars, $varnames);
            foreach ($array as $var => $varname) {
                $image = $base.$var."/".$imagedate.".png";
                $newpage = "gallery.php?gallery=".$var;
                $gallery = $var;  # set gallery variable

                print "<div class=\"responsive\"><div class=\"gallery\">";
                print "<a href=$newpage width=\"300\" height=\"200\"><img src=$image alt=$varname></a>";
                print "<div class=\"desc\">$varname</div>";
                print "</div></div>";
            }
        }


    ?>


</div>
