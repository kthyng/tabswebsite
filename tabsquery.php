
<head>
    <script src="js/dynamic_dropdown.js"></script>
</head>


<?php

umask(0022);

$cm2e=.01943845;
$m2e=1.943845;
$degc="&#176;C";
$degf="&#176;F";
$degm="&#176;M";
$degt="&#176;T";

$PageTitle="TABS Buoy Database Query page";
include("includes/header.html");
include("includes/navigation.html");

if ($_SERVER['REQUEST_METHOD'] != 'GET') {
echo "<meta HTTP-EQUIV=\"REFRESH\" CONTENT=\"3;URL=http://tabs1.gerg.tamu.edu/tglo/tabsqueryform.php\">";
echo "<meta HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">";

	print "<p><b>Database search form is here:</b> <a href=tabsqueryform.php>http://tabs.gerg.tamu.edu/tglo/tabsqueryform.php</a>";
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

# Met instrument availability
if ($table == "met" && ! preg_match('/B|H|J|K|N|V/',$Buoyname) ) {
    include("includes/control.php");  // show bottom control options
    die( "<h2>No meteorological data available for buoy ".$Buoyname."</h2>\n" );
}
# Salt instrument availability
if ($table == "salt" && ! preg_match('/B|D|F|J|K|N|R|V|W|X/',$Buoyname) ) {
    include("includes/control.php");  // show bottom control options
    die( "<h2>No water property data available for buoy ".$Buoyname."</h2>\n" );
}
# Wave instrument availability
if ($table == "wave" && ! preg_match('/K|N|V|X/',$Buoyname) ) {
    include("includes/control.php");  // show bottom control options
    die( "<h2>No wave data available for buoy ".$Buoyname."</h2>\n" );
}

# if being called from front page, show previously-made "recent" image from daily directory
if ($datepicker == "recent") {
    $tempaccess = "daily/tabs_".$Buoyname."_".$table;
    // // header
    // $command = escapeshellcmd('/anaconda/bin/python buoy_header.py "'.$Buoyname.'"');
    // passthru($command);
    // command to show table
    $command = escapeshellcmd('/anaconda/bin/python get_data.py "'.$tempaccess.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tz.'"');

}
// If being called from tabs query form, need to interpret dates chosen, etc.
else{
    // change format of date from yyyy/m/d to yyyy-m-d if needed (depends on where this is called from)
    // if (strpos($datepicker, '/') !== false) {
    //     $datepicker = str_replace ("/", "-", $datepicker);
    // }
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
    $tempfile=tempnam("tmp","tabs_".$Buoyname."_".$table."_");  // full file location
    // $tempfile=tempnam("/home/woody/htdocs/Tglo/tmp",$Buoyname . $table);
    $tempout=basename($tempfile);  // just file name itself
    $tempaccess = "tmp/".$tempout;  // relative path to buoy

    $command = escapeshellcmd('/anaconda/bin/python get_data.py "'.$tempaccess.'" --dstart "'.$dstart.'" --dend "'.$dend.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tz.'"');

    chmod($tempaccess, 0644);

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

// show header file contents for "recent" data, above table
if ($datepicker=="recent") {
    echo file_get_contents( "daily/tabs_".$Buoyname."_header" );
}

// Show results of query
	print "<TABLE cellspacing=0 cellpadding=0  border=0 width=100%>";
	print "<TR><TD valign=top width=120><font face=helvetica><BR>";
    print "<table>\n";
    print "</table>\n";
	print "</TD><TD valign=top><br>";

    print "<font face=helvetica><b><big>Results of TABS Data query</big></b>(<a href=$tempaccess>download</a>)</font><br>\n";
    // if not using recent image, call to database
    // Runs table or image for database
    if ($datepicker!="recent"){
        // exec($command, $output);
        passthru($command);
        // if data is missing from this time period, just say that
        if (filesize($tempaccess) == 0){
            print "<br>";
            print "<font face=helvetica color='gray'><b><big>Data is not available for buoy $Buoyname during the selected time period $dstart to $dend</big></b></font><br>\n";
        }
    }
    elseif ($datepicker == "recent" && $datatype == "data"){
        passthru($command);
    }
    if ($datatype=="pic"){
        if (file_exists($tempaccess.".png")){
        	print "<a href=".$tempaccess.".pdf> <img src=".$tempaccess.".png></A>\n";}
        }
	print "</TD></TR></TABLE>\n";
// }

// show bottom control options
include("includes/control.php");



print "</TD><TD style=\"text-align:left !important;\">";
print "<pre>";
// // Top of data table:
if ($table == 'met' ) {
    print "<br><i>Note: East and North wind data show direction toward.&nbsp;Wind Speed and direction data show direction from.</i>\n<br>";
}
print "</pre></p>";
print "</TD></TR></TABLE>";

}

?>
