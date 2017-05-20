<head>
    <title>Models</title>
</head>

<div id="container">

    <!-- include header from separate file -->
    <?php include("../includes/header.html");?>


    <!-- include navigation from separate file -->
    <?php include("../includes/navigation.html");?>

    <a name="txla"></a>

    <h2><a href=#txla>Texas-Louisiana Shelf Model</a></h2>


    <h3>Links</h3>

    <ul>
    <li> Forecast output (7 days): <a href=http://barataria.tamu.edu:8080/thredds/dodsC/NcML/oof_latest_agg/roms_his_f_latest.nc>thredds opendap</a> </li>
    <li> Nowcast output (past 3 months): <a href=http://barataria.tamu.edu:8080/thredds/dodsC/NcML/oof_archive_agg>thredds opendap</a></li>
    <li> Hindcast output (1993 &ndash; near present): <a href=http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg>thredds opendap</a></li>
    <li> <a href=http://pong.tamu.edu/gallery.html>Animations</a> of model output</li>
    </ul>

    <h3>Description</h3>

    <p>This is the source of the highly-realistic model output shown on the front page and alongside buoy data. The domain covers the Texas and Louisiana shelves and captures the Mississippi and Atchafalaya river plume dynamics and wind-driven flow on these shelves. Loop Current information is input into the domain via the open boundary forcing, which does assimilate the Loop Current data. The domain is shown in turquoise in the image, and the actual horizonal resolution is shown near Galveston Bay. Model output is available from 1993 to present day and up through a 7 day forecast which is run operationally. Model output is available at 3 different links because forcing information varies depending on how recent the simulation is; the best forcing information available is used for the hindcast model. Funding for the model development has come primarily from the Texas General Land Office (GRANT NUMBERS).</p>

    <img src="../images/TXLA_domain_labeled.jpg" width="50%">

    <ul>
    <li> Horizontal resolution: The grid is curvilinear, with horizontal resolution from about 500m near the Mississippi river delta in Louisiana to 1-2km near the border with Mexico. </li>
    <li> Vertical resolution:  </li>
    <li> Open boundary forcing (different for different times) </li>
    <li> River forcing </li>
    <li> Surface forcing (different for different times)</li>
    <li> ROMS parameters </li>
    </ul>

    Note that there is a legacy version of the hindcast model, run from 2004-2014. This model output is <a href=http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_nesting6.nc>available</a>.



    <h2><a href=#tglo>Legacy Gulf-wide Model</a></h2>

    <h3>Links</h3>

    <ul>
    <!-- <li> Forecast output (7 days): <a href=http://barataria.tamu.edu:8080/thredds/dodsC/NcML/oof_latest_agg/roms_his_f_latest.nc>thredds opendap</a> </li>
    <li> Nowcast output (past 3 months): <a href=http://barataria.tamu.edu:8080/thredds/dodsC/NcML/oof_archive_agg>thredds opendap</a></li>
    <li> Hindcast output (1993 &ndash; near present): <a href=http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg>thredds opendap</a></li> -->
    <li> <a href=http://seawater.tamu.edu/tglo/index.html>Animations</a> of model output</li>
    </ul>

    <h3>Description</h3>

    <p>This model covers the full Gulf and is being run operationally. It is lower resolution than the shelf model and is driven only by winds (i.e., it does not include the Loop Current).</p>

    <a href=http://seawater.tamu.edu/tglo/RG17051507.gif><img src="http://seawater.tamu.edu/tglo/RG17051507.gif" width="50%"></a>

    <ul>
    <li> Horizontal resolution: The grid is curvilinear, with horizontal resolution from about 500m near the Mississippi river delta in Louisiana to 1-2km near the border with Mexico. </li>
    <li> Vertical resolution:  </li>
    <li> Open boundary forcing (different for different times) </li>
    <li> River forcing </li>
    <li> Surface forcing (different for different times)</li>
    <li> ROMS parameters </li>
    </ul>

</div>
