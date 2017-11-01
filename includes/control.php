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


print "<TABLE width=70%>";
print "<TR>";
print "<td>Update results: </td>";
print "<td>";
// print "<br> &nbsp;\n";
print "<br><form action=\"/tabswebsite/subpages/tabsquery.php\" method=\"get\">\n";

if (($datatype == "data")) {
    print "<Select Name=tz>\n";
    // print "<option value=''>Time Zone</Option>\n";
    print "<option selected value='$tz'>$tzname</option>\n";
    print "<option value='UTC'>UTC</Option>\n";
    print "<option value='central'>US/Central</option>\n</select></td><br>\n";
}
else {
    print "<input NAME=tz TYPE=hidden value=$tz>\n";
}
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

// Change buoy
print "<td><Select Name=Buoyname id=json-one>\n";
print "<OPTION SELECTED value='$Buoyname'>$Buoyname</option>\n";
print "<option value='B'>B</option>\n";
print "<option value='D'>D</option>\n";
print "<option value='F'>F</option>\n";
print "<option value='J'>J</option>\n";
print "<option value='K'>K</option>\n";
print "<option value='R'>R</option>\n";
print "<option value='V'>V</option>\n";
print "<option value='W'>W</option>\n";
print "<option value='X'>X</option>\n";
print "<OPTION value='42001'>42001</option>\n";
print "<OPTION value='42002'>42002</option>\n";
print "<OPTION value='42019'>42019</option>\n";
print "<OPTION value='42020'>42020</option>\n";
print "<OPTION value='42035'>42035</option>\n";
print "<OPTION value='42036'>42036</option>\n";
print "<OPTION value='42039'>42039</option>\n";
print "<OPTION value='42040'>42040</option>\n";
print "<OPTION value='SRST2'>SRST2</option>\n";
print "<OPTION value='PTAT2'>PTAT2</option>\n";
print "<OPTION value='BURL1'>BURL1</option>\n";
print "<OPTION value='GISL1'>GISL1</option>\n";
print "<OPTION value='AMRL1'>AMRL1</option>\n";
print "<OPTION value='PSTL1'>PSTL1</option>\n";
print "<OPTION value='g06010'>g06010</option>\n";
print "<OPTION value='8770475'>8770475</option>\n";
print "<OPTION value='8770520'>8770520</option>\n";
print "<OPTION value='8770733'>8770733</option>\n";
print "<OPTION value='8770777'>8770777</option>\n";
print "<OPTION value='8770808'>8770808</option>\n";
print "<OPTION value='8770822'>8770822</option>\n";
print "<OPTION value='8770971'>8770971</option>\n";
print "<OPTION value='8771486'>8771486</option>\n";
print "<OPTION value='8771972'>8771972</option>\n";
print "<OPTION value='8772985'>8772985</option>\n";
print "<OPTION value='8773037'>8773037</option>\n";
print "<OPTION value='8773146'>8773146</option>\n";
print "<OPTION value='8773259'>8773259</option>\n";
print "<OPTION value='8773701'>8773701</option>\n";
print "<OPTION value='8774230'>8774230</option>\n";
print "<OPTION value='8775237'>8775237</option>\n";
print "<OPTION value='8775241'>8775241</option>\n";
print "<OPTION value='8775244'>8775244</option>\n";
print "<OPTION value='8775296'>8775296</option>\n";
print "<OPTION value='8775792'>8775792</option>\n";
print "<OPTION value='8776139'>8776139</option>\n";
print "<OPTION value='8776604'>8776604</option>\n";
print "<OPTION value='8777812'>8777812</option>\n";
print "<OPTION value='8778490'>8778490</option>\n";
print "<OPTION value='8779280'>8779280</option>\n";
print "<OPTION value='8779748'>8779748</option>\n";
print "<OPTION value='8779749'>8779749</option></select></td>\n";

// Change table (variable file)
print "<td><select id=json-two name=table>";
print "<option selected value='$table'>$table</option></select></td>";

print "<TD><input type='text' value='$datepicker' id='datepicker' name='datepicker'></TD>";

// print "<input NAME=Buoyname TYPE=hidden value=$Buoyname>\n";
// print "<input NAME=table TYPE=hidden value=$table>\n";
print "<input NAME=Datatype TYPE=hidden value=$datatype>\n";
print "<input NAME=model TYPE=hidden value='$model'>\n";
// print "<input NAME=norecentdata TYPE=hidden value=$norecentdata>\n";
// print "<input NAME=norecentdata TYPE=hidden value=$norecentdatabutmodel>\n";

// print "<BR>";
print "<td><input type=submit  value=Change></td>\n</form>\n";
print "</font>\n";

?>
