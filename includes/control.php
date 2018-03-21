<!-- bottom control options for query page -->


<?php

print "<br><br>";
print "<font face=\"Helvetica\" size=-1>\n";
print "<TABLE width=100%>";
print "<TR>";
print "<td>";

// Switch to data from pic or pic from data (when data is available)
if (! $norecentdata and !$norecentdatabutmodel){
    print "Switch to <a href=/tabswebsite/subpages/tabsquery.php?Buoyname=$Buoyname&table=$table&Datatype=$newdatatype&tz=$tz&units=$units&datepicker=".urlencode($datepicker).">$newdatatypename</a></TD>\n";
}
// If on data, but no recent data, can switch to pic with model output
elseif (($norecentdata or $norecentdatabutmodel) and $datatype == "data") {
    print "Switch to <a href=/tabswebsite/subpages/tabsquery.php?Buoyname=$Buoyname&table=$table&Datatype=pic&tz=$tz&units=$units&datepicker=".urlencode($datepicker).">$newdatatypename</a></TD>\n";
}
// If on image, but no recent data, nothing to switch to
else {
    print "No table to show</TD>\n";
}
print "<TD>Go to <a href=/tabswebsite/subpages/tabsqueryform.php?Buoyname=$Buoyname&table=$table&datepicker=".urlencode($datepicker)."&tz=$tz&units=$units>database query</a></TD>\n";
print "<TD>Go to <a href=/tabswebsite/index.php>homepage</a></TR></TD>\n";
print "</table>\n";


print "<TABLE width=90%>";
print "<TR>";
print "<td>Update results: </td>";
// print "<br> &nbsp;\n";
print "<br><form action=\"/tabswebsite/subpages/tabsquery.php\" method=\"get\">\n";

// read into an array the active buoys
// read in buoy list from csv file with buoy info
$csv = array_map("str_getcsv", file("../includes/buoys.csv"));
$header = array_shift($csv); // Seperate the header from data
$col = array_search("buoy", $header);  # save column name for buoys
$active = array_search("active", $header);  # save column name for buoys being active
foreach ($csv as $row) {  // loop over each row in csv file
    // check if buoy is active
    if (strcmp($row[$active], "TRUE") == 0) {
    	$blet[] = $row[$col];  // if so, save buoy name
    }
}

// Change buoy
print "<td><Select Name=Buoyname id=json-one>\n";
print "<OPTION SELECTED value='$Buoyname'>$Buoyname</option>\n";
foreach ($blet as $f) {
    print "<option value='$f'>$f</option>\n";
}
print "</select></td>\n";

// Change table (variable file)
print "<td><select id=json-two name=table>";
print "<option selected value='$table'>$table</option></select></td>";

# Units
if (($table != "eng") and ($datatype == "data")) {
    print "<td><Select Name=units>\n";
    // print "<option value=''>Units</Option>\n";
    print "<option selected value='$units'>$unitsname</option>\n";
    print "<option value='M'>Metric</Option>\n";
    print "<option value='E'>English</option>\n</select></td>\n";
}
else {
    print "<input NAME=units TYPE=hidden value=$units>\n";
}

# Calendar
print "<TD><input type='text' value='$datepicker' id='datepicker' name='datepicker'></TD>";

if ($tz == 'UTC') {
    $tzname = 'UTC';
}
else if ($tz == 'US/Central') {
    $tzname = 'Local';
}
else if ($tz == 'Etc/GMT+6') {
    $tzname = 'CST';
}

# time zone
print "<td>";
print "<Select Name=tz>\n";
print "<option selected value='$tz'>$tzname</option>\n";
print "<option value='UTC'>UTC</Option>\n";
print "<option value='US/Central'>Local</option>\n";
print "<option value='Etc/GMT+6'>CST</option>\n</select></td>\n";

# Model: yes or no
if ($datepicker=="recent"){
    $model = "True";
}
print "<td>";
print "<Select Name=model>\n";
print "<option value='$model'>Model: $model</Option>\n";
print "<option value='True'>True</Option>\n";
print "<option value='False'>False</option>\n</select></td>\n";

print "<input NAME=Datatype TYPE=hidden value=$datatype>\n";
// print "<input NAME=norecentdata TYPE=hidden value=$norecentdata>\n";
// print "<input NAME=norecentdata TYPE=hidden value=$norecentdatabutmodel>\n";

// print "<BR>";
print "<td><input type=submit  value=Update></td>\n</form>\n";
print "</font>\n";

?>
