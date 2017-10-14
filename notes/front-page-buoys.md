# Controlling buoys on front page

This includes all listed on the right hand side of the map in index.php.

## Where buoy data needs to be updated to add a buoy

* buoy list in index.php
* buoy information needs to be provided in python/buoy_data.py
* details for how to read in buoy data in python/tools.read()
* details for how to plot the new data in python/plot_buoy.plot()
* need to be added to front page map
* update hover image (see below)
* update "Last Data Report" listing (see below)
* update list of buoys in subpages/tabsqueryform.php
* update python/buoy_header.py and subpages/tabsquery.php (under header part)

## How to update hover images on front page

Update list in js/ddimgtooltip.js. Must be in same order as hard-wired buoy list in index.php.


## How to update "Last Data Report" listing

Need to update how code will recognize new buoy data, which is given by variables $venfile and $table in index.php.
