<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
		<title>TABS Buoy Database Query page</title>
        <script
          src="https://code.jquery.com/jquery-2.2.4.min.js"
          integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44="
          crossorigin="anonymous"></script>
<!-- <script src="http://code.jquery.com/jquery-migrate-1.4.1.js"></script> -->
		<!-- <script type="text/javascript" src="js/jquery-3.1.1.min.js"></script> -->
        <!-- <script type="text/javascript" src="js/jquery-1.3.1.min.js"></script> -->
		<script type="text/javascript" src="js/jquery-ui.min.js"></script>
        <!-- <script type="text/javascript" src="js/jquery-ui-1.7.1.custom.min.js"></script> -->
		<script type="text/javascript" src="js/daterangepicker.jQuery.js"></script>
		<link rel="stylesheet" href="css/ui.daterangepicker.css" type="text/css" />
		<link rel="stylesheet" href="css/redmond/jquery-ui-1.7.1.custom.css" type="text/css" title="ui-theme" />
        <!-- <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>jQuery UI Datepicker - Default functionality</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <link rel="stylesheet" href="/resources/demos/style.css">
        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script> -->
        <!-- <script type="text/javascript">
            $(function(){
                  $('input').daterangepicker({arrows: true, dateFormat: 'M d, yy'});
             });
        </script> -->
		<script type="text/javascript">
			$(function(){
				  $('#datepicker').daterangepicker({
                    datepickerOptions: {changeMonth: true, changeYear: true,
                    minDate: new Date(1995, 1, 1), maxDate: 0,
                    yearRange: "1995:+0"}
                    });//{arrows:true});
                    // $('#datepicker').daterangepicker({
                    //   datepickerOptions: {changeMonth: true, changeYear: true,
                    //   minDate: new Date(1995, 1, 1), maxDate: 0,
                    //   yearRange: "1995:" + new Date().getFullYear()}
                    //   });//{arrows:true});
			 });
// var date = document.getElementById("datepicker").value;
//             console.log(date, "Hello, world!");
		</script>

		<!-- from here down, demo-related styles and scripts -->
<!--		<style type="text/css">
			body { font-size: 62.5%; }
			input {width: 196px; height: 1.1em; display:block;}
		</style>-->
        <!-- <script src="//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script> -->
        <!-- <script type="text/javascript">
        var date = document.getElementById("datepicker").value;
            console.log(date, "Hello, world!");
        </script> -->

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

// OLD

print <<<_HTML_
<BR>
<TABLE border=0>
<TR>
<TD><B>Select Buoy:</B></TD>
<TD><SELECT name="Buoyname" id="json-one">
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

_HTML_;

print <<<_HTML_

<input type="text" value="Choose date" id="datepicker" name="datepicker"/>

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

</body>
</html>
