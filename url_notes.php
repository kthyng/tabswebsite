<head>
    <title>Query URL Building</title>
</head>

<div id="container">

    <!-- include header from separate file -->
    <?php include("includes/header.html");?>


    <!-- include navigation from separate file -->
    <?php include("includes/navigation.html");?>

    <h2>Building a query URL to access database outside of webform</h2>
    <p>Instead of using the <a href="tabsqueryform.php">web form</a> to build your query for the database, you can create it yourself. The url is as follows:</p>

    <p>tabsquery.php?<b>Buoyname</b>=<i>[Name of buoy]</i>&amp;<b>table</b>=<i>[instrument type file name]</i>&amp;<b>datepicker</b>=<i>[date or date range]</i>&amp;<b>Datatype</b>=<i>[presentation of data]</i>&amp;<b>units</b>=<i>[units]</i>&amp;<b>tz</b>=<i>[time zone]</i></p>

    <ul>
    <li><b>Buoyname:</b> B, D, etc</li><br>
    <li><b>table:</b> ven (water currents, temperature), met (wind direction, temperature), wave (wave properties), salt (water properties, salt, temperature), eng (buoy function properties)</li><br>
    <li><b>datepicker:</b> single date (e.g. 2017/1/23 or 2017-1-23) or date range (e.g. 2017-1-23+-+2017-1-30)</li><br>
    <li><b>Datatype:</b> data (to get a table of data), pic (to get an image), download (to only download the data)</li><br>
    <li><b>units:</b> 'M' (metric, default) or 'E' (English)</li><br>
    <li><b>tz:</b> 'UTC' (GMT, default) or 'central' (local Texas/buoy time)</li><br>
    <ul>

    <p>For example:

    tabsquery.php?Buoyname=F&amp;table=ven&amp;datepicker=2017-1-23+-+2017-1-30&amp;Datatype=pic&amp;units=M&amp;tz=UTC</p>
</div>
