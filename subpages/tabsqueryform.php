<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
        <?php include("../includes/queryhead.html");?>
        <title>Buoy Query Form</title>
	</head>

<body>

<div id="container">

<?php

$buoy = isset($_GET["Buoyname"]) ? $_GET["Buoyname"] : "";
$table = isset($_GET["table"]) ? $_GET["table"] : "";
$datepicker = isset($_GET["datepicker"]) ? $_GET["datepicker"] : "";
$tz = isset($_GET["tz"]) ? $_GET["tz"] : "";
$units = isset($_GET["units"]) ? $_GET["units"] : "";
$datum = isset($_GET["datum"]) ? $_GET["datum"] : "";

if (! $units) {$units = 'M';}
if (! $tz) {$tz = 'UTC';}
if (! $datum) {$datum = 'MSL';}

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

// read into an array the active buoys
$csv = array_map("str_getcsv", file("../includes/buoys.csv"));
$header = array_shift($csv); // Seperate the header from data
$col = array_search("buoy", $header);  # save column name for buoys
$active = array_search("active", $header);  # save column name for buoys being active
foreach ($csv as $row) {  // loop over each row in csv file
    // check if buoy is active
    if (strcmp($row[$active], "TRUE") == 0) {
    	$buoysa[] = $row[$col];  // if so, save buoy name
    }
    // check if buoy is inactive
    if (strcmp($row[$active], "FALSE") == 0) {
    	$buoysia[] = $row[$col];  // if so, save buoy name
    }
}


include("../includes/header.html");
include("../includes/navigation.html");

print "<form action=\"/tabswebsite/subpages/tabsquery.php\" method=\"get\">\n";


print <<<_HTML_
<BR>

<TABLE border=0>
<TR>

<TD><B>Select Buoy:</B> (* inactive)</TD>
<TD><SELECT name="Buoyname" id="json-one">
<OPTION SELECTED value="$buoy">$buoy
_HTML_;

// list active bouys
foreach ($buoysa as $b) {
    print "<option value='$b'>$b</option>\n";
}
// then list inactive buoys
foreach ($buoysia as $b) {
    print "<option value='$b'>$b*</option>\n";
}
print "</select></td>\n";

print <<<_HTML_

<TD>
<B>... then select dataset&nbsp;</B>
<select id="json-two" name="table">
    <option selected value='$table'>$table</option>
</select>
</TD>
</tr>


<TR><TD><br></TD></TR>

<TR><TD><B>Select Date: </B> </TD>
<TD>
<input type="text" value="$datepicker" id="datepicker" name="datepicker"/>
</TD>


<TR><TD><br></TD></TR>
<br>
<br>
<TR><TD><B>Output Format: </B></TD><TD>
<input type=radio name="Datatype" value="pic" checked>Graphic&nbsp;
<input type=radio name="Datatype" value="data">Data table&nbsp;
<input type=radio name="Datatype" value="download">Download
</TD></TR>
<TR><TD><br></TD></TR>

<tr>
<TD><B>Timezone:&nbsp; </b></td>
<td>
<Select Name="tz">
<option selected value=$tz>$tzname</Option>
<option value='UTC'>UTC</Option>
<option value='US/Central'>Local</option>
<option value='Etc/GMT+6'>CST</option>
</select>
</td>
</tr>
<TR><TD><br></TD></TR>


<TR>
<td><b>&nbsp;for data table:</b></td>
<TD>Units:&nbsp;
<Select Name="units">
<option selected value=$units>$unitsname</Option>
<option value='M'>Metric</Option>
<option value='E'>English</option>
</select>
</td>
<tr>


<TR>
<td><b>&nbsp;for graphic:</b></td>
<TD>Include model:&nbsp;
<input type=radio name="model" value="False" checked>No
<input type=radio name="model" value="True">Yes
</td>
</TR>


<TR>
<td><b>&nbsp;for tidal heights:</b> (if available) &nbsp; &nbsp;</td>
<TD><a href="https://tidesandcurrents.noaa.gov/datum_options.html">Tidal Datum:</a>&nbsp;
<Select Name="datum">
<option selected value=$datum>$datum</Option>
<option value='MHHW'>MHHW</option>
<option value='MHW'>MHW</option>
<option value='MTW'>MTW</option>
<option value='MSL'>MSL</Option>
<option value='MLW'>MLW</option>
<option value='MLLW'>MLLW</option>
</select>
</td>
<tr>


<TR><TD><br></TD></TR>
<TR><TD><br></TD></TR>

<TR>
<!-- <TD><input type=reset name="Reset" Value="Reset Fields"></TD> -->
<TD><input type=submit color='#009933' value="Submit Query"></TD>
</TR>
</TABLE>
</form>
<br><br>


<TR>
<TD></TD><TD><i>Archives are available on the <a href="buoy_status.php">buoy information</a> page. You can also <a href="query_notes.php">build your own database query</a>.</i></TD>
</TR>
<br>
<TR>
<TD></TD><TD><i>A Python package is <a href="https://github.com/kthyng/tabs">available</a> to allow easy access to both data and model time series.</i></TD>
</TR>

_HTML_;

include("../includes/footer.html");


?>


</div>

</body>
</html>
