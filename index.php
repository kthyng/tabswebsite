

<HEAD>
<!-- <link href="/tglo/newtabs.css" rel="stylesheet" type="text/css"> -->
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

<TITLE>Texas Automated Buoy System (TABS)</TITLE>

<!-- <meta HTTP-EQUIV="REFRESH" CONTENT="300">
<meta HTTP-EQUIV="Expires" CONTENT="1800">
<meta HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate">
<meta HTTP-EQUIV="Pragma" CONTENT="no-cache"> -->
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="HandheldFriendly" content="true">
<meta name="viewport" content="width=device-width,maximum-scale=1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">

<!-- Script to make refresh user-controlled with a button -->
<!-- https://stackoverflow.com/questions/7351725/auto-submit-a-radio-button-but-keep-it-selected -->
<script>
function autoSubmit()
{
    var formObject = document.forms['theForm'];
    formObject.submit();
}
</script>

<!-- allow for user to turn off refresh
Default to refresh being on. If refresh is on, refresh every 300 seconds. -->
<?php
$refresh=$_GET["refresh"];
if (! $refresh) {$refresh = 'on';}

if ($refresh == "on") {
print <<<_HTML_
    <meta HTTP-EQUIV="REFRESH" CONTENT="300">
_HTML_;
}
?>

<!-- allow for low bandwidth option. Turn off hover images on front page to
save on loading. -->
<?php
$bandwidth=$_GET["bandwidth"];
if (! $bandwidth) {$bandwidth = 'high';}
if ($bandwidth == "high") {
print <<<_HTML_
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <link rel="stylesheet" type="text/css" href="css/ddimgtooltip.css" />
    <script type="text/javascript" src="js/ddimgtooltip.js">
    /***********************************************
    * Image w/ description tooltip v2.0- (c) Dynamic Drive DHTML code library (www.dynamicdrive.com)
    * This notice MUST stay intact for legal use
    * Visit Dynamic Drive at http://www.dynamicdrive.com/ for this script and 100s more
    ***********************************************/
    </script>
_HTML_;

}
?>

<!-- <link href="css/leaflet.css"  rel="stylesheet" type="text/css"> -->
<!-- <link href="css/bootstrap.css" media="all" rel="stylesheet" type="text/css"> -->
<!-- <link href="css/bootstrap-responsive.css" media="all" rel="stylesheet" type="text/css"> -->


<!-- <link href="css/leaflet.ie.css"  rel="stylesheet" type="text/css"> -->
<!-- <link href="css/default.css" media="all" rel="stylesheet" type="text/css"> -->
<!-- <link href="css/style.css" media="all" rel="stylesheet" type="text/css"> -->
<!-- <link href="css/SAglobal.css" media="all" rel="stylesheet" type="text/css"> -->
<!-- <link href="css/SAprint.css" media="print" rel="stylesheet" type="text/css"> -->

<!-- <link rel="stylesheet" href="css/zentools.css" type="text/css" /> -->
<!-- <link href="images/favicon.ico" rel="icon" type="image/x-icon" /> -->

</HEAD>

<!-- this div centers content dynamically -->
<div id="container">

<!-- include header from separate file -->
<?php include("includes/header.html");?>


<!-- include navigation from separate file -->
<?php include("includes/navigation.html");?>

<div id="mapbuoycontainer">

<div id="mapcontainer">

<div id="map" >
  <!-- <iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0" width="100%" height="100%" src="http://pong.tamu.edu/tabs_map/?framed"  allowfullscreen webkitallowfullscreen -->
<!-- mozallowfullscreen msallowfullscreen></iframe> -->
<?php
  print "<iframe frameborder='0' scrolling='no' marginheight='0' marginwidth='0' width='800px' height='480px' src=http://pong.tamu.edu/tabs_map/?framed&bandwidth=$bandwidth  allowfullscreen webkitallowfullscreen
mozallowfullscreen msallowfullscreen></iframe>\n"
?>
<!-- text below map -->
<center>
<p><i><font class=bkvsm style="font-size:6pt;">
The vectors on the map point toward the direction that the currents or winds are flowing and represent the average for the
last three hours of the available data, potentially with a delay indicated.<br>
</font></i></p>
</center>
</div>


<!-- Refresh and bandwidth buttons -->
<form name='theForm' id='theForm'><b>Refresh:</b>
    <input type="radio" name="refresh" <?php if ($refresh == 'on') { ?>checked='checked' <?php } ?>value="on" onChange="autoSubmit();" />On
    <input type="radio" name="refresh" <?php if ($refresh == 'off') { ?>checked='checked' <?php } ?> value="off" onChange="autoSubmit();" />Off
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Bandwidth:</b>
    <input type="radio" name="bandwidth" <?php if ($bandwidth == 'high') { ?>checked='checked' <?php } ?>value="high" onChange="autoSubmit();" />Normal
    <input type="radio" name="bandwidth" <?php if ($bandwidth == 'low') { ?>checked='checked' <?php } ?> value="low" onChange="autoSubmit();" />Low
</form>


</div>
<!-- end map -->


<!-- buoy list on right hand side -->
<div id="buoycontainer">
<table border=0 bgcolor="#f8f8f8" >
<!-- <TD><div id="blank"><TABLE border=0><TH colspan=1 align=left><font class==bknorm size=1.5em><br>&nbsp &nbsp &nbsp &nbsp &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp </font></th></table></div></TD> -->
<tr>
<td><b>Recent</b></td>
<TD valign=top colspan=2><div id="Report"><b><a href="subpages/currents.php"><font size='3em'>Last data report</font></a></b></div></td>
</tr>

