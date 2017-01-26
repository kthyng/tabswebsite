<div id="container">

    <?php

    // include header from separate file
    include("includes/header.html");

    // include navigation from separate file
    include("includes/navigation.html");

    if (php_uname('n') == 'barataria.tamu.edu') {
        $command = escapeshellcmd('/usr/bin/python3 run_buoy_status.py');
    }
    else if (php_uname('n') == 'tahoma.local') {
        $command = escapeshellcmd('/anaconda/bin/python run_buoy_status.py');
    }

    print "<br><br>";
    print "<center><h2>TABS Buoy Status</h2></center>";
    passthru($command);

    ?>

</div>
