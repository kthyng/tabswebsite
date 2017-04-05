<?php

umask(0022);

$cm2e=.01943845;
$m2e=1.943845;
$degc="&#176;C";
$degf="&#176;F";
$degm="&#176;M";
$degt="&#176;T";

$PageTitle="TABS Buoy Database Query page";

if ($_SERVER['REQUEST_METHOD'] != 'GET') {
echo "<meta HTTP-EQUIV=\"REFRESH\" CONTENT=\"3;URL=tabsqueryform.php\">";
echo "<meta HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">";

	print "<p><b>Database search form is here:</b> <a href=/tabswebsite/subpages/tabsqueryform.php>tabsqueryform.php</a>";
} else {

// bring in data from tabsqueryform.php
$Buoyname=$_GET["Buoyname"];
$table=$_GET["table"];
$datepicker=$_GET["datepicker"];
$datatype=$_GET["Datatype"];
$tz=$_GET["tz"];
$units = $_GET["units"];

if (! $units) {$units = 'M';}
if (! $tz) {$tz = 'UTC';}

if ($tz == 'UTC') {
    $tzname = 'UTC';
}
else if ($tz == 'central') {
    $tzname = 'US/Central';
}

if ($units == 'M') {
    $unitsname = 'Metric';
}
else if ($units == 'E') {
    $unitsname = 'English';
}

// convert from table short name to descriptive name string
if ($table == 'ven') {
    $tablename = 'Velocity data';
}
elseif ($table == 'met') {
    $tablename = 'Meteorological data';
}
elseif ($table == 'salt') {
    $tablename = 'Water property data';
}
elseif ($table == 'eng') {
    $tablename = 'System data';
}
elseif ($table == 'wave') {
    $tablename = 'Wave data';
}
elseif ($table == 'ndbc') {
    $tablename = 'NDBC data';
}


// if recent and data table, give ability to switch to recent and image
if ($datatype=="data"){
    $newdatatype="pic";
    $newdatatypename="image";
}
elseif ($datatype=="pic"){
    $newdatatype="data";
    $newdatatypename="table";
}
elseif ($datatype=="download"){
    $newdatatype="data";
    $newdatatypename="table";
}

$noinstr = False;  // Flag for if instrument is not available
// Met instrument availability
if ($table == "met" && ! preg_match('/B|H|J|K|N|V/',$Buoyname) ) {
    $noinstr = True;
    $statement = "No meteorological data available for buoy ".$Buoyname;
}
// Salt instrument availability
else if ($table == "salt" && ! preg_match('/B|D|F|J|K|N|R|V|W|X/',$Buoyname) ) {
    $noinstr = True;
    $statement = "No water property data available for buoy ".$Buoyname;
}
// Wave instrument availability
else if ($table == "wave" && ! preg_match('/K|N|V|X/',$Buoyname) ) {
    $noinstr = True;
    $statement = "No wave data available for buoy ".$Buoyname;
}

if ($noinstr) {
    // Repeating header type stuff here because otherwise it needs to be below download
    print "<html><head>";
    print "<title>Query Results</title>";
    include("../includes/queryhead.html");
    print "</head>";

    print "<div id='container'>";
    include("../includes/header.html");
    include("../includes/navigation.html");
    print "<h2>".$statement."</h2>\n" ;
    include("../includes/control.php");  // show bottom control options
    die();
}

# if being called from front page, show previously-made "recent" image from daily directory
if ($datepicker == "recent") {
    if ($table != 'ndbc') {
        $tempaccess = "../daily/tabs_".$Buoyname."_".$table;
    }
    else if ($table == 'ndbc') {
        $tempaccess = "../daily/ndbc_".$Buoyname;
    }
    // command to show table
    if (php_uname('n') == 'barataria.tamu.edu') {
        $command = escapeshellcmd('/usr/bin/python3 ../python/get_data.py "'.$tempaccess.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tz.'"');
    }
    else if (php_uname('n') == 'tahoma.local') {
        $command = escapeshellcmd('/anaconda/bin/python ../python/get_data.py "'.$tempaccess.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tz.'"');
    }
}
// If being called from tabs query form, need to interpret dates chosen, etc.
else{
    // split date range into two dates. if it is just one date, still becomes an array but of length 1
    $dates = explode(" - ", $datepicker);
    // start date is the first date
    $dstart = $dates[0];
    if (count($dates)==2) {
            // if there is an end date, use it
            $dend = $dates[1];
    } else {
            // if there is not an end date, use start date
            $dend = $dstart;
    }
    if ($table != 'ndbc') {
        $tempfile=tempnam("../tmp","tabs_".$Buoyname."_".$table."_");  // full file location
    }
    else if ($table == 'ndbc') {
        $tempfile=tempnam("../tmp", "ndbc_".$Buoyname."_");  // full file location
    }
    // $tempfile=tempnam("/home/woody/htdocs/Tglo/tmp",$Buoyname . $table);
    $tempout=basename($tempfile);  // just file name itself
    $tempaccess = "../tmp/".$tempout;  // relative path to buoy

    # set up command for later use. Different python location on different machines.
    if (php_uname('n') == 'barataria.tamu.edu') {
        $command = escapeshellcmd('/usr/bin/python3 ../python/get_data.py "'.$tempfile.'" --dstart "'.$dstart.'" --dend "'.$dend.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tz.'"');
    }
    else if (php_uname('n') == 'tahoma.local') {
        $command = escapeshellcmd('/anaconda/bin/python ../python/get_data.py "'.$tempfile.'" --dstart "'.$dstart.'" --dend "'.$dend.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tz.'"');
    }

    chmod($tempfile, 0644);

}

// Account for if download option was chosen here, since data has now been read in.
if ($datatype == 'download'){
    passthru($command);
    if (file_exists($tempaccess)) {
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="'.$tempaccess.'"');
        // header('Content-Disposition: attachment; filename="'.basename($tempaccess).'"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($tempaccess));
        readfile($tempaccess);
        exit;
    }
}

// Have to wait to start page itself until after download logic
print "<html><head>";
print "<title>Query Results</title>";
include("../includes/queryhead.html");
print "</head>";

print "<div id='container'>";


include("../includes/header.html");
include("../includes/navigation.html");

// show header file contents for "recent" data, above table
if ($datepicker=="recent") {
    if ($table != 'ndbc') {
        echo file_get_contents( "../daily/tabs_".$Buoyname."_header" );
    }
    else if ($table == 'ndbc') {
        echo file_get_contents( "../daily/ndbc_".$Buoyname."_header" );
    }
}

// Show results of query
	print "<TABLE cellspacing=0 cellpadding=0  border=0 width=100%>";
	print "<TD valign=top><br>";

    print "<font face=helvetica><b><big>Results of TABS Data query</big></b> (<a href=$tempaccess>download</a>)</font>";

    // Warning about data being out of data if most recent point is more than 3 days old
    if ($datepicker=="recent") {
        $lines = file($tempaccess);
        $lnum = count($lines)-1;  # gives index for last line in file
        $datestr =  preg_split('/\s+/', $lines[$lnum])[0];  # split by white space or by tab and get first entry (date)
        $lastdate = new DateTime($datestr, new DateTimeZone('UTC'));  # last date of file (most recent data)
        $today = new DateTime('now', new DateTimeZone('UTC'));
        $interval = date_diff($lastdate, $today);  # difference in days between now and most recent data
        $intervalstr = $interval->format('%R%a days');
        if ($intervalstr>3){ // old report
            print "<font color='red'><i>&emsp;&emsp;&emsp;This data is more than 3 days old.</i></font>";
        }
    }

    // note for met and table
    if ($table == 'met' and $datatype == 'data') {
        print "<i><br><br>Note: East and North wind data show direction toward.&nbsp;Direction data show direction from.</i>";
    }
    print "<br><br>";
    // if not using recent image, call to database
    // Runs table or image for database
    if ($datepicker!="recent"){
        // exec($command, $output);
        passthru($command);
        // if data is missing from this time period, just say that
        if (filesize($tempfile) == 0){
            print "<font face=helvetica color='gray'><b><big>Data is not available for buoy $Buoyname during the selected time period $dstart to $dend</big></b></font><br>\n";
        }
    }
    elseif ($datepicker == "recent" && $datatype == "data"){
        passthru($command);
    }
    if ($datatype=="pic"){
        if (file_exists($tempaccess.".png")){
        	print "<a href=".$tempaccess.".pdf> <img src=".$tempaccess.".png></A>\n";
        }
        }
	print "</TD></TR></TABLE>\n";
// }

// show bottom control options
include("../includes/control.php");

}

?>
</div>
</html>
