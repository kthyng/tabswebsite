<head>
    <title>Buoy Statuses</title>
</head>

<div id="container">

    <?php

    // include header from separate file
    include("../includes/header.html");

    // include navigation from separate file
    include("../includes/navigation.html");

    // read into an array the buoys
    $csv = array_map("str_getcsv", file("../includes/buoys.csv"));
    $header = array_shift($csv); // Seperate the header from data
    $buoycol = array_search("buoy", $header);  # save column name for buoys
    $table1col = array_search("table1", $header);  # save column name for table1
    $notescol = array_search("notes", $header);  # save column name for notes
    $active = array_search("active", $header);  # save column name for buoys being active

    // Select buoys by origin
    foreach ($csv as $row) {  // loop over each row in csv file
        // check if buoy is ndbc and active, etc
        if (strcmp($row[$active], "TRUE") == 0) {
            if (substr_compare($row[$table1col], "ndbc", 0, 4) == 0) {
            	$buoysndbc[] = $row[$buoycol];  // if so, save buoy name
            }
            elseif (substr_compare($row[$table1col], "ports", 0, 5) == 0) {
            	$buoysports[] = $row[$buoycol];
            }
            elseif (substr_compare($row[$table1col], "tcoon", 0, 5) == 0) {
            	$buoystcoon[] = $row[$buoycol];
            }
            elseif (substr_compare($row[$table1col], "nos", 0, 3) == 0) {
            	$buoysnos[] = $row[$buoycol];
            }
            elseif (substr_compare($row[$table1col], "ven", 0, 3) == 0) {
            	$buoystabs[] = $row[$buoycol];
            }
        }
        # inactive
        if (strcmp($row[$active], "FALSE") == 0) {
            if (substr_compare($row[$table1col], "ndbc", 0, 4) == 0) {
            	$buoysndbcia[] = $row[$buoycol];  // if so, save buoy name
            }
            elseif (substr_compare($row[$table1col], "ports", 0, 5) == 0) {
            	$buoysportsia[] = $row[$buoycol];
            }
            elseif (substr_compare($row[$table1col], "tcoon", 0, 5) == 0) {
            	$buoystcoonia[] = $row[$buoycol];
            }
            elseif (substr_compare($row[$table1col], "nos", 0, 3) == 0) {
            	$buoysnosia[] = $row[$buoycol];
            }
            elseif (substr_compare($row[$table1col], "ven", 0, 3) == 0) {
            	$buoystabsia[] = $row[$buoycol];
            }
        }
    }

    print "<br>";
    print "<h1>Station Information</h1>";

    print 'Note that a Python package is <a href="https://github.com/kthyng/tabs">available</a> to allow easy access to both data and model time series.';

    print "<h2>Active Stations</h2>";

    // TABS
    print "<h3>TABS Stations</h3>";
    print "<table cellspacing=1 width=100% align=left>";
    print "<tr> <th align=left>Station</th>	<th align=left>Notes</th> </tr>";
    # loop through rows in file
    foreach ($csv as $row) {  // loop over each row in csv file
        if ((strcmp($row[$active], "TRUE") == 0) && (strcmp($row[$table1col], "ven") == 0)) {
            print "<tr>";
            print "<th align=left>";  # Station name
            print "<a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$row[$buoycol]'>$row[$buoycol]</a>";
            print "</th>";
            print "<td align=left>$row[$notescol]</td>";
            print "</tr>";
        }
    }
    print "</table>";

    print "&nbsp;<br>";

    // Other stations
    print "<h3>Other Stations</h3>";
    print "<table cellspacing=1 width=100% align=left>";
    print "<tr> <th align=left>NDBC</th> <th align=left>TCOON</th> <th align=left>PORTS</th> <th align=left>NOS</th> </tr>";
    # loop through rows in file
    $nloops = max(count($buoysndbc),count($buoysports),count($buoystcoon),count($buoysnos));
    for ($i = 0; $i <= $nloops; $i++) {
        print "<tr>";
        print "<td><a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$buoysndbc[$i]'>$buoysndbc[$i]</a></td>";
        print "<td><a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$buoystcoon[$i]'>$buoystcoon[$i]</a></td>";
        print "<td><a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$buoysports[$i]'>$buoysports[$i]</a></td>";
        print "<td><a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$buoysnos[$i]'>$buoysnos[$i]</a></td>";
        print "</tr>";
    }
    print "</table>";


    print "<hr>";

    print "<h2>Inactive Stations</h2>";

    // TABS
    print "<h3>TABS Stations</h3>";
    print "<table cellspacing=1 width=100% align=left>";
    print "<tr> <th align=left>Station</th>	<th align=left>Notes</th> </tr>";
    # loop through rows in file
    foreach ($csv as $row) {  // loop over each row in csv file
        if ((strcmp($row[$active], "FALSE") == 0) && (strcmp($row[$table1col], "ven") == 0)) {
            print "<tr>";
            print "<th align=left>";  # Station name
            print "<a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$row[$buoycol]'>$row[$buoycol]</a>";
            print "</th>";
            print "<td align=left>$row[$notescol]</td>";
            print "</tr>";
        }
    }
    print "</table>";

    print "&nbsp;<br>";

    // Other stations
    print "<h3>Other Stations</h3>";

    print "<table cellspacing=1 width=100% align=left>";
    print "<tr> <th align=left>NDBC</th> <th align=left>TCOON</th> <th align=left>PORTS</th> <th align=left>NOS</th> </tr>";
    # loop through rows in file
    $nloops = max(count($buoysndbc),count($buoysports),count($buoystcoon),count($buoysnos));
    for ($i = 0; $i <= $nloops; $i++) {
        print "<tr>";
        print "<td><a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$buoysndbcia[$i]'>$buoysndbcia[$i]</a></td>";
        print "<td><a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$buoystcoonia[$i]'>$buoystcoonia[$i]</a></td>";
        print "<td><a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$buoysportsia[$i]'>$buoysportsia[$i]</a></td>";
        print "<td><a href='/tabswebsite/subpages/buoy_status_station.php?buoy=$buoysnosia[$i]'>$buoysnosia[$i]</a></td>";
        print "</tr>";
    }
    print "</table>";

    ?>

    <!-- include footer from separate file -->
    <?php include("../includes/footer.html");?>

</div>
