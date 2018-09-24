<head>
    <title>Files for Oil Spill Tracking with GNOME</title>
</head>

<div id="container">

    <!-- include header from separate file -->
    <?php include("../includes/header.html");?>


    <!-- include navigation from separate file -->
    <?php include("../includes/navigation.html");?>

    <h2>Texas-Louisiana Shelf Model Access Options</h2>

    OOF forecast and hindcast outputs can be downloaded from the followig links via THREDDS server or HTTP server. The output files are ROMS history file in NetCDF format. All necessary variables including grids are in the file. Frequency of forecast output is 1 hour.
    <br><br>
    Note: Vector variables (e.g. current velocity or wind vector) are on orthogonal grids. If you need East-West and North-South vectors, users need to convert them. There is a variable named "angle" to convert the orthogonal grids into the North-South/East-West grids. Vertical coordinate is terrain-following stretching coordinate with values ranging from -1 to 0. Users need to convert it into z-coordinate. More information about ROMS grids can be obtained on <a href='http://myroms.org'>myroms.org</a>.

    <h3>THREDDS Server</h3>

    <ul>
    <li><a href='http://barataria.tamu.edu:8080/thredds/dodsC/forecast_latest/roms_his_f_latest.nc.html'>Latest 5-day forecast (OPeNDAP)</a></li>
    <li><a href="http://barataria.tamu.edu:8080/thredds/dodsC/forecast_latest/roms_his_f_latest_surface.nc.html">Latest 5-day forecast (Surface only) (OPeNDAP)</a></li>
    <li><a href="http://barataria.tamu.edu:8080/thredds/dodsC/NcML/forecast_his_archive_agg.nc.html
">Forecast archives (Recent output) (OPeNDAP)</a></li>
    <li><a href="http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_hindcast_agg.html">Hindcast archives (1993 &ndash; recent past) (OPeNDAP)</a></li>
    </ul>

    <h3>NetCDF subset</h3>

    <ul>
    <li><a href="http://barataria.tamu.edu:8080/thredds/ncss/forecast_latest/roms_his_f_latest.nc/dataset.html">Latest 5-day forecast (NetCDF Subset)</a></li>
    <li><a href="http://barataria.tamu.edu:8080/thredds/ncss/NcML/txla_hindcast_agg/dataset.html">Hindcast archives (1993-almost present) (NetCDF Subset)</a></li>
    </ul>

    <!-- <h3>HTTP server</h3>
    Note: when you click a link below, the model output file will be downloaded.

    <ul>
        <li><a href="http://barataria.tamu.edu:8080/thredds/fileServer/oof_other/roms_his_f_latest.nc">Latest 5-day forecast (Full 3-D) (~15 GB)</a></li>
        <li><a href="http://barataria.tamu.edu:8080/thredds/fileServer/oof_other/roms_his_f_latest_surface.nc">Latest 5-day forecast (surface only) (~1 GB)</a></li>
        <li><a href="http://barataria.tamu.edu:8080/thredds/dodsC/forecast_latest/roms_his_f_latest_bottom.nc">Latest 5-day forecast (bottom only) (~1 GB)</a></li>
    </ul> -->

    <h3>GNOME-ready files</h3>
    Based on the latest 5-day forecast.
    <br><br>
    Note: You need to load the following three files and manually set up oil spill information on the GNOME software to run oil spill model.

    <ul>
        <li><a href="http://pong.tamu.edu/oof_v2/main/coast.bna">Coastline map file (coast.bna)</a></li>
        <li><a href="http://barataria.tamu.edu:8080/thredds/fileServer/forecast_latest/roms2gnome_wind_surface.nc">Variable surface wind (NetCDF format) (~50 MB)</a></li>
        <li><a href="http://barataria.tamu.edu:8080/thredds/fileServer/forecast_latest/roms2gnome_current_surface.nc">Variable surface current (NetCDF format) (~50 MB)</a></li>
        <li><a href="http://barataria.tamu.edu:8080/thredds/fileServer/forecast_latest/roms2gnome_current_bottom.nc">Variable bottom current (NetCDF format) (~50 MB)</a></li>
    </ul>


    <h3>GOODS (GNOME Online Oceanographic Data Server)</h3>

    You can also create GNOME ready netCDF file from the following link provided by NOAA Office of Response and Restoration. You can download file for 2-D or 3-D GNOME run.

    <a href="https://gnome.orr.noaa.gov/goods/currents/TAMU/choose_file">Go to GOODS</a>

    <br><br>
    Contact for GOOS: orr.gnome@noaa.gov


    <!-- include footer from separate file -->
    <?php include("../includes/footer.html");?>

</div>
