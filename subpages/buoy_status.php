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

    print "<br><br>";
    print "<h2>TABS Buoy Status</h2>";
    passthru($command);

    ?>

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
    <tr> <td bgcolor='firebrick'></td>	<td>Data systems are not functioning; no good data returned. Primary and backup telemetry systems both not functioning; no data is returned in real time.</td> </tr>
    <tr> <td bgcolor='lightgray'></td>	<td>Data system used to run but is now discontinued.</td> </tr>
    <tr> <td></td>	<td>Data system never existed.</td> </tr>

    </table>
</div>
