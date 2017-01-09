
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
#include("DB.php");



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
die( "<h2>No meteorological data available for buoy ".$Buoyname."</h2>\n" ); }
# Salt instrument availability
if ($table == "salt" && ! preg_match('/B|D|F|J|K|N|R|V|W|X/',$Buoyname) ) {
die( "<h2>No water property data available for buoy ".$Buoyname."</h2>\n" ); }
# Wave instrument availability
if ($table == "wave" && ! preg_match('/K|N|V|X/',$Buoyname) ) {
die( "<h2>No wave data available for buoy ".$Buoyname."</h2>\n" ); }

# if being called from front page, show previously-made "recent" image from daily directory
if ($datepicker == "recent") {
    $tempaccess = "daily/tabs_".$Buoyname."_".$table;
    // keep options on the side
    // header
    $command = escapeshellcmd('/anaconda/bin/python buoy_header.py "'.$Buoyname.'"');
    passthru($command);
    // command to show table
    $command = escapeshellcmd('/anaconda/bin/python get_data.py "'.$tempaccess.'" "'.$datatype.'" --units "'.$units.'"');

}
// If being called from tabs query form, need to interpret dates chosen, etc.
else{
    // change format of date from yyyy/m/d to yyyy-m-d
    $datepicker = str_replace ("/", "-", $datepicker);
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

    $command = escapeshellcmd('/anaconda/bin/python get_data.py "'.$tempaccess.'" --dstart "'.$dstart.'" --dend "'.$dend.'" "'.$datatype.'" --units "'.$units.'"');
    // $command = escapeshellcmd('/anaconda/bin/python get_data.py "'.$tempaccess.'" --dstart "'.$dstart.'" --dend "'.$dend.'" "'.$datatype.'"');

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
            // print "<a href=tmp/".$tempout.".pdf> <img src=tmp/".$tempout.".png></A>\n";}
        }
	print "</TD></TR></TABLE>\n";
// }

print "<TABLE width=100%>";
print "<TR><TD valign=top width=120 align=left>";
print "</td>";
print "<td>";
print "<br> &nbsp;\n";
// print "<br><FORM Action=$PHP_SELF method=\"GET\">\n";
print "<br><form action=\"tabsquery.php\" method=\"get\">\n";

// print "<input NAME=buoy TYPE=hidden value=$buoylet>\n";
print "<font face=\"Helvetica\" size=-1>\n";
print "<Select Name=tz>\n";
print "<option value=''>Time Zone</Option>\n";
print "<option value='UTC'>UTC</Option>\n";
print "<option value='STN'>Station Local</option>\n</select><br>\n";
if ($table != "eng") {
print "<Select Name=units>\n";
print "<option value=''>Units</Option>\n";
print "<option value='M'>Metric</Option>\n";
print "<option value='E'>English</option>\n</select>\n";
}

// Change table (variable file)
print "<Select Name=table>\n";
print "<OPTION SELECTED value='$table'>$tablename</option>\n";
print "<option value='ven'>Velocity data</option>\n";
print "<option value='met'>Meteorological data</option>\n";
print "<option value='eng'>System data</option>\n";
print "<option value='salt'>Water property data</option>\n";
print "<option value='wave'>Wave data</option>\n</select>\n";


// Change buoy
print "<Select Name=Buoyname>\n";
print "<OPTION SELECTED value='$Buoyname'>$Buoyname</option>\n";
print "<option value='B'>B</option>\n";
print "<option value='D'>D</option>\n";
print "<option value='F'>F</option>\n";
print "<option value='J'>J</option>\n";
print "<option value='K'>K</option>\n";
print "<option value='N'>N</option>\n";
print "<option value='R'>R</option>\n";
print "<option value='V'>V</option>\n";
print "<option value='W'>W</option>\n";
print "<option value='X'>X</option>\n";
print "<option value='A'>A*</option>\n";
print "<option value='C'>C*</option>\n";
print "<option value='E'>E*</option>\n";
print "<option value='G'>G*</option>\n";
print "<option value='H'>H*</option>\n";
print "<option value='P'>P*</option>\n";
print "<option value='S'>S*</option>\n</select>\n";

// print "<input NAME=Buoyname TYPE=hidden value=$Buoyname>\n";
// print "<input NAME=table TYPE=hidden value=$table>\n";
print "<input NAME=Datatype TYPE=hidden value=$datatype>\n";
print "<input NAME=datepicker TYPE=hidden value=$datepicker>\n";

print "<BR><input type=submit  value=Change>\n</form>\n";

print "<br><table>\n";
// Switch to
print "<TR><TD>Switch to <a href=tabsquery.php?Buoyname=$Buoyname&table=$table&Datatype=$newdatatype&datepicker=$datepicker>$newdatatypename</a></TD></TR>\n";

print "<TR><TD>Return to <a href=tabsqueryform.php>database query</a></TD></TR>\n";
print "<TR><TD>Return to <a href=index.php>homepage</a></TR></TD>\n";
print "</table>\n";
print "</font>\n";
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
