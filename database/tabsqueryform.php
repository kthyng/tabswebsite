<?php

$buoy = isset($_GET["buoy"]) ? $_GET["buoy"] : "";
$type = isset($_GET["type"]) ? $_GET["type"] : "";
$time = isset($_GET["time"]) ? $_GET["time"] : "";
$units = isset($_GET["units"]) ? $_GET["units"] : "";


$PageTitle="TABS Buoy Database Query page";
// include("tgloheader2.php");

include("includes/header.html");
include("includes/navigation.html");

print "<form action=\"tabsquery.php\" method=\"post\">\n";


print <<<_HTML_
<BR>
<TABLE border=0>
<TR>
<TD><B>Select Buoy:</B></TD>
<TD><SELECT name="Buoyname">
<OPTION SELECTED value="$buoy">$buoy
<OPTION value="A">A
<OPTION value="B">B
<OPTION value="C">C
<OPTION value="D">D
<OPTION value="E">E
<OPTION value="F">F
<OPTION value="G">G
<OPTION value="H">H
<OPTION value="J">J
<OPTION value="K">K
<OPTION value="N">N
<OPTION value="P">P
<OPTION value="R">R
<OPTION value="S">S
<OPTION value="V">V
<OPTION value="W">W
</SELECT>
</TD></TR>
<TR><TD><br></TD></TR>
<TR><TD><B>Select Data Type: </B> </TD>
<TD>
<input type=radio name="table" value="ven" checked> Velocity Data
<input type=radio name="table" value="met"> Meteorological Data
<input type=radio name="table" value="eng">System Data
<input type=radio name="table" value="salt">Water Property Data
</TD></TR>
<TR><TD><BR></TD></TR>
<TR><TD>
<B>Select Start Date:</B>
</TD><TD>
<SELECT name="Month">
<OPTION value="1">January
<OPTION value="2">February
<OPTION value="3">March
<OPTION value="4">April
<OPTION value="5">May
<OPTION value="6">June
<OPTION value="7">July
<OPTION value="8">August
<OPTION value="9">September
<OPTION value="10">October
<OPTION value="11">November
<OPTION value="12">December
</SELECT>
_HTML_;

print "<SELECT name=\"Day\">\n";

for ($dd=1; $dd < 32; $dd++) {
print "<OPTION value=$dd>$dd\n";
}
print "</SELECT>\n";

// http://stackoverflow.com/a/24394179/7076910
$now = new DateTime("now", new DateTimeZone('UTC') );
$curyear = $now->format("Y");

print "<SELECT name=\"Year\">\n";
for ($yy=1995;$yy < $curyear;$yy++) {
print "<OPTION value=$yy>$yy\n";
}
print "<OPTION SELECTED>$curyear\n";

print "</SELECT></TD></TR>\n";

print "<TR><TD><br></TD></TR>\n";

print "<TR><TD>\n";
print "<B>Include in Data Set:</B></TD><TD>";
print "<SELECT name=\"Prevdays\">";
for ($dd=0; $dd < 31; $dd++) {
print "<OPTION value=$dd>$dd\n";
}
print "</SELECT>";
print "<B>days before selected start date.</B></TD></TR>";

print "<TR><TD><br></TD></TR>\n";
print "<TR><TD><B>Include in Data Set:</B></TD><TD>";
print "<SELECT name=\"Nextdays\">";
for ($dd=0; $dd < 31; $dd++) {
print "<OPTION value=$dd>$dd\n";
}
print "</SELECT>";

print "<B>days after selected start date.</B></TD></TR>";
print "<TR><TD><br></TD></TR>\n";
print <<<_HTML_

<br>
<br>
<TR><TD><B>Output Format: </B></TD><TD>
<input type=radio name="Datatype" value="pic" checked> Graphic
<input type=radio name="Datatype" value="data">Data Table
</TD></TR>
<TR><TD><br></TD></TR>
<input type=hidden  name="tz" value="UTC">
<input type=hidden  name="stage" value="TRUE">
<TR><TD>
<input type=reset name="Reset" Value="Reset Fields">
</TD><TD>
<input type=submit color=#009933 value="Submit Query">
</TD></TR>
</TABLE>
</form>
<br><br>
_HTML_;

include("includes/footer.html");

?>
