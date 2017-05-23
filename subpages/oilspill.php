<head>
    <title>Spill Tracking</title>
</head>

<div id="container">

    <!-- include header from separate file -->
    <?php include("../includes/header.html");?>


    <!-- include navigation from separate file -->
    <?php include("../includes/navigation.html");?>

    <h2>Oil Spill Tracking Information</h2>
    <p>Oil spills can be tracked with NOAA's <a href=http://response.restoration.noaa.gov/oil-and-chemical-spills/oil-spills/response-tools/downloading-installing-and-running-gnome.html>GNOME</a> software. In GNOME, model output needs to be in particular form. Several model products in this form are available:</p>

    <ul>
    <li> Realistic Texas-Louisiana <a href=http://pong.tamu.edu/oof_v2/main/download.php?lang=en>shelf model</a> forecast </li>
    <li> Legacy Gulf-wide, wind-driven <a href=http://csanady.tamu.edu/GNOME/gnome2.html>TGLO/TABS model</a> forecast </li>
    <li> TWDB estuaries and bays model <a href=http://midgewater.twdb.state.tx.us/bays_estuaries/GNOME/>output</a></li>
    </ul>

    <p>A newer version of GNOME written in Python is under development at NOAA &ndash; called <a href=http://noaa-orr-erd.github.io/PyGnome/>pyGNOME</a> &ndash; which takes a broader range of input files. A summary of model output from the Texas shelf is <a href=http://pong.tamu.edu/oof_v2/main/download.php?lang=en>available</a>.</p>

    <!-- include footer from separate file -->
    <?php include("../includes/footer.html");?>

</div>