<tr>
<td><font size='2em'>jump below:</font></td>
<td><font size='2em'><a href="#ndbc">NDBC</a>, <a href="#ports">PORTS</a>, <a href="#tcoon">TCOON</a>, <a href="#nos">NOS</a></font></td>
</tr>

<!-- <tr><br></tr> -->

<?php
print "<tr><td></td><td><i>TABS</i></td></tr>";  // Label before TABS buoys

// read in buoy list from csv file with buoy info
$csv = array_map("str_getcsv", file("includes/buoys.csv"));
$header = array_shift($csv); // Seperate the header from data
$col = array_search("buoy", $header);  # save column name for buoys
$active = array_search("active", $header);  # save column name for buoys being active
$table1 = array_search("table1", $header);  # save column name for buoy table1

foreach ($csv as $row) {  // loop over each row in csv file
    // check if buoy is active
    if (strcmp($row[$active], "TRUE") == 0) {
    	$blet[] = $row[$col];  // if so, save buoy name
        $btable1[] = $row[$table1];  // also save table1 value to know when to put in headers
    }
}

$bidx=0;  // counter for each line
foreach ($blet as $f) {
    if (strlen($f) == 1) {
    	$venfile="daily/tabs_".$f."_sum";
        $table = "sum";
    }
    else {
    	$venfile="daily/".$f;
    }

    // $venfile="http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_".$f."_ven.txt";
    if (file_exists($venfile) and count(file($venfile)) > 1) {

        $lines=file($venfile);
        $l=array_pop($lines);  // grab last line in file
    	if (trim($l)) {
    		$line=trim($l);  # strip white space from beginning and end of string
            $data = preg_split('/\s+/', $line);  # split by white space or by tab
            $datestr=$data[0];
    		$timestr=substr($data[1],0,5);

            # last data datetime is in UTC -> for local time
            $dtTX = new DateTime($datestr.$timestr, new DateTimeZone('UTC'));
            $TXtz = new DateTimeZone('America/Chicago');
            $dtTX->setTimezone($TXtz);
            $dtTXstr = $dtTX->format('M d, Y H:i');
            $dtTXtz = $dtTX->format('T');

            # last data datetime, for UTC
            $dtUTC = new DateTime($datestr.$timestr, new DateTimeZone('UTC'));
            $dtUTCstr = $dtUTC->format('H:i');
            $dtUTCtz = $dtUTC->format('T');

            // check for if report is more than about 3 days old (ignoring time zones, etc)
            $today = new DateTime('now', new DateTimeZone('America/Chicago'));
            $interval = date_diff($dtTX, $today);  # difference in days between now and most recent data
            $intervalstr = $interval->format('%R%a days');
            if ($intervalstr>3){ // old report
                $buoystr = "<td nowrap valign=top><div id=\"Report\">$dtTXstr $dtTXtz ($dtUTCstr $dtUTCtz)\n</div></td>";
            }
            elseif ($intervalstr<=7) { // bold for recent report
                $buoystr =  "<td nowrap valign=top><div id=\"Report\"><b>$dtTXstr $dtTXtz ($dtUTCstr $dtUTCtz)\n</div></b></td>";
            }
            else {  // missing plot
                $buoystr = "<td><div id=\"Report\">Not reporting</div></td></tr>";
            }
            }
    }
    else {
        $buoystr = "<td><div id=\"Report\">Not reporting</div></td></tr>";
    }
    // print letter of buoy with link to query page with image and hover of image
    // in low bandwidth case, don't load hover images
    if ($bandwidth == "low") {
        print "<TR bgcolor=\"#f8f8f8\"><td valign=top><div id=\"Report\"><a href=subpages/tabsquery.php?Buoyname=$f&table=$table&Datatype=pic&datepicker=recent&tz=US/Central&units=M>$f</a></div></TD>\n";
    }
    else {
        print "<TR bgcolor=\"#f8f8f8\"><td valign=top><div id=\"Report\"><a href=subpages/tabsquery.php?Buoyname=$f&table=$table&Datatype=pic&datepicker=recent&tz=US/Central&units=M rel=\"imgtip[$bidx]\">$f</a></div></TD>\n";
    }
    print $buoystr;
    $bidx++;
    // looks at next buoy since count + already happened
    if ((strpos($btable1[$bidx],'ndbc')===0) and (strpos($btable1[$bidx-1],'ndbc')!==0)) {
    print "<tr><td><br></td></tr>";  // space
    print "<tr><td></td><td><i><a name='ndbc'>NDBC</a></i></td></tr>";  // Label between TABS and NDBC buoys
    }
    else if ((strpos($btable1[$bidx],'ports')===0) and (strpos($btable1[$bidx-1],'ports')!==0)) {
    print "<tr><td><br></td></tr>";  // space
    print "<tr><td></td><td><i><a name='ports'>PORTS</a></i></td></tr>";
    }
    else if ((strpos($btable1[$bidx],'tcoon')===0) and (strpos($btable1[$bidx-1],'tcoon')!==0)) {
    print "<tr><td><br></td></tr>";  // space
    print "<tr><td></td><td><i><a name='tcoon'>TCOON</a></i></td></tr>";  // Label between PORTS and TCOON buoys
    }
    else if ((strpos($btable1[$bidx],'nos')===0) and (strpos($btable1[$bidx-1],'nos')!==0)) {
    print "<tr><td><br></td></tr>";  // space
    print "<tr><td></td><td><i><a name='nos'>NOS</a></i></td></tr>";  // Label between PORTS and TCOON buoys
    }
}
print "<tr></tr>";

?>

</tr>
</table>

</div>
</div>

<!-- include footer from separate file -->
<?php include("includes/footer.html");?>

</div>

</body>
</html>
