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

if (! $units) {$units = 'M';}
if (! $tz) {$tz = 'UTC';}
// if (! $table) {$table = 'ven';}

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

// $PageTitle="TABS Buoy Database Query page";

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
<OPTION value="B">B
<OPTION value="D">D
<OPTION value="F">F
<OPTION value="J">J
<OPTION value="K">K
<OPTION value="R">R
<OPTION value="V">V
<OPTION value="W">W
<OPTION value="X">X
<OPTION value="42019">42019
<OPTION value="42020">42020
<OPTION value="42035">42035
<OPTION value="SRST2">SRST2
<OPTION value="PTAT2">PTAT2
<OPTION value="A">A*
<OPTION value="C">C*
<OPTION value="E">E*
<OPTION value="G">G*
<OPTION value="H">H*
<OPTION value="N">N*
<OPTION value="P">P*
<OPTION value="S">S*
<OPTION value="42001">42001*
<OPTION value="42002">42002*
<OPTION value="42007">42007*
<OPTION value="42036">42036*
<OPTION value="42039">42039*
<OPTION value="42040">42040*
</SELECT>
</TD>


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
<input type=radio name="Datatype" value="pic" checked>Graphic
<input type=radio name="Datatype" value="data">Data table
<input type=radio name="Datatype" value="download">Download
</TD></TR>
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

<TD>Timezone:&nbsp;
<Select Name="tz">
<option selected value=$tz>$tzname</Option>
<option value='UTC'>UTC</Option>
<option value='central'>US/Central</option>
</select>
</td><tr>


<TR>
<td><b>&nbsp;for graphic:</b></td>
<TD>Include model:&nbsp;
<input type=radio name="model" value=False checked>No
<input type=radio name="model" value=True>Yes
</td>
</TR>

<TR><TD><br></TD></TR>


<TR>
<!-- <TD><input type=reset name="Reset" Value="Reset Fields"></TD> -->
<TD><input type=submit color='#009933' value="Submit Query"></TD>
</TR>
</TABLE>
</form>
<br><br>

_HTML_;

include("../includes/footer.html");


?>


</div>

</body>
</html>
