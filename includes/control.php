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
print "<OPTION value='g06010'>g06010</option>\n";
print "<OPTION value='mc0101'>mc0101</option>\n";
print "<OPTION value='sn0101'>sn0101</option>\n";
print "<OPTION value='sn0201'>sn0201</option>\n";
print "<OPTION value='sn0301'>sn0301</option>\n";
print "<OPTION value='sn0401'>sn0401</option>\n";
print "<OPTION value='sn0501'>sn0501</option>\n";
print "<OPTION value='sn0701'>sn0701</option>\n";
print "<OPTION value='lc0101'>lc0101</option>\n";
print "<OPTION value='lc0201'>lc0201</option>\n";
print "<OPTION value='mg0101'>mg0101</option>\n";
print "<OPTION value='8770475'>8770475</option>\n";
print "<OPTION value='8770520'>8770520</option>\n";
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
print "<OPTION value='8779749'>8779749</option>\n";
print "<OPTION value='8734673'>8734673</option>\n";
print "<OPTION value='8735180'>8735180</option>\n";
print "<OPTION value='8741003'>8741003</option>\n";
print "<OPTION value='8741041'>8741041</option>\n";
print "<OPTION value='8741094'>8741094</option>\n";
print "<OPTION value='8741501'>8741501</option>\n";
print "<OPTION value='8741533'>8741533</option>\n";
print "<OPTION value='8747437'>8747437</option>\n";
print "<OPTION value='8760721'>8760721</option>\n";
print "<OPTION value='8760922'>8760922</option>\n";
print "<OPTION value='8761305'>8761305</option>\n";
print "<OPTION value='8761724'>8761724</option>\n";
print "<OPTION value='8764227'>8764227</option>\n";
print "<OPTION value='8764314'>8764314</option>\n";
print "<OPTION value='8766072'>8766072</option>\n";
print "<OPTION value='8768094'>8768094</option>\n";
print "<OPTION value='8770570'>8770570</option>\n";
print "<OPTION value='8770613'>8770613</option>\n";
print "<OPTION value='8771013'>8771013</option>\n";
print "<OPTION value='8771341'>8771341</option>\n";
print "<OPTION value='8771450'>8771450</option>\n";
print "<OPTION value='8773767'>8773767</option>\n";
print "<OPTION value='8775870'>8775870</option>\n";
print "<OPTION value='8779770'>8779770</option></select></td>\n";

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

# time zone
print "<td>";
print "<Select Name=tz>\n";
print "<option selected value='$tz'>$tz</option>\n";
print "<option value='UTC'>UTC</Option>\n";
print "<option value='US/Central'>US/Central</option>\n</select></td>\n";


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
