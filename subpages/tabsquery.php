<?php

umask(0022);

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
$model = $_GET["model"];
$datum = $_GET["datum"];
$modelonly = $_GET["modelonly"];
$s_rho = $_GET["s_rho"];

if (! $units) {$units = 'M';}
if (! $tz) {$tz = 'UTC';}
if (! $model) {$model = 'False';}
if (! $datum) {$datum = 'MSL';}
if (! $modelonly) {$modelonly = 'False';}
if (! $s_rho) {$s_rho = '-1';}

// get environmental variable for python to use
$TABSPYTHON = getenv('TABSPYTHON');

if ($tz == 'UTC') {
    $tzname = 'UTC';
}
else if ($tz == 'US/Central') {
    $tzname = 'Local';
}
else if ($tz == 'Etc/GMT+6') {
    $tzname = 'CST';
}

if ($units == 'M') {
    $unitsname = 'Metric';
}
else if ($units == 'E') {
    $unitsname = 'English';
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
if ($table == "met" && ! preg_match('/B|H|J|K|N|V|X/',$Buoyname) ) {
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
    if (strlen($Buoyname) == 1) {
        $tempaccess = "../daily/tabs_".$Buoyname."_".$table;
    }
    else {
        $tempaccess = "../daily/".$Buoyname;
    }
    // command to show table (not used for pic)
    if (php_uname('n') == 'barataria.tamu.edu') {
        $command = escapeshellcmd('/home/kthyng/miniconda3/envs/tabs/bin/python ../python/get_data.py "'.$tempaccess.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tzname.'"');
    }
    else if (strpos(php_uname(), 'Darwin') !== false) {
        $command = escapeshellcmd('/Users/kthyng/miniconda3/envs/tabs/bin/python ../python/get_data.py "'.$tempaccess.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tzname.'"');
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
    if (strlen($Buoyname) == 1) {
        $tempfile=tempnam("../tmp","tabs_".$Buoyname."_".$table."_");  // full file location
    }
    else {
        $tempfile=tempnam("../tmp", $Buoyname."_");  // full file location
    }
    $tempout=basename($tempfile);  // just file name itself
    $tempaccess = "../tmp/".$tempout;  // relative path to buoy

    # set up command for later use. Different python location on different machines.
    if (php_uname('n') == 'barataria.tamu.edu') {
        $command = escapeshellcmd('/home/kthyng/miniconda3/envs/tabs/bin/python ../python/get_data.py "'.$tempfile.'" --dstart "'.$dstart.'" --dend "'.$dend.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tzname.'" --usemodel "'.$model.'" --datum "'.$datum.'" --modelonly "'.$modelonly.'" --s_rho "'.$s_rho.'"');
    }
    # checks for Mac and assumes Kristen's mac
    else if (strpos(php_uname(), 'Darwin') !== false) {
        $command = escapeshellcmd('/Users/kthyng/miniconda3/envs/tabs/bin/python ../python/get_data.py "'.$tempfile.'" --dstart "'.$dstart.'" --dend "'.$dend.'" "'.$datatype.'" --units "'.$units.'" --tz "'.$tzname.'" --usemodel "'.$model.'" --datum "'.$datum.'" --modelonly "'.$modelonly.'" --s_rho "'.$s_rho.'"');
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

// Figure out if buoy should have TXLA or NOAA model output to set flag
$csv = array_map("str_getcsv", file("../includes/buoys.csv"));
$header = array_shift($csv); // Separate the header from data
$txlacol = array_search("txla", $header);  // column index for txla model info
$table2col = array_search("table2", $header);
// Find row for buoy, either with built-in function or by search
if (!function_exists('array_column')) {
    $buoycol = array_search("buoy", $header);  # save column name for buoy
    foreach ($csv as $row) {
        # if the desired buoy is found in the column, stop so that $row is correct
        if (strcmp($row[$buoycol],$Buoyname) == 0) {
            break;
        }
    }
}
else {
    $buoyarr = array_column($csv, 0);
    $buoyrow = array_search($Buoyname, $buoyarr);
    $row = $csv[$buoyrow];
}
// check all model cases
if (($row[$txlacol] == "TRUE") or ($row[$table2] == "currentspredict")
    or ($row[$table2] == "tidepredict")) {
    $havemodel = True;  // this buoy should have model output
}
else {
    $havemodel = False;
}

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
        $norecentdata = True;  # flag to use for rest of page for when data is not up-to-date
        print "<font color='red'><br><br><i>Data is not coming in right now for buoy ".$Buoyname.".</i></font>";
        // Image selected, model output available, no recent data
        if ($table != 'eng' and $table != 'wave' and $havemodel and $datatype == 'pic') {
            print "<font color='red'><i> Model output is shown instead.</i></font>";
            $norecentdatabutmodel = True;  # flag to use for rest of page for when data is not up-to-date but model is available
        }
        // Image selected, no model output available (wave or eng), no recent data
        elseif ($havemodel and $datatype == 'pic') {
            print "<font color='red'><i> Model output might be available for other data types.</i></font>";
        }
    }
}


if ($datepicker=="recent") {
    if ($intervalstr<=2){
        // show header file contents for "recent" data, below table
        if (strlen($Buoyname) == 1) {
            echo file_get_contents( "../daily/tabs_".$Buoyname."_header" );
        }
        else {
            echo file_get_contents( "../daily/".$Buoyname."_header" );
        }
    }
}

// show bottom control options
include("../includes/control.php");


// Show results of query
print "<TABLE cellspacing=0 cellpadding=0  border=0 width=100%>";
print "<TD valign=top><br>";

// data download link as long as there is recent data
print "<font face=helvetica><b><big>Results of TABS Data query</big></b></font>";
if (! $norecentdata){
    print "<font face=helvetica> (<a href=$tempaccess>download data</a>)</font>";
}

// note for met and table
if ($table == 'met' and $datatype == 'data') {
    print "<i><br><br>Note: East and North wind data show direction toward.&nbsp;Direction data show direction from.</i>";
}
print "<br><br>";
// if not using recent image, call to database
// Runs table or image for database
if ($datepicker!="recent"){
    passthru($command);
    // if data is missing from this time period, just say that
    if (filesize($tempfile) == 0 and !file_exists($tempaccess.".png")){
        print "<font face=helvetica color='gray'><b><big>Data is not available for buoy $Buoyname during the selected time period $dstart to $dend</big></b></font><br>\n";
        $norecentdata = True;  # flag to use for rest of page for when data is not up-to-date
    }
    // if data is missing but model output is available and image has been made
    else if (filesize($tempfile) == 0 and file_exists($tempaccess.".png")) {
        print "<font color='red'><i>Data is not coming in right now for buoy ".$Buoyname.".</i></font>";
        print "<font color='red'><i> Model output is shown instead.</i></font><br><br>";
    }
}
elseif ($datepicker == "recent" && $datatype == "data" && ! $norecentdata){
    passthru($command);
}

if ($datatype=="pic" && ($havemodel or !$norecentdata)){
    if (file_exists($tempaccess.".png")){
    	print "<a href=".$tempaccess.".pdf> <img src=".$tempaccess.".png></A>\n";
    }
}
print "</TD></TR></TABLE>\n";
echo $TABSPYTHON;


}

?>
</div>
</html>
