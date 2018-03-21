

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


<!-- this div centers content dynamically -->
<div id="container">

<!-- include header from separate file -->
<?php include("includes/header.html");?>


<!-- include navigation from separate file -->
<?php include("includes/navigation.html");?>

<div id="mapbuoycontainer">

<div id="mapcontainer">

<div id="map" >
  <iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0" width="800px" height="480px" src="http://pong.tamu.edu/tabs_map/?framed"></iframe>
<!-- text below map -->
<center>
<p><i><font class=bkvsm style="font-size:6pt;">
The vectors on the map point toward the direction that the currents or winds are flowing and represent the average for the
last three hours of the available data.<br>
The date and time at each station indicates the end of the three-hour average.<br>
</font></i></p>
</center>
</div>
</div>
<!-- end map -->


<!-- buoy list on right hand side -->
<div id="buoycontainer">
<table border=0 bgcolor="#f8f8f8" >
<!-- <TD><div id="blank"><TABLE border=0><TH colspan=1 align=left><font class==bknorm size=1.5em><br>&nbsp &nbsp &nbsp &nbsp &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp </font></th></table></div></TD> -->
<tr>
<td><b>Recent</b></td>
<TD valign=top colspan=2><div id="Report"><b><a href="subpages/currents.php">Last data report</a></b></div></td>
</tr>

<?php

// read in buoy list from csv file with buoy info
$csv = array_map("str_getcsv", file("includes/buoys.csv"));
$header = array_shift($csv); // Seperate the header from data

$col = array_search("buoy", $header);  # save buoys
$active = array_search("active", $header);  # save if buoys are active or not

foreach ($csv as $row) {  // loop over each row in csv file
    // check if buoy is active
    // echo strcmp($row[$active], "TRUE") == 0;
    // if (strcmp($row[$active], "True")) {
    if (strcmp($row[$active], "TRUE") == 0) {
    	$blet[] = $row[$col];  // if so, save buoy name
    }
}

// // this list should match the "active" buoy list in python/buoy_data.py
// $blet=array("B","D","F","J","K","R","V","W","X",
//             '42001', '42002', '42019','42020','42035', '42036', '42039', '42040',
//             'SRST2', 'PTAT2', 'BURL1',
//             'g06010', 'g08010', 'g09010', 'mc0101', 'sn0101', 'sn0201', 'sn0301', 'sn0401', 'sn0501',
//             'sn0701', 'lc0101', 'lc0201', 'mg0101',
//             '8770475','8770520', '8770777', '8770808',
//             '8770822','8770971', '8771486', '8771972', '8772985', '8773037',
//             '8773146', '8773259', '8773701', '8774230', '8775237',
//             '8775241', '8775244', '8775296', '8775792', '8776139',
//             '8776604', '8777812', '8778490', '8779280', '8779748', '8779749',
//             '8734673', '8735180', '8741003', '8741041', '8741094', '8741501',
//             '8741533', '8747437', '8760721', '8760922', '8761305', '8761724',
//             '8764227', '8764314', '8766072', '8768094', '8770570', '8770613',
//             '8771013', '8771341', '8771450', '8773767', '8775870', '8779770'
//             );
$bidx=0;
foreach ($blet as $f) {
    if (strlen($f) == 1) {
    	$venfile="daily/tabs_".$f."_sum";
        $table = "sum";
    }
    else {
    	$venfile="daily/".$f;
    }

    // $venfile="http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_".$f."_ven.txt";
    if (file_exists($venfile)) {

        $lines=file($venfile);
    	$l=array_pop($lines);  // grab last line in file
    	if (trim($l)) {
    		$line=trim($l);  # strip white space from beginning and end of string
            $data = preg_split('/\s+/', $line);  # split by white space or by tab
            $datestr=$data[0];
    		$timestr=substr($data[1],0,5);

            $dtTX = new DateTime($datestr.$timestr, new DateTimeZone('America/Chicago'));
            $dtTXstr = $dtTX->format('M d, Y H:i');
            $dtTXtz = $dtTX->format('T');

            // check for if report is more than about 3 days old (ignoring time zones, etc)
            $today = new DateTime('now', new DateTimeZone('America/Chicago'));
            $interval = date_diff($dtTX, $today);  # difference in days between now and most recent data
            $intervalstr = $interval->format('%R%a days');
            if ($intervalstr>3){ // old report
                $buoystr = "<td nowrap valign=top><div id=\"Report\">$dtTXstr $dtTXtz\n</div></td>";
            }
            elseif ($intervalstr<=7) { // bold for recent report
                $buoystr =  "<td nowrap valign=top><div id=\"Report\"><b>$dtTXstr $dtTXtz\n</div></b></td>";
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
    print "<TR bgcolor=\"#f8f8f8\"><td valign=top><div id=\"Report\"><a href=subpages/tabsquery.php?Buoyname=$f&table=$table&Datatype=pic&datepicker=recent&tz=US/Central&units=M rel=\"imgtip[$bidx]\">$f</a></div></TD>\n";
    print $buoystr;
    $bidx++;
    if ($f == "X") {
    print "<tr><td><br></td></tr>";  // space
    print "<tr><td></td><td><i>NDBC</i></td></tr>";  // Label between TABS and NDBC buoys
    }
    else if ($f == "BURL1") {
    print "<tr><td><br></td></tr>";  // space
    print "<tr><td></td><td><i>PORTS</i></td></tr>";
    }
    else if ($f == "mg0101") {
    print "<tr><td><br></td></tr>";  // space
    print "<tr><td></td><td><i>TCOON</i></td></tr>";  // Label between PORTS and TCOON buoys
    }
    else if ($f == "8779749") {
    print "<tr><td><br></td></tr>";  // space
    print "<tr><td></td><td><i>NOS</i></td></tr>";  // Label between PORTS and TCOON buoys
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
