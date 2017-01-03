

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



<!-- <script type="text/javascript" src="js/jquery.min.js?v=1.8.2"></script>
<script type="text/javascript" src="js/jquery.once.js?v=1.2"></script>
<script type="text/javascript" src="js/tamustyle.js"></script>
<script type="text/javascript" src="js/bootstrap.min.js"></script>
 <script type="text/javascript" src="js/leaflet.js"></script> -->
<!-- <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.css" /> -->
<!--[if lte IE 8]>
     <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.ie.css" />
 <![endif]-->
  <!-- <script src="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.js"></script> -->

<!-- <script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-21828695-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })
  //example user location
//var userLocation = new L.LatLng();
   function initmap() {
	var userLocation = new L.LatLng(30.623944, -96.354405);

// var map = L.map('map').setView(userLocation, 13)
//
// 	L.tileLayer('http://{s}.tile.cloudmade.com/f6a65c832e93471b9c3f55e6a1cc1f83/997/256/{z}/{x}/{y}.png', {
// 	    maxZoom: 18,
// 	    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery � <a href="http://cloudmade.com">CloudMade</a>'
// 	}).addTo(map);
// }

	var marker = new L.Marker(userLocation);
	map.addLayer(marker);

</script> -->

<!-- <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script> -->

<!-- <link rel="stylesheet" type="text/css" href="css/ddimgtooltip.css" /> -->

<!-- <script type="text/javascript" src="js/ddimgtooltip.js">

/***********************************************
* Image w/ description tooltip v2.0- (c) Dynamic Drive DHTML code library (www.dynamicdrive.com)
* This notice MUST stay intact for legal use
* Visit Dynamic Drive at http://www.dynamicdrive.com/ for this script and 100s more
***********************************************/



tooltips[0]=["images/tabs_B_ven.png", {width:"200px", height: "100px";}]

</script> -->

<!-- <script type="text/javascript">
$(document).ready(function(){
	var pagebody = $("#head");
	var themenu = $("#navmenu");
	var topbar  = $("#toolbarnav");
	var content = $("#content");
	var viewport = {
  	width : $(window).width(),
  	height : $(window).height()
	};
	// retrieve variables as
	// viewport.width / viewport.height

	function openme() {
	$(function () {
	  topbar.animate({
	    left: "290px"
	  }, { duration: 300, queue: false });
	  pagebody.animate({
	    left: "290px"
	  }, { duration: 300, queue: false });
	});
}

function closeme() {
	var closeme = $(function() {
  	topbar.animate({
      left: "0px"
  	}, { duration: 180, queue: false });
  	pagebody.animate({
      left: "0px"
  	}, { duration: 180, queue: false });
	});
}
</script> -->

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

$blet=array("B","D","F","J","K","N","R","V","W","X");
	$bidx=0;
foreach ($blet as $f) {
	if (preg_match("/Z/",$f)) {
		print "<TR bgcolor=\"#f8f8f8\"><td valign=top><font class=bksm><A href=/tglo/ven.php?buoy=$f>$f</a></font></TD>\n";
		print "<td nowrap valign=top><font class=bksm>Not Reporting</font>\n";
		}
    else {
	$venfile="http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_".$f."_ven.txt";
	$lines=file($venfile);
	$l=array_pop($lines);
	if (trim($l)) {
		$line=trim($l);
		$data=explode(' ',$line);$datestr=$data[0];
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
        $dtTXstr = $dtTX->format('H:i');
        $dtTXtz = $dtTX->format('T');
        # date range for the php call
        $recent = $dtUTC->format('Y-m-d');  # most recent date for buoy
        $earlier = $dtUTC->modify('-4 days')->format('Y-m-d');
        $timerange = $earlier."+-+".$recent;  # + makes the space between the dates somehow
        // print "<TR bgcolor=\"#f8f8f8\"><td valign=top><font class=bksm><a href=/tglo/ven.php?buoy=$f rel=\"imgtip[$bidx]\">$f</a></font></TD>\n";
        // print "<TR bgcolor=\"#f8f8f8\"><td valign=top><font class=bksm><a href=http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_B_ven.png rel=http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_B_ven.png>$f</a></font></TD>\n";
        print "<TR bgcolor=\"#f8f8f8\"><td valign=top><font class=bksm><a href=tabsquery.php?Buoyname=$f&table=ven&Datatype=pic&datepicker=$timerange>$f</a></font></TD>\n";
		print "<td nowrap valign=top><font class=bksm>$dtUTCstr $dtUTCtz ($dtTXstr $dtTXtz)\n";
		}

    }
	$bidx++;
}
echo "</table>";
?>
<BR>
<a href="http://localhost:5000/static/index.html"  target="_blank" style="font-size: 18px; color:#009933; text-decoration: none">&nbsp &nbsp Click for full-screen map </a>
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
