

<HEAD>
<!-- <link href="/tglo/newtabs.css" rel="stylesheet" type="text/css"> -->
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

<TITLE>TABS, Texas Automated Buoy System, Gulf of Mexico Ocean Observatory, Texas Coastal Ocean Observation, Real Time
Oceanographic Data Supporting Oil Spill Prevention and Response</TITLE>

<meta HTTP-EQUIV="REFRESH" CONTENT="300">
<meta HTTP-EQUIV="Expires" CONTENT="1800">
<meta HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate">
<meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="HandheldFriendly" content="true">
<meta name="viewport" content="width=device-width,maximum-scale=1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">


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

<!-- This is for the hovering images -->
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
<link rel="stylesheet" type="text/css" href="css/ddimgtooltip.css" />
<script type="text/javascript" src="js/ddimgtooltip.js">
/***********************************************
* Image w/ description tooltip v2.0- (c) Dynamic Drive DHTML code library (www.dynamicdrive.com)
* This notice MUST stay intact for legal use
* Visit Dynamic Drive at http://www.dynamicdrive.com/ for this script and 100s more
***********************************************/
</script>

</HEAD>


<!-- include header from separate file -->
<?php include("includes/header.html");?>


<!-- include navigation from separate file -->
<?php include("includes/navigation.html");?>


<!-- Map from server-->
<TR>
<TD valign=top width=44 rowspan=11>
<div id="map" >
  <iframe width="815" height="485" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://localhost:5000/static/tabs.html"></iframe>
</div>
<!-- text below map -->
<center>
<i><font class=bkvsm style="font-size:6pt;">
The vectors on the map point toward the direction that the currents or winds are flowing and represent the average for the
last three hours of the available data.<br>
The date and time at each station indicates the end of the three-hour average.<br>
</i></font>
</td>
</center>
<!-- end map -->


<!-- buoy list on right hand side -->
<TR>
<TD><div id="blank"><TABLE border=0><TH colspan=2 align=left><font class==bknorm size=2em><br>&nbsp &nbsp &nbsp &nbsp &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp </font></th></table></div></TD>
<TD valign=top>
<div id="Report">
<b>Most Recent Report</b>

<?php
echo "<table border=0 bgcolor=\"#f8f8f8\">";

// slow!
// $command = escapeshellcmd('/anaconda/bin/python return_recent_datetime.py');
// exec($command, $output);
// var_dump($output);

$blet=array("B","D","F","J","K","N","R","V","W","X");
$bidx=0;
foreach ($blet as $f) {
	$venfile="daily/tabs_".$f."_ven";
    // $venfile="http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_".$f."_ven.txt";
    if (file_exists($venfile)) {

        $lines=file($venfile);
    	$l=array_pop($lines);
    	if (trim($l)) {
    		$line=trim($l);
            $data = preg_split('/\s+/', $line);  # split by white space or by tab
            $datestr=$data[0];
    		$timestr=substr($data[1],0,5);

            // tabs datetime in UTC and Texas time (CST/CDT)
            // set up date and time together with UTC timezone (which is what the data is in)
            $dtUTC = new DateTime($datestr.$timestr, new DateTimeZone('UTC'));
            // echo $dtUTC->format('Y-m-d H:i');
            // save formatted string
            // http://php.net/manual/en/datetime.formats.date.php
            // $dtUTCstr = $dtUTC->format('Y-m-d H:i');
            $dtUTCstr = $dtUTC->format('M d, Y H:i');
            // find time zone abbreviation
            // http://stackoverflow.com/questions/5362628/how-to-get-the-names-and-abbreviations-of-a-time-zone-in-php
            $dtUTCtz = $dtUTC->format('T');

            // start from UTC datetime
            $dtTX = $dtUTC;
            // convert to TX
            // http://www.silenceit.ca/2011/06/15/how-to-convert-timetimezones-with-php/
            $dtTX->setTimezone(new DateTimeZone('America/Chicago'));
            $dtTXstr = $dtTX->format('M d, Y H:i');
            $dtTXtz = $dtTX->format('T');
            # date range for the php call
            $recent = $dtUTC->format('Y-m-d');  # most recent date for buoy
            $earlier = $dtUTC->modify('-4 days')->format('Y-m-d');
            $timerange = $earlier."+-+".$recent;  # + makes the space between the dates somehow

            // check for if report is more than about 5 days old (ignoring time zones, etc)
            $today = new DateTime('now', new DateTimeZone('UTC'));
            $interval = date_diff($dtUTC, $today);  # difference in days between now and 5 days ago
            $intervalstr = $interval->format('%R%a days');
            if ($intervalstr>5){ // old report
                $buoystr = "<td nowrap valign=top><font class=bksm>$dtUTCstr $dtUTCtz ($dtTXstr $dtTXtz)\n</td>";
            }
            elseif ($intervalstr<=5) { // bold for recent report
                $buoystr =  "<td nowrap valign=top><b><font class=bksm>$dtUTCstr $dtUTCtz ($dtTXstr $dtTXtz)\n</b></td>";
            }
            else {  // missing plot
                $buoystr = "<td>Not reporting</td></tr>";
            }
            }
    }
    else {
        $buoystr = "<td>Not reporting</td></tr>";
    }
    // print letter of buoy with link to query page with image and hover of image
    print "<TR bgcolor=\"#f8f8f8\"><td valign=top><font class=bksm><a href=tabsquery.php?Buoyname=$f&table=ven&Datatype=pic&datepicker=recent rel=\"imgtip[$bidx]\">$f</a></font></TD>\n";
    print $buoystr;
    $bidx++;
}
print "<tr></tr>";
print "<tr><td></td> <td><a href=tabsqueryform.php>Search TABS database</a></td></tr>";
// print "<tr><td></td> <td><a href=tabsqueryform.php><font color='black'>Search TABS database</font></a></td></tr>";
echo "</table>";
?>
<BR>
<a href="http://localhost:5000/static/index.html"  target="_blank" style="font-size: 18px; text-decoration: none">&nbsp &nbsp Click for full-screen map </a>
<!-- <a href="http://localhost:5000/static/index.html"  target="_blank" style="font-size: 18px; color:#009933; text-decoration: none">&nbsp &nbsp Click for full-screen map </a> -->
</TD>
</TR>

</TABLE>
</div>

<!-- separate text below map from footer -->
<BR><BR>

<!-- include footer from separate file -->
<?php include("includes/footer.html");?>

</body>
</html>
