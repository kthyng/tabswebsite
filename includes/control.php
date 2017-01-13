<!-- bottom control options for query page -->


<?php


print "<TABLE width=100%>";
print "<TR><TD valign=top width=120 align=left>";
print "</td>";
print "<td>";
print "<br> &nbsp;\n";
print "<br><form action=\"tabsquery.php\" method=\"get\">\n";

print "<font face=\"Helvetica\" size=-1>\n";
print "<Select Name=tz>\n";
print "<option value=''>Time Zone</Option>\n";
print "<option value='UTC'>UTC</Option>\n";
print "<option value='STN'>Station Local</option>\n</select><br>\n";
if (($table != "eng") and ($datatype != "pic")) {
print "<Select Name=units>\n";
print "<option value=''>Units</Option>\n";
print "<option value='M'>Metric</Option>\n";
print "<option value='E'>English</option>\n</select>\n";
}

// Change buoy
print "<Select Name=Buoyname id=json-one>\n";
print "<OPTION SELECTED value='$Buoyname'>$Buoyname</option>\n";
print "<option value='B'>B</option>\n";
print "<option value='D'>D</option>\n";
print "<option value='F'>F</option>\n";
print "<option value='J'>J</option>\n";
print "<option value='K'>K</option>\n";
print "<option value='N'>N</option>\n";
print "<option value='R'>R</option>\n";
print "<option value='V'>V</option>\n";
print "<option value='W'>W</option>\n";
print "<option value='X'>X</option>\n";
print "<option value='A'>A*</option>\n";
print "<option value='C'>C*</option>\n";
print "<option value='E'>E*</option>\n";
print "<option value='G'>G*</option>\n";
print "<option value='H'>H*</option>\n";
print "<option value='P'>P*</option>\n";
print "<option value='S'>S*</option>\n</select>\n";

// Change table (variable file)
// print "<select id=json-two name=table>\n";
// print "<option selected value='$table'>$table</option>";

print "<Select Name=table>\n";
print "<OPTION SELECTED value='$table'>$tablename</option>\n";
print "<option value='ven'>Velocity data</option>\n";
print "<option value='met'>Meteorological data</option>\n";
print "<option value='eng'>System data</option>\n";
print "<option value='salt'>Water property data</option>\n";
print "<option value='wave'>Wave data</option>\n</select>\n";

// print "<input NAME=Buoyname TYPE=hidden value=$Buoyname>\n";
// print "<input NAME=table TYPE=hidden value=$table>\n";
print "<input NAME=Datatype TYPE=hidden value=$datatype>\n";
print "<input NAME=datepicker TYPE=hidden value=$datepicker>\n";

print "<BR><input type=submit  value=Change>\n</form>\n";

print "<br><table>\n";
// Switch to
print "<TR><TD>Switch to <a href=tabsquery.php?Buoyname=$Buoyname&table=$table&Datatype=$newdatatype&datepicker=$datepicker>$newdatatypename</a></TD></TR>\n";

print "<TR><TD>Return to <a href=tabsqueryform.php>database query</a></TD></TR>\n";
print "<TR><TD>Return to <a href=index.php>homepage</a></TR></TD>\n";
print "</table>\n";
print "</font>\n";

?>
