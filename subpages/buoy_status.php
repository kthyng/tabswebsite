<head>
    <title>Buoy Statuses</title>
</head>

<div id="container">

    <?php

    // include header from separate file
    include("../includes/header.html");

    // include navigation from separate file
    include("../includes/navigation.html");

    if (php_uname('n') == 'barataria.tamu.edu') {
        $command = escapeshellcmd('/usr/bin/python3 ../python/run_buoy_status.py');
    }
    else if (php_uname('n') == 'tahoma.local') {
        $command = escapeshellcmd('/anaconda/bin/python ../python/run_buoy_status.py');
    }

    // print "<br><br>";
    // print "<h2>TABS Buoy Status</h2>";
    // passthru($command);

    // read into an array the buoys
    $csv = array_map("str_getcsv", file("../includes/buoys.csv"));
    $header = array_shift($csv); // Seperate the header from data
    $buoycol = array_search("buoy", $header);  # save column name for buoys
    $aliascol = array_search("alias", $header);  # save column name for alias
    $descriptioncol = array_search("description", $header);  # save column name for description
    $loncol = array_search("lon", $header);  # save column name for lon
    $latcol = array_search("lat", $header);  # save column name for lat
    $table1col = array_search("table1", $header);  # save column name for table1
    $table2col = array_search("table2", $header);  # save column name for table2
    $table3col = array_search("table3", $header);  # save column name for table3
    $table4col = array_search("table4", $header);  # save column name for table4
    $table5col = array_search("table5", $header);  # save column name for table5
    $active = array_search("active", $header);  # save column name for buoys being active
    foreach ($csv as $row) {  // loop over each row in csv file
        // check if buoy is active
        if (strcmp($row[$active], "TRUE") == 0) {
        	$buoysa[] = $row[$buoycol];  // if so, save buoy name
        }
        // check if buoy is inactive
        if (strcmp($row[$active], "FALSE") == 0) {
        	$buoysia[] = $row[$buoycol];  // if so, save buoy name
        }
    }

    print "<h2>Station Information</h2>\n";

    print "<h3>Active Stations</h3>\n";
    print "<table cellspacing=1 width=100% align=center>";

    # loop through rows in file
    foreach ($csv as $row) {  // loop over each row in csv file
        if (strcmp($row[$active], "TRUE") == 0) {
            print "<tr><th>$row[$buoycol]</th>";  # Station name
            print "<td>$row[$aliascol]</td>";  # Alternate station name
            print "<td>$row[$descriptioncol]</td>";  # Description of station
            print "<td>$row[$loncol]</td>";  # longitude
            print "<td>$row[$latcol]</td>";  # latitude

            if (strcmp($row[$table1col], "ven") == 0) {
                print "<td>Currents</td>";
            }
            if (strcmp($row[$table3col], "salt") == 0) {
                print "<td>Water properties</td>";
            }
            if (strcmp($row[$table4col], "met") == 0) {
                print "<td>Met</td>";
            }
            if (strcmp($row[$table5col], "wave") == 0) {
                print "<td>Waves</td>";
            }
            print "</tr>";
        }
        // // check if buoy is active
        // if (strcmp($row[$active], "TRUE") == 0) {
        // 	$buoysa[] = $row[$col];  // if so, save buoy name
        // }
        // // check if buoy is inactive
        // if (strcmp($row[$active], "FALSE") == 0) {
        // 	$buoysia[] = $row[$col];  // if so, save buoy name
        // }
    }


    // // list active bouys
    // foreach ($buoysa as $b) {
    //     print "<tr><th>$b</th></tr>\n";
    // }



    ?>

    <!-- <h2>TABS Buoy Status</h2>
    <table cellspacing=4 width=100% align=center> -->
    <!-- header -->
    <!-- <tr> <th>Buoy</th>	<th>System health</th> <th>Lat [N]</th> <th>Lon [W]</th> <th>Lease block</th> <th>Water depth</th> <th>Archive*</th> <th>Notes</th> </tr> -->




    <!-- active buoys -->
    <!-- <tr> <td>B</td> -->
        <!-- <td><span class="green">C</span>
            <span class="green">M</span>
            <span class="green">T</span>
            <span class="green">E</span>
            <span class="none">W</span>
            <span class="red">P</span></td>
        <td>28&deg; 58.939'</td>
        <td>94&deg; 53.944'</td>
        <td>GA-252</td>
        <td>62 ft (19 m)</td>
        <td><a href="/tabswebsite/daily/tabs_B_ven_all.gz">C</a>
            <a href="/tabswebsite/daily/tabs_B_met_all.gz">M</a>
            W
            <a href="/tabswebsite/daily/tabs_B_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed 02/03/2017. Batteries Dead.</td> </tr> -->

    <!-- <tr> <td>D</td>
        <td><span class="green">C</span>
            <span class="none">M</span>
            <span class="green">T</span>
            <span class="green">E</span>
            <span class="none">W</span>
            <span class="green">P</span></td>
        <td>27&deg; 56.376'</td>
        <td>96&deg; 50.574'</td>
        <td>MA-691</td>
        <td>59 ft (18 m)</td>
        <td><a href="/tabswebsite/daily/tabs_D_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_D_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed 04/09/2017.</td> </tr>

    <tr> <td>F</td>
        <td><span class="green">C</span>
            <span class="none">M</span>
            <span class="green">T</span>
            <span class="green">E</span>
            <span class="none">W</span>
            <span class="green">P</span></td>
        <td>28&deg; 50.550'</td>
        <td>94&deg; 14.496'</td>
        <td>HI-A69</td>
        <td>79 ft (24 m)</td>
        <td><a href="/tabswebsite/daily/tabs_F_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_F_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed on 02/02/2017.</td> </tr>

    <tr> <td>J</td>
        <td><span class="green">C</span>
            <span class="green">M</span>
            <span class="green">T</span>
            <span class="green">E</span>
            <span class="none">W</span>
            <span class="green">P</span></td>
        <td>26&deg; 11.484'</td>
        <td>97&deg; 03.042'</td>
        <td>PS-1126</td>
        <td>66 ft (20 m)</td>
        <td><a href="/tabswebsite/daily/tabs_J_ven_all.gz">C</a>
            <a href="/tabswebsite/daily/tabs_J_met_all.gz">M</a>
            W
            <a href="/tabswebsite/daily/tabs_J_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed on 01/05/2017.</td> </tr>

    <tr> <td>K</td>
        <td><span class="green">C</span>
            <span class="green">M</span>
            <span class="red">T</span>
            <span class="green">E</span>
            <span class="green">W</span>
            <span class="green">P</span></td>
        <td>26&deg; 13.008'</td>
        <td>96&deg; 29.988'</td>
        <td>PI-745</td>
        <td>203 ft (62 m)</td>
        <td><a href="/tabswebsite/daily/tabs_K_ven_all.gz">C</a>
            <a href="/tabswebsite/daily/tabs_K_met_all.gz">M</a>
            <a href="/tabswebsite/daily/tabs_K_wave_all.gz">W</a>
            <a href="/tabswebsite/daily/tabs_K_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed on 04/08/2017.</td> </tr> -->

    <!-- <tr> <td>R</td>
        <td><span class="green">C</span>
            <span class="none">M</span>
            <span class="green">T</span>
            <span class="green">E</span>
            <span class="none">W</span>
            <span class="green">P</span></td>
        <td>29&deg; 38.100'</td>
        <td>93&deg; 38.502'</td>
        <td>WC-055</td>
        <td>30 ft (9 m)</td>
        <td><a href="/tabswebsite/daily/tabs_R_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_R_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed on 02/02/2017.</td> </tr>

    <tr> <td>V</td>
        <td><span class="green">C</span>
            <span class="green">M</span>
            <span class="green">T</span>
            <span class="green">E</span>
            <span class="green">W</span>
            <span class="red">P</span></td>
        <td>27&deg; 53.796'</td>
        <td>93&deg; 35.838'</td>
        <td>HI-A389</td>
        <td>292 ft (89 m)</td>
        <td><a href="/tabswebsite/daily/tabs_V_ven_all.gz">C</a>
            <a href="/tabswebsite/daily/tabs_V_met_all.gz">M</a>
            <a href="/tabswebsite/daily/tabs_V_wave_all.gz">W</a>
            <a href="/tabswebsite/daily/tabs_V_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed on 08/04/2016.</td> </tr>

    <tr> <td>W</td>
        <td><span class="green">C</span>
            <span class="none">M</span>
            <span class="green">T</span>
            <span class="green">E</span>
            <span class="none">W</span>
            <span class="green">P</span></td>
        <td>28&deg; 21.042'</td>
        <td>96&deg; 00.348'</td>
        <td>BR-492</td>
        <td>69 ft (21 m)</td>
        <td><a href="/tabswebsite/daily/tabs_W_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_W_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed on 06/05/2017</td> </tr>

    <tr> <td>X</td>
        <td><span class="green">C</span>
            <span class="green">M</span>
            <span class="green">T</span>
            <span class="green">E</span>
            <span class="green">W</span>
            <span class="green">P</span></td>
        <td>27&deg; 03.960'</td>
        <td>96&deg; 20.298'</td>
        <td></td>
        <td>948 ft (289 m)</td>
        <td><a href="/tabswebsite/daily/tabs_X_ven_all.gz">C</a>
            <a href="/tabswebsite/daily/tabs_X_met_all.gz">M</a>
            <a href="/tabswebsite/daily/tabs_X_wave_all.gz">W</a>
            <a href="/tabswebsite/daily/tabs_X_salt_all.gz">P</a></td>
        <td>In Service. Buoy redeployed on 04/08/2017.</td> </tr>

    <tr> <td>A</td>
        <td><span class="gray">C</span>
            <span class="none">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>29&deg; 31.950'</td>
        <td>93&deg; 48.700'</td>
        <td>SP-018</td>
        <td>39 ft (12 m)</td>
        <td><a href="/tabswebsite/daily/tabs_A_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_A_salt_all.gz">P</a></td>
        <td>Retired 1997/3/25. Data available 1995/8/12 - 1995/10/8.</td> </tr>

    <tr> <td>C</td>
        <td><span class="gray">C</span>
            <span class="none">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>28&deg; 48.549'</td>
        <td>94&deg; 45.126'</td>
        <td>GA-320</td>
        <td>72 ft (22 m)</td>
        <td><a href="/tabswebsite/daily/tabs_C_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_C_salt_all.gz">P</a></td>
        <td>Retired 1997/3/17. Data available 1995/4/2 - 1996/11/29.</td> </tr>

    <tr> <td>E</td>
        <td><span class="gray">C</span>
            <span class="none">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>27&deg; 20.300'</td>
        <td>97&deg; 06.000'</td>
        <td>MU-858</td>
        <td>90 ft (27 m)</td>
        <td><a href="/tabswebsite/daily/tabs_E_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_E_salt_all.gz">P</a></td>
        <td>Retired 1996/6/5 (no cell service). <br>Data available 1995/6/1-1995/7/20 and 1995/11/2-1996/1/16.</td> </tr>

    <tr> <td>G</td>
        <td><span class="gray">C</span>
            <span class="none">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>29&deg; 33.000'</td>
        <td>93&deg; 28.000'</td>
        <td>WC-095</td>
        <td>41 ft (12 m)</td>
        <td><a href="/tabswebsite/daily/tabs_G_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_G_salt_all.gz">P</a></td>
        <td>Retired 1998/6/15. Data available 1997/3/11 - 1998/6/8.</td> </tr>

    <tr> <td>H</td>
        <td><span class="gray">C</span>
            <span class="gray">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>27&deg; 52.045'</td>
        <td>96&deg; 32.601'</td>
        <td></td>
        <td></td>
        <td><a href="/tabswebsite/daily/tabs_H_ven_all.gz">C</a>
            <a href="/tabswebsite/daily/tabs_H_met_all.gz">M</a>
            W
            <a href="/tabswebsite/daily/tabs_H_salt_all.gz">P</a></td>
        <td>Retired. Data available 1997/06/05 - 1998/6/22,<br>2005/08/27 - 2005/10/14, 2006/8/24 - 2007/8/5.</td> </tr>

    <tr> <td>L</td>
        <td><span class="gray">C</span>
            <span class="none">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>28&deg; 02.500'</td>
        <td>94&deg; 07.000'</td>
        <td>HI-A543</td>
        <td>270 ft (82 m)</td>
        <td><a href="/tabswebsite/daily/tabs_L_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_L_salt_all.gz">P</a></td>
        <td>Retired 1998/10/28. Data available 1998/4/20 - 1998/10/28.</td> </tr>

    <tr> <td>M</td>
        <td><span class="gray">C</span>
            <span class="none">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>28&deg; 11.526'</td>
        <td>94&deg; 11.484'</td>
        <td>HI-A515</td>
        <td>186 ft (57 m)</td>
        <td><a href="/tabswebsite/daily/tabs_M_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_M_salt_all.gz">P</a></td>
        <td>Retired 1999/12/1. Data available 1999/3/2 - 1999/12/1.</td> </tr>

    <tr> <td>N</td>
        <td><span class="gray">C</span>
            <span class="gray">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="gray">W</span>
            <span class="gray">P</span></td>
        <td>27&deg; 53.418'</td>
        <td>94&deg; 02.202'</td>
        <td>HI-A595</td>
        <td>344 ft (105 m)</td>
        <td><a href="/tabswebsite/daily/tabs_N_ven_all.gz">C</a>
            <a href="/tabswebsite/daily/tabs_N_met_all.gz">M</a>
            <a href="/tabswebsite/daily/tabs_N_wave_all.gz">W</a>
            <a href="/tabswebsite/daily/tabs_N_salt_all.gz">P</a></td>
        <td>Retired 2017/1/4. Data available 2002/01/23 - 2016/11/10.</td> </tr>

    <tr> <td>P</td>
        <td><span class="gray">C</span>
            <span class="none">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>29&deg; 09.972'</td>
        <td>94&deg; 02.202'</td>
        <td>VR-102</td>
        <td>66 ft (20 m)</td>
        <td><a href="/tabswebsite/daily/tabs_P_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_P_salt_all.gz">P</a></td>
        <td>Retired 2000/2/19. Data available 1998/7/22 - 2000/2/19.</td> </tr> -->

    <!-- <tr> <td>S</td>
        <td><span class="gray">C</span>
            <span class="none">M</span>
            <span class="gray">T</span>
            <span class="gray">E</span>
            <span class="none">W</span>
            <span class="none">P</span></td>
        <td>28&deg; 26.185'</td>
        <td>92&deg; 48.669'</td>
        <td>BR-492</td>
        <td>72 ft (22 m)</td>
        <td><a href="/tabswebsite/daily/tabs_S_ven_all.gz">C</a>
            M
            W
            <a href="/tabswebsite/daily/tabs_S_salt_all.gz">P</a></td>
        <td>Retired 2001/7/26. Data available 1999/2/19 - 2001/7/23.</td> </tr> -->


    <br><br>
    <table cellspacing=4 width=80% align=center>
    <caption style="text-align:left"><h3>Legend</h3></caption>
    <tr> <td>C</td>	<td>Current meter systems (current speed, direction, water temperature)</td> </tr>
    <tr> <td>M</td>	<td>Meteorological systems (wind speed,direction, air temperature, air pressure, humidity)</td> </tr>
    <tr> <td>T</td>	<td>Telemetry system (primary: satellite or cellular, backup: Argos)</td> </tr>
    <tr> <td>E</td>	<td>Engineering system</td> </tr>
    <tr> <td>W</td>	<td>Wave data system</td> </tr>
    <tr> <td>P</td>	<td>Water property system</td> </tr>

    <tr> <td bgcolor='limegreen'></td>	<td>Data systems and telemetry system are functioning normally.</td> </tr>
    <tr> <td bgcolor='yellow'></td>	<td>Data systems are functioning normally with degraded data quality. Telemetry system is functioning normally but with degraded performance.</td> </tr>
    <tr> <td bgcolor='orange'></td>	<td>Data systems are partially functional with some loss of data. Primary telemetry system is not functioning; data is returned via backup telemetry.</td> </tr>
    <tr> <td bgcolor='#D96259'></td>	<td>Data systems are not functioning; no good data returned. Primary and backup telemetry systems both not functioning; no data is returned in real time.</td> </tr>
    <tr> <td bgcolor='lightgray'></td>	<td>Data system used to run but is now discontinued.</td> </tr>
    <tr> <td></td>	<td>Data system never existed.</td> </tr>
    <tr> <td></td>	<td>*Note: any archive file can be accessed either with or without the suffix '.gz' to get a gzipped compressed file or an uncompressed text file, respectively.</td></td>

    </table>

    <!-- include footer from separate file -->
    <?php include("../includes/footer.html");?>

</div>
