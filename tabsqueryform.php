<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
		<title>TABS Buoy Database Query page</title>
        <script
          src="https://code.jquery.com/jquery-2.2.4.min.js"
          integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44="
          crossorigin="anonymous"></script>
		<script type="text/javascript" src="js/jquery-ui.min.js"></script>
		<script type="text/javascript" src="js/daterangepicker.jQuery.js"></script>
		<link rel="stylesheet" href="css/ui.daterangepicker.css" type="text/css" />
		<link rel="stylesheet" href="css/redmond/jquery-ui-1.7.1.custom.css" type="text/css" title="ui-theme" />
        <!-- <script src="http://code.jquery.com/jquery-migrate-1.4.1.js"></script> -->
		<script type="text/javascript">
			$(function(){
				  $('#datepicker').daterangepicker({
                    datepickerOptions: {changeMonth: true, changeYear: true,
                    minDate: new Date(1995, 1, 1), maxDate: 0,
                    yearRange: "1995:+0"}
                    });
			 });
		</script>

    <script src="js/dynamic_dropdown.js"></script>

	</head>

<body>

<div id="container">

<?php

$buoy = isset($_GET["buoy"]) ? $_GET["buoy"] : "";
$type = isset($_GET["type"]) ? $_GET["type"] : "";
$time = isset($_GET["time"]) ? $_GET["time"] : "";
$units = isset($_GET["units"]) ? $_GET["units"] : "";


$PageTitle="TABS Buoy Database Query page";

include("includes/header.html");
include("includes/navigation.html");

print "<form action=\"tabsquery.php\" method=\"get\">\n";


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
<OPTION value="A">A*
<OPTION value="C">C*
<OPTION value="E">E*
<OPTION value="G">G*
<OPTION value="H">H*
<OPTION value="N">N*
<OPTION value="P">P*
<OPTION value="S">S*
</SELECT>
</TD>


<TD>
<B>... then select dataset&nbsp;</B>
<select id="json-two" name="table">
    <option>available data</option>
</select>
</TD>
</tr>


<TR><TD><br></TD></TR>
<TR><TD><B>Select Date: </B> </TD>
<TD>
<input type="text" value="Click here" id="datepicker" name="datepicker"/>
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
<option selected value='M'>Metric</Option>
<option value='E'>English</option>
</select>
</td>

<TD>Timezone:&nbsp;
<Select Name="tz">
<option selected value='UTC'>UTC</Option>
<option value='central'>US/Central</option>
</select>
</td><tr>
<TR><TD><br></TD></TR>


<!-- <input type=hidden  name="tz" value="UTC"> -->
<input type=hidden  name="stage" value="TRUE">
<TR><TD>
<input type=reset name="Reset" Value="Reset Fields">
</TD><TD>
<input type=submit color='#009933' value="Submit Query">
</TD></TR>
</TABLE>
</form>
<br><br>

_HTML_;

include("includes/footer.html");


?>


</div>

</body>
</html>
