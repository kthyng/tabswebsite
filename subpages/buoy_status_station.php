<head>
    <title>Station Status</title>
</head>

<div id="container">

    <!-- include header from separate file -->
    <?php include("../includes/header.html");?>


    <!-- include navigation from separate file -->
    <?php include("../includes/navigation.html");?>

    <?php

    $buoy=$_GET["buoy"];

    // Get buoy information
    // read into an array the buoys
    $csv = array_map("str_getcsv", file("../includes/buoys.csv"));
    $header = array_shift($csv); // Separate the header from data

    // Find row for buoy, either with built-in function or by search
    if (!function_exists('array_column')) {
        $buoycol = array_search("buoy", $header);  # save column name for buoy
        foreach ($csv as $row) {
            # if the desired buoy is found in the column, stop so that $row is correct
            if (strcmp($row[$buoycol],$buoy) == 0) {
                break;
            }
        }
    }
    else {
        $buoyarr = array_column($csv, 0);
        $buoyrow = array_search($buoy, $buoyarr);
        $row = $csv[$buoyrow];
    }

    // names
    $aliascol = array_search("alias", $header);  # save column name for alias
    $alias = $row[$aliascol];
    if (count($alias)>1) {
        print "<h2>Station $buoy/$alias</h2>";  // Station name/alternate name
    }
    else {
        print "<h2>Station $buoy</h2>";  // Station name
    }

    print "<table cellspacing=1 width=100% align=left>";

    // Who owns
    $table1col = array_search("table1", $header);  # save column name for table1
    $table1 = $row[$table1col];
    if (strpos($table1, 'ndbc') !== false) {
        $owns = "NDBC/NOAA";  // if so, save buoy name
    }
    elseif (strpos($table1, 'ports') !== false) {
        $owns = "PORTS/NOAA";
    }
    elseif (strpos($table1, 'tcoon') !== false) {
        $owns = "TCOON/NOAA";
    }
    elseif (strpos($table1, 'nos') !== false) {
        $owns = "NOS/NOAA";
    }
    elseif (strpos($table1, 'ven') !== false) {
        $owns = "TABS";
    }
    print "<tr><th align=left>$owns\n</th></tr>";


    // lat/lon
    $latcol = array_search("lat", $header);
    $loncol = array_search("lon", $header);
    print "<tr><td>$row[$latcol],$row[$loncol]</td></tr>";

    // description
    $col = array_search("description", $header);
    print "<tr><td>$row[$col]</td></tr>";

    print "<tr><td><br></td></tr>";

    // notes
    $col = array_search("notes", $header);
    $status = $row[$col];
    if (!empty($status)) {
        print "<tr><td><b>Status:</b> $status</td></tr>";
        print "<tr><td><br></td></tr>";
    }

    // depth
    $col = array_search("depth", $header);
    $depth = $row[$col];
    if (!empty($depth)) {
        print "<tr><td><b>Depth:</b> $depth [meters]</td></tr>";
    }

    // angle
    $col = array_search("angle", $header);
    $angle = $row[$col];
    if (!empty($depth)) {
        print "<tr><td><b>Flood tide rotation angle:</b> $angle [&deg; True]</td></tr>";
        print "<tr><td><br></td></tr>";
    }

    // data available
    $tables = array("table1", "table2", "table3", "table4", "table5");
    print "<tr><th align=left>Data types available: </th> <th align=left> Complete Archives (download)</th></tr>";
    foreach ($tables as $table) {
        $col = array_search($table, $header);
        if (strcmp($row[$col], "ven") == 0) {
            print "<tr><td>&bull; Currents</td>";
            $url = "../daily/tabs_".$buoy."_ven_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
        }
        elseif (strcmp($row[$col], "salt") == 0) {
            print "<tr><td>&bull; Water temperature, Salinity</td>";
            $url = "../daily/tabs_".$buoy."_salt_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
        }
        elseif (strcmp($row[$col], "met") == 0) {
            print "<tr><td>&bull; Wind, Atmospheric pressure, Relative humidity</td>";
            $url = "../daily/tabs_".$buoy."_met_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
        }
        elseif (strcmp($row[$col], "wave") == 0) {
            print "<tr><td>&bull; Wave height, Wave period</td>";
            $url = "../daily/tabs_".$buoy."_wave_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
        }
        elseif (strcmp($row[$col], "ndbc") == 0) {
            print "<tr><td>&bull; Wind, Atmospheric pressure, Relative humidity, Air temp</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
            print "<tr><td>&bull; Wave height, Wave period</td></tr>";
            print "<tr><td>&bull; Water temperature</td></tr>";
        }
        elseif (strcmp($row[$col], "ndbc-met") == 0) {
            print "<tr><td>&bull; Wind, Atmospheric pressure, Air temp</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
        }
        elseif (strcmp($row[$col], "ndbc-nowave") == 0) {
            print "<tr><td>&bull; Wind, Atmospheric pressure, Air temp</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
            print "<tr><td>&bull; Water temperature</td></tr>";
        }
        elseif (strcmp($row[$col], "ports") == 0) {
            print "<tr><td>&bull; Currents</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
            // either cross-channel or with depth
            $colsideways = array_search("Distance to center of bin [m]", $header);
            // echo $row[$colsideways];
            // adcp is sideways if has a number in this place
            if (is_numeric($row[$colsideways])) {
                print "<tr><td>&bull; Cross-channel ADCP data</td>";
                $url = "../daily/".$buoy."_full_all";
                print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
            }
            // a few stations don't have this data
            elseif (strcmp($buoy, "ps0201") == 0 or strcmp($buoy, "ps0301") == 0 or strcmp($buoy, "ps0401") == 0) {
                } //nothing for these buoys
            // adcp is with depth if made it to this point
            else {
                print "<tr><td>&bull; ADCP data with depth</td>";
                $url = "../daily/".$buoy."_full_all";
                print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
                }
            }
        elseif (strcmp($row[$col], "currentspredict") == 0) {
            print "<tr><td>&bull; NOAA-modeled currents</td></tr>";
        }
        elseif (strcmp($row[$col], "tcoon") == 0) {
            print "<tr><td>&bull; Wind, Atmospheric pressure, Air temp</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
            print "<tr><td>&bull; Sea surface height</td></tr>";
            print "<tr><td>&bull; Water temperature</td></tr>";
        }
        elseif (strcmp($row[$col], "tcoon-tide") == 0) {
            print "<tr><td>&bull; Sea surface height</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
        }
        elseif (strcmp($row[$col], "nos") == 0) {
            print "<tr><td>&bull; Wind, Atmospheric pressure, Air temp</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
            print "<tr><td>&bull; Sea surface height</td></tr>";
            print "<tr><td>&bull; Water temperature</td></tr>";
        }
        elseif (strcmp($row[$col], "nos-met") == 0) {
            print "<tr><td>&bull; Wind, Atmospheric pressure, Air temp</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
        }
        elseif (strcmp($row[$col], "nos-water") == 0) {
            print "<tr><td>&bull; Sea surface height</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
            print "<tr><td>&bull; Water temperature</td></tr>";
        }
        elseif (strcmp($row[$col], "nos-cond") == 0) {
            print "<tr><td>&bull; Wind, Atmospheric pressure, Air temp</td>";
            $url = "../daily/".$buoy."_all";
            print "<td><a href=$url>uncompressed text</a>, <a href=$url.hdf>hdf</a></td></tr>";
            print "<tr><td>&bull; Sea surface height</td></tr>";
            print "<tr><td>&bull; Water temperature</td></tr>";
            print "<tr><td>&bull; Salinity</td></tr>";
        }
    }
    print "<tr><td><br></td></tr>";

    // links to websites
    $col = array_search("url_station", $header);
    $var = $row[$col];
    if (!empty($var)) {
        print "<tr><td><b><a href='$var'>Station home page</b></a></td></tr>";
        print "<tr><td><br></td></tr>";
    }

    $col = array_search("url_data", $header);
    $var = $row[$col];
    if (!empty($var)) {
        print "<tr><td><b><a href='$var'>Station data page</b></a></td></tr>";
        print "<tr><td><br></td></tr>";
    }

    print "</table>";

    // include footer from separate file
    include("../includes/footer.html")

    ?>

</div>
