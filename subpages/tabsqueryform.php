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

// if ($tz == 'UTC') {
//     $tzname = 'UTC';
// }
// else if ($tz == 'central') {
//     $tzname = 'US/Central';
// }

if ($units == 'M') {
    $unitsname = 'Metric';
}
else if ($units == 'E') {
    $unitsname = 'English';
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
<OPTION value="B">B
<OPTION value="D">D
<OPTION value="F">F
<OPTION value="J">J
<OPTION value="K">K
<OPTION value="R">R
<OPTION value="V">V
<OPTION value="W">W
<OPTION value="X">X
<OPTION value="42001">42001
<OPTION value="42002">42002
<OPTION value="42019">42019
<OPTION value="42020">42020
<OPTION value="42035">42035
<OPTION value="42036">42036
<OPTION value="42039">42039
<OPTION value="42040">42040
<OPTION value="SRST2">SRST2
<OPTION value="PTAT2">PTAT2
<OPTION value="BURL1">BURL1
<OPTION value="g06010">g06010
<OPTION value="mc0101">mc0101
<OPTION value="sn0101">sn0101
<OPTION value="sn0201">sn0201
<OPTION value="sn0301">sn0301
<OPTION value="sn0401">sn0401
<OPTION value="sn0501">sn0501
<OPTION value="sn0701">sn0701
<OPTION value="lc0101">lc0101
<OPTION value="lc0201">lc0201
<OPTION value="mg0101">mg0101
<OPTION value='8770475'>8770475
<OPTION value='8770520'>8770520
<OPTION value='8770777'>8770777
<OPTION value='8770808'>8770808
<OPTION value='8770822'>8770822
<OPTION value='8770971'>8770971
<OPTION value='8771486'>8771486
<OPTION value='8771972'>8771972
<OPTION value='8772985'>8772985
<OPTION value='8773037'>8773037
<OPTION value='8773146'>8773146
<OPTION value='8773259'>8773259
<OPTION value='8773701'>8773701
<OPTION value='8774230'>8774230
<OPTION value='8775237'>8775237
<OPTION value='8775241'>8775241
<OPTION value='8775244'>8775244
<OPTION value='8775296'>8775296
<OPTION value='8775792'>8775792
<OPTION value='8776139'>8776139
<OPTION value='8776604'>8776604
<OPTION value='8777812'>8777812
<OPTION value='8778490'>8778490
<OPTION value='8779280'>8779280
<OPTION value='8779748'>8779748
<OPTION value='8779749'>8779749
<OPTION value='8734673'>8734673
<OPTION value='8735180'>8735180
<OPTION value='8741003'>8741003
<OPTION value='8741041'>8741041
<OPTION value='8741094'>8741094
<OPTION value='8741501'>8741501
<OPTION value='8741533'>8741533
<OPTION value='8747437'>8747437
<OPTION value='8760721'>8760721
<OPTION value='8760922'>8760922
<OPTION value='8761305'>8761305
<OPTION value='8761724'>8761724
<OPTION value='8764227'>8764227
<OPTION value='8764314'>8764314
<OPTION value='8766072'>8766072
<OPTION value='8768094'>8768094
<OPTION value='8770570'>8770570
<OPTION value='8770613'>8770613
<OPTION value='8771013'>8771013
<OPTION value='8771341'>8771341
<OPTION value='8771450'>8771450
<OPTION value='8773767'>8773767
<OPTION value='8775870'>8775870
<OPTION value='8779770'>8779770
<OPTION value="A">A*
<OPTION value="C">C*
<OPTION value="E">E*
<OPTION value="G">G*
<OPTION value="H">H*
<OPTION value="N">N*
<OPTION value="P">P*
<OPTION value="S">S*
<OPTION value="42007">42007*
<OPTION value="ps0201">ps0201*
<OPTION value="ps0301">ps0301*
<OPTION value="ps0401">ps0401*
<OPTION value="g09010">g09010*
<OPTION value='8770733'>8770733*
<OPTION value='8774513'>8774513*
<OPTION value='8775283'>8775283*
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
<option selected value=$tz>$tz</Option>
<option value='UTC'>UTC</Option>
<option value='US/Central'>US/Central</option>
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
<TD></TD><TD><i>Archives are available on the <a href="buoy_status.php">status</a> page.</i></TD>
</TR>

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
