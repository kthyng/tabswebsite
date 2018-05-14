<head>
    <title>Query URL Building</title>
</head>

<div id="container">

    <!-- include header from separate file -->
    <?php include("../includes/header.html");?>


    <!-- include navigation from separate file -->
    <?php include("../includes/navigation.html");?>

    <h2>Building a query URL to access database outside of webform</h2>
    <p>Instead of using the <a href="/tabswebsite/subpages/tabsqueryform.php">web form</a> to build your query for the database, you can create it yourself. The url is as follows:</p>

    <p>[website base]/subpages/tabsquery.php?<b>Buoyname</b>=<i>[Name of buoy]</i>
                    &amp;<b>table</b>=<i>[instrument type file name]</i>
                    &amp;<b>datepicker</b>=<i>[date or date range]</i>
                    &amp;<b>Datatype</b>=<i>[presentation of data]</i>
                    &amp;<b>units</b>=<i>[units]</i>
                    &amp;<b>tz</b>=<i>[time zone]</i>
                    &amp;<b>model</b>=<i>[also plot model output?]</i></p>
                    &amp;<b>datum</b>=<i>[choose tidal elevation datum]</i></p>

    <ul>
    <li><b>Buoyname:</b> B, D, PTAT2, etc. Full list <a href="https://github.com/kthyng/tabswebsite/blob/master/includes/buoys.csv">available</a>.</li><br>
    <li><b>table:</b> (this only matters for TABS buoys) ven (water currents, temperature), met (wind direction, temperature), wave (wave properties), salt (water properties, salt, temperature), eng (buoy function properties)</li><br>
    <li><b>datepicker:</b> single date (e.g. 2017/1/23 or 2017-1-23), date range (e.g. 2017-1-23+-+2017-1-30), or "recent" to get recently available data</li><br>
    <li><b>Datatype:</b> data (to get a table of data), pic (to get an image), download (to only download the data)</li><br>
    <li><b>units:</b> 'M' (metric, default) or 'E' (English)</li><br>
    <li><b>tz:</b> 'UTC' (GMT, default) or 'US/Central' (local Texas/buoy time) or 'Etc/GMT+6' (Always CST, not CDT)</li><br>
    <li><b>model:</b> 'False' (model output not included, default) or 'True' (plot model output with data)</li><br>
    <li><b>datum:</b> 'MSL' (mean sea level, default), 'MHHW' (mean higher high water), 'MHW' (mean high water), 'MTL' (mean tide level), 'MLW' (mean low water), 'MLLW' (mean lower low water) </li><br>
    <ul>

    <p>For example:

    [websitebase]/subpages/tabsquery.php?Buoyname=F&amp;table=ven&amp;datepicker=2017-1-23+-+2017-1-30&amp;Datatype=pic&amp;units=M&amp;tz=UTC&amp;model=True&datum=MLLW</p>

    <!-- include footer from separate file -->
    <?php include("../includes/footer.html");?>

</div>
