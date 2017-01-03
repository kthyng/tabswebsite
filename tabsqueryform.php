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


        <!-- <script>

        var data = {
            "base" : ["Please choose from above"],
            "A": ["eng","ven"],
            "B": ["eng","met","salt","ven"],
            "C": ["eng", "ven"],
            "D": ["eng", "salt", "ven"],
            "E": ["eng", "ven"],
            "F": ["eng", "salt", "ven"],
            "G": ["eng", "ven"],
            "H": ["eng", "met", "ven"],
            "J": ["eng", "met", "salt", "ven"],
            "K": ["eng", "met", "salt", "ven", "wave"],
            "N": ["eng", "met", "salt", "ven", "wave"],
            "P": ["eng", "ven"],
            "R": ["eng", "salt", "ven"],
            "S": ["eng", "ven"],
            "V": ["eng", "met", "salt", "ven", "wave"],
            "W": ["eng", "salt", "ven"],
            "X": ["eng", "met", "salt", "ven", "wave"],
        }

    		$(function() {
https://css-tricks.com/dynamic-dropdowns/
http://jsfiddle.net/NaUAL/

    			$("#json-one").change(function() {

                    var first = $(this),
                        second = $("#json-two"),
                        key = first.val(),
                        // instead of the original switch code
                        vals = data[key] == undefined ? data.base : data[key],
                        html = [];
                     // create insert html before adding
                     $.each(vals,function(i,val){
                          html.push('<option>'+val+'</option>')
                     });
                     // no need to empty the element before adding the new content
                     second.html(html.join());
});


    		});
    	</script> -->

	</head>

<body>

<?php

$buoy = isset($_GET["buoy"]) ? $_GET["buoy"] : "";
$type = isset($_GET["type"]) ? $_GET["type"] : "";
$time = isset($_GET["time"]) ? $_GET["time"] : "";
$units = isset($_GET["units"]) ? $_GET["units"] : "";


$PageTitle="TABS Buoy Database Query page";

include("includes/header.html");
include("includes/navigation.html");

print "<form action=\"tabsquery.php\" method=\"post\">\n";


// Connect to Database
if (! $dbh=mysql_connect('tabs1.gerg.tamu.edu','tabsweb','tabs')) {
	die("Can't connect: ".mysql_error());
	}

$dbase="tabsdb";

mysql_select_db($dbase) or die(mysql_error());

?>


<?php


print <<<_HTML_
<BR>
<TABLE border=0>
<TR>
<TD><B>Select Buoy:</B> (* inactive)</TD>
<TD><SELECT name="Buoyname" id="json-one">
<OPTION SELECTED value="$buoy">$buoy
<OPTION value="A">A*
<OPTION value="B">B
<OPTION value="C">C*
<OPTION value="D">D
<OPTION value="E">E*
<OPTION value="F">F
<OPTION value="G">G*
<OPTION value="H">H*
<OPTION value="J">J
<OPTION value="K">K
<OPTION value="N">N
<OPTION value="P">P*
<OPTION value="R">R
<OPTION value="S">S*
<OPTION value="V">V
<OPTION value="W">W
<OPTION value="X">X
</SELECT>
</TD></TR>

<TR><TD><br></TD></TR>
<TR><TD><B>Select Data Type: </B> </TD>
<TD>
<input type=radio name="table" value="ven" checked> Velocity Data
<input type=radio name="table" value="met"> Meteorological Data
<input type=radio name="table" value="eng">System Data
<input type=radio name="table" value="salt">Water Property Data
<input type=radio name="table" value="wave">Wave Data
</TD></TR>

<br>

<br />
<!--<br>

<TR><TD>
<B>Select dataset</B>
<select id="json-two">
    <option>Please choose from above</option>
</select>
</TR></TD>-->


<TR><TD><br></TD></TR>
<TR><TD><B>Select Date: </B> </TD>
<TD>
<input type="text" value="Click here" id="datepicker" name="datepicker"/>
</TD>

<TR><TD><br></TD></TR>
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
<input type=submit color='#009933' value="Submit Query">
</TD></TR>
</TABLE>
</form>
<br><br>

_HTML_;

include("includes/footer.html");


?>

</body>
</html>
