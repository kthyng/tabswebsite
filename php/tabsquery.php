
<?php

umask(0022);

$cm2e=.01943845;
$m2e=1.943845;
$degc="&#176;C";
$degf="&#176;F";
$degm="&#176;M";
$degt="&#176;T";

$PageTitle="TABS Buoy Database Query page";
include("tgloheader2.php");
#include("DB.php");



if ($_SERVER['REQUEST_METHOD'] != 'POST') {
echo "<meta HTTP-EQUIV=\"REFRESH\" CONTENT=\"3;URL=http://tabs1.gerg.tamu.edu/tglo/tabsqueryform.php\">";
echo "<meta HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">";

	print "<p><b>Database search form is here:</b> <a href=tabsqueryform.php>http://tabs.gerg.tamu.edu/tglo/tabsqueryform.php</a>";
} else {


$Buoyname=$_POST["Buoyname"];
$Year=$_POST["Year"];
$Month=$_POST["Month"];
$Day=$_POST["Day"];
$Nextdays=$_POST["Nextdays"];
$Prevdays=$_POST["Prevdays"];
$table=$_POST["table"];

$tempfile=tempnam("/home/woody/htdocs/Tglo/tmp",$Buoyname . $table);
$tempout=basename($tempfile);

#echo "BUOY: $Buoyname  $table<br>TMP: $tempout  $tempfile<BR>";

if ($table == "met" && ! preg_match('/B|H|J|K|N|V/',$Buoyname) ) {
die( "<h2>No Met Data Available for selected station</h2>\n" ); }

#if ($table == salt && ! preg_match('/B|H|J|K|N|V/',$Buoyname) ) {
#die( "<h2>No Water Property Data Available for selected station</h2>\n" ); }


$dstart=$Year."-".$Month."-".$Day;

// related to conneting to the database server
// change localhost to polonium.gerg.tamu.edu
// if (! $dbh=mysql_connect('localhost','tabsweb','tabs')) {
// user tabsweb might be in sql database (or on woody's)
if (! $dbh=mysql_connect('tabs1.gerg.tamu.edu','tabsweb','tabs')) {
	die("Can't connect: ".mysql_error());
	}

#$dbase="tabs_".$Buoyname;
$dbase="tabsdb";
$tablename="tabs_".$Buoyname."_".$table;
#echo "DB: $dbase  TAB: $tablename<br>\n";

#$dsn='mysql://woody@localhost/'.$dbase;

mysql_select_db($dbase) or die(mysql_error());
#$dbh=DB::connect($dsn);

#if (DB::isError($dbh)) {die ($dbh->getMessage());}

$q="SELECT * FROM $tablename WHERE (date BETWEEN '$dstart' - interval $Prevdays day AND '$dstart' + interval $Nextdays day) order by obs_time";
$result = mysql_query($q)
    or die(mysql_error());


#$rows=$dbh->getAll($q);
while ($row = mysql_fetch_row($result)) {
$rows[] = $row;
#print_r($row);echo "<br>";
}

mysql_close();



foreach ($rows as $data) {

if ($table == 'ven'){
list($datetime,$date,$time,$ve,$vn,$comp,$twater,$tx,$ty)=$data;
$date=strftime("%m/%d/%Y",strtotime($data[1]));
$speed=hypot($ve,$vn);


$dir=90.-(rad2deg(atan2($vn,$ve)));
if ($dir < 0.) {$dir+=360.;}

$tmpfh=fopen($tempfile,'a') or die($php_errormsg);
$outstr=sprintf("%s %s %8.2f %8.2f %8.2f %8.1f %8.1f\n",$date,$time,$ve,$vn,$speed,$dir,$twater);
fputs($tmpfh,$outstr);
fclose($tmpfh) or die($php_errormsg);


}

if ($table == 'met'){
list($datetime,$date,$time,$ve,$vn,$airt,$atmp,$gust,$comp,$tx,$ty,$par,$relh)=$data;
$date=strftime("%m/%d/%Y",strtotime($data[1]));

$tmpfh=fopen($tempfile,'a') or die($php_errormsg);
$outstr=sprintf("%s %s %7.2f %7.2f %7.1f %7.2f %7.2f %5.1f %4.0d %4.0d %7.1f %7.1f\n",
$date,$time,$ve,$vn,$airt,$atmp,$gust,$comp,$tx,$ty,$par,$relh);
fputs($tmpfh,$outstr);
fclose($tmpfh) or die($php_errormsg);

}

if ($table == 'eng'){
list($datetime,$date,$time,$vbatt,$sigstr,$comp,$nping,$tx,$ty,$adcpv,$adcpcurr,$vbatt2)=$data;
$date=strftime("%m/%d/%Y",strtotime($data[1]));
$tmpfh=fopen($tempfile,'a') or die($php_errormsg);
$outstr=sprintf("%s %s %7.1f %7.2f %7.1f %7.0f %3.0d %3.0d %7.1f %7.1f %7.1f\n",
$date,$time,$vbatt,$sigstr,$comp,$nping,$tx,$ty,$adcpv,$adcpcurr,$vbatt2);
fputs($tmpfh,$outstr);
fclose($tmpfh) or die($php_errormsg);

}


if ($table == 'salt'){
list($datetime,$date,$time,$watertemp,$conduct,$salinity,$density,$soundvel)=$data;
$date=strftime("%m/%d/%Y",strtotime($data[1]));
$tmpfh=fopen($tempfile,'a') or die($php_errormsg);
$outstr=sprintf("%s %s %7.2f %7.2f %7.2f %7.2f %7.2f\n",
$date,$time,$watertemp,$conduct,$salinity,$density,$soundvel);
fputs($tmpfh,$outstr);
fclose($tmpfh) or die($php_errormsg);

}

}
chmod($tempfile, 0644);

if ($_POST['Datatype']=="pic") {
	system('/home/woody/htdocs/tglo/prog/queryplot.csh '.escapeshellarg($tempfile));
	print "<TABLE cellspacing=0 cellpadding=0  border=0 width=100%>";
	print "<TR><TD valign=top width=240><font face=helvetica><HR width=100%><BR>";
print "<table>\n";
print "<TR valign=top><TD>Return to <a href=/tglo/tabsqueryform.php>TABS Database query</a></TD></TR>\n";
print "<TR><TD>Return to <a href=/tglo/>TABS page</a></TR></TD>\n";
print "</table>\n";
	print "</TD><TD valign=top><HR width=100%><br>";
        print "<font face=helvetica><b>Results of TABS Data query</b>(<a href=/tglo/viewtmp.php?file=$tempout>download</a>)</font><br>\n";
	print "<a href=/tglo/tmp/".$tempout.".pdf> <img src=/tglo/tmp/".$tempout.".png></A>\n";
	print "</TD></TR></TABLE>\n";
}

if ($_POST['Datatype']=="data") {
print "<TABLE width=100%>";
print "<TR><TD valign=top width=240 align=left>";
print "<br> &nbsp;\n";
print "<br><FORM Action=$PHP_SELF method=\"POST\">\n";
print "<input NAME=buoy TYPE=hidden value=$buoylet>\n";
print "<font face=\"Helvetica\" size=-1>\n";
print "<Select Name=tz>\n";
print "<option value=''>Time Zone</Option>\n";
print "<option value='UTC'>UTC</Option>\n";
print "<option value='STN'>Station Local</option>\n</select><br>\n";
if ($table != "eng") {
print "<Select Name=units>\n";
print "<option value=''>Units</Option>\n";
print "<option value='M'>Metric</Option>\n";
print "<option value='E'>English</option>\n</select>\n";
}
print "<input NAME=Buoyname TYPE=hidden value=$Buoyname>\n";
print "<input NAME=table TYPE=hidden value=$table>\n";
print "<input NAME=Prevdays TYPE=hidden value=$Prevdays>\n";
print "<input NAME=Nextdays TYPE=hidden value=$Nextdays>\n";
print "<input NAME=Year TYPE=hidden value=$Year>\n";
print "<input NAME=Month TYPE=hidden value=$Month>\n";
print "<input NAME=Day TYPE=hidden value=$Day>\n";
print "<input NAME=Datatype TYPE=hidden value=$Datatype>\n";

print "<BR><input type=submit  value=Change>\n</form>\n";

print "<br><table>\n";
print "<TR><TD>Return to <a href=/tglo/tabsqueryform.php>TABS Database query</a></TD></TR>\n";
print "<TR><TD>Return to <a href=/tglo/>TABS page</a></TR></TD>\n";
print "</table>\n";
print "</font>\n";
print "</TD><TD style=\"text-align:left !important;\">";
print "<pre>";

if (! $units) {$units = 'M';}

$data=explode(" ",$venlines[0]);
if ($_POST['tz'] == 'UTC' || $_POST['tz'] == '') {
        $ts_utc=strtotime($data[0]." ".$data[1]);
		$timez="UTC";
        } else {
        $ts_utc=strtotime($data[0]." ".$data[1]." UTC");
$timez=strftime("%Z",strtotime($data[0]." ".$data[1]));
                }

if ($table == 'ven' ) {
if ($units=="M") {$convfac=1;$ut="(cm/s)";$tut=$degc;}
	else {$convfac=$cm2e;$ut=" (kts)";$tut=$degf;}

$header=$table."tableheader.php";
print "<b>Results of TABS Data query</b>(<a href=/tglo/tmp/$tempout>download</a>)<br>\n";
include($header);

$venlines1=file($tempfile);
foreach ($venlines1 as $elem) {
        $elem=preg_replace("/\s+/"," ",$elem);
        $data=explode(" ",$elem);
        if ($_POST['tz'] == 'UTC' || $_POST['tz'] == '') {
                $ts_utc=strtotime($data[0]." ".$data[1]);
                } else {
                $ts_utc=strtotime($data[0]." ".$data[1]." UTC");
		$timez=strftime("%Z",strtotime($data[0]." ".$data[1]));
                }
        $datestr=strftime("%m/%d/%Y",$ts_utc);
        $timestr=strftime("%T",$ts_utc);
        $east=$data[2] * $convfac;
        $north=$data[3]* $convfac;
        $speed=$data[4] * $convfac;
        $dir=$data[5];
        $temp=$data[6];
        if ($units == 'E') {$temp=(1.8*$temp)+32;}
        printf ("%8s %8s %8.2f %8.2f %8.2f %6.1f %7.1f\n",
        $datestr,$timestr,$east,$north,$speed,$dir,$temp);
}

}

if ($table == 'met' ) {
if ($units=="M") {$convfac=1;$ut=" (m/s)";$tut=$degc;$aut=' (mb) ';$atmconv=1;}
	else {$convfac=$m2e; $ut="(kts)";$tut=$degf;$aut='(inHg)';$atmconv=33.863886;}

if ($table=='met') {
	print "<br>Note: East and North wind data show direction toward.&nbsp;Wind Speed and direction data show direction from\n";

}
$header=$table."tableheader.php";
print "<b>Results of TABS Data query</b>(<a href=/tglo/tmp/$tempout>download</a>)<br>\n";

include($header);

$metlines1=file($tempfile);
foreach ($metlines1 as $elem) {
        $elem=preg_replace("/\s+/"," ",$elem);
        $data=explode(" ",$elem);
        if ($_POST['tz'] == 'UTC' || $_POST['tz'] == '') {
                $ts_utc=strtotime($data[0]." ".$data[1]);
                } else {
                $ts_utc=strtotime($data[0]." ".$data[1]." UTC");
		$timez=strftime("%Z",strtotime($data[0]." ".$data[1]));
                }
        $datestr=strftime("%m/%d/%Y",$ts_utc);
        $timestr=strftime("%T",$ts_utc);
        $veast_c=$data[2] * $convfac;
        $vnorth_c=$data[3]* $convfac;
        $veast=$data[2];
        $vnorth=$data[3];
	$airtemp=$data[4];
        $atmpr=$data[5] / $atmconv;
        $gust=$data[6] * $convfac;
	$comp=$data[7];
	$tx=$data[8]; $ty=$data[9];
	$par=$data[10]; $relh=$data[11];
	$wspeed=hypot($veast,$vnorth);
	$wspd=$wspeed * $convfac;
	$wdir=90.-(rad2deg(atan2(-$vnorth,-$veast)));
	if ($wdir < 0.) {$wdir+=360.;}


        if ($units == 'E') {$airtemp=(1.8*$airtemp)+32;}
 	printf ("%s %s %7.2f %7.2f %7.1f %7.2f %7.2f %7.1f %4d %4d %6.1f %6.1f %7.2f %7.1f\n",
        $datestr,$timestr,$veast_c,$vnorth_c,$airtemp,$atmpr,$gust,$comp,$tx,$ty,$par,$relh,$wspd,$wdir);

}

}


if ($table == 'eng' ) {

$header=$table."tableheader.php";
print "<b>Results of TABS Data query</b>(<a href=/tglo/tmp/$tempout>download</a>)<br>\n";
include($header);

$englines1=file($tempfile);
foreach ($englines1 as $elem) {
        $elem=preg_replace("/\s+/"," ",$elem);
        $data=explode(" ",$elem);
        if ($_POST['tz'] == 'UTC' || $_POST['tz'] == '') {
                $ts_utc=strtotime($data[0]." ".$data[1]);
                } else {
                $ts_utc=strtotime($data[0]." ".$data[1]." UTC");
		$timez=strftime("%Z",strtotime($data[0]." ".$data[1]));
                }
        $datestr=strftime("%m/%d/%Y",$ts_utc);
        $timestr=strftime("%T",$ts_utc);
        $vbatt=$data[2];
        $sigstr=$data[3];
	$comp=$data[4];
        $nping=$data[5];
	$tx=$data[6]; $ty=$data[7];
	$adcpvolt=$data[8]; $adcpcurr=$data[9];
        $vbatt2=$data[10];

 	printf ("%s %s %7.1f %7.2f %7.1f %6.0f %4d %4d %6.1f %6.1f %6.1f\n",
        $datestr,$timestr,$vbatt,$sigstr,$comp,$nping,$tx,$ty,$adcpvolt,$adcpcurr,$vbatt2);

}
}


if ($table == 'salt' ) {

if ($units=="M") {$convfac=1;$ut="(m/s)";$tut=$degc;$aut=' (mb) ';$atmconv=1;}
	else {$convfac=$m2e; $ut="(kts)";$tut=$degf;$aut='(inHg)';$atmconv=33.863886;}

$header=$table."tableheader.php";
print "<b>Results of TABS Data query</b>(<a href=/tglo/tmp/$tempout>download</a>)<br>\n";
include($header);

$englines1=file($tempfile);
foreach ($englines1 as $elem) {
        $elem=preg_replace("/\s+/"," ",$elem);
        $data=explode(" ",$elem);
        if ($_POST['tz'] == 'UTC' || $_POST['tz'] == '') {
                $ts_utc=strtotime($data[0]." ".$data[1]);
                } else {
                $ts_utc=strtotime($data[0]." ".$data[1]." UTC");
		$timez=strftime("%Z",strtotime($data[0]." ".$data[1]));
                }
        $datestr=strftime("%m/%d/%Y",$ts_utc);
        $timestr=strftime("%T",$ts_utc);
        $watertemp=$data[2];
        $conduct=$data[3];
	$salinity=$data[4];
        $density=$data[5];
	$soundvel=$data[6];
        if ($units == 'E') {$watertemp=(1.8*$watertemp)+32;}

 	printf ("%s %s %8.2f %8.2f %8.2f %8.2f %8.2f\n",
        $datestr,$timestr,$watertemp,$conduct,$salinity,$density,$soundvel);

}
}

}
print "</pre></p>";
print "</TD></TR></TABLE>";

}



?>
